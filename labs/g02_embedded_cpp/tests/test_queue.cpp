#include "g02_queue.hpp"
#include "test_support.hpp"

#if G02_RETEST
#include "retest-2.3-v1.hpp"
#else
#include "sprint-2.3-v1.hpp"
#endif

#include <algorithm>
#include <array>
#include <atomic>
#include <barrier>
#include <cstddef>
#include <cstdint>
#include <semaphore>
#include <thread>

namespace {
using g02::PopState;
using g02::PushResult;
using g02::WaitEvent;
using g02::WorkQueue;

struct WaitProbe {
    std::counting_semaphore<8> before_wait{0};
    std::counting_semaphore<8> after_wake{0};
    std::binary_semaphore continue_after_wake{0};
    std::atomic<bool> block_after_wake{false};
};

void observe_wait(void* context, WaitEvent event) noexcept {
    auto& probe = *static_cast<WaitProbe*>(context);
    if (event == WaitEvent::BeforeWait) {
        probe.before_wait.release();
        return;
    }
    probe.after_wake.release();
    if (probe.block_after_wake.exchange(false, std::memory_order_acq_rel)) {
        probe.continue_after_wake.acquire();
    }
}

int fill_queue(WorkQueue& queue) {
    for (std::size_t index = 0U; index < WorkQueue::capacity; ++index) {
        G02_CHECK(queue.try_push(static_cast<int>(index)) == g02::TryPushResult::Accepted);
    }
    return 0;
}

int test_spurious_wakeup_does_not_overfill_queue() {
    // Given a full queue and a producer blocked by its predicate.
    WaitProbe probe{};
    probe.block_after_wake.store(true, std::memory_order_release);
    WorkQueue queue{g02::WaitObserver{observe_wait, &probe}};
    G02_CHECK(fill_queue(queue) == 0);
    PushResult producer_result = PushResult::Accepted;
    std::jthread producer([&] { producer_result = queue.push(99); });
    probe.before_wait.acquire();
    // When a notification occurs without creating capacity.
    queue.notify_waiters_for_test();
    probe.after_wake.acquire();
    probe.continue_after_wake.release();
    // Then the producer rechecks the predicate and capacity stays bounded.
    G02_CHECK(queue.size() == WorkQueue::capacity);
    const auto popped = queue.pop();
    G02_CHECK(popped.state == PopState::Item);
    producer.join();
    G02_CHECK(producer_result == PushResult::Accepted);
    G02_CHECK(queue.size() == WorkQueue::capacity);
    return 0;
}

int test_close_wakes_blocked_producer() {
    // Given a producer blocked on a full queue.
    WaitProbe probe{};
    WorkQueue queue{g02::WaitObserver{observe_wait, &probe}};
    G02_CHECK(fill_queue(queue) == 0);
    PushResult producer_result = PushResult::Accepted;
    std::jthread producer([&] { producer_result = queue.push(100); });
    probe.before_wait.acquire();
    // When the queue is closed.
    queue.close();
    producer.join();
    // Then the blocked producer wakes with Closed and no value is inserted.
    G02_CHECK(producer_result == PushResult::Closed);
    G02_CHECK(queue.size() == WorkQueue::capacity);
    return 0;
}

int test_close_allows_drain_then_reports_closed() {
    // Given two queued values.
    WorkQueue queue{};
    G02_CHECK(queue.try_push(11) == g02::TryPushResult::Accepted);
    G02_CHECK(queue.try_push(12) == g02::TryPushResult::Accepted);
    // When close is requested before the consumer drains them.
    queue.close();
    const auto first = queue.pop();
    const auto second = queue.pop();
    const auto terminal = queue.pop();
    // Then existing work is preserved and only the empty closed queue terminates.
    G02_CHECK(first.state == PopState::Item && first.value == 11);
    G02_CHECK(second.state == PopState::Item && second.value == 12);
    G02_CHECK(terminal.state == PopState::Closed);
    return 0;
}

int test_two_producers_preserve_every_value_for_100_seeds() {
    // Given 100 reproducible input seeds, two producers and one consumer.
    for (std::uint32_t offset = 0U; offset < 100U; ++offset) {
        WorkQueue queue{};
        constexpr std::size_t maximum_values = 64U;
        std::array<int, maximum_values> observed{};
        std::atomic<std::size_t> observed_count{0U};
        std::barrier start{3};
        const int per_producer = g02::fixture::values_per_producer;
        const int seed = static_cast<int>(g02::fixture::seed_base + offset);
        std::jthread first([&] {
            start.arrive_and_wait();
            for (int index = 0; index < per_producer; ++index) {
                static_cast<void>(queue.push(seed * 1000 + index));
            }
        });
        std::jthread second([&] {
            start.arrive_and_wait();
            for (int index = 0; index < per_producer; ++index) {
                static_cast<void>(queue.push(seed * 1000 + 100 + index));
            }
        });
        std::jthread consumer([&] {
            start.arrive_and_wait();
            for (int index = 0; index < per_producer * 2; ++index) {
                const auto item = queue.pop();
                const auto target = observed_count.fetch_add(1U, std::memory_order_relaxed);
                observed[target] = item.value;
            }
        });
        first.join();
        second.join();
        consumer.join();
        // When all workers have joined, Then each distinct value appears exactly once.
        G02_CHECK(observed_count.load(std::memory_order_relaxed) ==
                  static_cast<std::size_t>(per_producer * 2));
        std::sort(observed.begin(), observed.begin() + per_producer * 2);
        for (int index = 0; index < per_producer; ++index) {
            G02_CHECK(observed[static_cast<std::size_t>(index)] == seed * 1000 + index);
            G02_CHECK(observed[static_cast<std::size_t>(per_producer + index)] ==
                      seed * 1000 + 100 + index);
        }
    }
    return 0;
}
}

int main() {
    if (test_spurious_wakeup_does_not_overfill_queue() != 0 ||
        test_close_wakes_blocked_producer() != 0 ||
        test_close_allows_drain_then_reports_closed() != 0 ||
        test_two_producers_preserve_every_value_for_100_seeds() != 0) {
        return 1;
    }
    std::puts("PASS bounded MPSC queue contract seeds=100");
    return 0;
}
