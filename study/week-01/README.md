# Week 01 — Baseline, C Object Model and Undefined Behavior

## Metadata

- Gate: G0 baseline with G1 preview
- Date:
- Related issue:
- Environment: host/OS, GCC, Clang, CMake, sanitizer versions

## 이번 주 결론 목표

현재 실력을 과장 없이 측정하고, C의 object representation·alignment·integer conversion·bounds·lifetime 문제가 실제 compiler behavior와 sanitizer 결과에 어떻게 나타나는지 작은 실험으로 증명합니다.

## 핵심 질문

1. undefined, unspecified, implementation-defined behavior는 어떻게 다른가?
2. `memcpy`, pointer cast와 byte access는 object representation과 alignment에 어떤 차이를 만드는가?
3. signed/unsigned conversion과 shift 경계는 CAN signal decoder를 어떻게 망가뜨릴 수 있는가?
4. Debug에서 동작한 코드가 `-O2`에서 달라지면 어떤 근거 순서로 원인을 찾을 것인가?
5. sanitizer, warning, static analyzer가 각각 찾는 것과 놓치는 것은 무엇인가?

## 시작 전 baseline

노트와 검색 없이 45분 안에 다음을 작성합니다. 모르는 항목은 추측하지 말고 `Unknown`으로 둡니다.

- C object/lifetime/aliasing 10문항 자체 답변
- C++ ownership/concurrency 5문항 자체 답변
- ARM/ABI/linker 5문항 자체 답변
- RTOS/CAN/Linux/AUTOSAR 각 5문항 자체 답변
- 빈 저장소에서 build/test 가능한 C 함수 하나 작성
- 처음 보는 결함 코드 하나를 symptom → hypothesis → observation → cause 순서로 진단

결과는 `docs/baseline.md`에 강점, 결손, 증거, 우선 보강 순서로 기록합니다. 점수는 남과 비교하지 않고 이후 재시험의 기준선으로만 사용합니다.

## 최소 구현

길이와 byte order가 명시된 8-byte CAN payload signal decoder를 작성합니다.

- 고정 폭 정수만 사용
- input length와 bit range 검증
- signed/unsigned signal 처리 분리
- unaligned input에서도 정의된 동작
- error가 application state를 변경하지 않는 contract
- table-driven 정상·경계·오류 test

## 필수 실험

동일한 corpus를 아래 matrix로 실행합니다.

```text
GCC / Clang
-O0 / -O2 / -Oz
warnings / ASan+UBSan / Release
```

다음 결함을 하나씩 의도적으로 넣고 관찰합니다.

- out-of-bounds read
- misaligned typed access
- signed overflow 또는 invalid shift
- truncated payload
- signed/unsigned comparison error

각 결함에 대해 compiler output, runtime result, sanitizer/static check, 수정 뒤 regression test를 남깁니다.

## 해야 할 일

- [ ] [ROADMAP](../../ROADMAP.md)의 G0/G1 범위와 [평가 규칙](../../ASSESSMENTS.md)을 읽었다.
- [ ] `docs/baseline.md`에 closed-book baseline과 환경을 기록했다.
- [ ] clean build/test 명령을 한 블록으로 만들었다.
- [ ] decoder의 input/output/error/ownership contract를 먼저 작성했다.
- [ ] 정상·경계·malformed corpus를 자동 테스트했다.
- [ ] GCC/Clang과 optimization별 assembly 또는 IR 차이를 하나 이상 설명했다.
- [ ] sanitizer가 찾은 결함과 찾지 못한 결함을 구분했다.
- [ ] AI 도움 없이 핵심 decoder를 빈 파일에서 다시 작성했다.

## 주차 완료와 Gate 통과의 차이

이번 주 완료는 G0/G1 통과가 아닙니다. 다음 결과만 만들면 됩니다.

- 재현 가능한 baseline
- 첫 C component와 fault evidence
- 모르는 영역이 명시된 skill-gap 목록
- 다음 2주 실험 이슈

G0는 clean environment 재현, GCC/Clang build, 실제 sanitizer defect 설명과 evidence discipline을 모두 만족할 때 별도 mastery review로 통과합니다.

## 결과 및 회고

- 확인한 내용:
- 틀렸던 가정:
- sanitizer/static analysis의 blind spot:
- 아직 `Unverified`인 내용:
- 다음 실험:
