# Gate Lab Packs

각 Sprint 파일은 시작 전에 동결합니다. 문제를 푼 뒤에는 입력, 판정 기준, 치명적 실패 조건을 바꾸지 않습니다.

## 준비 상태

| Gate | Lab pack | 상태 |
| --- | --- | --- |
| G0 | [2 Sprint](g00/) | Ready |
| G1 | [5 Sprint](g01/) | Ready |
| G2 | [4 Sprint](g02/) | Ready |
| G3 | [5 Sprint](g03/) | Ready |
| G4–G12 | [Gate Playbook](../docs/gate-playbook.md) | Curriculum backlog; 해당 Gate 진입 전 동결 필요 |

`Ready`는 과제 명세와 판정 기준이 있다는 뜻입니다. Starter code와 자동 test가 생기면 파일에 commit SHA를 추가합니다. SHA가 비어 있는 과제는 문서에 제시된 빈 디렉터리 또는 inline fixture에서 시작합니다.

## 파일에 필요한 항목

- 정확한 기준 자료와 절
- 시작 파일과 입력 corpus
- 안내 실습, 독립 실습, 전이 과제
- expected output, invariant, 허용 오차
- 단계별 힌트
- 치명적 실패 조건과 채점 기준
- 보충 과제와 시간 예산

평가용 비공개 고장은 이 디렉터리에 저장하지 않습니다. 시험 때 사용하는 manifest의 hash와 검증 날짜만 [mastery review](../docs/templates/mastery-review.md)에 기록합니다.
