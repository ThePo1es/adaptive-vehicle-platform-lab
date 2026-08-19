# System Requirements

요구사항은 `Draft → Baselined → Implemented → Verified` 순서로 진행합니다. `Baselined`로 올릴 때 stimulus, precondition, observable response, time/tolerance, rationale, applicable node를 확정하고 설계 배정과 검증 계획을 연결합니다. 수치는 버전이 붙은 설정 파일에 고정하고 요구사항에서 그 항목을 참조합니다.

| 상태 | 들어가기 위한 조건 |
| --- | --- |
| Draft | 논의 중인 문장. 링크가 없어도 됨 |
| Baselined | 문장·근거·인수 조건을 검토했고 설계 배정과 검증 계획을 연결함 |
| Implemented | 설계, 구현, 자동 검증 위치를 모두 연결함. 시험 결과는 아직 `Not run`일 수 있음 |
| Verified | 고정한 커밋 또는 CI 실행에서 통과했고 검토자가 결과를 확인함 |

## RTOS timing

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-RTOS-001 | MCU | Each periodic task shall record scheduled release, actual release, start, finish and deadline outcome using the configured monotonic clock. | Trace schema and timing test | Draft |
| REQ-RTOS-002 | MCU | The task set shall define period or minimum inter-arrival time, deadline, priority, blocking resource and provisional execution bound before implementation acceptance. | Task-model review | Draft |
| REQ-RTOS-003 | MCU | Fixed-priority tasks shall have a response-time analysis that includes release jitter, blocking and configured interrupt interference. | Independent calculation + review | Draft |
| REQ-RTOS-004 | MCU | A deadline miss or overrun shall increment an observable counter and execute the configured bounded response. | Overload fault test | Draft |
| REQ-RTOS-005 | MCU | ISR-to-task communication shall use bounded storage with a configured full policy and no unbounded wait in interrupt context. | Queue saturation test + code review | Draft |
| REQ-RTOS-006 | MCU | Each task shall have a stack budget, measured high-water mark, margin rationale and detectable overflow response. | Stress test + stack report | Draft |
| REQ-FALLBACK-001 | MCU simulation | Simulated outputs shall enter the state defined by the current functional or hazard analysis after fatal fault, watchdog reset or invalid transition. | Reset/fault state test | Draft |

## CAN and ECU diagnostics

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-CAN-001 | MCU/Linux adapter | CAN input processing shall remain within the configured CPU and queue budget under the specified flood workload. | Load test + budget review | Draft |
| REQ-CAN-002 | MCU/Linux adapter | A malformed, out-of-range or truncated signal shall leave the last valid application value unchanged and update the configured quality counter. | Property/fuzz test | Draft |
| REQ-CAN-003 | MCU | A bus-off indication shall publish communication unavailable with the controller error state and follow the configured recovery limit and delay. | Physical bench + simulation | Draft |
| REQ-CAN-004 | MCU | The selected CAN message set shall have calculated load and priority response-time bounds for the configured bit timing. | Analysis + trace comparison | Draft |
| REQ-CAN-005 | MCU/Linux adapter | CAN FD DLC values shall map to payload lengths 0–64 exactly, and Classic/FD frame-type mismatches shall be rejected before signal decode. | Golden vectors + mixed-frame negative test | Draft |
| REQ-CAN-006 | MCU/bench | Nominal bit rate, data bit rate, BRS and ESI behavior shall be recorded with controller and transceiver capability; unsupported combinations shall fail configuration. | Capability review + physical trace | Draft |
| REQ-CAN-007 | MCU | CAN FD load and priority bounds shall include arbitration phase, data phase, payload length and the stated stuffing assumption. | Analysis + analyzer comparison | Draft |
| REQ-ECU-DIAG-001 | MCU | The ECU shall support the configured read-only UDS services and return the specified NRC for unsupported or disallowed requests. | Tester interoperability | Draft |
| REQ-ECU-DIAG-002 | MCU | ISO-TP shall enforce the configured addressing, BS, STmin, sequence and timeout rules without corrupting application state. | Timer matrix + negative corpus | Draft |
| REQ-ECU-DIAG-003 | MCU | Diagnostic work shall remain bounded under the specified request rate and shall expose queue, timeout and rejection counters. | Load/fault test | Draft |
| REQ-DTC-001 | MCU | A configured application fault shall update its event and DTC state with timestamp or occurrence metadata. | State-model test | Draft |
| REQ-DTC-002 | MCU | Persisted DTC records shall recover the last committed valid version or configured default after reset or corruption. | Reboot/corruption test | Draft |

