# Mastery Assessments

평가는 실제 작업과 가까운 형태로 진행합니다. 설명, 구현, 고장 진단, 측정, 설계 변경, 새 환경 재현을 함께 봅니다. 해당 Gate의 핵심 능력은 3–4개 과제로 확인합니다.

## 숙련도

| Level | 관찰 가능한 행동 |
| --- | --- |
| 0 — Recognize | 용어나 코드를 알아본다. |
| 1 — Reproduce | 안내를 따라 같은 결과를 만든다. |
| 2 — Apply | 익숙한 문제를 독립적으로 처리한다. |
| 3 — Diagnose | 낯선 고장과 경계 조건의 원인을 찾는다. |
| 4 — Design | 요구와 제약에서 구조를 정하고 trade-off를 책임진다. |
| 5 — Teach/Review | 새로운 문제를 해결하고 타인의 판단과 구현 품질을 높인다. |

각 Gate는 관련 역량 Level 3과 설계 항목 Level 4를 목표로 합니다. Level 5는 하위 시스템 하나를 3–6개월 유지하고, 낯선 결함 수정과 다른 환경 이식까지 마친 뒤 외부 검토로 판정합니다.

## 평가 종류

| 평가 | 적용 시점 | 방식 |
| --- | --- | --- |
| Lab exit | 모든 Gate | 자동 oracle과 짧은 전이 과제 |
| Major Gate exam | G0, G3, G5, G7–G11, G12 | 설명·구현·진단·설계 defense를 3–4개 task로 확인 |
| 포트폴리오 검토 | G7, G10, G12 | 릴리스, 재현성, 주장 범위를 외부 검토 |
| Quarterly cumulative | 분기마다 | 이전 Gate의 기술 2–3개를 표본 재평가 |
| Level 5 판정 | 선택한 하위 시스템의 유지·이식 종료 | 독립 검토자 두 명 또는 upstream maintainer 검토 |

Gate를 시작하기 전에는 [입구 진단과 보강 모듈](docs/gate-entry-diagnostics.md)을 사용합니다. 일반 Sprint는 자동 oracle, 공개된 upstream 결함, 두 번째 구현체로 먼저 판정합니다. 외부 검토는 Major Gate와 포트폴리오 릴리스에 모읍니다.

## 공통 합격 조건

다음 항목을 모두 충족해야 합니다.

- 필수 불변 조건과 인수 시험이 통과한다.
- 숨겨진 fault의 root cause를 찾고 regression test를 추가한다.
- 측정 환경과 원본 자료가 commit에 연결된다.
- 새 환경에서 build/test/demo를 재현한다.
- 주장, 확인된 근거, 남은 가정을 구분한다.
- 치명적인 safety/security invariant 실패가 없다.
- 검토자의 필수 수정 사항을 반영한다.

외부 검토를 받기 전에는 `Provisional`로 표시합니다. 다음 Major Gate에 들어가기 전에 검토를 받거나 아래 대체 절차를 통과합니다.

## 관찰 기준

| 항목 | 실패 | 통과 | 강한 통과 |
| --- | --- | --- | --- |
| Correctness | 정상 경로도 불안정 | 오류 경로와 invariant test 통과 | property·model·differential test가 결함을 잡음 |
| Diagnosis | 로그를 늘리며 추측 | 가설과 관찰 도구로 root cause 확인 | 작은 reproducer와 재발 방지 체계까지 완성 |
| Measurement | 단일 숫자 | 조건·분포·원본 자료·오차 기록 | analytical budget과 validity threat까지 연결 |
| Design | 구현을 사후 설명 | 요구와 대안에서 결정을 도출 | 요구 변경에도 영향과 trade-off를 즉시 추적 |
| Reliability | 일부 retry | fault containment와 bounded recovery 확인 | 조합 fault와 장기 soak에서도 상태 일관성 유지 |
| Independence | 기존 답을 재생 | 새로운 표면의 과제를 독립 수행 | 다른 target·codebase로 전이하고 review 가능 |
| Reproducibility | 개인 환경 의존 | 제3자가 문서로 재현 | versioned 릴리스와 근거 자동 재생성 |

