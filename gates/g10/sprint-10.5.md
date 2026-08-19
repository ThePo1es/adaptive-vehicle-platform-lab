# Sprint 10.5 — Alive·Deadline·Logical Supervision

## 시간과 기준 자료

24–30시간. R25-11 `Platform Health Management`의 supervision, checkpoint, local/global supervision status, recovery 관련 절을 읽습니다. 로컬 감시기가 구현하는 범위와 공식 PHM에서 빠진 기능을 `phm-mapping.md`에 적습니다.

## 시작 조건과 fixture

fixture 프로세스는 정상 heartbeat, 누락, 빠른 heartbeat, 늦은 checkpoint, 잘못된 checkpoint 순서, 중복 checkpoint를 생성합니다. 모든 테스트는 virtual monotonic clock을 사용합니다. supervision cycle, expected count, min/max margin, deadline, logical graph를 config로 고정합니다.

## 안내 실습

Alive Supervision에서 cycle별 기대 횟수와 허용 margin을 검사합니다. Deadline Supervision은 start/end checkpoint 사이 시간을 확인합니다. Logical Supervision은 허용 checkpoint graph 밖의 전이를 잡습니다. 세 결과가 로컬 supervision status로 모이는 표를 만듭니다.

## 독립 실습

monitor는 supervision 결과와 recovery request만 냅니다. P03 Process Controller가 versioned policy로 restart·degraded·shutdown을 선택하고 P01이 action을 실행합니다. systemd는 managed application을 재시작하지 않습니다. startup grace, recovery cooldown, restart budget을 넣어 false positive와 recovery storm을 막습니다.

## 전이 과제

비공개 trace에는 정확히 경계에 놓인 heartbeat, 프로세스 restart 뒤 오래된 checkpoint, clock advance, logical cycle이 섞입니다. reference evaluator와 로컬 monitor 결과를 비교하고 첫 divergence를 찾습니다.

## 판정 기준

- 세 supervision type의 positive·boundary·negative 테스트가 존재
- 실제 sleep 없이 수 시간 trace를 1초 안에 평가
- 고장 detection, supervision status, recovery decision, action이 각각 기록됨
- [lifecycle ownership contract](../../docs/lifecycle-ownership.md)와 실제 restart actuator가 일치
- restart 뒤 이전 프로세스 instance checkpoint를 수용하지 않음
- false positive와 missed detection corpus가 모두 예상 결과와 일치
- 로컬 prototype과 R25-11 PHM 차이가 section citation과 함께 정리됨

## 감시 로직 확인

1. heartbeat payload에는 프로세스 instance와 sequence를 둡니다.
2. deadline의 양 끝 checkpoint 포함 여부를 테스트 vector로 고정합니다.
3. supervision failure가 곧바로 restart를 뜻하지는 않습니다. policy가 action을 고릅니다.

## 감시 결과를 인정하지 않는 경우

wall clock으로 deadline을 계산했거나 이전 instance의 heartbeat가 새 프로세스를 살렸거나 감지와 조치를 한 함수에 숨겼다면 Alive Supervision 하나만 남깁니다. 가상 trace 평가기와 결과를 맞춘 뒤 다른 감시를 추가합니다.
