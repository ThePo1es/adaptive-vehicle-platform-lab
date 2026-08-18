# System Requirements

요구사항은 구현 전에 작성하고, 검증 가능한 `shall` 문장으로 유지합니다. 상태가 확정되지 않은 항목은 `Draft`로 둡니다.

## RTOS timing and safe behavior

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-RTOS-001 | Each periodic task shall record scheduled release, actual release, start, finish and deadline outcome using a monotonic clock. | Timing test + raw trace review | Draft |
| REQ-RTOS-002 | A task overrun or deadline miss shall increment an observable counter and trigger the configured deterministic degraded or safe action. | Overload fault-injection test | Draft |
| REQ-RTOS-003 | ISR-to-task communication shall use bounded storage with an explicit full policy and shall not perform an unbounded wait in interrupt context. | Queue saturation test + code review | Draft |
| REQ-RTOS-004 | Each task shall have a documented stack budget, measured high-water mark and detectable overflow policy. | Stress test + stack report | Draft |
| REQ-SAFE-001 | Simulated actuator outputs shall initialize to and return to the defined safe value on fatal fault, watchdog reset or invalid state transition. | Reset/fault state test | Draft |

## Communication

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-COM-001 | Vehicle State Service shall provide a versioned service instance discoverable on the configured interface. | Integration test + packet capture | Draft |
| REQ-COM-002 | The client shall recover availability after the service is restarted without restarting the client process. | Fault-injection test | Draft |
| REQ-COM-003 | Event delivery shall enforce a bounded queue and expose a drop counter under overload. | Load test | Draft |
| REQ-COM-004 | The service shall reject or explicitly handle an incompatible major interface version. | Negative integration test | Draft |

## Execution and State

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-EXEC-001 | The manager shall start applications in dependency order and reject cyclic dependencies. | Unit/integration test | Draft |
| REQ-EXEC-002 | The manager shall request graceful termination before forcefully terminating an unresponsive process. | Integration test | Draft |
| REQ-EXEC-003 | A restart policy shall enforce both a retry limit and backoff interval. | Fault-injection test | Draft |
| REQ-STATE-001 | Update activation shall be rejected while the system is in Driving state. | State transition test | Draft |
| REQ-HEALTH-001 | A missed heartbeat deadline shall cause a deterministic degraded or recovery transition. | Virtual-time unit test | Draft |

## Diagnostics and CAN

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-DIAG-001 | The gateway shall translate supported DoIP diagnostic requests to CAN ISO-TP and return the corresponding response. | vcan integration test | Draft |
| REQ-DIAG-002 | Unsupported or unauthorized diagnostic services shall be rejected and audited. | Negative policy test | Draft |
| REQ-DIAG-003 | A malformed, truncated or timed-out ISO-TP/UDS request shall be rejected without corrupting diagnostic or application state. | Negative corpus + state invariant test | Draft |
| REQ-CAN-001 | CAN input processing shall remain bounded under a configured flood rate. | Load/fault test | Draft |
| REQ-CAN-002 | Malformed or truncated signal input shall not update the published vehicle state. | Fuzz/property test | Draft |
| REQ-CAN-003 | A bus-off indication shall make communication unavailable, preserve an observable reason and follow a bounded recovery policy. | Bus-off simulation + recovery test | Draft |

## Boot and MCU update

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-BOOT-001 | The boot manager shall select only an image whose metadata, target, version and configured integrity checks are valid. | Positive/negative image corpus | Draft |
| REQ-BOOT-002 | Loss of power or reset during an update shall leave a previously known-good image bootable or enter an explicit recovery mode. | Reset-at-each-state test | Draft |
| REQ-BOOT-003 | Firmware version, selected slot and reset reason shall be observable after boot and retained across the configured reset classes. | Reboot integration test | Draft |

## Secure Update

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-UCM-001 | The update manager shall verify manifest and payload integrity before staging. | Tamper test | Draft |
| REQ-UCM-002 | The update manager shall verify an authorized package signature before installation. | Signature positive/negative test | Draft |
| REQ-UCM-003 | The update manager shall reject a version lower than the persisted minimum accepted version. | Downgrade test | Draft |
| REQ-UCM-004 | Failed post-activation health checks shall restore the previous known-good slot. | Rollback integration test | Draft |
| REQ-UCM-005 | An interrupted update shall recover to a defined state using a durable transaction journal. | Crash-at-each-state test | Draft |

## Cross-node architecture

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-ARCH-001 | End-to-end vehicle data shall carry sufficient timestamp, sequence and quality information to distinguish fresh, stale, lost and unavailable data. | Contract and loss/reorder tests | Draft |
| REQ-ARCH-002 | Timing, CPU, memory and network budgets shall be documented per component and reconciled with measured totals and margin. | Budget report review | Draft |
| REQ-ARCH-003 | MCU and Linux state machines shall define deterministic propagation and containment for task overrun, watchdog reset, bus-off, process crash and network loss. | End-to-end fault campaign | Draft |
| REQ-ARCH-004 | An incompatible MCU firmware, gateway or service-interface version shall be rejected before activation or handled by a documented degraded policy. | Compatibility matrix test | Draft |
| REQ-ARCH-005 | Every critical system requirement shall link to an architecture decision, implementation, automated verification and commit-specific result. | Traceability audit | Draft |
| REQ-TOOL-001 | Critical functions shall have a reproducible GCC/Clang analysis comparing selected optimization profiles and target code for Cortex-M and AArch64. | Compiler-analysis report replay | Draft |

## Observability and Quality

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-OBS-001 | Every lifecycle, policy, and update state transition shall produce a structured audit event. | Log assertion test | Draft |
| REQ-PERF-001 | Performance reports shall include p50, p95, p99, sample count, CPU and RSS under a documented workload. | Benchmark report review | Draft |
| REQ-QUAL-001 | Supported builds shall pass unit and integration tests under GCC and Clang. | CI | Draft |
| REQ-QUAL-002 | Testable components shall run under ASan and UBSan without reported errors. | CI/runtime evidence | Draft |

## 변경 규칙

- ID는 한 번 공개한 뒤 재사용하지 않습니다.
- 구현 세부사항보다 외부에서 관찰 가능한 동작을 적습니다.
- `Verification`이 불명확하면 요구사항도 아직 불명확한 것입니다.
- 요구사항 변경 PR은 [traceability.md](traceability.md)를 함께 갱신합니다.
