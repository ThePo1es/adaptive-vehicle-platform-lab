#include "g02_lifetime.hpp"

#include <utility>

namespace g02 {
PayloadLease::PayloadLease(std::shared_ptr<const MessageStorage> storage) noexcept
    : storage_{std::move(storage)} {}

PayloadLease::PayloadLease(PayloadLease&& other) noexcept : storage_{other.storage_} {}

PayloadLease& PayloadLease::operator=(PayloadLease&& other) noexcept {
    storage_ = other.storage_;
    return *this;
}

std::span<const std::byte> PayloadLease::bytes() const noexcept {
    return {};
}

std::uint32_t PayloadLease::sequence() const noexcept {
    return 0U;
}

MessageOwner::MessageOwner(std::shared_ptr<MessageStorage> storage) noexcept
    : storage_{std::move(storage)} {}

Result<MessageOwner, OwnerError> MessageOwner::create(
    std::span<const std::byte> bytes,
    std::uint32_t) noexcept {
    return Result<MessageOwner, OwnerError>{
        bytes.empty() ? OwnerError::Empty : OwnerError::AllocationFailed};
}

Result<PayloadLease, LeaseError> MessageOwner::lease() const noexcept {
    return Result<PayloadLease, LeaseError>{LeaseError::MovedFrom};
}
}
