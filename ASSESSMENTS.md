# Mastery Assessments

체크박스를 채우는 것과 실력이 생기는 것은 다릅니다. 각 Gate는 **도움 없이 설명**, **빈 저장소에서 구현**, **고장 진단**, **측정 해석**, **설계 방어**, **깨끗한 환경 재현**을 모두 평가합니다.

## 숙련도 단계

| Level | Observable ability |
| --- | --- |
| 0 — Recognize | 용어나 코드를 보면 알아본다. |
| 1 — Reproduce | 안내를 따라 동일 결과를 만든다. |
| 2 — Apply | 비슷한 문제에 독립적으로 적용한다. |
| 3 — Diagnose | 고장·성능 저하·경계 조건의 원인을 찾는다. |
| 4 — Design | 요구사항과 제약에서 구조와 trade-off를 결정한다. |
| 5 — Teach/Review | 다른 구현을 비평하고 명확히 가르친다. |

Gate 통과는 핵심 항목이 최소 Level 3, 설계 항목이 최소 Level 4일 때만 인정합니다. Level 표와 아래 0–4점 scorecard는 서로 다른 척도입니다. Level은 장기 역량, scorecard는 해당 Gate 산출물의 품질을 평가합니다.

## 공통 시험 7종

### 1. Closed-book explanation

- 노트와 검색 없이 30–45분 설명
- 정의 나열이 아니라 input, state, output, failure, trade-off 설명
- 질문이 바뀌어도 같은 원리로 답변

### 2. Blank-page implementation

- 빈 저장소에서 핵심 구성요소를 제한 시간 내 구현
- 기존 코드를 복사하지 않음
- compiler warning, unit test, error path 포함

### 3. Fault diagnosis

- 원인을 미리 모르는 fault 3개 이상
- 증상 → 가설 → 관찰 도구 → root cause → regression test 순서 기록
- 로그 추가만으로 우연히 고치는 방식 금지

### 4. Measurement defense

- 동일 조건 반복 측정
- raw data와 요약 script 제공
- p50/p95/p99/worst, sample count, environment 기록
- 왜 그 metric과 workload를 선택했는지 방어

### 5. Architecture defense

- requirement, constraint, quality attribute에서 decision 도출
- 최소 두 대안과 trade-off 비교
- failure containment와 observability 포함
- 구현 결과가 decision을 지지하지 않으면 수정

### 6. Clean-room reproduction

- 새 clone 또는 새 VM/container/board 환경 사용
- README만으로 다른 사람이 build/test/demo
- 숨은 환경 변수, 수동 복사, 개인 경로 제거

### 7. Teach-back and review

- 10–20분 기술 설명 또는 문서
- 다른 구현의 결함·모호한 contract를 찾아 review
- 질문을 받았을 때 불확실한 부분을 사실처럼 답하지 않음

## AI 사용 규칙

LLM은 탐색·비평·테스트 아이디어·문서 검토에 사용할 수 있지만, 학습 여부를 속이지 않도록 평가를 분리합니다.

| Mode | AI allowed | Purpose |
| --- | --- | --- |
| Learn | Yes | 자료 탐색, 설명 비교, 실험 후보 생성 |
| Build | Yes, recorded | 구현 속도 향상과 code review |
| Debug exam | No initial hints | 자신의 관찰·가설 능력 검증 |
| Blank-page exam | No | 독립 구현 능력 검증 |
| Architecture defense | No prepared answers | 실제 reasoning 검증 |
| Postmortem | Yes | 빠진 반례와 대안 검토 |

AI가 생성한 코드는 다음 질문에 답하지 못하면 병합하지 않습니다.

- 각 state와 invariant는 무엇인가?
- failure path에서 resource ownership은 어떻게 정리되는가?
- thread/ISR/process boundary는 어디인가?
- 이 test가 어떤 결함을 막는가?
- compiler/OS/hardware가 달라지면 어떤 가정이 깨지는가?

## Gate scorecard

| Dimension | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| Correctness | 실행 불가 | happy path 일부 | 정상 경로 | 오류 경로 포함 | invariant/property로 검증 |
| Depth | 용어 암기 | API 사용 | 원리 설명 | 내부 동작·경계 설명 | 대안과 trade-off 설계 |
| Debugging | 추측 | 로그 의존 | 도구 사용 | 체계적 root cause | 재발 방지 체계 설계 |
| Measurement | 없음 | 단일 숫자 | 반복 수치 | 분포·환경·raw data | validity와 budget 연결 |
| Reliability | 없음 | 재시도 | 몇 개 오류 처리 | fault campaign | containment/recovery 증명 |
| Documentation | 메모 | 실행법 | 설계·테스트 | 요구사항·증거 연결 | 제3자 재현·review 가능 |
| Independence | 복사 | 안내 의존 | 일부 독립 | blank-page 재현 | 다른 문제로 전이·교육 |

통과 조건:

- 모든 dimension 3점 이상
- Depth, Reliability, Independence 중 두 항목 4점 이상
- critical safety/security invariant 실패 0개
- clean-room reproduction 성공
- `Unverified` 항목과 residual risk가 명시됨

## Gate별 실전 시험

### G0 Engineering baseline

- 새 clone/VM에서 문서만으로 toolchain setup과 build/test 재현
- GCC/Clang warning-clean build와 실제 ASan/UBSan defect 진단
- 시작 baseline의 timed practical을 같은 조건으로 재시험
- observation, interpretation, assumption과 `Unverified`를 구분한 evidence review

### G1 Systems C

- 90분: bounded ring buffer와 test 작성
- 45분: integer/aliasing/alignment UB 사례 분석
- hidden corpus: malformed CAN/UDS frame parser
- compiler flags 변화에 따른 behavior 설명

### G2 Embedded C++

- 120분: ownership-safe message pipeline
- dangling view, use-after-move, race가 섞인 코드 진단
- exception/RTTI/heap 정책 architecture defense

### G3 ARM/LLVM

- C 함수에서 ABI와 assembly를 역으로 설명
- linker map과 fault register로 crash 진단
- `-O2/-Oz` 차이를 IR→machine code→measurement로 연결

### G4 Bare-metal

- 빈 프로젝트에서 vector/startup/timer/interrupt 경로 구성
- interrupt storm 또는 stack fault 진단
- boot/memory map whiteboard defense

### G5 RTOS

- task set에 priority/deadline/stack budget 배정
- priority inversion과 overload hidden fault
- 100,000 release timing report 재생성

### G6 Classic concepts

- CAN frame부터 SWC-like application까지 call path 구현·설명
- ISO-TP timeout/NRC/storage corruption 진단
- CanIf/PduR/COM/RTE/DCM/DEM/NvM 책임 경계 방어

### G7 Linux platform

- hanging child/process group shutdown fault
- `strace`, core dump, `perf` 중 적절한 도구 선택
- restart policy와 resource limit 설계

### G8 Vehicle networks

- unknown packet capture에서 SOME/IP/DoIP/ISO-TP 계층 식별
- bus-off와 service restart end-to-end recovery
- 주기·event·stale-data 정책 방어

### G9 Adaptive concepts

- EM/SM/PHM 책임이 뒤섞인 설계 refactor
- manifest dependency cycle와 health/reboot fault
- concept mapping에서 과장 표현 찾기

### G10 Security/resilience

- signed package negative corpus
- update state마다 kill/power-loss simulation
- threat model에서 빠진 trust boundary와 residual risk 찾기

### G11 Architecture capstone

- 요구사항 변경 3개를 architecture와 traceability에 반영
- timing/memory/network budget 초과 원인 진단
- 외부 reviewer 앞에서 45–60분 design defense
- clean machine/board에서 end-to-end demo

## 유지 시험

한 번 통과한 지식도 다음 간격에 짧게 재평가합니다.

- 2주 후: 핵심 개념 closed-book 설명
- 6주 후: blank-page 핵심 구성요소 구현
- 12주 후: 새로운 fault 또는 다른 target으로 전이
- 6개월 후: 이전 architecture decision 재검토

재평가에서 실패하면 Gate를 취소하는 대신 `Needs refresh`로 표시하고 1주 복구 sprint를 수행합니다.

## Level 5 expert endorsement

G11 통과만으로 Level 5를 자동 부여하지 않습니다. 선택 subsystem에서 다음을 모두 증명해야 합니다.

- 3개월 이상 upstream source/issue/release를 지속 추적했다.
- 처음 보는 defect 5개 이상을 재현·진단하고 regression을 설계했다.
- 두 target 이상에 이식해 같은 contract/fault suite를 재사용했다.
- maintainer 또는 외부 expert feedback으로 자신의 결정을 수정했다.
- 타인 code/design review 5회 이상과 교육 자료를 남겼다.
- 학습자가 문서/세션만으로 핵심 실험을 독립 재현했다.
- 성능·신뢰성 개선의 raw evidence와 부작용 분석이 있다.

Level 5는 “모든 것을 안다”가 아니라 특정 subsystem에서 새로운 문제를 해결하고 타인의 판단 품질도 높일 수 있다는 뜻입니다.

## 승급 기록

각 Gate 종료 시 [mastery review template](docs/templates/mastery-review.md)을 작성합니다. “통과했다고 느낌”이 아니라 commit, test, raw data, packet, report, reviewer feedback 링크를 남깁니다.
