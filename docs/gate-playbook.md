# Gate Playbook

이 문서는 ROADMAP의 각 Gate를 2주 Sprint로 풀어 쓴 실행안입니다. 한 Sprint는 주 12–15시간을 기준으로 합니다. 시작 전에 예상 시간을 다시 적고, 끝난 뒤 실제 시간을 기록합니다.

## Sprint 공통 형식

각 Sprint 이슈에는 다음 여덟 항목을 넣습니다.

| 항목 | 작성 내용 |
| --- | --- |
| 선수 진단 | 도움 없이 풀어 볼 질문 또는 작은 코드 |
| 기준 자료 | 문서명, release/edition/commit, 읽을 절, 접근 상태 |
| 풀이 예제 | 따라 하며 관찰할 공식 예제 또는 작은 모델 |
| 안내 실습 | 일부 뼈대와 test가 주어진 과제 |
| 독립 실습 | 힌트 없이 완성할 과제 |
| 전이 과제 | 다른 자료형·target·fault로 바꾼 과제 |
| 판정 기준 | expected output, invariant, reference test, second implementation |
| 근거 | commit, test, 원본 자료, 회고, 실제 소요 시간 |

기준 자료는 [references.md](references.md)의 manifest 형식을 사용합니다. 유료 규격에 합법적으로 접근할 수 없으면 `Unverified`로 표시하고 공개 구현·공식 설명 자료로 확인한 범위만 기록합니다.

## 일정이 밀렸을 때 줄이는 순서

일정이 늦어지면 아래 순서로 범위를 줄입니다.

1. UI, dashboard, 시각 효과
2. 두 번째 library·RTOS·board 비교
3. optional protocol과 고급 최적화
4. stretch 성능 목표

필수 불변 조건, negative test, 재현 명령, 측정 자료, Gate 전이 과제는 유지합니다.

## Gate마다 쌓는 안전·보안 기록

각 Sprint의 1–2시간을 아래 작업에 씁니다. 이 시간은 Sprint의 24–30시간 안에 포함됩니다. 결과는 [foundation outcomes](embedded-foundations.md)에 연결합니다.

| Gate | 짧은 작업 | Outcome |
| --- | --- | --- |
| G1 | parser misuse case와 입력 경계 정리 | `OUT-XCUT-G1` |
| G2 | 소유권 침해·race가 만드는 failure path 정리 | `OUT-XCUT-G2` |
| G3 | compiler·ABI 가정과 깨지는 조건 기록 | `OUT-XCUT-G3` |
| G4 | debug port, boot image, key 보관 경계 표시 | `OUT-XCUT-G4` |
| G5 | deadline miss와 fallback 선택 근거 작성 | `OUT-XCUT-G5` |
| G6 | 진단 권한과 flood misuse case 시험 | `OUT-XCUT-G6` |
| G7 | E2E·SecOC 적용 지점과 빠진 보장 기록 | `OUT-XCUT-G7` |
| G8 | privilege와 CPU·memory·storage 제한 시험 | `OUT-XCUT-G8` |
| G9 | service discovery·diagnostic gateway 위협 시나리오 작성 | `OUT-XCUT-G9` |
| G10 | identity·policy·audit 책임을 공식 개념과 매핑 | `OUT-XCUT-G10` |

---

## G0 — Engineering Baseline

| Sprint | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- |
| 0.1 환경과 진단 | CMake/CTest skeleton, GCC·Clang profile, sanitizer defect | 새 디렉터리에서 60분 build/test practical | CI command, 경고 없는 build log, baseline score |
| 0.2 운영 고정 | 개발 환경, 근거 보관 구조, hardware/access ADR | 새 VM에서 README만으로 재현 | 제3자 또는 새 VM 재현, license decision issue |

MVP는 C/C++ skeleton, CI, baseline dossier입니다. Board 구매와 상용 문서 접근은 ADR에 `Available / Planned / Blocked`로 기록합니다.

## G1 — Systems C

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 1.1 정수와 직렬화 | conversion, overflow, endianness | 8-byte signal decoder | 다른 bit layout과 signed signal | golden vectors, UBSan |
| 1.2 객체와 메모리 | representation, alignment, aliasing, bounds | padding/alignment lab | unaligned packet view 수정 | compiler matrix, sanitizer |
| 1.3 bounded storage | ring, pool, overflow policy | ring buffer skeleton | packet pool 또는 DMA descriptor queue | invariant/property tests |
| 1.4 parser 강건성 | state, length, error propagation | framed parser | truncated/reordered corpus | fuzz coverage, mutation score |
| 1.5 MMIO·동시성 전이 | volatile, atomic, barrier, ISR contract | mock register driver | 처음 보는 peripheral shell | assembly review, 비공개 고장 과제 |