합격에는 전 항목 `통과`가 필요합니다. 해당 Gate의 중점 항목 두 개는 `강한 통과`를 받아야 합니다. Gate별 중점 항목과 즉시 탈락 조건은 [동결 평가 계약](assessments/README.md)에서 관리합니다.

## 시험 준비와 봉인 절차

### 시험 전

1. 응시할 commit SHA를 고정합니다.
2. build와 공개 test가 통과하는지 확인합니다.
3. 검토자가 고장 문제 모음 또는 전이 과제를 고릅니다.
4. fault 내용은 시험 시작 전까지 응시자에게 공개하지 않습니다.
5. 제한 시간, 허용 도구, 인터넷·AI 사용 범위를 기록합니다.

### 시험 중

- terminal transcript, 화면 기록 또는 command log를 남깁니다.
- 증상, 가설, 다음 관찰, 결론을 시간 순서대로 적습니다.
- 외부 힌트를 받으면 시각과 내용을 기록합니다.
- 환경 문제로 중단되면 문제를 수정한 뒤 새 fault로 다시 시작합니다.

### 시험 후

- 검토자가 준비한 기준 원인과 비교합니다.
- 놓친 경계 조건을 regression test로 추가합니다.
- fault는 다음 응시자에게 재사용하지 않거나 공개 시점을 늦춥니다.
- 재시험은 같은 개념을 다른 구현과 증상으로 바꿉니다.

## Fault bank

Fault bank에는 다음 필드를 둡니다.

| 필드 | 내용 |
| --- | --- |
| ID | 공개 목록과 분리된 식별자 |
| Target commit | 주입 가능한 기준 SHA |
| Seed patch | 검토자만 보관하는 변경 |
| Symptom | 응시자에게 제공할 관찰 |
| Root cause | 기대 원인과 관련 invariant |
| Required evidence | 최소 command·trace·test 근거 |
| Fatal miss | 합격을 막는 오판 |
| Partial credit | 원인 범위를 좁힌 정도와 근거 |

학습자가 직접 만든 고장은 연습용으로 사용합니다. 평가용 문제는 검토자, upstream bug corpus, 다른 구현체의 conformance suite에서 가져옵니다. LLM이 만든 문제는 검토자가 먼저 실행해 정답과 재현성을 확인한 뒤 봉인합니다.

## 검토자 기준

### 필요한 사람

- G1/G3: 해당 언어·compiler·binary 작업을 검토할 수 있는 개발자 1명
- G5: RTOS·CAN·embedded 경험이 있는 검토자 1명
- G7: Classic Platform 경험이 있거나 선택한 AUTOSAR release의 관련 공식 문서를 직접 검토한 사람 1명
- G8/G9: Linux platform·network protocol 결과를 새 환경에서 재현할 수 있는 검토자 1명
- G10: Adaptive Platform 경험이 있거나 선택한 release 문서와 Linux lifecycle·service architecture를 함께 검토한 사람 1명
- G11: safety와 security 관점을 나눠 보는 검토자 2명
- G12: embedded 또는 platform 검토자 1명과 새 환경 재현 담당 1명

### 대체 절차

사람을 구하지 못하면 official test, second implementation, mutation test, known upstream bug로 기술 정확성을 보완합니다. architecture defense와 Level 5 endorsement는 자동 oracle만으로 끝낼 수 없습니다. 해당 상태는 `Provisional`로 남깁니다.

재현 담당자는 명령, 입력, 결과가 같은지 확인합니다. 도메인 검토자는 표준 해석, 책임 경계, 주장 범위를 봅니다. 한 사람이 두 역할을 맡을 수 있지만 서명란은 나눠 기록합니다. 검토자 답변을 기다린 시간은 Sprint 작업 시간에 넣지 않고 별도 대기 시간으로 남깁니다.

검토자는 다음 내용을 기록합니다.

