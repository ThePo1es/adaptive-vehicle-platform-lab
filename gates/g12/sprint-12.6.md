# Sprint 12.6 — CAN에서 VehicleState event까지

Sprint 12.5의 최소 통합 골격에 실제 P05-HW 데이터 경로를 연결합니다. 물리 CAN 결과와 vCAN 회귀 결과는 [통합 계약](contract.md)의 HW·SIM 등급으로 따로 남깁니다.

## 시간과 실험표

26–32시간. signal mapping 검토 5–7시간, physical path 계측 8–10시간, 고장 주입 8–10시간, 결과 정리 5시간입니다. DBC 또는 동결한 signal table, CAN bit timing, SOME/IP service·instance·event ID, freshness 정책을 실행 전에 잠급니다.

## 안내 실습

MCU sample에 source boot/session ID와 rolling counter를 붙여 CAN frame으로 보냅니다. gateway는 scale·range·counter gap·session change를 확인하고 VehicleState value와 quality를 발행합니다. client까지 raw frame, decoded value, event payload를 같은 trace ID로 연결합니다.

정상, late frame, duplicate counter, MCU reset, bus-off 뒤 복구, SOME/IP subscriber 재접속을 순서대로 실행합니다. 실제 bus-off는 두 물리 node와 controller error state로 확인합니다.

## 독립 실습

speed와 다른 signal 하나를 추가합니다. 10 Hz와 100 Hz, CAN load 세 단계, subscriber 1개와 여러 개 조합에서 loss·latency·queue depth를 기록합니다. source가 바뀌는 순간 이전 value가 client에 재등장하는지도 검사합니다.

## 전이 과제

rolling counter는 계속 증가하지만 source timestamp가 150 ms씩 늦어지는 입력을 받습니다. counter, freshness, clock uncertainty 중 어떤 판단이 quality를 바꾸는지 결정하고 packet·state 근거로 설명합니다.

## 판정 기준

- CAN raw 값에서 service field까지 scale·단위·invalid 규칙이 추적되고 session 변경 시 counter와 cached value가 함께 초기화됨
- late·duplicate·gap·reset이 서로 다른 audit reason을 냄
- 물리 bus-off 결과에 controller state와 복구 시각이 있음
- client 재접속 중 queue bound와 drop policy가 유지됨
- 부하별 raw latency·loss·queue 자료와 clock uncertainty가 저장됨
- 추가 signal이 기존 speed 회귀 시험을 그대로 통과함

## 데이터 경로 재시험

각 실행의 SIM·HW 등급은 controller 자료 유무로 정합니다. HW 근거가 부족한 실행은 필요한 controller log·packet·client state를 이슈에 적고 다음 장비 일정에서 다시 수집합니다.
