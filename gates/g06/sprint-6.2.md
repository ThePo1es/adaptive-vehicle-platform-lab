# Sprint 6.2 — 격리된 CAN FD bench와 error confinement

추적 대상: `OUT-XCUT-G6`, `REQ-CAN-003`, `REQ-CAN-006`. `FATAL-G6.2-BENCH`는 실차 송신, 안전 한계 초과, vcan/logic evidence를 analog 근거로 사용한 경우입니다.

## 시간과 기준 자료

28–34시간. [G6 bench contract](bench-contract.md)의 NUCLEO-G474RE 두 대, MCP2562FD, 기록 가능한 error injector, 80 MHz FDCAN clock, 500 kbit/s·2 Mbit/s timing을 사용합니다. controller·transceiver·injector 문서의 absolute maximum, standby, loop delay, common-mode 조건을 확인합니다.

시간 분해와 산출물 계보는 [G6 실행 계약](contract.md) 6.2에서 관리합니다.

## 중단 장치와 계측

실차와 분리된 bench에서만 송신합니다. 전원 차단 스위치, SWD 복구, fault injection 최대 시간을 먼저 확인합니다. controller counter와 packet log는 필수입니다. differential voltage·ringing·reflection 합격은 대역폭이 맞는 oscilloscope와 differential probe가 있을 때만 판정하며, logic analyzer만 있으면 analog 항목은 `Unverified`로 남깁니다.

## 안내 실습

두 node 사이를 짧은 twisted pair로 연결하고 양 끝 termination, common ground, transceiver supply·standby 상태를 점검합니다. Classic CAN baseline을 통과한 뒤 nominal 500 kbit/s, data 2 Mbit/s 같은 versioned 설정으로 FD+BRS frame을 보냅니다. 실제 값은 계산된 timing과 transceiver capability 안에서 결정합니다.

controller 상태, TX/RX error counter, packet timestamp, scope가 있으면 CAN_H/CAN_L differential trace를 같은 시험 ID로 묶습니다. 정상 frame, ACK 부재, 한쪽 listen-only를 구분합니다.

## 독립 실습

nominal 또는 data phase mismatch는 오류 증가와 상호 운용 실패 관찰에 사용합니다. 결정적 bus-off 시험은 정상 ACK 노드를 유지한 채 승인한 injector가 송신 frame의 recessive data bit를 dominant로 바꾸는 CAN-BENCH-03으로 수행합니다. ACK 부재만으로 bus-off를 기대하지 않습니다. ESI는 error-passive 송신 node에서 확인합니다. recovery delay와 횟수 상한을 policy로 고정하고 communication unavailable 상태를 publish합니다.

## 전이 과제

CAN-BENCH-02부터 05까지 순서대로 실행합니다. termination 제거는 topology 민감도 관찰이며 오류 발생 자체를 합격 조건으로 쓰지 않습니다. 전압·온도·error counter가 안전 범위를 벗어나면 즉시 전원을 끄고, 정상 topology에서 CAN-BENCH-01을 다시 통과합니다.

## 판정 기준

- topology·termination·supply·ground·cable length·board ID가 사진과 도면으로 남음
- controller와 transceiver capability가 nominal/data/BRS 설정을 지원
- injector의 bit 위치·횟수와 error 상태·counter가 packet/계측 timeline에 연결됨
- bus-off 뒤 recovery limit·delay와 unavailable 상태가 정책대로 동작
- 정상 복구 후 기준 traffic이 loss 없이 재통과
- analog 근거의 계측기·probe·bandwidth·calibration이 기록되거나 `Unverified` 표시
- vcan, logic-level, analog 결과가 서로 다른 근거 묶음에 저장됨

## 벤치 안전 카드

실차 연결, 과전류, 과열, absolute maximum 근접, SWD 복구 실패가 보이면 즉시 전원을 끄고 고장 주입을 중단합니다. 사진·전원 제한값·마지막 정상 frame을 사고 기록에 남깁니다.

재개 지점은 정상 termination의 Classic CAN입니다. 그 상태에서 전류와 송수신이 안정된 뒤에만 FD와 bitrate mismatch를 한 항목씩 다시 붙입니다.