MVP는 decoder, bounded storage, parser와 자동 corpus입니다. ISO-TP/UDS 의미론은 G6에서 배웁니다.

## G2 — Embedded C++

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 2.1 수명과 소유권 | RAII, move, view | buffer owner/view pair | dangling-view bug repair | ASan, lifetime tests |
| 2.2 제한된 runtime | fixed capacity, allocator, errors | event queue | heap-free message pipeline | allocation counter, size report |
| 2.3 동시성 | mutex, condition, atomic | producer/consumer | unfamiliar race diagnosis | TSan 또는 deterministic scheduler |
| 2.4 ABI와 설계 | virtual/type erasure/template | C/C++ facade 비교 | exception·RTTI policy defense | map file, review, transfer exam |

MVP는 P01과 P02에 필요한 runtime layer까지만 만듭니다.

## G3 — ARM ABI and LLVM

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 3.1 AAPCS32 | register, stack, structure passing | Cortex-M cross compile | unknown function ABI decode | ABI spec, assembly assertions |
| 3.2 AAPCS64·ELF | relocation, PLT/GOT, shared object | AArch64 binary walk | stripped crash symbol path | readelf/objdump/gdb logs |
| 3.3 LLVM IR | UB, optimization, data layout | parser IR diff | new vehicle function analysis | executable equivalence tests |
| 3.4 target code | instruction selection, size, LTO | GCC/Clang same-target matrix | optimization regression | pinned flags, raw size/runtime |
| 3.5 upstream 전이 | minimization, test-first report | known issue reproduction | new issue or review response | minimized reproducer, peer review |

성능 수치는 target별 budget 안에서 비교합니다. Cortex-M은 cycle, AArch64는 해당 환경의 latency와 counter를 사용합니다.

## G4 — Bare-metal Cortex-M

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 4.1 부팅 | reset, vector, linker, init | vendor example 축소 | 빈 image bring-up | map, UART marker, debugger trace |
| 4.2 clock·timer | clock tree, timer, monotonic clock | periodic interrupt | clock misconfiguration diagnosis | scope/logic analyzer |
| 4.3 interrupt·queue | NVIC, nesting, deferred work | UART/GPIO ISR | interrupt storm handling | event trace, overflow counter |
| 4.4 고장 기록 | exception frame, fault registers | deliberate fault set | 비공개 고장 진단 | GDB + persisted crash record |
| 4.5 peripheral·DMA | driver state, timeout, DMA/cache where present | one interrupt driver | different peripheral transfer | reference-manual checklist |
| 4.6 watchdog·flash | reset reason, image layout | watchdog recovery | reset-at-state matrix | board log, layout ADR |

MVP는 실제 보드에서 부팅·timer·interrupt·fault·watchdog가 작동하는 image입니다.

## G5 — RTOS and Real-Time Analysis

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 5.1 task model | period, deadline, WCET estimate, jitter | synthetic task set | 요구 변경에 따른 모델 수정 | task model review |
| 5.2 RTA | response time, blocking, interference | fixed-priority worksheet | unseen task set analysis | independent calculator/test vectors |
| 5.3 동기화 | inversion, inheritance, ceiling | inversion reproduction | 비공개 blocking 고장 | trace + analytical bound |
| 5.4 RTOS 구현 | task/ISR/queue/timer | P00-A skeleton | overload policy | deterministic tests |
| 5.5 계측 | cycle counter, trace overhead, stack | timing recorder | alternate clock source | calibration report |
| 5.6 stress·soak | interrupt load, phase, long run | workload matrix | random seed replay | miss/stack/queue raw data |
| 5.7 종합시험 | P00-A 릴리스 | 처음 보는 task-set 변경 | 비공개 고장 + 설계 질의 | 외부 검토, release tag |

Deadline과 인수 예산은 Sprint 5.1에서 고정합니다. 실측이 실패하면 구현·모델·요구 중 무엇을 바꿀지 ADR로 결정합니다.

