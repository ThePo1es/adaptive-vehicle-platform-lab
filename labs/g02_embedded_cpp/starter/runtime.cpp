#include "g02_runtime.hpp"

namespace g02 {
EventRuntime::EventRuntime(FullPolicy policy) noexcept : policy_{policy} {}

PushStatus EventRuntime::push(const Event&) noexcept {
    return PushStatus::RejectedNewest;
}

std::optional<CallbackHandle> EventRuntime::register_callback(Callback) noexcept {
    return std::nullopt;
}

bool EventRuntime::unregister_callback(CallbackHandle) noexcept {
    return false;
}

bool EventRuntime::dispatch_one() noexcept {
    return false;
}

std::size_t EventRuntime::size() const noexcept {
    return count_;
}

std::uint64_t EventRuntime::rejected_count() const noexcept {
    return rejected_;
}

std::uint64_t EventRuntime::dropped_count() const noexcept {
    return dropped_;
}
}
