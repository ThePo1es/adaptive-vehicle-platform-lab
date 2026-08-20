#pragma once

#include "g02_abi_c.h"

#include <cstddef>
#include <cstdint>

namespace g02 {
enum class OperationStatus : std::uint8_t {
    Ok,
    Timeout,
    Failed,
};

struct FakeDependencies {
    std::int32_t clock_value{0};
    std::int32_t transport_value{0};
    std::int32_t launcher_value{0};
    bool timeout{false};
    std::size_t cleanup_count{0U};
};

struct ScenarioResult {
    OperationStatus status{OperationStatus::Failed};
    std::int32_t checksum{0};
    std::size_t cleanup_count{0U};
};

[[nodiscard]] ScenarioResult run_virtual(FakeDependencies& dependencies) noexcept;
[[nodiscard]] ScenarioResult run_static(FakeDependencies& dependencies) noexcept;
[[nodiscard]] ScenarioResult run_manual(FakeDependencies& dependencies) noexcept;
}
