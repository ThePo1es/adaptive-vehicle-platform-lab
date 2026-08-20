#include "g02_lifetime.hpp"
#include "test_support.hpp"

#if G02_RETEST
#include "retest-2.1-v1.hpp"
#else
#include "sprint-2.1-v1.hpp"
#endif

#include <array>
#include <cstddef>
#include <deque>
#include <span>
#include <vector>

namespace {
using g02::LeaseError;
using g02::MessageOwner;
using g02::OwnerError;
using g02::PayloadLease;

int test_empty_payload_is_rejected() {
    // Given an empty byte range.
    const std::span<const std::byte> empty{};
    // When an owner is requested.
    const auto result = MessageOwner::create(empty, 1U);
    // Then the boundary reports Empty instead of constructing a partial owner.
    G02_CHECK(!result.has_value());
    G02_CHECK(result.error() == OwnerError::Empty);
    return 0;
}

int test_lease_survives_owner_move_and_container_relocation() {
    // Given an owner and a lease to its backing storage.
    auto result = MessageOwner::create(g02::fixture::payload, g02::fixture::sequence);
    G02_CHECK(result.has_value());
    std::vector<MessageOwner> owners;
    owners.reserve(1U);
    owners.push_back(std::move(result.value()));
    const auto lease_result = owners.front().lease();
    G02_CHECK(lease_result.has_value());
    const PayloadLease lease = lease_result.value();
    // When vector growth moves the owner.
    auto second = MessageOwner::create(g02::fixture::payload, 9U);
    G02_CHECK(second.has_value());
    owners.push_back(std::move(second.value()));
    // Then the lease still owns the original backing storage.
    G02_CHECK(lease.sequence() == g02::fixture::sequence);
    G02_CHECK(lease.bytes().size() == g02::fixture::payload.size());
    G02_CHECK(lease.bytes().front() == g02::fixture::payload.front());
    G02_CHECK(lease.bytes().back() == g02::fixture::payload.back());
    return 0;
}

int test_lease_survives_queue_pop_and_owner_destruction() {
    // Given a lease taken from an owner stored in a queue.
    std::deque<MessageOwner> queue;
    auto result = MessageOwner::create(g02::fixture::payload, g02::fixture::sequence);
    G02_CHECK(result.has_value());
    queue.push_back(std::move(result.value()));
    const auto original_backing = queue.front().weak_backing_for_test();
    const auto lease_result = queue.front().lease();
    G02_CHECK(lease_result.has_value());
    const PayloadLease lease = lease_result.value();
    // When the queue destroys its owner.
    queue.pop_front();
    // Then the retained lease remains readable under ASan.
    G02_CHECK(!original_backing.expired());
    G02_CHECK(lease.bytes().size() == g02::fixture::payload.size());
    G02_CHECK(lease.bytes()[2] == g02::fixture::payload[2]);
    return 0;
}

int test_moved_from_owner_has_one_explicit_result() {
    // Given an owner moved into another owner.
    auto result = MessageOwner::create(g02::fixture::payload, 77U);
    G02_CHECK(result.has_value());
    MessageOwner source = std::move(result.value());
    MessageOwner destination = std::move(source);
    // When the moved-from owner is queried.
    const auto source_result = source.lease();
    const auto destination_result = destination.lease();
    // Then it reports MovedFrom and the destination remains usable.
    G02_CHECK(!source_result.has_value());
    G02_CHECK(source_result.error() == LeaseError::MovedFrom);
    G02_CHECK(destination_result.has_value());
    return 0;
}

int test_maximum_payload_keeps_every_byte() {
    // Given the largest accepted payload.
    std::array<std::byte, MessageOwner::max_payload_size> bytes{};
    for (std::size_t index = 0; index < bytes.size(); ++index) {
        bytes[index] = std::byte{static_cast<unsigned char>(index)};
    }
    // When it is leased.
    auto result = MessageOwner::create(bytes, 91U);
    G02_CHECK(result.has_value());
    const auto lease_result = result.value().lease();
    G02_CHECK(lease_result.has_value());
    const auto lease = lease_result.value();
    // Then both boundary bytes and the exact length are preserved.
    G02_CHECK(lease.bytes().size() == MessageOwner::max_payload_size);
    G02_CHECK(lease.bytes().front() == std::byte{0x00});
    G02_CHECK(lease.bytes().back() == std::byte{0xFF});
    return 0;
}

int test_moving_lease_keeps_both_handles_valid() {
    // Given a valid lease.
    auto result = MessageOwner::create(g02::fixture::payload, g02::fixture::sequence);
    G02_CHECK(result.has_value());
    auto lease_result = result.value().lease();
    G02_CHECK(lease_result.has_value());
    PayloadLease source = lease_result.value();
    // When it is used to construct another lease.
    PayloadLease destination = std::move(source);
    // Then both handles retain the same immutable backing storage.
    G02_CHECK(source.bytes().size() == g02::fixture::payload.size());
    G02_CHECK(destination.sequence() == source.sequence());
    return 0;
}
}

int main() {
    if (test_empty_payload_is_rejected() != 0 ||
        test_lease_survives_owner_move_and_container_relocation() != 0 ||
        test_lease_survives_queue_pop_and_owner_destruction() != 0 ||
        test_moved_from_owner_has_one_explicit_result() != 0 ||
        test_maximum_payload_keeps_every_byte() != 0 ||
        test_moving_lease_keeps_both_handles_valid() != 0) {
        return 1;
    }
    std::puts("PASS lifetime lease contract");
    return 0;
}
