#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <span>
#include <utility>
#include <variant>

namespace g02 {
template <typename Value, typename Error>
class Result {
public:
    explicit Result(Value&& value) : storage_{std::move(value)} {}
    explicit Result(Error error) : storage_{error} {}

    [[nodiscard]] bool has_value() const noexcept {
        return std::holds_alternative<Value>(storage_);
    }

    [[nodiscard]] Value& value() & {
        return std::get<Value>(storage_);
    }

    [[nodiscard]] const Value& value() const& {
        return std::get<Value>(storage_);
    }

    [[nodiscard]] Error error() const {
        return std::get<Error>(storage_);
    }

private:
    std::variant<Value, Error> storage_;
};

enum class OwnerError : std::uint8_t {
    Empty,
    TooLarge,
    AllocationFailed,
};

enum class LeaseError : std::uint8_t {
    MovedFrom,
};

struct MessageStorage {
    std::array<std::byte, 256U> bytes{};
    std::size_t size{0U};
    std::uint32_t sequence{0U};
};

class PayloadLease {
public:
    PayloadLease(const PayloadLease&) noexcept = default;
    PayloadLease& operator=(const PayloadLease&) noexcept = default;
    PayloadLease(PayloadLease&& other) noexcept;
    PayloadLease& operator=(PayloadLease&& other) noexcept;
    ~PayloadLease() = default;

    [[nodiscard]] std::span<const std::byte> bytes() const noexcept;
    [[nodiscard]] std::uint32_t sequence() const noexcept;

private:
    friend class MessageOwner;
    explicit PayloadLease(std::shared_ptr<const MessageStorage> storage) noexcept;

    std::shared_ptr<const MessageStorage> storage_;
};

class MessageOwner {
public:
    static constexpr std::size_t max_payload_size = 256U;

    MessageOwner(const MessageOwner&) = delete;
    MessageOwner& operator=(const MessageOwner&) = delete;
    MessageOwner(MessageOwner&&) noexcept = default;
    MessageOwner& operator=(MessageOwner&&) noexcept = default;
    ~MessageOwner() = default;

    [[nodiscard]] static Result<MessageOwner, OwnerError> create(
        std::span<const std::byte> bytes,
        std::uint32_t sequence) noexcept;
    [[nodiscard]] Result<PayloadLease, LeaseError> lease() const noexcept;
#if G02_TESTING
    [[nodiscard]] std::weak_ptr<const MessageStorage> weak_backing_for_test() const noexcept {
        return storage_;
    }
#endif

private:
    explicit MessageOwner(std::shared_ptr<MessageStorage> storage) noexcept;

    std::shared_ptr<MessageStorage> storage_;
};
}
