# Vehicle Platform Mastery Roadmap

이 로드맵은 “읽은 주제 수”가 아니라 **혼자 설계·구현·디버깅·측정·설명할 수 있는 범위**를 넓히는 과정입니다. Gate별 범위는 합계 92–121주이며, 재시험·통합·외부 리뷰를 포함하면 주 12–15시간 기준 약 24–30개월을 보수적으로 예상합니다. 실제 진도는 각 Gate의 통과 증거로만 결정합니다.

## 운영 원칙

- 한 번에 진행 중인 Gate는 하나만 둡니다.
- 학습 시간의 최소 60%를 코드·실험·디버깅에 사용합니다.
- 공식 문서 요약만으로는 어떤 Gate도 통과할 수 없습니다.
- 정상 동작을 만든 뒤 반드시 malformed input, timeout, resource pressure, restart를 주입합니다.
- 측정은 hardware, OS, compiler, flags, commit, workload, sample count와 함께 기록합니다.
- 모든 “안다”는 말은 code, test, packet, trace, assembly, measurement 중 둘 이상으로 증명합니다.
- AUTOSAR 이름을 붙였다는 이유로 적합 구현이라고 주장하지 않습니다.

## 전체 경로

| Gate | 예상 범위 | 중심 역량 | 승급 프로젝트 |
| --- | ---: | --- | --- |
| G0 | 2–3주 | 재현 환경·Git·테스트·측정 규율 | Baseline dossier |
| G1 | 6–8주 | Systems C | Low-level component library |
| G2 | 6–8주 | Embedded C++ | Ownership-safe runtime |
| G3 | 8–10주 | ARM·ABI·LLVM | Compiler analysis suite |
| G4 | 6–8주 | Bare-metal MCU | Minimal MCU runtime |
| G5 | 8–10주 | RTOS·real-time evidence | Measured ECU simulator |
| G6 | 8–10주 | Classic AUTOSAR concepts | ECU communication/diagnostic stack |
| G7 | 8–10주 | Linux/QNX platform | Process Supervisor |
| G8 | 8–10주 | CAN/Ethernet/diagnostics | Vehicle service and gateway |
| G9 | 10–14주 | Adaptive platform concepts | Managed Linux vehicle node |
| G10 | 8–10주 | Security·resilience·update | Fault-tolerant signed update |
| G11 | 14–20주 | Architecture·integration | Mixed-Criticality Vehicle Platform |
| **Total** | **92–121주** | 반복 평가 제외 | 일정이 아닌 Gate 증거로 종료 |

일부 Gate는 복습 차원에서 겹치지만, 첫 통과는 순서대로 진행합니다. G3의 compiler analysis와 OSS 기여는 이후 모든 Gate에서 20% 트랙으로 계속합니다.

---

## G0 — Engineering Baseline

### 목표

코드가 “내 컴퓨터에서 한 번 실행됨”이 아니라 다른 환경에서 재현되고, 실패 이유와 측정 조건이 남는 작업 방식을 만든다.

### 학습·구현

- Git branch, atomic commit, self-review PR
- CMake/Ninja 또는 선택한 빌드 시스템
- GCC/Clang Debug/Release/Sanitizer profile
- unit/integration/fault test 분리
- warning policy, static analysis, formatter
- raw evidence와 report 분리
- reproducible environment 기록

### 결과물

- [Engineering baseline dossier](docs/baseline.md): 현재 C/C++·ARM·RTOS·Linux·CAN·AUTOSAR·LLVM 수준
- clean clone에서 한 명령으로 실행되는 작은 C/C++ 테스트 프로젝트
- 실패한 테스트 하나를 재현·원인 분석·수정한 기록

### 통과 기준

- [ ] 새 Ubuntu 환경에서 README만 보고 build/test가 통과한다.
- [ ] GCC와 Clang 결과를 모두 남겼다.
- [ ] ASan/UBSan이 실제 결함 하나를 탐지하는 예제를 설명한다.
- [ ] 근거, 관찰, 해석, 미확인 가정을 구분한다.

---

## G1 — Systems C Mastery

### 핵심 범위