- 관련 경험과 이해관계
- 검토한 commit과 환경
- 필수 수정, 권고 수정, 동의하지 않은 주장
- 재검토 결과

## AI 사용

| 단계 | 허용 범위 |
| --- | --- |
| 학습 | 설명 비교, source 탐색, 반례 후보 생성 |
| 구현 | 허용. 사용 지점과 검토 내용을 PR에 기록 |
| 공개 test 작성 | 허용. mutation과 비공개 corpus로 강도를 확인 |
| 비공개 고장 진단 | 초기 힌트 금지 |
| timed implementation | 코드 생성 금지 |
| design defense | 준비된 답변 없이 직접 응답 |
| postmortem | 허용. 빠진 반례와 대안을 찾는 데 사용 |

생성 코드를 병합한 사람은 state, invariant, ownership, concurrency boundary, cleanup과 test 목적을 직접 설명할 수 있어야 합니다.

## Major Gate 시험

### G0 — Engineering baseline

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| 새 환경 build | 60분 | 문서만으로 GCC/Clang test 재현 |
| sanitizer diagnosis | 45분 | 결함 원인과 regression test 확인 |
| baseline replay | 기존과 동일 | 실제 향상과 남은 gap 기록 |

### G3 — ARM ABI and LLVM

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| ABI reverse walk | 60분 | source↔assembly↔AAPCS32/64 연결 |
| binary diagnosis | 60분 | ELF/map/symbol에서 원인 찾기 |
| compiler transfer | 90분 | 처음 보는 함수의 IR·기계어·측정 분석 |

### G5 — RTOS and Real-Time Analysis

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| task-set analysis | 75분 | blocking·jitter·interference를 포함한 RTA |
| 비공개 scheduling 고장 | 90분 | inversion 또는 overload root cause와 수정 |
| measurement defense | 45분 | 분석 bound, 실측, 오차, workload를 연결 |

### G7 — Classic Platform Concepts

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| unknown CAN/UDS path | 90분 | packet에서 application·DTC까지 추적 |
| 비공개 책임 경계 고장 | 60분 | layer 오배치와 상태 결함 수정 |
| concept defense | 45분 | 공식 책임과 local 단순화를 정확히 구분 |

### G8 — Embedded Linux Platform and Image

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| lifecycle incident | 90분 | pidfd·cgroup 경계에서 descendant와 stale action 원인 진단 |
| clean image replay | wall time 반나절 | pinned Buildroot image, SBOM, writable-state policy 재현 |
| policy fault | 60분 | systemd/cgroup/seccomp/resource limit의 최소 수정과 근거 |
| scheduling defense | 45분 | policy·affinity·inversion·PREEMPT_RT 측정 범위 설명 |

### G9 — Service-oriented Vehicle Communication

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| interface transfer | 60분 | Service Interface 변경을 Proxy/Skeleton·binding 영향으로 연결 |
| malformed SOME/IP | 75분 | framing·length·version 오류를 parser와 packet에서 진단 |
| SD lifecycle fault | 75분 | availability·subscription·TTL의 최초 divergence 확인 |
| vertical-slice replay | 90분 | rolling counter·session·quality를 vCAN부터 client까지 추적 |

### G10 — Adaptive Platform Concepts

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| manifest/lifecycle fault | 90분 | dependency·state·health 원인 진단 |
| design repair | 60분 | EM/SM/PHM 책임을 재배치하고 test 정의 |
| managed-node replay | active 90분, build wall time 별도 | 새 환경 배포와 failure recovery 재현 |
| diagnostic/IAM fault | 75분 | transport ID와 principal을 구분하고 policy·audit 경계 수정 |

### G11A — Adaptive Security and UCM

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| package attack corpus | 90분 | canonical form, signer authorization, path identity 결함 진단 |
| interruption campaign | wall time 반나절 | transfer·processing·activation durable boundary 재생 |
| state/version conflict | 75분 | Function Group·compatibility·health·rollback 결정 복구 |

