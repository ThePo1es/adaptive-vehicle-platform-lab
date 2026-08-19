# Sprint 9.8 — P05 CAN–SOME/IP vertical slice

## 시간과 기준 자료

24–30시간. [P05 범위](../../projects/05-can-ethernet-vertical-slice/README.md), Linux kernel의 [SocketCAN 문서](https://docs.kernel.org/networking/can.html), P02 interface와 time contract를 사용합니다. vCAN을 필수 재현 환경으로 두고 실제 CAN hardware 결과는 별도 lane에 둡니다.

## 시작 조건과 signal contract

CAN frame 하나에 vehicle speed와 gear signal을 정의합니다. CAN ID, endian, start bit, length, scale, offset, range, invalid, cycle, timeout을 표로 작성합니다. SOME/IP event에는 value, unit, source sequence, source timestamp, gateway receive timestamp, quality를 담습니다.

## 안내 실습

node A의 `vcan` producer가 frame을 보내고 gateway가 decode해 P02 event로 발행합니다. node B consumer는 service discovery 후 subscribe합니다. CAN frame, gateway structured log, SOME/IP packet, consumer state를 같은 `trace_id`와 sequence로 연결합니다.

## 독립 실습

duplicate, gap, out-of-range, invalid value, stale timeout을 주입합니다. gateway process와 SOME/IP provider를 각각 재시작하고 source freshness와 service availability가 어떻게 바뀌는지 확인합니다. physical CAN이 있으면 bus-off와 recovery를 별도 fixture로 실행합니다.

## 전이 과제

외부 검토자가 signal scale 또는 service minor version을 바꾼 replay bundle을 줍니다. compatibility가 허용하는 변화와 거부할 변화를 contract에서 찾아 적용합니다. 검토자는 공개된 raw CAN log만으로 node B 결과를 재생합니다.

## 판정 기준

- CAN input부터 SOME/IP consumer까지 sequence·value·quality 추적 가능
- 정상 10Hz 10분 run에서 보존식과 latency report가 재생됨
- invalid·stale·gap이 normal value로 조용히 전달되지 않음
- gateway/provider/consumer restart 후 bounded recovery와 중복 수를 보고
- vCAN clean-machine replay가 통과하고 hardware 결과는 환경 정보 포함
- version change 전이 과제와 외부 검토 기록이 release에 포함

## 힌트

1. CAN receive timestamp와 signal의 실제 물리 측정 시점이 다를 수 있음을 contract에 적습니다.
2. restart 뒤 sequence 초기화 규칙에는 source instance 식별자가 필요합니다.
3. public capture에는 실제 차량의 arbitration ID와 payload를 넣지 않습니다.

## 치명적 실패와 보충

단위·scale이 문서와 code에서 다르거나, stale data가 정상 quality로 남거나, 외부 replay가 재현되지 않으면 Gate를 통과하지 못합니다. 실패 Sprint를 12–20시간 보강하고 새 release tag로 다시 심사합니다.
