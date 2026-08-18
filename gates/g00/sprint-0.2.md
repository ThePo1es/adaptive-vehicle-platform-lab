# Sprint 0.2 — 작업 환경 동결

## 시간

24–30시간. 환경 재현 12h, baseline 8h, 검토·기록 4–10h.

## 기준 자료

- [Git documentation](https://git-scm.com/doc): branching, commits, revisions
- [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Workflow artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts)
- [baseline dossier](../../docs/baseline.md)

## 시작 상태

Sprint 0.1 결과와 이 저장소를 사용합니다. Hardware/Access ADR은 [development environment](../../docs/development-environment.md)의 필드를 그대로 가져옵니다.

## 안내 실습

1. compiler, CMake, Ninja, Python version을 기록합니다.
2. `docs-integrity`와 C/C++ build job의 책임을 분리합니다.
3. 실패한 sanitizer log를 artifact로 보존하고 수정 commit과 연결합니다.
4. baseline의 timed practical을 첫 조건으로 수행합니다.

## 독립 실습

새 Ubuntu VM에서 저장소를 clone한 뒤 README만 사용해 모든 공개 check를 실행합니다. 누락된 package와 암묵적 환경 변수를 setup 문서에 반영합니다.

## 전이 과제

GCC 또는 Clang 중 하나를 다른 minor version으로 바꿉니다. 경고, binary size, test 결과의 차이를 기록하고 supported version 범위를 정합니다.

## 판정 기준

- OS·compiler·build tool version이 고정됨
- setup command가 idempotent하게 다시 실행됨
- baseline 답과 학습 뒤 보완 답이 분리됨
- board·RTOS·CAN bench·Linux node·표준 접근 상태가 ADR에 기록됨
- license 선택 이슈와 외부 검토자 후보 3명 또는 대체 경로가 등록됨

## 검토자 계획

| 역할 | 후보 / 경로 | 연락일 | 응답 목표 | 대체 방법 |
| --- | --- | --- | --- | --- |
| C/compiler |  |  | 14일 | public test + upstream review |
| RTOS/CAN |  |  | 14일 | second implementation + provisional |
| Linux/platform |  |  | 14일 | upstream/user review + provisional |
| Safety |  |  | 21일 | self-review only; G11 provisional |
| Security |  |  | 21일 | public crypto vectors; G11 provisional |

## 힌트

1. `env`, compiler `--version`, CMake cache에서 재현에 필요한 값만 고릅니다.
2. 도구 설치와 project build를 분리합니다.
3. 상용 문서 접근은 `Available / Limited / Unavailable`로 기록합니다.

## 치명적 실패

- 실제 키·토큰·개인 경로가 저장소에 들어감
- 검토자와 장비가 비어 있는데 이후 Gate를 확정 일정으로 표기함
- 라이선스 결정을 미룬 채 공개 code PR을 병합함

## 보충 과제

다른 VM image에서 setup을 한 번 더 실행하고 실패 원인을 issue로 분리합니다.
