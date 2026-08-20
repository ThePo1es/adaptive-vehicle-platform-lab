#include "g02_abi.hpp"

#include <new>

#ifndef G02_MUTANT
#define G02_MUTANT 0
#endif

namespace {
class Clock {
public:
    virtual ~Clock() = default;
    [[nodiscard]] virtual std::int32_t now() const noexcept = 0;
};

class Transport {
public:
    virtual ~Transport() = default;
    [[nodiscard]] virtual g02::OperationStatus send(std::int32_t& value) noexcept = 0;
};

class Launcher {
public:
    virtual ~Launcher() = default;
    [[nodiscard]] virtual std::int32_t launch() noexcept = 0;
    virtual void cleanup() noexcept = 0;
};

class VirtualDependencies final : public Clock, public Transport, public Launcher {
public:
    explicit VirtualDependencies(g02::FakeDependencies& dependencies) noexcept
        : dependencies_{dependencies} {}

    [[nodiscard]] std::int32_t now() const noexcept override {
        return dependencies_.clock_value;
    }

    [[nodiscard]] g02::OperationStatus send(std::int32_t& value) noexcept override {
        if (dependencies_.timeout) {
            return g02::OperationStatus::Timeout;
        }
        value = dependencies_.transport_value;
        return g02::OperationStatus::Ok;
    }

    [[nodiscard]] std::int32_t launch() noexcept override {
        return dependencies_.launcher_value;
    }

    void cleanup() noexcept override {
        ++dependencies_.cleanup_count;
    }

private:
    g02::FakeDependencies& dependencies_;
};

template <typename Dependencies>
g02::ScenarioResult execute_static(Dependencies& dependencies) noexcept {
    std::int32_t transport = 0;
    const auto status = dependencies.send(transport);
    if (status != g02::OperationStatus::Ok) {
        dependencies.cleanup();
        return {status, 0, dependencies.cleanup_count()};
    }
    const auto checksum = dependencies.now() + transport + dependencies.launch();
    dependencies.cleanup();
    return {g02::OperationStatus::Ok, checksum, dependencies.cleanup_count()};
}

class StaticDependencies {
public:
    explicit StaticDependencies(g02::FakeDependencies& dependencies) noexcept
        : dependencies_{dependencies} {}

    [[nodiscard]] std::int32_t now() const noexcept {
        return dependencies_.clock_value;
    }

    [[nodiscard]] g02::OperationStatus send(std::int32_t& value) noexcept {
        if (dependencies_.timeout) {
            return g02::OperationStatus::Timeout;
        }
        value = dependencies_.transport_value;
        return g02::OperationStatus::Ok;
    }

    [[nodiscard]] std::int32_t launch() const noexcept {
        return dependencies_.launcher_value;
    }

    void cleanup() noexcept {
        ++dependencies_.cleanup_count;
    }

    [[nodiscard]] std::size_t cleanup_count() const noexcept {
        return dependencies_.cleanup_count;
    }

private:
    g02::FakeDependencies& dependencies_;
};

struct ManualTable {
    std::int32_t (*now)(void*) noexcept;
    g02::OperationStatus (*send)(void*, std::int32_t&) noexcept;
    std::int32_t (*launch)(void*) noexcept;
    void (*cleanup)(void*) noexcept;
};

std::int32_t manual_now(void* context) noexcept {
    return static_cast<g02::FakeDependencies*>(context)->clock_value;
}

g02::OperationStatus manual_send(void* context, std::int32_t& value) noexcept {
    auto& dependencies = *static_cast<g02::FakeDependencies*>(context);
    if (dependencies.timeout) {
        return G02_MUTANT == 402 ? g02::OperationStatus::Ok : g02::OperationStatus::Timeout;
    }
    value = dependencies.transport_value;
    return g02::OperationStatus::Ok;
}

std::int32_t manual_launch(void* context) noexcept {
    return static_cast<g02::FakeDependencies*>(context)->launcher_value;
}

void manual_cleanup(void* context) noexcept {
    ++static_cast<g02::FakeDependencies*>(context)->cleanup_count;
}
}

namespace g02 {
ScenarioResult run_virtual(FakeDependencies& dependencies) noexcept {
    VirtualDependencies adapter{dependencies};
    std::int32_t transport = 0;
    const auto status = adapter.send(transport);
    if (status != OperationStatus::Ok) {
        if constexpr (G02_MUTANT != 401) {
            adapter.cleanup();
        }
        return {status, 0, dependencies.cleanup_count};
    }
    const auto checksum = adapter.now() + transport + adapter.launch();
    adapter.cleanup();
    return {OperationStatus::Ok, checksum, dependencies.cleanup_count};
}

ScenarioResult run_static(FakeDependencies& dependencies) noexcept {
    StaticDependencies adapter{dependencies};
    return execute_static(adapter);
}

ScenarioResult run_manual(FakeDependencies& dependencies) noexcept {
    constexpr ManualTable table{manual_now, manual_send, manual_launch, manual_cleanup};
    std::int32_t transport = 0;
    const auto status = table.send(&dependencies, transport);
    if (status != OperationStatus::Ok) {
        table.cleanup(&dependencies);
        return {status, 0, dependencies.cleanup_count};
    }
    const auto checksum = table.now(&dependencies) + transport + table.launch(&dependencies);
    table.cleanup(&dependencies);
    return {OperationStatus::Ok, checksum, dependencies.cleanup_count};
}
}

struct G02RuntimeHandle {
    G02CDependencies dependencies;
};

std::int32_t g02_runtime_create(
    const G02CDependencies* dependencies,
    G02RuntimeHandle** output) noexcept {
    if (output == nullptr) {
        return G02_C_INVALID_ARGUMENT;
    }
    *output = nullptr;
    if (dependencies == nullptr || dependencies->context == nullptr ||
        dependencies->clock_now == nullptr || dependencies->transport_send == nullptr ||
        dependencies->launch == nullptr || dependencies->cleanup == nullptr) {
        return G02_C_INVALID_ARGUMENT;
    }
    auto* handle = new (std::nothrow) G02RuntimeHandle{*dependencies};
    if (handle == nullptr) {
        return G02_C_NO_MEMORY;
    }
    *output = handle;
    return G02_C_OK;
}

std::int32_t g02_runtime_run(G02RuntimeHandle* handle, std::int32_t* checksum) noexcept {
    if (handle == nullptr || checksum == nullptr) {
        return G02_C_INVALID_ARGUMENT;
    }
    *checksum = 0;
    auto& dependencies = handle->dependencies;
    std::int32_t transport = 0;
    const std::int32_t transport_status =
        dependencies.transport_send(dependencies.context, &transport);
    if (transport_status == G02_C_TIMEOUT) {
        if constexpr (G02_MUTANT != 403) {
            dependencies.cleanup(dependencies.context);
        }
        return G02_C_TIMEOUT;
    }
    if (transport_status != G02_C_OK) {
        dependencies.cleanup(dependencies.context);
        return G02_C_FAILED;
    }
    std::int32_t launcher = 0;
    if (dependencies.launch(dependencies.context, &launcher) != G02_C_OK) {
        dependencies.cleanup(dependencies.context);
        return G02_C_FAILED;
    }
    std::int32_t clock = 0;
    if (dependencies.clock_now(dependencies.context, &clock) != G02_C_OK) {
        dependencies.cleanup(dependencies.context);
        return G02_C_FAILED;
    }
    *checksum = clock + transport + launcher;
    dependencies.cleanup(dependencies.context);
    return G02_C_OK;
}

void g02_runtime_destroy(G02RuntimeHandle* handle) noexcept {
    delete handle;
}
