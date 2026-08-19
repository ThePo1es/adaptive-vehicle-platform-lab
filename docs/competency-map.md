# Vehicle Platform Competency Map

## 깊이 배분

| 축 | 목표 깊이 | 설명 |
| --- | --- | --- |
| Primary | Linux/Adaptive platform integration, Level 4 | process·service·deployment·diagnostics·update를 통합 설계 |
| Secondary | MCU/RTOS/Classic concepts, Level 3–4 | 실제 보드와 CAN bench에서 구현·진단 |
| Differentiator | LLVM/ABI/codegen, Level 4–5 | 차량 함수의 source부터 target code까지 분석 |
| Cross-cutting | Safety·cybersecurity·architecture, Level 3–4 | 요구·위험·예산·복구를 각 프로젝트에 적용 |

Primary 축은 baseline과 목표 공고를 보고 바꿀 수 있습니다. Level 5는 한 번에 한 subsystem만 선택합니다.

## 목표 역할

| 우선순위 | Role family | 필요한 포트폴리오 근거 |
| --- | --- | --- |
| 1 | Vehicle platform / middleware SW | C++/Linux, SOME/IP, diagnostics, lifecycle, image, update |
| 2 | MCU / ECU / BSW development | C, Cortex-M, RTOS, CAN, UDS, watchdog, boot |
| 3 | SW integration | configuration, deployment, version, traceability, recovery |
| 성장 방향 | Component/System Architect | budgets, failure containment, safety/security argument, design defense |

분기마다 목표 공고 10–15개를 표본으로 확인합니다. 반복해서 등장하는 기술과 산출물을 현재 Gate backlog에 연결하고, vendor tool은 합법적인 접근이 있을 때 선택 과제로 추가합니다.

## 두 compute domain

| 항목 | MCU ECU | Linux vehicle computer |
| --- | --- | --- |
| CPU | Cortex-M/R 계열 | Cortex-A/x86/vehicle SoC |
| OS | Bare metal / RTOS | Linux; QNX 선택 이식 |
| 언어 | C, 제한된 C++ | Modern C++ |
| 통신 | CAN/CAN FD | Ethernet/SOME-IP/DoIP |
| AUTOSAR 관점 | Classic concept flow | Adaptive concept flow |
| 주요 제약 | interrupt, deadline, RAM/flash | process, service, distribution, deployment |
| 복구 | watchdog, reset, fallback | restart, degraded state, rollback |
| 증거 | RTA, jitter, measured worst, stack | latency distribution, CPU/RSS, recovery |

두 영역은 data, time, state, version, update, recovery 계약으로 연결합니다.

## Gate별 성장

| 구간 | 독립적으로 할 수 있어야 하는 일 |
| --- | --- |
| G0–G3 | 저수준 결함을 언어·ABI·compiler 수준에서 재현하고 설명 |
| G4–G5 | 보드와 RTOS에서 timing·memory·fault를 분석하고 수정 |
| G6–G7 | CAN·진단과 Classic 책임 경계를 세 vertical slice로 구현 |
| G8–G10 | Linux image·process·generated service·diagnostics·identity·state·health를 운영하고 복구 |
| G11A | authenticated update endpoint와 UCM lifecycle을 고장 시험으로 검증 |
| G11B | safety/security 요구와 hardware trust chain을 근거로 검토 |
| G12 | 두 node의 예산·상태·version·고장을 통합 설계 |

## 신뢰할 수 있는 증거

| 주장 | 최소 근거 |
| --- | --- |
| Systems C | malformed corpus, sanitizer, mutation, ABI 설명 |
| Real-time | task model, response-time analysis, timing·stack 원본 자료 |
| CAN/diagnostics | physical trace, timer matrix, tester interoperability |
| Classic concepts | communication·diagnostic·DTC vertical slice와 release mapping |
| Linux platform | image build, lifecycle 고장, core/syscall 분석, bounded recovery |
| SOME/IP/DoIP | generated boundary, packet, version·availability 정책, latency·drop·reconnect 자료 |
| Adaptive concepts | manifest·state·health·diagnostics·IAM artifact와 deliberate-difference mapping |
| Update security | trust assumption, negative corpus, power-cut/rollback 근거 |
| Safety engineering | 교육용 HARA/FMEA와 주장–논리–근거 |
| Architecture | budgets, ADR, fault table, traceability, external review |
| LLVM | source→IR→assembly→runtime 보고서와 upstream feedback |

## Portfolio release

| 시점 | 공개 release | 보여 주는 역량 |
| --- | --- | --- |
| G3 | Compiler Analysis Pack | C/C++·ABI·LLVM 분석 |
| G5 | P00-A | RTOS modeling·RTA·timing 근거 |
| G7 | P00 v1 | MCU/CAN/diagnostics/Classic concept flow |
| G8 | P01 v1 | Linux lifecycle·image·observability |
| G9 | P02 + P05-SIM v1 | Proxy/Skeleton, SOME/IP/DoIP, vCAN–Ethernet vertical slice |
| G10 | Managed Linux Node v1 | manifest·state·health·persistency·Diagnostics·IAM |
| G11A | P04-T2 | update crash consistency·authenticity·activation·rollback |
| G11B | P04 assurance | safety/security review와 hardware trust evidence |
| G12 | P06 v1 | MCU–Linux end-to-end platform |

각 릴리스에는 영어 요약, 재현 명령, 짧은 demo, 원본 자료, 검토 의견을 포함합니다. 완성된 vertical slice부터 차례로 공개합니다.
