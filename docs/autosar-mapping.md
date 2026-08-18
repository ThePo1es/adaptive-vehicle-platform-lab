# AUTOSAR Concept Mapping

이 표는 local prototype과 AUTOSAR Classic/Adaptive의 책임 경계를 비교합니다. 호환성 범위는 `Implemented scope`에 적힌 동작까지이며, API·ARXML·timing guarantee·규격 적합성·안전 인증은 포함하지 않습니다.

## Classic Platform concepts

| Local component / flow | Related Classic concept | 구현한 범위 | 의도적으로 뺀 범위 | 근거 |
| --- | --- | --- | --- | --- |
| RTOS periodic task set | AUTOSAR OS | priority, release, resource/blocking, deadline/overrun, stack evidence | OSEK/AUTOSAR API, event/alarm/ScheduleTable, IOC, protection과 conformance 미구현 | Planned |
| application port facade | SWC / RTE | typed read/write/call contract와 generated-like adapter | ARXML, RTE generator, runnable semantics 미구현 | Planned |
| CAN driver boundary | MCAL / CanIf | interrupt input, controller state, bounded frame queue | vendor MCAL API와 hardware abstraction breadth 미구현 | Planned |
| PDU router | PduR | static route table과 upper/lower adapter 분리 | configuration generator와 모든 routing path 미구현 | Planned |
| signal store | COM | endian-safe packing, update bit/freshness, cyclic/on-change policy | 전체 COM signal/group/filter model 미구현 | Planned |
| ISO-TP transport | CanTp | single/multi-frame reassembly, sequence, timeout | 전체 channel/concurrency/timing parameter set 미구현 | Planned |
| diagnostic dispatcher | DCM | read-focused UDS session/service/NRC dispatch | production session/security/access control과 전체 service 미구현 | Planned |
| fault/DTC store | DEM | event status, DTC snapshot, persistence | standardized event memory, aging/debounce 전체 미구현 | Planned |
| journaled storage | NvM | versioned records, CRC, restore/default path | block model, MemIf/Fee/Ea와 endurance algorithm 미구현 | Planned |
| watchdog supervisor | WdgM | alive/deadline observation과 safe/degraded trigger | supervision entity/checkpoint model과 safety validation 미구현 | Planned |
| startup/mode state machine | EcuM / BswM | deterministic startup, run, diagnostic, update, shutdown modes | generated rules, wakeup validation, 전체 BSW orchestration 미구현 | Planned |
| communication state manager | ComM / CanSM / CanNm | requested communication mode, controller state, bus-off recovery policy | full channel/user mapping, network-management timing과 generated configuration 미구현 | Planned |
| data protection adapter | E2E Library concept | sequence, data ID, CRC와 receiver state 실험 | profile-specific conformance와 safety integration 미구현 | Planned |
| authenticated PDU adapter | SecOC / CSM / CryptoIf concept | freshness, MAC verification, key-adapter boundary 실험 | production key management, HSM integration과 conformance 미구현 | Planned |
| boot/update prototype | OEM/vendor flash-bootloader integration concept | image metadata, integrity, known-good fallback | standardized Classic BSW module로 취급하지 않음; OEM protocol, HSM root, production secure boot chain 미구현 | Planned |

## Adaptive Platform concepts

| Local component | Related Adaptive concept | 구현한 범위 | 의도적으로 뺀 범위 | 근거 |
| --- | --- | --- | --- | --- |
| `vehicle-state-service` | Communication Management / `ara::com` | service, method, event, discovery, reconnection | vsomeip API 사용, `ara::com` API·generator 미구현 | Planned |
| `execution-manager` | Execution Management | process spawn/stop, dependency order, restart policy | 자체 manifest와 POSIX process 사용, `ara::exec` 미구현 | Planned |
| manifest mapper | Execution/Service Interface/Service Instance/Machine Manifest concepts | selected fields, validation, deployment relation | 공식 ARXML schema와 generator/toolchain 미구현 | Planned |
| `state-manager` | State Management | Startup/Driving/Diagnostic/Update/Shutdown 결정 | Function Group 모델을 단순 enum/config로 표현 | Planned |
| `health-monitor` | Platform Health Management | alive/deadline supervision, recovery trigger | supervision 종류와 recovery policy 일부만 구현 | Planned |
| `persistency-service` | Persistency | version/config/journal 저장과 복구 | `ara::per` API, redundancy 정책 미구현 | Planned |
| `diagnostic-gateway` | Diagnostics | DoIP–UDS–ISO-TP read-only routing, policy | 전체 diagnostic conversation·Classic DEM 연동 미구현 | Planned |
| `update-manager` | Update and Configuration Management | 검증, staging, activation, health check, rollback | 공식 package/manifest 모델 대신 자체 최소 형식 | Planned |
| `crypto-adapter` | Cryptography | hash/signature verification, key abstraction | `ara::crypto` API·key slot 모델 미구현 | Planned |
| `audit-service` | Log and Trace / IAM-related auditing | 구조화 이벤트와 상태 변경 추적 | `ara::log`가 아닌 자체 logger 또는 DLT 도구 | Planned |
| `policy-engine` | Identity and Access Management | caller/service/action allow-list | 공식 identity/credential model 미구현 | Planned |

## Cross-platform path

| End-to-end path | Classic-side responsibility | Adaptive/Linux-side responsibility | Contract to prove |
| --- | --- | --- | --- |
| Vehicle state | task → RTE-like port → COM/PduR/CanIf | CAN adapter → domain model → SOME/IP event | timing, freshness, version, loss |
| Diagnostics | DCM → CanTp → CAN | DoIP → policy → ISO-TP route | timeout, NRC, authorization, audit |
| Fault | WdgM/DEM/NvM | health/state/persistency | detection, containment, degraded state, recovery |
| Update | bootloader and known-good image | package verification, UCM-like activation | compatibility, power-loss safety, rollback |

## 매핑 갱신 규칙

각 프로젝트 PR에서 다음을 확인합니다.

1. 관련 Classic module 또는 Adaptive Functional Cluster의 책임을 공식 문서에서 다시 확인했는가?
2. 구현한 범위와 의도적으로 생략한 범위가 분리되어 있는가?
3. 비슷한 이름만 차용하고 동작이 다른 부분을 명시했는가?
4. 코드와 자동 테스트 링크가 `Evidence`에 연결되어 있는가?
5. “AUTOSAR compliant”, “production-ready”, “complete platform”처럼 검증하지 못한 표현을 쓰지 않았는가?
