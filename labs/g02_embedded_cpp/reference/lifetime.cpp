#include "g02_lifetime.hpp"

#include <algorithm>
#include <memory>

#ifndef G02_MUTANT
#define G02_MUTANT 0
#endif

namespace g02 {
PayloadLease::PayloadLease(std::shared_ptr<const MessageStorage> storage) noexcept
    : storage_{std::move(storage)} {}

PayloadLease::PayloadLease(PayloadLease&& other) noexcept : storage_{other.storage_} {}

PayloadLease& PayloadLease::operator=(PayloadLease&& other) noexcept {
    storage_ = other.storage_;
    return *this;
}

std::span<const std::byte> PayloadLease::bytes() const noexcept {
    const std::size_t size = G02_MUTANT == 102 && storage_->size > 0U
                                 ? storage_->size - 1U
                                 : storage_->size;
    return {storage_->bytes.data(), size};
}

std::uint32_t PayloadLease::sequence() const noexcept {
    return storage_->sequence;
}

MessageOwner::MessageOwner(std::shared_ptr<MessageStorage> storage) noexcept
    : storage_{std::move(storage)} {}

Result<MessageOwner, OwnerError> MessageOwner::create(
    std::span<const std::byte> bytes,
    std::uint32_t sequence) noexcept {
    if (bytes.empty()) {
        return Result<MessageOwner, OwnerError>{OwnerError::Empty};
    }
    if (bytes.size() > max_payload_size) {
        return Result<MessageOwner, OwnerError>{OwnerError::TooLarge};
    }
    try {
        auto storage = std::make_shared<MessageStorage>();
        std::copy(bytes.begin(), bytes.end(), storage->bytes.begin());
        storage->size = bytes.size();
        storage->sequence = sequence;
        return Result<MessageOwner, OwnerError>{MessageOwner{std::move(storage)}};
    } catch (const std::bad_alloc&) {
        return Result<MessageOwner, OwnerError>{OwnerError::AllocationFailed};
    }
}

Result<PayloadLease, LeaseError> MessageOwner::lease() const noexcept {
    if (!storage_) {
        return Result<PayloadLease, LeaseError>{LeaseError::MovedFrom};
    }
    if constexpr (G02_MUTANT == 101) {
        auto borrowed = std::shared_ptr<const MessageStorage>(
            storage_.get(), [](const MessageStorage*) noexcept {});
        return Result<PayloadLease, LeaseError>{PayloadLease{std::move(borrowed)}};
    }
    return Result<PayloadLease, LeaseError>{PayloadLease{storage_}};
}
}