### G11B — Cross-domain Assurance

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| changed operating scenario | 60분 | HARA/FMEA/TARA와 derived requirement 영향 갱신 |
| trust-root challenge | 60분 | T1/T2/T3 주장과 hardware assumption을 정확히 제한 |
| assurance defense | 75분 | safety·security reviewer의 반대 의견을 evidence로 처리 |

### G12 — Architecture and Integration

| 과제 | 시간 | 합격 기준 |
| --- | ---: | --- |
| 새 환경 재현 | 반나절 | 제3자가 릴리스를 재현 |
| 비공개 end-to-end 고장 | 120분 | 두 node를 가로지르는 root cause와 regression |
| requirement change | 60분 | 영향, budget, interface, test, ADR 갱신 |
| design defense | 60분 | 외부 질문과 반대 의견에 근거로 응답 |

## Gate별 Lab Exit

| Gate | 전이 과제 | 핵심 oracle |
| --- | --- | --- |
| G1 | ring buffer 대신 packet pool 구현 | invariant + property/mutation test |
| G2 | 처음 보는 ownership bug가 든 pipeline 수리 | sanitizer + lifetime contract |
| G4 | 다른 interrupt/fault를 register dump로 진단 | reference manual + crash record |
| G6 | 다른 timer parameter의 ISO-TP peer와 상호 운용 | packet trace + second stack |
| G8 | session을 이탈한 child와 stale PID action 수정 | cgroup/pidfd + bounded shutdown |
| G9 | delayed SD offer, version mismatch, source-session 변경 처리 | packet/state/contract oracle |
| G11A | 새로운 중단 지점·attacker capability 추가 | update state model + policy corpus |
| G11B | operating scenario와 common-cause 가정 변경 | safety/security argument review |

## Challenge-out

기존 프로젝트로 Gate의 일부 또는 전부를 인정할 수 있습니다.

1. `docs/baseline.md`에 이전 근거, 본인 기여, 공개 가능한 범위를 적습니다.
2. 현재 Gate의 독립 실습과 전이 과제를 그대로 수행합니다.
3. Major Gate에서는 비공개 고장 과제와 설계 질의도 진행합니다.
4. evidence가 오래됐으면 현재 toolchain에서 재현합니다.
5. 통과하면 상태를 `Validated`로 기록하고 1–2주 보강 Sprint만 진행합니다.

이전 경험의 근거는 공개 가능한 설명, 새로 만든 작은 reproducer, 검토자 확인으로 구성합니다. 소속 회사의 비공개 코드와 문서는 제외합니다.

## 누적 유지 시험

분기마다 필수 선수 기술 2개, 간격 반복 대기열 1개, 나머지 Gate에서 무작위 기술 1개를 뽑습니다. 총 소요 시간은 6–10시간이며 각 Sprint의 누적 복습 예산에서 충당합니다.

- 도움 없는 설명 20분
- 작은 전이 구현 60–90분
- 숨겨진 fault 하나 60–90분
- 오래된 릴리스의 새 환경 build
- ADR 하나를 현재 근거로 재검토

핵심 선수 기술에서 실패하면 상태를 `Needs refresh`로 바꾸고 1주 보강합니다. 후속 Gate가 해당 기술에 의존하면 보강을 마칠 때까지 승급을 멈춥니다.

## Expert Endorsement

Level 5는 선택 subsystem 이름과 검토 날짜를 함께 적습니다. 다음 증거가 필요합니다.

- 한 release cycle 이상 upstream 또는 실제 사용자 요구를 따라 유지했다.
- 낯선 incident의 root cause와 regression을 독립적으로 만들었다.
- 두 target 또는 두 구현에서 같은 contract를 검증했다.
- 독립 검토자 두 명 또는 upstream maintainer가 결과를 검토했다.
- 반대 의견으로 설계나 주장을 수정했다.
- 변경 후 3–6개월 동안 회귀 여부를 관찰했다.
- 다른 사람이 설명 자료로 핵심 실험을 재현했다.

Gate 종료 기록은 [mastery review template](docs/templates/mastery-review.md)을 사용합니다.
