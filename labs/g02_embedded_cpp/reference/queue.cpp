#include "g02_queue.hpp"

#ifndef G02_MUTANT
#define G02_MUTANT 0
#endif

namespace g02 {
WorkQueue::WorkQueue(WaitObserver observer) noexcept : observer_{observer} {}

void WorkQueue::observe(WaitEvent event) const noexcept {
    if (observer_.function != nullptr) {
        observer_.function(observer_.context, event);
    }
}

void WorkQueue::insert(int value) noexcept {
    values_[tail_] = value;
    tail_ = (tail_ + 1U) % capacity;
    ++count_;
}

int WorkQueue::remove() noexcept {
    const int value = values_[head_];
    head_ = (head_ + 1U) % capacity;
    --count_;
    return value;
}

PushResult WorkQueue::push(int value) noexcept {
    std::unique_lock lock{mutex_};
    while (count_ == capacity && !closed_) {
        observe(WaitEvent::BeforeWait);
        not_full_.wait(lock);
        observe(WaitEvent::AfterWake);
        if constexpr (G02_MUTANT == 301) {
            break;
        }
    }
    if (closed_) {
        return PushResult::Closed;
    }
    insert(value);
    lock.unlock();
    not_empty_.notify_one();
    return PushResult::Accepted;
}

TryPushResult WorkQueue::try_push(int value) noexcept {
    std::lock_guard lock{mutex_};
    if (closed_) {
        return TryPushResult::Closed;
    }
    if (count_ == capacity) {
        return TryPushResult::Full;
    }
    insert(value);
    not_empty_.notify_one();
    return TryPushResult::Accepted;
}

PopResult WorkQueue::pop() noexcept {
    std::unique_lock lock{mutex_};
    while (count_ == 0U && !closed_) {
        not_empty_.wait(lock);
    }
    if (count_ == 0U) {
        return PopResult{PopState::Closed, 0};
    }
    const int value = remove();
    lock.unlock();
    not_full_.notify_one();
    return PopResult{PopState::Item, value};
}

PopResult WorkQueue::try_pop() noexcept {
    std::lock_guard lock{mutex_};
    if (count_ == 0U) {
        return PopResult{closed_ ? PopState::Closed : PopState::Empty, 0};
    }
    const int value = remove();
    not_full_.notify_one();
    return PopResult{PopState::Item, value};
}

void WorkQueue::close() noexcept {
    {
        std::lock_guard lock{mutex_};
        closed_ = true;
    }
    not_empty_.notify_all();
    if constexpr (G02_MUTANT != 302) {
        not_full_.notify_all();
    }
}

void WorkQueue::notify_waiters_for_test() noexcept {
    not_empty_.notify_all();
    not_full_.notify_all();
}

std::size_t WorkQueue::size() const noexcept {
    std::lock_guard lock{mutex_};
    return count_;
}

bool WorkQueue::closed() const noexcept {
    std::lock_guard lock{mutex_};
    return closed_;
}
}