## G6 — CAN, ISO-TP and UDS

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 6.1 CAN link | arbitration, bit timing, frame | SocketCAN trace | unknown trace decode | can-utils + analyzer |
| 6.2 physical bench | termination, transceiver, error state | two-node CAN | bit-rate mismatch/bus-off | scope + controller counters |
| 6.3 CAN timing | load, priority, response time | message set analysis | changed message set | analytical and measured result |
| 6.4 ISO-TP I | addressing, SF/FF/CF/FC | reassembly state machine | sequence and truncation faults | Linux ISO-TP differential test |
| 6.5 ISO-TP II | BS, STmin, timers, concurrency | sender/receiver pair | timeout matrix | virtual time tests |
| 6.6 UDS I | session, P2/P2*, S3, NRC | ReadDataByIdentifier | unfamiliar read service | tester interoperability |
| 6.7 UDS II | DTC read, access policy | read-only endpoint | malformed/flood corpus | state invariants, audit |
| 6.8 P00-B 릴리스 | end-to-end CAN/UDS | physical replay | 비공개 network 고장 | packet 자료, 검토자 |

진단 쓰기와 다운로드는 선택 과제로 둡니다. 허가된 벤치와 위협 모델을 준비한 뒤 진행합니다.

## G7 — Classic Platform Concept Fluency

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 7.1 OS/RTE | runnable, event, resource, port | static runnable table | mode-dependent runnable | schedule/call trace |
| 7.2 COM path | CanIf, PduR, COM, RTE | RX vertical slice | TX/on-change path | packet-to-application trace |
| 7.3 진단 path | CanTp, DCM | UDS routing | timeout/NRC fault | protocol oracle |
| 7.4 fault storage | DEM, NvM | DTC journal | corruption/reboot | golden state model |
| 7.5 mode·network | EcuM, BswM, WdgM, ComM/CanSM | startup/mode machine | bus-off startup interaction | model-based tests |
| 7.6 P00-C defense | configuration generation, mapping | three vertical slices | unfamiliar responsibility fault | external review, v1 release |

공식 AUTOSAR release를 고정하고 읽은 절을 기록합니다. ARXML·generator 경험은 접근 가능한 교육 stack이 있을 때 별도 evidence로 추가합니다.

책임 경계 매핑을 `Validated`로 판정하는 검토자는 Classic Platform 경험이 있거나, 선택한 release의 관련 공식 문서를 직접 읽고 인용 절을 확인해야 합니다. 동작 시험만 통과하고 이 검토를 받지 못하면 구현 결과는 `Validated`, AUTOSAR 매핑은 `Provisional`로 따로 기록합니다.

## G8 — Linux Platform and BSP

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 8.1 process lifecycle | spawn, signal, group, wait | P01 child runner | forked-child cleanup | integration tests |
| 8.2 supervisor | restart, backoff, virtual clock | state machine | hanging child fault | deterministic oracle |
| 8.3 IPC·resource | epoll, socket, shared memory | bounded IPC | backpressure fault | load test |
| 8.4 진단 | core, gdb, strace, perf | seeded crash/hang | unknown incident | root-cause rubric |
| 8.5 service hardening | systemd, cgroup, capability, seccomp | packaged service | privilege/resource fault | policy tests |
| 8.6 BSP·image | boot chain, kernel config, DT | Buildroot image | 새 target 배포 | image hash, SBOM, boot log |
| 8.7 P01 릴리스 | target deployment | crash campaign | 새 환경 전이 | 외부 검토, 릴리스 |

Core는 Buildroot image, kernel config, Device Tree, SBOM까지입니다. Kernel module과 Yocto 비교는 B1 심화로 넘깁니다.

## G9 — Ethernet Vehicle Services

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 9.1 Ethernet | VLAN, multicast, TCP/UDP | packet lab | routing/interface fault | tcpdump/Wireshark |
| 9.2 SOME/IP | header, method, event | request/response | malformed message | protocol parser tests |
| 9.3 SD | offer/find, TTL, subscription | discovery pair | delayed start/restart | packet/state oracle |
| 9.4 P02 service | versioned interface | state service | incompatible version | integration test |
| 9.5 성능·복구 | backpressure, load, reconnect | 10/100Hz matrix | loss/reorder workload | raw latency/drop data |
| 9.6 DoIP | routing activation, alive check | read path | timeout/malformed route | tester/packet 자료 |
| 9.7 time contract | clock domain, PTP basics | offset/drift lab | no-sync latency bound | uncertainty report |
| 9.8 P05 vertical slice | CAN signal→SOME/IP event | two-node slice | restart/bus fault | release + external replay |

TSN scheduling과 hardware timestamp는 N1 선택 Gate로 넘깁니다.

