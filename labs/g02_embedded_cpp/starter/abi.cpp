#include "g02_abi.hpp"

namespace g02 {
ScenarioResult run_virtual(FakeDependencies&) noexcept {
    return {OperationStatus::Failed, 0, 0U};
}

ScenarioResult run_static(FakeDependencies&) noexcept {
    return {OperationStatus::Failed, 0, 0U};
}

ScenarioResult run_manual(FakeDependencies&) noexcept {
    return {OperationStatus::Failed, 0, 0U};
}
}

struct G02RuntimeHandle {};

std::int32_t g02_runtime_create(
    const G02CDependencies*,
    G02RuntimeHandle** output) noexcept {
    if (output != nullptr) {
        *output = nullptr;
    }
    return G02_C_INVALID_ARGUMENT;
}

std::int32_t g02_runtime_run(G02RuntimeHandle*, std::int32_t*) noexcept {
    return G02_C_INVALID_ARGUMENT;
}

void g02_runtime_destroy(G02RuntimeHandle*) noexcept {}
