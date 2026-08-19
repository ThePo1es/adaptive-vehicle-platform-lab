# Sprint 10.5 — Alive·Deadline·Logical Supervision

## 시간과 기준 자료

24–30시간. R25-11 `Platform Health Management`의 supervision, checkpoint, local/global supervision status, recovery 관련 절을 읽습니다. local monitor가 구현하는 범위와 공식 PHM에서 빠진 기능을 `phm-mapping.md`에 적습니다.

## 시작 조건과 fixture

fixture process는 정상 heartbeat, 누락, 빠른 heartbeat, 늦은 checkpoint, 잘못된 checkpoint 순서, 중복 checkpoint를 생성합니다. 모든 test는 virtual monotonic clock을 사용합니다. supervision cycle, expected count, min/max margin, deadline, logical graph를 config로 고정합니다.

## 안내 실습

Alive Supervision에서 cycle별 기대 횟수와 허용 margin을 검사합니다. Deadline Supervision은 start/end checkpoint 사이 시간을 확인합니다. Logical Supervision은 허용 checkpoint graph 밖의 전이를 잡습니다. 세 결과가 local supervision status로 모이는 표를 만듭니다.

## 독립 실습

P01 restart와 P03 degraded-state 요청을 recovery action으로 연결합니다. monitor가 fault를 감지한 event와 policy가 action을 선택한 event를 분리합니다. startup grace, recovery cooldown, restart budget을 넣어 false positive와 recovery storm을 막습니다.

## 전이 과제

비공개 trace에는 정확히 경계에 놓인 heartbeat, process restart 뒤 오래된 checkpoint, clock advance, logical cycle이 섞입니다. reference evaluator와 local monitor 결과를 비교하고 첫 divergence를 찾습니다.

## 판정 기준

- 세 supervision type의 positive·boundary·negative test가 존재
- 실제 sleep 없이 수 시간 trace를 1초 안에 평가
- fault detection, supervision status, recovery decision, action이 각각 기록됨
- restart 뒤 이전 process instance checkpoint를 수용하지 않음
- false positive와 missed detection corpus가 모두 예상 결과와 일치
- local prototype과 R25-11 PHM 차이가 section citation과 함께 정리됨

## 힌트

1. heartbeat payload에는 process instance와 sequence를 둡니다.
2. deadline의 양 끝 checkpoint 포함 여부를 test vector로 고정합니다.
3. supervision failure가 곧바로 restart를 뜻하지는 않습니다. policy가 action을 고릅니다.

## 치명적 실패와 보충

wall clock을 deadline에 쓰거나, 이전 instance heartbeat가 새 process를 살리거나, 감지와 action을 한 함수에서 숨기면 실패입니다. 보충 과제는 Alive Supervision 하나와 virtual trace evaluator만 다시 완성하는 것입니다.
