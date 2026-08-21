#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <optional>

namespace g02 {
struct Event {
    std::array<std::byte, 16U> payload{};
    std::uint16_t type{0U};
    std::uint32_t sequence{0U};
};

enum class FullPolicy : std::uint8_t {
    RejectNewest,
    DropOldest,
};

enum class PushStatus : std::uint8_t {
    Accepted,
    RejectedNewest,
    DroppedOldest,
};

struct CallbackHandle {
    std::size_t index{0U};
    std::uint64_t generation{0U};
};

class EventRuntime;
using CallbackFunction = void (*)(void*, const Event&, EventRuntime&) noexcept;

struct Callback {
    CallbackFunction function{nullptr};
    void* context{nullptr};
};

class EventRuntime {
public:
    static constexpr std::size_t capacity = 32U;
    static constexpr std::size_t callback_capacity = 8U;

    explicit EventRuntime(FullPolicy policy) noexcept;
    EventRuntime(const EventRuntime&) = delete;
    EventRuntime& operator=(const EventRuntime&) = delete;
    EventRuntime(EventRuntime&&) = delete;
    EventRuntime& operator=(EventRuntime&&) = delete;

    [[nodiscard]] PushStatus push(const Event& event) noexcept;
    [[nodiscard]] std::optional<CallbackHandle> register_callback(Callback callback) noexcept;
    [[nodiscard]] bool unregister_callback(CallbackHandle handle) noexcept;
    [[nodiscard]] bool dispatch_one() noexcept;
    [[nodiscard]] std::size_t size() const noexcept;
    [[nodiscard]] std::uint64_t rejected_count() const noexcept;
    [[nodiscard]] std::uint64_t dropped_count() const noexcept;
#if G02_TESTING
    void seed_counters_for_test(std::uint64_t rejected, std::uint64_t dropped) noexcept {
        rejected_ = rejected;
        dropped_ = dropped;
    }
    [[nodiscard]] bool seed_callback_generation_for_test(
        std::size_t index, std::uint64_t generation) noexcept;
#endif

private:
    struct CallbackSlot {
        Callback callback{};
        std::uint64_t generation{1U};
        bool occupied{false};
        bool retired{false};
    };

    std::array<Event, capacity> queue_{};
    std::array<CallbackSlot, callback_capacity> callbacks_{};
    std::size_t head_{0U};
    std::size_t tail_{0U};
    std::size_t count_{0U};
    FullPolicy policy_;
    std::uint64_t rejected_{0U};
    std::uint64_t dropped_{0U};
};
}
