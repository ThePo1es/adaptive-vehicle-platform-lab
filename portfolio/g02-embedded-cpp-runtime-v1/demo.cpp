#include "g02_abi.hpp"
#include "g02_lifetime.hpp"
#include "g02_queue.hpp"
#include "g02_runtime.hpp"

#include <array>
#include <cstddef>
#include <cstdio>

namespace {
void count_event(void* context, const g02::Event&, g02::EventRuntime&) noexcept {
    ++*static_cast<int*>(context);
}
}

int main() {
    const std::array<std::byte, 3> bytes{
        std::byte{0x10},
        std::byte{0x20},
        std::byte{0x30},
    };
    auto owner = g02::MessageOwner::create(bytes, 7U);
    if (!owner.has_value()) {
        return 1;
    }
    auto lease = owner.value().lease();
    if (!lease.has_value() || lease.value().bytes().size() != bytes.size()) {
        return 2;
    }

    g02::EventRuntime runtime{g02::FullPolicy::RejectNewest};
    int callback_count = 0;
    if (!runtime.register_callback(g02::Callback{count_event, &callback_count}).has_value()) {
        return 3;
    }
    if (runtime.push(g02::Event{}) != g02::PushStatus::Accepted || !runtime.dispatch_one()) {
        return 4;
    }

    g02::WorkQueue queue{};
    if (queue.try_push(42) != g02::TryPushResult::Accepted) {
        return 5;
    }
    const auto popped = queue.try_pop();
    if (popped.state != g02::PopState::Item || popped.value != 42) {
        return 6;
    }

    g02::FakeDependencies dependencies{10, 20, 30, false};
    const auto scenario = g02::run_manual(dependencies);
    if (scenario.status != g02::OperationStatus::Ok || scenario.checksum != 60 ||
        scenario.cleanup_count != 1U || callback_count != 1) {
        return 7;
    }
    std::puts("G2 C++ runtime demo: PASS");
    return 0;
}