## Communication and gateway

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-SI-001 | Linux service/client | The language-neutral Service Interface shall define each method, event and field with type, unit, range, error, freshness and compatibility semantics independently of transport deployment. | Contract review + golden vectors | Draft |
| REQ-SI-002 | Code generator | Proxy and Skeleton artifacts shall be generated deterministically from a versioned interface input and shall not contain hand-written application logic. | Clean generation + tree hash + build | Draft |
| REQ-SI-003 | Linux service/client | Generated Proxy and Skeleton boundaries shall pass method, event, subscription-lifetime and error tests with an in-memory transport before SOME/IP binding. | Generated-code integration test | Draft |
| REQ-SI-004 | Release | Interface changes shall have an old/new client-service compatibility matrix and shall identify whether regeneration, rebuild or major-version change is required. | Four-way compatibility test | Draft |
| REQ-COM-001 | Linux | Vehicle State Service shall provide the configured versioned service instance on the specified interface. | Integration test + packet capture | Draft |
| REQ-COM-002 | Linux client | The client shall restore availability and subscription within the configured recovery time after service restart. | Restart test | Draft |
| REQ-COM-003 | Linux service | Event delivery shall use a bounded queue and expose drop, stale and unavailable counters under the configured workload. | Load test | Draft |
| REQ-COM-004 | Linux | An incompatible major interface version shall be rejected before data exchange; minor-version behavior shall follow the compatibility matrix. | Negative integration test | Draft |
| REQ-COM-005 | MCU/Linux | Vehicle data shall carry a payload rolling counter, source boot/session identity, source timestamp, unit and quality sufficient to classify fresh, stale, lost and unavailable states. A gateway observation counter shall not be presented as proof of upstream CAN delivery. | Contract tests | Draft |
| REQ-GW-DIAG-001 | Linux gateway | The gateway shall route only configured DoIP diagnostic targets and read services to the mapped CAN ISO-TP endpoint. | Bench integration test | Draft |
| REQ-GW-DIAG-002 | Linux gateway | Routing activation, alive check and diagnostic timeout shall follow the versioned gateway policy; DoIP rejection, backend transport failure and ECU-originated UDS NRC shall remain distinct results. | Protocol-state test | Draft |
| REQ-GW-DIAG-003 | Linux gateway | A disallowed caller, target or service shall be rejected and recorded with a correlation identifier. | Policy negative test | Draft |

## Execution, state and Linux platform

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-EXEC-001 | Linux | The manager shall validate dependencies, reject cycles and start applications in topological order. | Unit/integration test | Draft |
| REQ-EXEC-002 | Linux | The manager shall request graceful termination before the configured timeout and shall use a dedicated containment unit to terminate and reap descendants that change session or process group. | cgroup/pidfd process-tree test | Draft |
| REQ-EXEC-003 | Linux | Each restart policy shall define retry limit, backoff range and terminal action. | Virtual-time fault test | Draft |
| REQ-EXEC-004 | Linux | Each managed process shall have exactly one lifecycle decision owner and one restart actuator; systemd, P01, P03, PHM and UCM roles shall match the versioned ownership table. | Ownership inspection + concurrent-recovery test | Draft |
| REQ-STATE-001 | Linux/system | The state model shall define allowed transitions and block update activation in the configured operational states. | Model-based test | Draft |
| REQ-STATE-002 | Linux/system | Boot shall begin in Startup and shall revalidate current vehicle conditions, software compatibility and process inventory before reapplying any persisted request. | Reboot/reconciliation test | Draft |
| REQ-HEALTH-001 | Linux | A missed heartbeat or deadline shall create an observation and trigger the configured state or lifecycle action within its time bound. | Virtual-time integration test | Draft |
| REQ-PLAT-001 | Linux | The reference image shall be reproducible from pinned configuration and shall emit image hash, package list and SBOM. | Clean image build | Draft |
| REQ-PLAT-002 | Linux | Platform services shall run with configured capabilities, resource limits and restart policy. | Policy inspection + fault test | Draft |
| REQ-PLAT-003 | Linux | A crash shall preserve the configured core/log artifacts and correlation data required for diagnosis. | Seeded crash test | Draft |
| REQ-PLAT-004 | Linux | A read-only root filesystem shall define bounded writable locations for logs, cores, persistency and update staging with quota, access-control and retention policy. | Image inspection + exhaustion test | Draft |
| REQ-LINUX-RT-001 | Linux | Scheduling policy, priority, affinity, memory-lock and privilege application shall be verified at runtime and failure shall be observable. | Scheduler configuration test | Draft |
| REQ-LINUX-RT-002 | Linux | Priority-inversion experiments shall compare the selected mutex protocols under a fixed workload and retain scheduler traces around the worst blocking interval. | Trace replay + report review | Draft |
| REQ-LINUX-RT-003 | Linux target | PREEMPT_RT comparison shall use the same kernel release, toolchain, target and workload with a recorded configuration delta; VM timing shall not be used as target latency evidence. | Image manifest + repeated target measurement | Draft |