- integer promotion, signed/unsigned conversion, overflow
- object representation, effective type, strict aliasing
- alignment, padding, endianness, bit fields의 위험
- pointer arithmetic, lifetime, bounds
- `volatile`, atomics, compiler barrier, memory barrier의 차이
- stack/heap/static storage와 section
- function pointer, callback, state machine
- ring buffer, fixed-size pool, intrusive data structure
- MMIO abstraction과 ISR-safe API 설계
- defensive parser와 error propagation
- MISRA 규칙이 막으려는 실제 failure mode

### 구현 과제

1. endian-safe CAN/DBC signal decoder
2. overwrite/reject 정책을 선택할 수 있는 bounded ring buffer
3. dynamic allocation 없는 fixed-size object pool
4. length-aware ISO-TP/UDS parser core
5. MMIO register access mock과 callback-driven driver shell

### 깨뜨릴 것

- unaligned input
- truncated frame
- shift width 경계
- signed/unsigned comparison
- buffer wrap-around
- producer/consumer overflow
- aliasing과 lifetime violation

### 측정·분석

- `sizeof`, alignment, padding map
- stack usage와 code size
- `-O0/-O2/-Oz` assembly 차이
- UBSan/ASan/static analyzer 탐지 범위와 blind spot

### 통과 기준

- [ ] blank page에서 ring buffer와 parser를 다시 구현한다.
- [ ] undefined, unspecified, implementation-defined behavior를 예제로 구분한다.
- [ ] `volatile`만으로 동기화가 되지 않는 이유를 assembly와 memory model로 설명한다.
- [ ] fuzz/property test가 malformed corpus를 자동 검증한다.
- [ ] public API마다 ownership, bounds, concurrency contract가 있다.

---

## G2 — Embedded C++ Mastery

### 핵심 범위

- object lifetime, value category, copy/move, RAII
- deterministic ownership과 `unique_ptr`/`shared_ptr` 선택
- `span`, `optional`, `variant`, expected-style error
- template instantiation과 code bloat
- virtual dispatch와 type erasure trade-off
- allocator, memory resource, fixed-capacity container
- exception/RTTI on/off 정책
- thread, mutex, condition variable, atomic ordering
- zero-copy와 buffer lifetime
- ABI, name mangling, vtable, structure passing

### 구현 과제

1. fixed-capacity event queue
2. ownership-safe message buffer와 zero-copy view
3. variant 기반 vehicle event/state model
4. RAII process/socket/file descriptor wrapper
5. dependency injection 가능한 clock, transport, process launcher

### 깨뜨릴 것

- dangling `span`/view
- use-after-move
- shared ownership cycle
- destructor order
- exception-disabled error path
- data race와 relaxed ordering 오용

### 통과 기준

- [ ] heap을 허용한 설계와 금지한 설계를 각각 방어한다.
- [ ] 동일 기능의 C/C++ 구현을 code size, lifetime risk, testability로 비교한다.
- [ ] TSan 또는 deterministic concurrency test로 실제 race를 재현·수정한다.
- [ ] public type의 move/copy/ownership contract를 설명한다.

---

## G3 — ARM, Computer Architecture and LLVM

### Cortex-M

- reset sequence, vector table, startup code
- MSP/PSP, exception entry/return, NVIC
- interrupt priority와 tail chaining 개념
- MPU, fault status register, fault handler
- `.text/.rodata/.data/.bss`, linker script
- memory-mapped peripheral, DMA와 memory ordering

### AArch64/Linux SoC

- exception level, virtual memory, page table
- cache/TLB, locality, false sharing
- DMA cache coherency 개념
- SMP, atomic, barrier
- ELF, ABI, calling convention, PLT/GOT
- dynamic linker와 shared library

### LLVM 연결

```text
C/C++ → Clang AST → LLVM IR → Optimization
      → SelectionDAG/GlobalISel → Machine Instruction → Measurement
```

### 분석 corpus

- CRC/checksum
- CAN/DBC signal extraction
- byte swap and lookup table
- ring buffer
- UDS parser
- state machine
- FIR/Kalman kernel 일부

### 비교 행렬

