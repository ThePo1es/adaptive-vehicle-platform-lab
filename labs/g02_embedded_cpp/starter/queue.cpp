#include "g02_queue.hpp"

namespace g02 {
WorkQueue::WorkQueue(WaitObserver observer) noexcept : observer_{observer} {}

void WorkQueue::observe(WaitEvent) const noexcept {}

void WorkQueue::insert(int) noexcept {}

int WorkQueue::remove() noexcept {
    return 0;
}

PushResult WorkQueue::push(int) noexcept {
    return PushResult::Closed;
}

TryPushResult WorkQueue::try_push(int) noexcept {
    return TryPushResult::Full;
}

PopResult WorkQueue::pop() noexcept {
    return {PopState::Closed, 0};
}

PopResult WorkQueue::try_pop() noexcept {
    return {PopState::Empty, 0};
}

void WorkQueue::close() noexcept {
    closed_ = true;
}

void WorkQueue::notify_waiters_for_test() noexcept {}

std::size_t WorkQueue::size() const noexcept {
    return count_;
}

bool WorkQueue::closed() const noexcept {
    return closed_;
}
}
