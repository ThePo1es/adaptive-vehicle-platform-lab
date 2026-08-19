# Gate Lab Packs

각 Sprint 파일은 시작 전에 동결합니다. 풀이를 시작한 뒤에는 입력, oracle, 허용 오차, 재시험 조건을 바꾸지 않습니다.

## 준비 상태

| Gate | Lab pack | 상태 |
| --- | --- | --- |
| G0 | [2 Sprint](g00/) | Specified |
| G1 | [5 Sprint](g01/) | Specified |
| G2 | [4 Sprint](g02/) | Specified |
| G3 | [5 Sprint](g03/) | Specified |
| G4 | [6 Sprint](g04/) | Specified |
| G5 | [7 Sprint](g05/) | Specified |
| G6 | [8 Sprint](g06/) | Specified |
| G7 | [6 Sprint](g07/) | Specified |
| G8 | [9 Sprint](g08/) | Specified |
| G9 | [10 Sprint](g09/) | Specified |
| G10 | [10 Sprint](g10/) | Specified |
| G11A | [4 Sprint](g11/) | Specified |
| G11B·G12 | [Gate Playbook](../docs/gate-playbook.md) | Outline; 15 Sprint 작성 필요 |

현재 91개 중 76개가 `Specified`, 15개가 `Outline`입니다. 이 수치는 문서 작성 진도이며 학습 효과를 뜻하지 않습니다.

| 상태 | 필요한 근거 |
| --- | --- |
| Outline | 주제, 선수 관계, 종료 결과가 Gate Playbook에 있음 |
| Specified | 기준 자료, 과제, oracle 성격, 전이 과제, 재시험 조건이 문서화됨 |
| Runnable | starter commit, fixture·corpus hash, 실행 명령, expected output, active/wall time이 검증됨 |
| Assessment-ready | 봉인 과제와 독립 oracle을 검토자가 실행했고 assessment manifest hash가 있음 |

파일을 `Runnable`로 올릴 때는 starter와 fixture commit SHA를 이 문서에 연결합니다. 빈 SHA나 아직 실행하지 않은 inline fixture는 `Specified` 상태로 둡니다. Gate 공통 수치와 산출물 계보는 각 Sprint가 연결한 `contract.md`에 둘 수 있습니다.

Linux/Adaptive 경로는 G3 다음에 G8부터 시작합니다. 권장 순서는 `G8 → G9 → G10 → G11A → G4–G7 → G11B → G12`입니다.

각 Gate에 들어가기 전에는 [입구 진단](../docs/gate-entry-diagnostics.md)을 먼저 수행합니다. 필수 항목에서 막힌 경우 전체 선행 과정을 반복하지 않고 해당 8–16시간 보강 모듈만 마친 뒤 다른 입력으로 재시험합니다.

## 파일에 필요한 항목

- 기준 자료의 release·document ID·section title 또는 requirement ID
- 시작 파일과 입력 corpus
- 안내 실습, 독립 실습, 전이 과제
- expected output, invariant, 허용 오차
- 필요한 경우에만 단계별 힌트
- 재시험 조건과 채점 기준
- Core, Gate evidence, Stretch별 active time과 build·soak wall time

G4–G7 공통 계약: [G4](g04/contract.md), [G5](g05/contract.md), [G6](g06/contract.md)·[physical bench](g06/bench-contract.md), [G7](g07/contract.md)·[R25-11 ledger](g07/source-ledger.md).

평가용 비공개 고장은 이 디렉터리에 저장하지 않습니다. 시험 때 사용하는 manifest의 hash와 검증 날짜만 [mastery review](../docs/templates/mastery-review.md)에 기록합니다.