- GCC vs Clang
- `-O0`, `-O2`, `-Oz`
- LTO off/on
- C vs C++
- Cortex-M vs AArch64
- code size, branch/load-store, latency/cycle, memory access, UB sensitivity

### 통과 기준

- [ ] linker map에서 모든 주요 section과 symbol의 위치를 설명한다.
- [ ] HardFault/BusFault 계열 하나를 재현하고 stacked context로 원인을 찾는다.
- [ ] AAPCS 관점에서 인자·구조체·return 전달을 assembly로 설명한다.
- [ ] LLVM IR 최적화 전후와 실제 machine code의 차이를 연결한다.
- [ ] 성능 차이를 추측이 아닌 동일 조건 측정으로 보고한다.

상세 실험 형식은 [compiler-analysis/README.md](compiler-analysis/README.md)를 따릅니다.

---

## G4 — Bare-metal MCU

### 목표

HAL 예제 복사 이전에 부팅, interrupt, timing, memory와 peripheral의 최소 실행 구조를 이해한다.

### 구현 과제

- 직접 작성하거나 최소화한 startup/vector/linker 구성
- monotonic timer와 deadline helper
- GPIO/UART/CAN 중 하나의 interrupt-driven driver
- lock-free라고 주장하지 않는 명확한 SPSC queue
- fault handler와 crash record
- watchdog reset reason 보존
- A/B 또는 dual-image flash layout 설계

### 통과 기준

- [ ] reset부터 `main`까지 제어 흐름과 메모리 초기화를 설명한다.
- [ ] ISR이 해도 되는 일과 task/main loop로 넘길 일을 contract로 정한다.
- [ ] interrupt storm, queue full, peripheral timeout을 주입한다.
- [ ] stack overflow 또는 fault를 GDB와 register dump로 진단한다.
- [ ] boot time, ISR latency 또는 timer error를 측정한다.

---

## G5 — RTOS and Measured ECU

### 핵심 범위

- preemptive/cooperative scheduling
- task states, priority, ready queue
- ISR/task context와 deferred work
- semaphore, mutex, queue, event, timer
- priority inversion/inheritance
- race, deadlock, starvation
- periodic release, deadline, jitter, overrun
- tick/tickless, monotonic time
- watchdog, stack high-water mark, heap fragmentation
- WCET 개념과 측정의 한계
- MPU-based task isolation

### 승급 프로젝트: P00 MCU/RTOS ECU Node

- 1ms/10ms/100ms 주기 task
- sensor/actuator simulation
- CAN TX/RX와 bounded queue
- UDS read session과 DTC
- watchdog와 safe/degraded state
- persistent firmware version

### 필수 수치

```text
Period / deadline
p50, p95, p99, worst execution time
Maximum release jitter
Stack peak per task
Queue high-water mark and drops
Deadline misses / total releases
Watchdog detection and recovery time
```

### 통과 기준

- [ ] 100,000회 이상 release에서 raw timing data를 보존한다.
- [ ] 의도적 overload에서 deadline miss를 재현하고 정책을 설명한다.
- [ ] priority inversion을 재현하고 inheritance 전후를 비교한다.
- [ ] task별 stack budget을 측정 근거와 함께 정한다.
- [ ] watchdog reset 뒤 safe state와 원인 기록을 검증한다.

---

## G6 — Classic AUTOSAR Concepts and ECU Stack

### 구조 이해

```text
SWC → RTE → Services → ECU Abstraction → MCAL → Hardware
```

### 우선 모듈

- AUTOSAR OS, RTE
- COM, PduR, CanIf, CanTp
- DCM, DEM, NvM
- WdgM, EcuM, BswM
- SecOC concept
- Flash Bootloader

### 직접 구현할 최소 흐름

```text
CAN RX → CanIf-like adapter → PduR-like router
       → COM-like signal store → RTE-like port → Application

Diagnostic RX → CanTp-like reassembly → PduR → DCM-like dispatcher
              → Application → response

Application fault → DEM-like event/DTC → NvM-like storage → reboot restore
```

### 통과 기준

