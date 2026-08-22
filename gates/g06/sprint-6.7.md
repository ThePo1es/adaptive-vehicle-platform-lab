# Sprint 6.7 — DTC read, access policy, flood control

추적 대상: `OUT-XCUT-G6`, `REQ-ECU-DIAG-001`, `REQ-ECU-DIAG-003`, `REQ-DTC-001`. `FATAL-G6.7-ACCESS`는 unauthorized request가 state를 바꾸거나 flood가 health work를 무제한 굶긴 경우입니다.

## 시간과 기준 자료

22–28시간. 같은 UDS edition의 ReadDTCInformation 허용 subfunction, P00의 event/DTC 상태 model, SECURITY의 bench 정책을 사용합니다. 실제 차량 DTC나 식별 자료를 fixture로 복사하지 않습니다.

flood rate, counter 보존식, 다음 Sprint로 넘길 결과는 [G6 실행 계약](contract.md) 6.7에서 동결합니다.

## 데이터 책임

diagnostic dispatcher는 request를 검증하고 DTC store를 조회합니다. event status, debounce, occurrence metadata, snapshot의 owner는 DTC component에 둡니다. 이번 Sprint의 store는 memory-backed reference이며 crash consistency는 G7.4에서 추가합니다.

## 안내 실습

합성 event 세 개로 pending, confirmed, healed transition을 만들고 허용한 `0x19` read 결과와 대조합니다. mask, count, ordering, response-size limit을 기준 model에서 계산합니다. audit에는 requester context, SID/subfunction, 결과, correlation ID를 남기되 payload secret은 기록하지 않습니다.

## 독립 실습

per-principal 또는 bench-client rate limit, 크기가 정해진 request 큐, maximum response size를 넣습니다. malformed length, unknown subfunction, DTC flood, provider unavailable에서도 diagnostic work가 RTOS health task budget을 침범하지 않게 합니다.

## 전이 과제

두 tester 동시 flood, status-mask 경계, event update/read race를 같은 초기 상태에서 비교합니다. accepted, rejected, completed, timed-out 수의 보존식과 DTC 상태 consistency를 확인합니다.

## 판정 기준

- dispatcher와 DTC 상태 책임자의 책임이 interface로 분리됨
- 허용 subfunction·status mask·response bound가 config에 고정됨
- malformed/unauthorized request가 DTC state를 바꾸지 않음
- `accepted = completed + active + timed_out + provider_failed` 관계가 성립
- flood 중 CPU·큐 budget과 health deadline이 유지되거나 정한 축소가 실행
- audit에서 credential·secret·실차 식별 data가 나오지 않음

## 부하 단계와 중단선

요청률은 1, 10, 100, 1,000 req/s 순으로 올립니다. 각 단계에서 counter 보존식과 health deadline을 먼저 확인합니다. deadline이 연속 두 번 깨지거나 probe가 불안정해지면 그 단계에서 멈춥니다.

복구는 요청 하나와 event 하나에서 시작합니다. 보존식을 다시 맞춘 뒤 새 seed로 바로 이전 단계까지만 올립니다.
