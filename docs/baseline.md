# Engineering Baseline Dossier

G0 시작과 종료에 같은 조건으로 능력을 측정합니다. 첫 답변은 검색·노트·AI 없이 작성하고, 모르는 내용은 `Unknown`으로 기록합니다. 학습 뒤 보완한 답은 별도 칸에 남깁니다.

## Prior evidence and challenge-out

| Gate / skill | Public artifact | My contribution | Last reproduced | Reviewer | Decision |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | Challenge / Gap Sprint / Full Gate |

Challenge-out evidence는 공개 가능한 작은 reproducer, 본인 기여 설명, reviewer 확인으로 구성합니다. 회사 비공개 자료는 제외합니다. 판정 절차는 [ASSESSMENTS.md](../ASSESSMENTS.md#challenge-out)를 따릅니다.

## Session metadata

| Item | Start baseline | G0 retest |
| --- | --- | --- |
| Date |  |  |
| Commit |  |  |
| Host / OS |  |  |
| GCC / Clang |  |  |
| Target / board |  |  |
| Time used |  |  |
| Assistance | None | None |

## Scoring

| Score | Observable ability |
| ---: | --- |
| 0 | 용어를 모르거나 잘못 설명함 |
| 1 | 용어를 인식하지만 example/constraint를 설명하지 못함 |
| 2 | 작은 예제에 적용하나 오류 경로에서 막힘 |
| 3 | 독립 구현·진단하고 test로 확인함 |
| 4 | 요구사항에서 설계하고 대안·trade-off를 방어함 |
| 5 | 낯선 문제로 전이하고 다른 구현을 리뷰·교육함 |

점수보다 답변, code, test와 debugging log를 증거로 남깁니다.

## Closed-book diagnostic

각 질문은 `Answer`, `Confidence`, `Evidence after test`, `Gap`을 기록합니다.

### Systems C/C++

1. object lifetime, effective type, strict aliasing과 alignment가 byte parser에 미치는 영향을 설명합니다.
2. integer promotion과 signed/unsigned conversion이 bit extraction을 망가뜨리는 예를 만듭니다.
3. `volatile`, C/C++ atomic, compiler barrier와 hardware memory barrier를 구분합니다.
4. ring buffer의 full/empty invariant와 overflow policy를 설명합니다.
5. RAII, `span`, smart pointer와 zero-copy view의 lifetime contract를 비교합니다.
6. data race가 undefined behavior인 이유와 mutex/atomic 선택 기준을 설명합니다.

### ARM, compiler and binary

1. reset에서 `main`까지 `.data/.bss`, vector table, stack과 linker의 역할을 설명합니다.
2. Cortex-M exception entry/return과 fault context에서 확인할 register를 설명합니다.
3. AAPCS 관점에서 scalar, pointer, small/large structure가 함수 경계를 지나는 방식을 설명합니다.
4. cache, TLB, DMA coherency와 memory ordering의 관계를 설명합니다.
5. C/C++ → AST → LLVM IR → machine code의 변환에서 optimization이 일어나는 위치를 설명합니다.
6. `-O0`, `-O2`, `-Oz`, LTO 비교를 공정하게 측정할 experiment를 설계합니다.

### RTOS and embedded runtime

1. ISR과 task의 책임 경계, queue full과 priority inversion failure를 설명합니다.
2. period, release jitter, execution time, response time, deadline과 WCET를 구분합니다.
3. task priority와 stack budget을 정하는 데 필요한 입력을 설명합니다.
4. watchdog이 단순 reset loop가 되지 않도록 supervision과 recovery policy를 설계합니다.
5. boot image 선택, power-loss, known-good fallback invariant를 설명합니다.

### Vehicle networks and AUTOSAR

1. CAN arbitration, error active/passive, bus-off가 application state에 미치는 영향을 설명합니다.
2. CAN frame, ISO-TP와 UDS의 책임을 구분하고 multi-frame timeout을 설명합니다.
3. SOME/IP message와 SOME/IP-SD, DoIP의 목적을 구분합니다.
4. Classic의 CanIf/PduR/COM/RTE와 CanTp/DCM/DEM/NvM 흐름을 설명합니다.
5. Adaptive의 EM/SM/PHM/Communication Management 책임을 구분합니다.

### Linux platform and architecture

1. process group을 포함한 graceful shutdown → timeout → forced termination을 설계합니다.
2. socket backpressure, bounded queue와 service availability의 관계를 설명합니다.
3. requirement → quality attribute → budget → component/interface → verification 연결을 설명합니다.
4. task overrun, bus-off와 process crash를 MCU–Linux 경계에서 어떻게 격리·전파할지 설명합니다.
5. signed update, anti-rollback, health check와 rollback의 trust/state boundary를 그립니다.

## Timed practical baseline

| Exercise | Limit | Required evidence | Start result | G0 retest |
| --- | ---: | --- | --- | --- |
| 빈 저장소에서 C/CMake unit-test project 작성 | 60 min | clean build/test commands |  |  |
| bounded ring buffer + wrap/full tests | 90 min | code, invariant, tests |  |  |
| malformed 8-byte vehicle signal decoder 진단 | 60 min | hypothesis log, root cause, regression |  |  |
| GCC/Clang + sanitizer matrix | 45 min | complete command/output summary |  |  |
| 처음 보는 crash 디버깅 | 60 min | symptom→hypothesis→observation→cause |  |  |
| 작은 component architecture defense | 30 min | requirements, alternatives, trade-off |  |  |

## Domain result

| Domain | Start score 0–5 | Evidence | Critical gaps | G0 retest | Next Gate action |
| --- | ---: | --- | --- | ---: | --- |
| Systems C |  |  |  |  |  |
| Embedded C++ |  |  |  |  |  |
| ARM / compiler |  |  |  |  |  |
| Bare-metal / RTOS |  |  |  |  |  |
| CAN / diagnostics |  |  |  |  |  |
| Linux platform |  |  |  |  |  |
| Classic / Adaptive concepts |  |  |  |  |  |
| Architecture / security |  |  |  |  |  |

## Prioritized gap backlog

| Priority | Gap | Risk if ignored | Smallest falsifiable experiment | Gate / issue |
| ---: | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

## G0 exit decision

- [ ] 새 환경에서 README만으로 build/test를 재현했다.
- [ ] GCC와 Clang에서 warning-clean build 증거가 있다.
- [ ] ASan/UBSan이 실제 defect를 찾고 수정하는 과정을 설명했다.
- [ ] raw observation, interpretation과 `Unverified` assumption을 구분했다.
- [ ] timed practical을 같은 조건으로 다시 수행해 개선과 남은 gap을 비교했다.
- [ ] [Mastery review](templates/mastery-review.md)에 독립성 증거를 연결했다.

Result: `Passed / Needs more evidence`

Reviewer or clean-room environment:

Next quarterly retention window:
