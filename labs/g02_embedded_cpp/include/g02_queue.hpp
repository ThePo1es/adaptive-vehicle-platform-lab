#pragma once

#include <array>
#include <condition_variable>
#include <cstddef>
#include <cstdint>
#include <mutex>

namespace g02 {
enum class WaitEvent : std::uint8_t {
    BeforeWait,
    AfterWake,
};

using WaitFunction = void (*)(void*, WaitEvent) noexcept;

struct WaitObserver {
    WaitFunction function{nullptr};
    void* context{nullptr};
};

enum class PushResult : std::uint8_t {
    Accepted,
    Closed,
};

enum class TryPushResult : std::uint8_t {
    Accepted,
    Full,
    Closed,
};

enum class PopState : std::uint8_t {
    Item,
    Empty,
    Closed,
};

struct PopResult {
    PopState state{PopState::Empty};
    int value{0};
};

class WorkQueue {
public:
    static constexpr std::size_t capacity = 8U;

    explicit WorkQueue(WaitObserver observer = {}) noexcept;
    WorkQueue(const WorkQueue&) = delete;
    WorkQueue& operator=(const WorkQueue&) = delete;

    [[nodiscard]] PushResult push(int value) noexcept;
    [[nodiscard]] TryPushResult try_push(int value) noexcept;
    [[nodiscard]] PopResult pop() noexcept;
    [[nodiscard]] PopResult try_pop() noexcept;
    void close() noexcept;
    void notify_waiters_for_test() noexcept;
    [[nodiscard]] std::size_t size() const noexcept;
    [[nodiscard]] bool closed() const noexcept;

private:
    void observe(WaitEvent event) const noexcept;
    void insert(int value) noexcept;
    [[nodiscard]] int remove() noexcept;

    std::array<int, capacity> values_{};
    std::size_t head_{0U};
    std::size_t tail_{0U};
    std::size_t count_{0U};
    bool closed_{false};
    WaitObserver observer_{};
    mutable std::mutex mutex_{};
    std::condition_variable not_empty_{};
    std::condition_variable not_full_{};
};
}