- [ ] 일반 통신, 진단, 고장 저장 경로를 packet과 call trace로 설명한다.
- [ ] 각 layer가 가져야 할 책임과 가져가면 안 되는 책임을 구분한다.
- [ ] timeout, NRC, multi-frame, storage corruption을 자동 테스트한다.
- [ ] EcuM/BswM 스타일 startup·mode transition을 상태 머신으로 만든다.
- [ ] 자체 미니 구현과 실제 AUTOSAR 사양의 차이를 매핑한다.

---

## G7 — Linux/QNX Systems Platform

### 핵심 범위

- process lifecycle, signal, process group
- thread scheduling, affinity, real-time policy
- `epoll`, Unix socket, shared memory, `mmap`
- TCP/UDP/multicast와 backpressure
- zero-copy의 실제 ownership 조건
- systemd service, watchdog, resource limit
- core dump, `gdb`, `strace`, `perf`, heap analysis
- cross compilation, Device Tree와 driver model 기초
- boot time, logging, tracing, observability

### 승급 프로젝트: P01 Process Supervisor

- manifest parsing
- dependency DAG
- start/stop and graceful shutdown
- heartbeat/deadline
- bounded restart/backoff
- resource policy and audit log

### 통과 기준

- [ ] child crash, hang, fork/spawn failure, shutdown race를 자동 재현한다.
- [ ] graceful stop → timeout → kill을 process group까지 검증한다.
- [ ] CPU affinity/scheduling 설정의 효과와 위험을 측정한다.
- [ ] core dump와 trace만으로 crash root cause를 설명한다.
- [ ] clean machine에서 전체 supervisor test를 재현한다.

---

## G8 — Vehicle Networks and Diagnostics

### CAN side

- arbitration, error frame, error active/passive, bus-off
- CAN FD, SocketCAN, DBC encoding
- ISO-TP, UDS session/service/NRC
- Network Management 개념
- gateway routing and rate policy

### Ethernet side

- VLAN, multicast, TCP/UDP selection
- SOME/IP, SOME/IP-SD
- DoIP
- service availability and versioning
- serialization and compatibility
- E2E protection vs cryptographic integrity
- time synchronization and TSN concepts

### 승급 프로젝트

- P02 Vehicle State Service
- CAN–SOME/IP signal gateway
- DoIP–UDS–ISO-TP diagnostic gateway

### 설계 질문

- CAN 10ms signal을 Ethernet 100ms event로 어떻게 aggregate할 것인가?
- on-change와 cyclic publish를 어떻게 선택할 것인가?
- stale data와 unavailable service를 어떻게 구분할 것인가?
- bus-off가 Linux service state와 diagnostic response에 어떻게 전파되는가?
- version mismatch와 partial deployment를 어떻게 처리하는가?

### 통과 기준

- [ ] bus-off와 service restart를 end-to-end state로 전파한다.
- [ ] SOME/IP-SD, SOME/IP, DoIP, ISO-TP 캡처를 layer별로 설명한다.
- [ ] loss, duplication, reordering, flood, malformed input을 자동 주입한다.
- [ ] latency뿐 아니라 drops, queue, CPU/RSS, recovery time을 보고한다.

---

## G9 — Adaptive Platform Concepts

### Functional Clusters

- Communication Management
- Execution Management
- State Management
- Platform Health Management
- Persistency
- Log and Trace
- Diagnostics
- Update and Configuration Management
- Cryptography
- Identity and Access Management

### 구현 순서

```text
Service Interface → Proxy/Skeleton pattern → SOME/IP
→ Manifest → Process Lifecycle → Function Group State
→ Health Supervision → Persistency/Logging
→ Diagnostics → UCM/Update
```

### 승급 프로젝트

- P03 Manifest-driven Execution Manager
- P04 Secure Update Manager
- P05 Secure Adaptive Gateway

### 통과 기준

- [ ] EM, SM, PHM의 decision/action/observation 책임이 코드에서 분리된다.
- [ ] dependency, state, health, persistency가 reboot/failure에서도 일관된다.
- [ ] `ara::*`와 유사한 이름보다 observable behavior를 먼저 검증한다.
- [ ] 구현/미구현/단순화 범위를 mapping table에 유지한다.
- [ ] service discovery부터 update rollback까지 통합 시나리오가 재현된다.