## Adaptive diagnostics and access policy

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-AD-DIAG-001 | Linux diagnostic manager | DoIP transport, authorization, diagnostic routing, UDS semantics and application data-provider responsibilities shall be separate interfaces and trace events. | Architecture review + scenario test | Draft |
| REQ-AD-DIAG-002 | Linux diagnostic manager | The core release shall route only configured read-only services and shall prevent disallowed requests from reaching an application or CAN backend. | Negative request corpus | Draft |
| REQ-AD-DIAG-003 | Linux diagnostic manager | Provider unavailable, provider timeout, routing rejection and ECU-originated UDS NRC shall remain distinguishable to audit and metrics. | Fault-isolation test | Draft |
| REQ-AD-DIAG-004 | Linux diagnostic manager | Concurrent testers, in-flight requests, payload size and provider wait time shall have versioned bounds and observable rejection counters. | Load and restart test | Draft |
| REQ-IAM-001 | Linux security service | Authorization shall consume an authenticated principal, action, resource, context and immutable policy version; IP address, SOME/IP Client ID and DoIP logical address alone are not principals. | Spoofing negative tests | Draft |
| REQ-IAM-002 | Linux security service | Local principal identity shall come from kernel-provided peer credentials bound to the current process instance; the optional network lane shall use an authenticated channel and explicit certificate-to-principal mapping. | Credential and stale-instance test | Draft |
| REQ-IAM-003 | Linux security service | Policy shall be default-deny, schema-validated and atomically reloaded so each decision uses one identifiable version. | Policy corpus + concurrent reload test | Draft |
| REQ-IAM-004 | Linux audit | Allow and deny decisions shall record principal, action, resource, rule, policy hash and correlation data without storing secret or credential material. | Audit assertion + secret scan | Draft |

## Boot and update

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-BOOT-001 | MCU/target | The boot path shall accept only an image whose target, format, metadata and configured integrity/authenticity policy pass. | Positive/negative image corpus | Draft |
| REQ-BOOT-002 | MCU/target | Reset or power interruption during update shall leave the previous committed image bootable or enter the documented recovery path. | Reset/power-cut matrix | Draft |
| REQ-BOOT-003 | MCU/target | Image version, selected slot, validation result and reset reason shall be observable after the configured reset classes. | Reboot integration test | Draft |
| REQ-UCM-001 | Linux/update target | The updater shall strictly parse one canonical manifest format and reject unknown, duplicate, malformed and out-of-range security-relevant fields. | Parser corpus | Draft |
| REQ-UCM-002 | Linux/update target | The authenticated tier shall verify an authorized package signature and every payload hash before staging. | Cryptographic corpus | Draft |
| REQ-UCM-003 | Linux/update target | The rollback-protected tier shall reject a version below the protected minimum accepted version. | Downgrade + power-cut test | Draft |
| REQ-UCM-004 | Linux/update target | Activation shall keep the previous committed slot unchanged until the new version passes its configured health check. | Integration test | Draft |
| REQ-UCM-005 | Linux/update target | Every durable transaction state shall recover to the reference state model after interruption. | Kill-at-each-state test | Draft |
| REQ-UCM-006 | Linux/update target | Package paths shall remain inside the staging root across traversal, symlink, hard-link and file-swap attempts. | Filesystem attack corpus | Draft |
| REQ-UCM-007 | Linux/update target | Key identity, authorization, rotation/revocation assumption and recovery path shall be versioned and auditable. | Policy review + negative test | Draft |
| REQ-UCM-008 | Linux/update target | Transfer resume shall verify immutable remote object identity, expected size and local durable progress; changed or ambiguous objects shall restart from a clean staging object. | Interruption/object-change matrix | Draft |
| REQ-UCM-009 | Linux/update target | Update staging shall be isolated from active executable paths and shall preserve the committed slot under quota, disk-full and inode-exhaustion faults. | Storage-exhaustion campaign | Draft |
| REQ-UCM-010 | Linux/update target | Processing and activation shall enforce package dependency, software compatibility and allowed Function Group State before slot selection and shall use the configured health result before commit. | State/version/health integration test | Draft |

