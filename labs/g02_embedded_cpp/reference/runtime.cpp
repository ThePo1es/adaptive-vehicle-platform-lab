#include "g02_runtime.hpp"

#include <limits>

#ifndef G02_MUTANT
#define G02_MUTANT 0
#endif

namespace g02 {
namespace {
void saturating_increment(std::uint64_t& value) noexcept {
    if (value != std::numeric_limits<std::uint64_t>::max()) {
        ++value;
    }
}
}

EventRuntime::EventRuntime(FullPolicy policy) noexcept : policy_{policy} {}

PushStatus EventRuntime::push(const Event& event) noexcept {
    PushStatus status = PushStatus::Accepted;
    if (count_ == capacity) {
        if (policy_ == FullPolicy::RejectNewest && G02_MUTANT != 201) {
            saturating_increment(rejected_);
            return PushStatus::RejectedNewest;
        }
        head_ = (head_ + 1U) % capacity;
        --count_;
        saturating_increment(dropped_);
        status = PushStatus::DroppedOldest;
    }
    queue_[tail_] = event;
    tail_ = (tail_ + 1U) % capacity;
    ++count_;
    return status;
}

std::optional<CallbackHandle> EventRuntime::register_callback(Callback callback) noexcept {
    if (callback.function == nullptr) {
        return std::nullopt;
    }
    for (std::size_t index = 0U; index < callbacks_.size(); ++index) {
        auto& slot = callbacks_[index];
        if (!slot.occupied && !slot.retired) {
            slot.callback = callback;
            slot.occupied = true;
            return CallbackHandle{index, slot.generation};
        }
    }
    return std::nullopt;
}

bool EventRuntime::unregister_callback(CallbackHandle handle) noexcept {
    if (handle.index >= callbacks_.size()) {
        return false;
    }
    auto& slot = callbacks_[handle.index];
    if (!slot.occupied || slot.generation != handle.generation) {
        return false;
    }
    slot.occupied = false;
    slot.callback = {};
    if (slot.generation == std::numeric_limits<std::uint64_t>::max() && G02_MUTANT != 204) {
        slot.retired = true;
    } else {
        ++slot.generation;
    }
    return true;
}

#if G02_TESTING
bool EventRuntime::seed_callback_generation_for_test(
    std::size_t index, std::uint64_t generation) noexcept {
    if (index >= callbacks_.size() || callbacks_[index].occupied) {
        return false;
    }
    callbacks_[index].generation = generation;
    callbacks_[index].retired = false;
    return true;
}
#endif

bool EventRuntime::dispatch_one() noexcept {
    if (count_ == 0U) {
        return false;
    }
    const Event event = queue_[head_];
    head_ = (head_ + 1U) % capacity;
    --count_;
    if constexpr (G02_MUTANT == 202) {
        for (auto& slot : callbacks_) {
            if (slot.occupied) {
                slot.callback.function(slot.callback.context, event, *this);
            }
        }
    } else {
        std::array<Callback, callback_capacity> snapshot{};
        std::size_t snapshot_size = 0U;
        for (const auto& slot : callbacks_) {
            if (slot.occupied) {
                snapshot[snapshot_size] = slot.callback;
                ++snapshot_size;
            }
        }
        for (std::size_t index = 0U; index < snapshot_size; ++index) {
            snapshot[index].function(snapshot[index].context, event, *this);
        }
    }
    if constexpr (G02_MUTANT == 203) {
        while (dispatch_one()) {
        }
    }
    return true;
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