---

## G10 — Security, Update and Resilience

보안은 별도 exploit 모음이 아니라 모든 계층에 적용되는 품질 속성입니다.

### 구현 범위

- firmware/package signature verification
- hash, canonical manifest, strict parser
- anti-rollback and replay policy
- A/B slot, activation, health check, rollback
- MCU bootloader version/fallback policy
- diagnostic access policy
- process privilege separation
- key abstraction and optional OP-TEE secure storage
- audit log and tamper-evident evidence concept
- malformed packet and resource exhaustion handling

### fault campaign

- package/manifest/payload byte tamper
- power loss at every update state
- disk/flash full and short write
- wrong key, old version, replay
- process crash during activation
- MCU watchdog reset during transfer
- unauthorized diagnostic service
- log storm, CAN flood, malformed SOME/IP/UDS

### 통과 기준

- [ ] 모든 security invariant에 negative test가 있다.
- [ ] 어떤 실패 지점에서도 last-known-good boot path가 보존된다.
- [ ] trust boundary, attacker capability, residual risk를 명시한다.
- [ ] OP-TEE 없이 기본 플랫폼을 완성한 뒤 보호 가치가 있는 key/version만 이동한다.

---

## G11 — Architecture and Mixed-Criticality Capstone

### 아키텍처 순서

```text
Stakeholder Requirement → System Requirement → Architecture Driver
→ Component Responsibility → Interface Contract
→ Runtime/Deployment → Failure Handling → Verification
```

### 필수 산출물

- System context, component, deployment diagrams
- SRS/SADS/SUDS 수준의 요구사항·설계·단위 설계
- interface and version specification
- task/process/thread model
- timing, CPU, memory, network budget
- startup/shutdown/update sequence
- failure mode and degraded/safe state table
- threat model
- requirement → architecture → code → test → result traceability
- reproducible CI and release procedure

### 최종 프로젝트: P06 Mixed-Criticality Vehicle Platform

- RTOS MCU ECU와 Linux vehicle computer
- CAN/CAN FD signal path
- SOME/IP vehicle service
- DoIP–UDS gateway
- lifecycle and health management
- DTC/persistency/logging
- signed Linux update와 MCU firmware update policy
- watchdog, bus-off, service crash, network loss, update rollback
- compiler analysis report for critical functions

### 최종 데모

1. 두 노드가 정의된 startup order로 부팅한다.
2. MCU 주기 task의 vehicle data가 SOME/IP event로 전달된다.
3. DoIP read request가 UDS/ISO-TP를 거쳐 응답한다.
4. bus-off, task overrun, service crash가 상위 state로 전파된다.
5. 변조 업데이트가 거부된다.
6. 정상 업데이트 후 health failure를 주입해 rollback한다.
7. traceability와 budget report에서 모든 동작을 추적한다.

### 통과 기준

- [ ] 처음 보는 사람이 문서만으로 clean build와 demo를 재현한다.
- [ ] 최소 한 명의 외부 리뷰어 질문에 architecture trade-off를 방어한다.
- [ ] timing/memory/CPU/network budget의 합계와 margin이 측정치와 연결된다.
- [ ] 10개 이상의 fault scenario가 자동 실행되고 기대 state를 검증한다.
- [ ] 영어 README와 5–10분 기술 데모가 문제·설계·증거·한계를 보여준다.
- [ ] 프로젝트를 다시 처음부터 설계한다면 바꿀 결정을 ADR로 정리한다.

---

## 지속 트랙

### LLVM/OSS — 20%

- 매 Gate의 critical function을 compiler-analysis corpus에 추가
- upstream issue reproduction과 test-first patch
- ARM/AArch64 codegen 또는 optimizer 관련 작은 기여
- 기여를 차량용 코드의 performance/reliability 분석과 연결

### Security research — 10%

- 메인 프로젝트 기능을 밀어내지 않는 범위
- secure boot/update, parser robustness, isolation, fault injection 중심
- 신규 취약점 탐색은 별도 허가 범위와 disclosure 절차로 분리

### Vehicle platform implementation — 70%