## Time and architecture

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-TIME-001 | MCU/Linux | Each cross-node timestamp shall identify its clock domain and measurement point. | Interface review + test | Draft |
| REQ-TIME-002 | MCU/Linux | Clock offset, drift and uncertainty shall be measured or bounded for any one-way latency or freshness claim. | Calibration report | Draft |
| REQ-TIME-003 | MCU/Linux | A synchronization loss beyond the configured uncertainty shall update data quality and suppress unsupported one-way latency claims. | Sync-loss test | Draft |
| REQ-ARCH-001 | System | Timing, CPU, memory, storage and network budgets shall be allocated per component with rationale and margin. | Budget review | Draft |
| REQ-ARCH-002 | System | Measured totals shall be reconciled with analytical budgets under the versioned acceptance workload. | Report replay | Draft |
| REQ-ARCH-003 | System | MCU and Linux state models shall define propagation and containment for overrun, watchdog reset, bus-off, process crash, network loss and update failure. | End-to-end campaign | Draft |
| REQ-ARCH-004 | System | Incompatible MCU firmware, gateway or service versions shall be blocked or handled by a versioned degraded policy. | Compatibility matrix test | Draft |
| REQ-ARCH-005 | System | Each baselined requirement shall link to design allocation and verification plan; each implemented or verified requirement shall also link to implementation and commit-specific verification evidence. | Traceability audit | Draft |
| REQ-ARCH-006 | System | Each interface shall define data, units, range, ownership, timing, version, error and fallback behavior. | Contract review | Draft |

## Safety, security, observability and quality

| ID | Applies to | Requirement | Verification | Status |
| --- | --- | --- | --- | --- |
| REQ-SAFE-001 | Safety claim | Each safety claim shall link item assumption, hazard/safety goal, derived requirement, mechanism and verification evidence. | Assurance-case review | Draft |
| REQ-SAFE-002 | System | Shared CPU, memory, network, storage and logging interference shall have an identified control or documented residual gap. | Interference analysis + fault test | Draft |
| REQ-SEC-001 | System | Trust boundaries, attacker capabilities, assets and residual risks shall be versioned with the release. | TARA review | Draft |
| REQ-SEC-002 | Diagnostic/update | Security-relevant authorization decisions shall identify the authenticated principal, requested action and policy version. | Audit/policy test | Draft |
| REQ-OBS-001 | System | Lifecycle, state, policy, fault and update transitions shall emit a structured event with reason and correlation data. | Log assertion test | Draft |
| REQ-PERF-001 | Linux | Performance reports shall include p50, p95, p99, measured worst, sample count, CPU and RSS for a versioned workload. | Report review | Draft |
| REQ-TOOL-001 | Critical functions | GCC/Clang analysis shall pin compiler, target, CPU, ABI, flags and linker and shall compare code size and runtime within each target. | Report replay | Draft |
| REQ-QUAL-001 | Host/Linux | Supported code builds shall pass unit and integration tests under the pinned GCC and Clang versions. | CI | Draft |
| REQ-QUAL-002 | Testable host code | Applicable components shall run under ASan and UBSan without findings. | CI/runtime evidence | Draft |
| REQ-QUAL-003 | Parser/state components | Test strength shall include coverage plus mutation, model or differential evidence selected in the component test plan. | Test-plan audit | Draft |
| REQ-QUAL-004 | Release | The release shall include clean reproduction instructions and a reviewer record. | Third-party replay | Draft |

## 변경 규칙

- 공개한 ID는 재사용하지 않습니다.
- `bounded`, `configured`, `supported`가 가리키는 수치와 목록을 versioned 파일에 연결합니다.
- `Baselined` 요구사항은 설계 배정과 검증 계획을 연결합니다.
- `Implemented` 요구사항은 설계·구현·자동 검증 링크를 모두 가집니다.
- `Verified` 요구사항은 전체 40자리 commit SHA 또는 CI 실행을 붙인 `Pass` 결과와 검토자를 가집니다.
- 변경 PR은 [traceability.md](traceability.md)와 영향 받는 budget·test를 함께 갱신합니다.
