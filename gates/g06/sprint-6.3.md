# Sprint 6.3 — CAN bus load와 response-time bound

추적 대상: `OUT-XCUT-G6`, `REQ-CAN-004`, `REQ-CAN-007`. `FATAL-G6.3-TIMING`은 측정 최대값을 analytical bound로 바꾸거나 arbitration/data phase를 합친 경우입니다.

## 시간과 기준 자료

24–30시간. CAN priority arbitration과 non-preemptive transmission response-time 분석 자료, [G6 bench contract](bench-contract.md)의 bit timing, [세 message RTA 입력](../../fixtures/g06/can-rta-three-message-v1.json)을 사용합니다. Classic CAN과 CAN FD의 arbitration phase·data phase·stuffing 가정을 별도 식으로 둡니다.

입력 message set의 판정 규칙과 결과 인계는 [G6 실행 계약](contract.md) 6.3을 따릅니다.

## 입력 명세

각 message에 ID, base/extended, Classic/FD, payload length, BRS, period 또는 minimum inter-arrival, deadline, release jitter, transmitter, error/retry policy를 적습니다. controller queue와 software task delay도 bus transmission과 섞지 않고 별도 항으로 둡니다.

## 안내 실습

작은 Classic CAN message set의 blocking, higher-priority interference, transmission time, response bound를 손으로 계산합니다. 같은 입력을 읽는 script가 iteration과 slack을 출력하게 하고 known vector로 검증합니다.

CAN FD는 arbitration bit rate와 data bit rate를 나눠 frame time을 구합니다. bit stuffing은 사용한 upper bound 또는 분석 가정을 명시합니다. error retransmission은 정상 부하에 숨기지 않고 별도 fault scenario로 계산합니다.

## 독립 실습

P00-B message set을 분석하고 analyzer timestamp와 비교합니다. measured maximum은 관찰 결과로 보존하며 analytical bound를 대신하지 않습니다. hardware filter·mailbox·driver queue가 만든 추가 지연도 trace에서 분리합니다.

## 전이 과제

payload, BRS, priority, burst arrival 중 두 값이 바뀐 message set을 받습니다. 전체 priority chain을 다시 계산해 deadline miss와 여유를 보고합니다.

## 판정 기준

- Classic/FD frame-time 계산과 stuffing assumption이 출처와 함께 기록됨
- non-preemptive lower-priority blocking을 포함
- release jitter와 higher-priority interference가 recurrence에 반영됨
- retransmission·bus-off는 정상 traffic bound와 분리된 scenario임
- script와 독립 손 계산이 기준 세트에서 일치
- analyzer 결과의 clock domain·sample count·invalid run 조건이 있음

## 계산표 반려 사유

analyzer에서 본 최대값에 임의 여유를 더한 수치, DLC와 payload length를 섞은 수치, stuffing 가정이 없는 수치는 모두 반려합니다. 고칠 때는 frame-time 기준 벡터 하나를 손으로 다시 계산하고 도구 출력과 맞춘 뒤 전체 message set으로 넓힙니다.