- 요구사항부터 배포·복구까지 하나의 시스템 완성
- 기능 수보다 failure handling, measurement, traceability 우선

## G11 이후 — Level 5 Expert Cycle

G11을 통과해도 모든 분야를 “완벽하게 안다”고 주장하지 않습니다. core mastery 뒤 선택한 subsystem 하나를 깊게 파고드는 첫 expert cycle에 12–18개월을 예상하며, 이후 다른 subsystem으로 반복합니다.

| Cycle | 예상 범위 | Mission | 통과 증거 |
| --- | ---: | --- | --- |
| E1 Maintainer | 12–16주 | 실제 upstream subsystem을 지속적으로 읽고 고친다 | issue triage, regression test, review 반영, release 변화 추적 |
| E2 Portability | 12–16주 | 새 MCU/SoC/RTOS/Linux 환경으로 contract를 이식한다 | 동일 contract suite, target delta, timing/memory 재예산 |
| E3 Performance/Reliability Research | 12–20주 | 측정으로 실제 병목·failure를 발견하고 개선한다 | reproducible artifact, before/after raw data, patch 또는 기술 보고서 |
| E4 Architecture/Teaching | 12–16주 | 타인 설계를 리뷰하고 요구 변경을 주도한다 | review 기록, 공개 설명, external design defense, revised ADR |

### E1 — Subsystem maintainer

- LLVM backend/optimizer, Zephyr/FreeRTOS kernel·driver, Linux CAN/networking, vsomeip, diagnostic/update component 중 하나를 선택합니다.
- 최소 3개월 동안 release note, issue, test와 relevant source를 추적합니다.
- 처음 보는 defect 5개 이상을 재현·분류하고, 최소 2개는 regression test 또는 patch로 제안합니다.
- merge 여부와 무관하게 maintainer feedback을 기록하고 설계 가정을 수정합니다.

### E2 — Cross-target portability

- 기존과 다른 MCU family 또는 RTOS 하나, 다른 AArch64/x86 Linux 환경 하나로 이식합니다.
- source fork로 조건문을 늘리기 전에 clock, transport, storage, scheduler contract를 분리합니다.
- simulator/board와 두 Linux target에서 동일 conformance/fault suite를 재사용합니다.
- ABI, endian, alignment, cache, scheduling, boot와 toolchain 차이를 porting report에 남깁니다.

### E3 — Measured research

- 실제 vehicle function에서 latency/jitter/code-size/memory/recovery 질문 하나를 고릅니다.
- 반증 가능한 hypothesis, controlled workload, raw data와 validity threat를 먼저 정의합니다.
- source → LLVM IR → machine code → runtime/fault evidence를 연결합니다.
- 개선이 다른 workload·target에서 만드는 regression과 trade-off까지 보고합니다.

### E4 — Architecture and teaching

- 다른 사람의 code/design review를 최소 5회 수행하고 actionable defect와 contract gap을 찾습니다.
- 자신이 만든 플랫폼에 외부 requirement change와 hidden fault를 받아 즉석 impact analysis를 수행합니다.
- 30–60분 기술 세션 또는 장문 문서로 subsystem을 가르치고 질문·오류 정정을 기록합니다.
- 6개월 이상 유지된 architecture decision을 실제 운영 evidence로 재평가합니다.

### 첫 expert cycle 통과 기준

- [ ] 선택 subsystem에서 처음 보는 문제를 독립적으로 진단·설계·리뷰하는 Level 5 증거가 있다.
- [ ] 두 target 이상에서 동일 contract와 fault suite가 재현된다.
- [ ] upstream maintainer 또는 외부 expert의 비동의·수정 feedback을 반영했다.
- [ ] 성능 또는 신뢰성 개선이 raw evidence와 regression analysis로 증명된다.
- [ ] 다른 사람에게 가르치고, 그 사람이 독립적으로 재현한 결과가 있다.
- [ ] 무엇을 아직 모르는지와 다음 12개월 연구 질문이 명확하다.

마스터리는 주제를 한 번 끝내는 것이 아니라, 낯선 시스템에서도 같은 문제 해결 방식을 재현하고 다른 사람의 품질까지 높이는 능력으로 판단합니다.