## G10 — Adaptive Platform Concept Fluency

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 10.1 release map | architecture와 manifest 종류 | official-doc map | unfamiliar manifest review | section citations |
| 10.2 manifest | schema, immutable model | app manifest | invalid corpus | schema tests |
| 10.3 dependency | DAG, start/stop plan | P03 planner | cycle/failure propagation | graph oracle |
| 10.4 state | platform/function state | decision component | illegal transition | model-based tests |
| 10.5 health | alive/deadline/logical supervision | monitor | missed heartbeat | virtual time tests |
| 10.6 persistency·log | crash consistency, audit | state store | corrupted record | reboot tests |
| 10.7 managed node | P01/P02/P03 integration | deployment | partial service failure | scenario suite |
| 10.8 설계 질의 | mapping and design review | release candidate | 비공개 경계 고장 | 검토자 + 릴리스 |

Adaptive 책임 매핑을 `Validated`로 판정하는 검토자는 Adaptive Platform 경험이 있거나, 선택한 release의 관련 공식 문서를 직접 검토해야 합니다. 그렇지 않으면 local 동작은 `Validated`, AUTOSAR 매핑은 `Provisional`로 기록합니다.

## G11 — Safety, Cybersecurity and Update

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 11.1 safety framing | item, hazard, goal, ASIL 개념 | synthetic HARA | 변경된 운행 상황 | 검토 checklist |
| 11.2 failure analysis | FMEA/FTA, mechanisms | one data path | common-cause fault | 주장–근거 검토 |
| 11.3 cybersecurity | asset, TARA, trust boundary | update threat model | new attacker capability | independent review |
| 11.4 transaction safety | journal, fsync, atomic metadata | crash-consistent updater | every-state kill | reference state model |
| 11.5 authenticity | canonical form, signature, key | secure tier | parser/path/key corpus | cryptographic vectors |
| 11.6 boot·rollback | trust root, monotonic state, recovery | T1 power-cut와 T2 가정 확인 | T3 hardware가 있으면 실제 rollback 시험 | tier별 board/storage 자료 |
| 11.7 assurance 질의 | P04 + case | 근거 검토 | 비공개 주장 검토 | 검토자 두 명, 릴리스 |

## G12 — Architecture and Integration

| Sprint | 주제 | 안내 실습 | 독립·전이 과제 | 판정 기준 / 종료 근거 |
| --- | --- | --- | --- | --- |
| 12.1 범위 | stakeholder need, use case, 주장 경계 | system context | 범위 변경 과제 | 검토자 확인 |
| 12.2 requirements | stimulus, condition, response, tolerance | requirement set | ambiguous requirement repair | lint + review |
| 12.3 interfaces | data, state, time, version | contract pack | partial deployment | contract tests |
| 12.4 budgets | RTA, CPU, memory, network | budget tree | changed workload | reconciliation script |
| 12.5 walking skeleton | P00↔P05↔P03 | startup path | 새 환경 배포 | smoke suite |
| 12.6 vehicle data | CAN→SOME/IP | event path | loss/stale fault | packet + state 자료 |
| 12.7 diagnostics | DoIP→UDS read | route path | timeout/version fault | tester 자료 |
| 12.8 lifecycle | startup, shutdown, degraded | state propagation | simultaneous reset/crash | sequence oracle |
| 12.9 update | Linux/MCU compatibility | activation policy | unhealthy new version | rollback matrix |
| 12.10 고장 campaign | 10개 이상 | automated runner | 검토자가 고른 고장 | 결과 묶음 |
| 12.11 새 환경 재현 | 새 host/board | release candidate | 제3자 실행 | 검토 기록 |
| 12.12 defense·release | requirement change, ADR, budget | public demo | live design defense | versioned release |

G12의 작업 범위는 기존 구성요소의 계약, 통합, 복구, 측정과 설명입니다.

## 분기 누적 시험

분기 누적 시험은 해당 분기의 복습 예산에서 6–10시간을 모아 진행합니다.

- 현재 Gate의 필수 선수 기술 2개
- 간격 반복 대기열에서 오래된 기술 1개
- 이전 Gate 전체에서 무작위 기술 1개
- 처음 보는 작은 구현 또는 fault 하나
- 지난 릴리스의 새 환경 build
- 오래된 ADR 하나 재검토
- 실패한 기술만 1주 보강 일정에 추가

시험 결과에는 표본을 뽑은 방식과 seed를 남깁니다. 같은 항목만 반복해서 고르는 일을 막기 위해 직전 두 분기에 나온 무작위 항목은 제외합니다.
