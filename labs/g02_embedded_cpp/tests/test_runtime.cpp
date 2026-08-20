#include "g02_runtime.hpp"
#include "test_support.hpp"

#if G02_RETEST
#include "retest-2.2-v1.hpp"
#else
#include "sprint-2.2-v1.hpp"
#endif

#include <atomic>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <new>
#include <limits>

namespace allocation_probe {
std::atomic<bool> enabled{false};
std::atomic<std::size_t> count{0U};
}

void* operator new(std::size_t size) {
    if (allocation_probe::enabled.load(std::memory_order_relaxed)) {
        allocation_probe::count.fetch_add(1U, std::memory_order_relaxed);
    }
    void* memory = std::malloc(size);
    if (memory == nullptr) {
        std::abort();
    }
    return memory;
}

void* operator new[](std::size_t size) {
    return ::operator new(size);
}

void operator delete(void* memory) noexcept {
    std::free(memory);
}

void operator delete[](void* memory) noexcept {
    std::free(memory);
}

void operator delete(void* memory, std::size_t) noexcept {
    std::free(memory);
}

void operator delete[](void* memory, std::size_t) noexcept {
    std::free(memory);
}

namespace {
using g02::Callback;
using g02::CallbackHandle;
using g02::Event;
using g02::EventRuntime;
using g02::FullPolicy;
using g02::PushStatus;

Event make_event(std::uint32_t sequence) {
    Event event{};
    event.type = g02::fixture::event_type;
    event.sequence = sequence;
    event.payload[0] = std::byte{0xA5};
    return event;
}

struct Recorder {
    std::size_t calls{0U};
    std::uint32_t first_sequence{0U};
};

void record_event(void* context, const Event& event, EventRuntime&) noexcept {
    auto& recorder = *static_cast<Recorder*>(context);
    if (recorder.calls == 0U) {
        recorder.first_sequence = event.sequence;
    }
    ++recorder.calls;
}

int test_reject_newest_keeps_existing_events() {
    // Given a RejectNewest runtime filled to its exact capacity.
    EventRuntime runtime{FullPolicy::RejectNewest};
    Recorder recorder{};
    G02_CHECK(runtime.register_callback(Callback{record_event, &recorder}).has_value());
    for (std::uint32_t sequence = 0U; sequence < EventRuntime::capacity; ++sequence) {
        G02_CHECK(runtime.push(make_event(sequence)) == PushStatus::Accepted);
    }
    // When one additional event arrives.
    const auto result = runtime.push(make_event(99U));
    G02_CHECK(runtime.dispatch_one());
    // Then it is rejected without replacing the oldest event.
    G02_CHECK(result == PushStatus::RejectedNewest);
    G02_CHECK(runtime.rejected_count() == 1U);
    G02_CHECK(runtime.size() == EventRuntime::capacity - 1U);
    G02_CHECK(recorder.first_sequence == 0U);
    return 0;
}

int test_drop_oldest_makes_room_for_new_event() {
    // Given a DropOldest runtime filled to its exact capacity.
    EventRuntime runtime{FullPolicy::DropOldest};
    Recorder recorder{};
    G02_CHECK(runtime.register_callback(Callback{record_event, &recorder}).has_value());
    for (std::uint32_t sequence = 0U; sequence < EventRuntime::capacity; ++sequence) {
        G02_CHECK(runtime.push(make_event(sequence)) == PushStatus::Accepted);
    }
    // When one additional event arrives.
    const auto result = runtime.push(make_event(99U));
    G02_CHECK(runtime.dispatch_one());
    // Then the new event is accepted and sequence zero is the one dropped.
    G02_CHECK(result == PushStatus::DroppedOldest);
    G02_CHECK(runtime.dropped_count() == 1U);
    G02_CHECK(runtime.size() == EventRuntime::capacity - 1U);
    G02_CHECK(recorder.first_sequence == 1U);
    return 0;
}

struct RemovalContext {
    CallbackHandle target{};
    std::size_t calls{0U};
};

void remove_target(void* context, const Event&, EventRuntime& runtime) noexcept {
    auto& removal = *static_cast<RemovalContext*>(context);
    ++removal.calls;
    static_cast<void>(runtime.unregister_callback(removal.target));
}

int test_dispatch_uses_callback_snapshot() {
    // Given a callback that removes a later callback during dispatch.
    EventRuntime runtime{FullPolicy::RejectNewest};
    RemovalContext removal{};
    Recorder target{};
    G02_CHECK(runtime.register_callback(Callback{remove_target, &removal}).has_value());
    const auto target_handle = runtime.register_callback(Callback{record_event, &target});
    G02_CHECK(target_handle.has_value());
    removal.target = *target_handle;
    G02_CHECK(runtime.push(make_event(g02::fixture::first_sequence)) == PushStatus::Accepted);
    // When the first event is dispatched and then a second event is dispatched.
    G02_CHECK(runtime.dispatch_one());
    G02_CHECK(runtime.push(make_event(g02::fixture::reentrant_sequence)) == PushStatus::Accepted);
    G02_CHECK(runtime.dispatch_one());
    // Then removal starts with the next dispatch, not halfway through the current snapshot.
    G02_CHECK(removal.calls == 2U);
    G02_CHECK(target.calls == 1U);
    return 0;
}

struct ReentrantContext {
    std::size_t calls{0U};
};

void enqueue_once(void* context, const Event&, EventRuntime& runtime) noexcept {
    auto& reentrant = *static_cast<ReentrantContext*>(context);
    ++reentrant.calls;
    if (reentrant.calls == 1U) {
        static_cast<void>(runtime.push(make_event(g02::fixture::reentrant_sequence)));
    }
}

int test_reentrant_event_waits_for_next_dispatch() {
    // Given a callback that enqueues one more event.
    EventRuntime runtime{FullPolicy::RejectNewest};
    ReentrantContext context{};
    G02_CHECK(runtime.register_callback(Callback{enqueue_once, &context}).has_value());
    G02_CHECK(runtime.push(make_event(g02::fixture::first_sequence)) == PushStatus::Accepted);
    // When exactly one dispatch operation is requested.
    G02_CHECK(runtime.dispatch_one());
    // Then the reentrant event remains queued until the caller dispatches again.
    G02_CHECK(context.calls == 1U);
    G02_CHECK(runtime.size() == 1U);
    G02_CHECK(runtime.dispatch_one());
    G02_CHECK(context.calls == 2U);
    return 0;
}

int test_runtime_operations_do_not_allocate_after_construction() {
    // Given a fully constructed runtime and callback table.
    EventRuntime runtime{FullPolicy::RejectNewest};
    Recorder recorder{};
    G02_CHECK(runtime.register_callback(Callback{record_event, &recorder}).has_value());
    allocation_probe::count.store(0U, std::memory_order_relaxed);
    allocation_probe::enabled.store(true, std::memory_order_release);
    // When normal, full and dispatch operations run.
    for (std::uint32_t sequence = 0U; sequence <= EventRuntime::capacity; ++sequence) {
        static_cast<void>(runtime.push(make_event(sequence)));
    }
    while (runtime.dispatch_one()) {
    }
    allocation_probe::enabled.store(false, std::memory_order_release);
    // Then the global allocation probe observed no heap calls.
    G02_CHECK(allocation_probe::count.load(std::memory_order_relaxed) == 0U);
    return 0;
}

int test_diagnostic_counters_saturate_instead_of_wrapping() {
    // Given full runtimes whose counters are one step below their maximum.
    EventRuntime reject{FullPolicy::RejectNewest};
    EventRuntime drop{FullPolicy::DropOldest};
    for (std::uint32_t sequence = 0U; sequence < EventRuntime::capacity; ++sequence) {
        G02_CHECK(reject.push(make_event(sequence)) == PushStatus::Accepted);
        G02_CHECK(drop.push(make_event(sequence)) == PushStatus::Accepted);
    }
    reject.seed_counters_for_test(std::numeric_limits<std::uint64_t>::max() - 1U, 0U);
    drop.seed_counters_for_test(0U, std::numeric_limits<std::uint64_t>::max() - 1U);
    // When each full policy is triggered twice.
    static_cast<void>(reject.push(make_event(90U)));
    static_cast<void>(reject.push(make_event(91U)));
    static_cast<void>(drop.push(make_event(90U)));
    static_cast<void>(drop.push(make_event(91U)));
    // Then both diagnostic counters stop at their maximum.
    G02_CHECK(reject.rejected_count() == std::numeric_limits<std::uint64_t>::max());
    G02_CHECK(drop.dropped_count() == std::numeric_limits<std::uint64_t>::max());
    return 0;
}
}

int main() {
    if (test_reject_newest_keeps_existing_events() != 0 ||
        test_drop_oldest_makes_room_for_new_event() != 0 ||
        test_dispatch_uses_callback_snapshot() != 0 ||
        test_reentrant_event_waits_for_next_dispatch() != 0 ||
        test_runtime_operations_do_not_allocate_after_construction() != 0 ||
        test_diagnostic_counters_saturate_instead_of_wrapping() != 0) {
        return 1;
    }
    std::puts("PASS fixed-capacity runtime contract");
    return 0;
}
