#include "g02_abi.hpp"
#include "test_support.hpp"

#if G02_RETEST
#include "retest-2.4-v1.hpp"
#else
#include "sprint-2.4-v1.hpp"
#endif

#include <array>
#include <cstdint>
#include <limits>

namespace {
using g02::FakeDependencies;
using g02::OperationStatus;
using g02::ScenarioResult;

FakeDependencies make_dependencies(bool timeout) {
    return FakeDependencies{
        g02::fixture::clock_value,
        g02::fixture::transport_value,
        g02::fixture::launcher_value,
        timeout,
    };
}

int test_three_designs_have_the_same_success_contract() {
    // Given three fresh dependency sets with the same successful behavior.
    auto virtual_deps = make_dependencies(false);
    auto static_deps = make_dependencies(false);
    auto manual_deps = make_dependencies(false);
    // When each design runs the same scenario.
    const std::array<ScenarioResult, 3> results{
        g02::run_virtual(virtual_deps),
        g02::run_static(static_deps),
        g02::run_manual(manual_deps),
    };
    // Then status, checksum and exactly-once cleanup are equivalent.
    for (const auto& result : results) {
        G02_CHECK(result.status == OperationStatus::Ok);
        G02_CHECK(result.checksum == g02::fixture::clock_value +
                                         g02::fixture::transport_value +
                                         g02::fixture::launcher_value);
        G02_CHECK(result.cleanup_count == 1U);
    }
    return 0;
}

int test_three_designs_cleanup_on_timeout() {
    // Given three fresh dependency sets whose transport reports timeout.
    auto virtual_deps = make_dependencies(true);
    auto static_deps = make_dependencies(true);
    auto manual_deps = make_dependencies(true);
    // When each design executes the timeout path.
    const std::array<ScenarioResult, 3> results{
        g02::run_virtual(virtual_deps),
        g02::run_static(static_deps),
        g02::run_manual(manual_deps),
    };
    // Then every design preserves Timeout and performs cleanup exactly once.
    for (const auto& result : results) {
        G02_CHECK(result.status == OperationStatus::Timeout);
        G02_CHECK(result.cleanup_count == 1U);
    }
    return 0;
}

int test_three_designs_reject_checksum_overflow() {
    // Given values whose positive and negative sums do not fit in int32_t.
    for (const auto clock : {std::numeric_limits<std::int32_t>::max(),
                             std::numeric_limits<std::int32_t>::min()}) {
        const std::int32_t transport = clock > 0 ? 1 : -1;
        auto virtual_deps = FakeDependencies{clock, transport, 0, false};
        auto static_deps = FakeDependencies{clock, transport, 0, false};
        auto manual_deps = FakeDependencies{clock, transport, 0, false};
        // When each design calculates the checksum.
        const std::array<ScenarioResult, 3> results{
            g02::run_virtual(virtual_deps),
            g02::run_static(static_deps),
            g02::run_manual(manual_deps),
        };
        // Then overflow is a value-level failure and cleanup still runs once.
        for (const auto& result : results) {
            G02_CHECK(result.status == OperationStatus::Failed);
            G02_CHECK(result.checksum == 0);
            G02_CHECK(result.cleanup_count == 1U);
        }
    }
    return 0;
}

std::int32_t c_clock(void* context, std::int32_t* output) noexcept {
    *output = static_cast<FakeDependencies*>(context)->clock_value;
    return G02_C_OK;
}

std::int32_t c_transport(void* context, std::int32_t* output) noexcept {
    const auto& deps = *static_cast<FakeDependencies*>(context);
    if (deps.timeout) {
        return G02_C_TIMEOUT;
    }
    *output = deps.transport_value;
    return G02_C_OK;
}

std::int32_t c_launch(void* context, std::int32_t* output) noexcept {
    *output = static_cast<FakeDependencies*>(context)->launcher_value;
    return G02_C_OK;
}

void c_cleanup(void* context) noexcept {
    ++static_cast<FakeDependencies*>(context)->cleanup_count;
}

int test_c_facade_has_one_owner_and_no_exception_boundary() {
    // Given an invalid request followed by a valid callback table.
    G02RuntimeHandle* handle = reinterpret_cast<G02RuntimeHandle*>(1U);
    G02_CHECK(g02_runtime_create(nullptr, &handle) == G02_C_INVALID_ARGUMENT);
    G02_CHECK(handle == nullptr);
    auto dependencies = make_dependencies(false);
    const G02CDependencies callbacks{
        &dependencies,
        c_clock,
        c_transport,
        c_launch,
        c_cleanup,
    };
    // When the C owner creates, runs and destroys the opaque handle.
    G02_CHECK(g02_runtime_create(&callbacks, &handle) == G02_C_OK);
    std::int32_t checksum = 0;
    G02_CHECK(g02_runtime_run(handle, &checksum) == G02_C_OK);
    g02_runtime_destroy(handle);
    // Then the output is stable and cleanup happened before ownership ended.
    G02_CHECK(checksum == g02::fixture::clock_value +
                              g02::fixture::transport_value +
                              g02::fixture::launcher_value);
    G02_CHECK(dependencies.cleanup_count == 1U);
    return 0;
}

int test_c_facade_cleans_up_timeout_path() {
    // Given a C callback table whose transport reports timeout.
    auto dependencies = make_dependencies(true);
    const G02CDependencies callbacks{
        &dependencies,
        c_clock,
        c_transport,
        c_launch,
        c_cleanup,
    };
    G02RuntimeHandle* handle = nullptr;
    G02_CHECK(g02_runtime_create(&callbacks, &handle) == G02_C_OK);
    std::int32_t checksum = 99;
    // When the opaque runtime executes that timeout path.
    const auto status = g02_runtime_run(handle, &checksum);
    g02_runtime_destroy(handle);
    // Then the error crosses C as a value, output is cleared and cleanup runs once.
    G02_CHECK(status == G02_C_TIMEOUT);
    G02_CHECK(checksum == 0);
    G02_CHECK(dependencies.cleanup_count == 1U);
    return 0;
}

int test_c_facade_rejects_checksum_overflow() {
    // Given callbacks that return values whose sum exceeds int32_t.
    auto dependencies = FakeDependencies{
        std::numeric_limits<std::int32_t>::max(), 1, 0, false};
    const G02CDependencies callbacks{
        &dependencies,
        c_clock,
        c_transport,
        c_launch,
        c_cleanup,
    };
    G02RuntimeHandle* handle = nullptr;
    G02_CHECK(g02_runtime_create(&callbacks, &handle) == G02_C_OK);
    std::int32_t checksum = 99;
    // When the C facade calculates the checksum.
    const auto status = g02_runtime_run(handle, &checksum);
    g02_runtime_destroy(handle);
    // Then no undefined signed overflow occurs at the ABI boundary.
    G02_CHECK(status == G02_C_FAILED);
    G02_CHECK(checksum == 0);
    G02_CHECK(dependencies.cleanup_count == 1U);
    return 0;
}
}

int main() {
    if (test_three_designs_have_the_same_success_contract() != 0 ||
        test_three_designs_cleanup_on_timeout() != 0 ||
        test_three_designs_reject_checksum_overflow() != 0 ||
        test_c_facade_has_one_owner_and_no_exception_boundary() != 0 ||
        test_c_facade_cleans_up_timeout_path() != 0 ||
        test_c_facade_rejects_checksum_overflow() != 0) {
        return 1;
    }
    std::puts("PASS ABI design equivalence contract");
    return 0;
}
