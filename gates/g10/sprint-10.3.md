# Sprint 10.3 — Dependency DAG와 실행 계획

## 시간과 기준 자료

24–30시간. R25-11 `Execution Management`의 process startup, dependency·configuration 관련 절과 [P03 scope](../../projects/03-execution-manager/README.md)를 읽습니다. 정확한 AUTOSAR dependency 표현은 읽은 manifest 절에서 인용하고 로컬 DAG 의미와 나란히 둡니다.

## 시작 조건과 reference model

node 1–50개, edge 0–200개를 만드는 graph generator를 준비합니다. Python 또는 짧은 독립 구현으로 topological order와 cycle 여부를 계산해 oracle JSON을 만듭니다. node name은 stable ID이며 입력 순서가 결과를 흔들지 않게 tie-break 규칙을 정합니다.

## 안내 실습

validated manifest에서 DAG를 만들고 deterministic start plan과 reverse stop plan을 냅니다. missing dependency, self-loop, duplicate edge, cycle을 실행 전에 거부합니다. cycle error에는 실제 cycle path를 하나 이상 보여 줍니다.

## 독립 실습

dependency가 `Ready`가 된 뒤 dependent를 시작하는 실행기를 P01에 연결합니다. start failure, readiness timeout, runtime failure가 direct dependent와 독립 branch에 미치는 정책을 표로 고정합니다. rollback 과정도 bounded timeout을 갖습니다.

## 전이 과제

비공개 graph에는 diamond, disconnected node, 긴 chain, 두 cycle, readiness 지연이 섞입니다. 90분 안에 plan과 failure propagation을 oracle과 비교하고 틀린 정책을 고칩니다.

## 판정 기준

- 모든 edge에서 dependency가 dependent보다 먼저 Ready
- stop plan이 살아 있는 dependency 관계를 깨지 않음
- cycle·missing node가 spawn 전에 구체적 path와 함께 거부됨
- 같은 graph는 입력 순서와 hash seed가 달라도 같은 plan 생성
- 1,000개 generated DAG/cyclic graph가 독립 oracle과 일치
- failure propagation과 rollback 상한이 scenario test로 확인됨

## 힌트

1. process spawn 성공과 service Ready를 같은 event로 쓰지 않습니다.
2. stop 중 이미 죽은 node는 idempotent하게 처리합니다.
3. graph library 결과도 작은 독립 oracle과 대조합니다.

## 치명적 실패와 보충

cycle 일부를 실행하거나, unordered container 순서가 plan을 바꾸거나, failed dependency 뒤 dependent를 시작하면 실패입니다. 보충 과제는 node 10개 이하 graph와 pure planner만 다시 검증하는 것입니다.
