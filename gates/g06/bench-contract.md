# G6 CAN FD bench contract v1

이 계약은 Sprint 6.2·6.3·6.8에서 같은 배선과 bit timing을 쓰기 위한 기준입니다. 첫 실제 run에서 board·probe·oscillator 정보를 채우고 hash를 남깁니다. 아래 값과 다른 설정은 별도 계약으로 다룹니다.

## Topology

| 항목 | 기준 |
| --- | --- |
| Node A/B | NUCLEO-G474RE 두 대, 각 board·silicon revision 기록. A는 시험 송신자, B는 정상 ACK·관찰 노드 |
| Transceiver | A/B용 MCP2562FD 두 개, VDD 5 V, VIO 3.3 V |
| Error injector C | frame ID와 bit 위치로 data-bit 오류를 반복 주입하고 횟수를 기록하는 격리형 CAN 장비. 승인한 장비·firmware·설정 hash를 기록 |
| Bus | 1 m 이하 twisted pair, 양 끝 120 Ω, 전원 차단 상태에서 CAN_H–CAN_L 약 60 Ω 확인 |
| Ground | 두 logic ground를 연결하고 bench supply current limit 설정 |
| Probe | 각 보드 ST-LINK/V3E. analog 판정에는 교정한 oscilloscope·differential probe 사용 |
| 송신 안전 | 실차와 물리적으로 분리. fault 한 번당 최대 5초 또는 40회 송신 |

## FDCAN clock과 bit timing

FDCAN kernel clock은 80 MHz로 고정합니다. register가 `value - 1` 형식이면 아래 표에는 사람이 읽는 논리값과 raw 값을 함께 기록합니다.

| Phase | Bit rate | Prescaler | TSEG1 | TSEG2 | SJW | Sample point |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Nominal | 500 kbit/s | 10 | 13 | 2 | 2 | 87.5% |
| Data | 2 Mbit/s | 2 | 15 | 4 | 4 | 80.0% |

계산은 `bit rate = f_fdcan / (prescaler × (1 + TSEG1 + TSEG2))`를 사용합니다. boot log와 register dump에서 80 MHz와 timing field를 확인합니다. oscillator tolerance, MCP2562FD 최대 propagation delay 120 ns, cable·probe 부하를 timing margin 보고서에 넣습니다.

## Deterministic scenarios

| ID | Setup and stimulus | Expected observation | Stop/invalid rule |
| --- | --- | --- | --- |
| CAN-BENCH-01 | A→B, Classic 0x123/8 B와 FD+BRS 0x321/64 B를 각 1,000회 | type·length·payload 일치, controller drop 0 | clock/register가 계약과 다르면 run 무효 |
| CAN-BENCH-02 | B는 ACK 가능한 정상 상태, data timing만 1 Mbit/s로 변경 | FD+BRS traffic error 증가, Classic baseline은 별도 보존 | 5초 또는 40회에서 중단 |
| CAN-BENCH-03 | B는 정상 active/ACK 상태. A가 Classic 0x123을 보내는 동안 C가 arbitration 뒤 미리 고른 recessive data bit에 dominant bit를 매 재전송마다 주입 | A의 data-bit error와 TEC 증가, error-active→error-passive→bus-off, communication unavailable을 같은 실행 ID로 기록. 성공 송신은 0회 | bus-off 전이라도 주입 40회 또는 5초에서 중단. C의 bit 위치·횟수 기록이 없으면 실행 무효 |
| CAN-BENCH-04 | B 정상 복구, bus idle 확보 뒤 A manual recovery | A가 error-active로 돌아오고 CAN-BENCH-01 재통과 | 200 ms 안에 회복하지 않으면 실패 기록 |
| CAN-BENCH-05 | 정상 run 뒤 한쪽 120 Ω 제거 | 전압·edge·error counter 변화를 관찰 | 오류 발생 자체를 합격 조건으로 쓰지 않음 |

CAN-BENCH-03의 C는 승인한 fault-injection 장비 또는 별도 검증한 timer/TXD jig만 사용합니다. 정상 CAN controller API로 같은 ID의 충돌 frame을 보내는 방식은 bit 위치와 양쪽 error counter를 고정하기 어려워 이 oracle에 쓰지 않습니다. ACK를 없애는 시험은 ACK-error와 error-passive 동작을 관찰하는 별도 자료일 뿐 bus-off 합격 근거가 될 수 없습니다.

A는 automatic retransmission을 사용하고 B는 frame을 정상 수신할 수 있는 active 상태를 유지합니다. C의 dominant pulse는 arbitration field, ACK slot, error delimiter를 피하고 A의 알려진 recessive data bit에만 둡니다. controller mode, 주입 장비 설정, manual bus-off recovery를 설정과 boot log에 적습니다. ESI 확인 실행은 error-passive A가 보내는 FD frame을 별도로 사용합니다.

## Evidence bundle

- topology 사진, 배선도, 무전원 저항값, supply voltage/current limit
- board·silicon·transceiver marking, C 장비 ID·firmware·주입 설정과 firmware/설정 hash
- clock tree, FDCAN logical/raw timing, controller mode와 error counter 원본
- `candump` 또는 두 번째 tester packet log
- scope가 있으면 CAN_H, CAN_L, differential waveform과 probe·bandwidth·calibration
- scenario별 시작·종료 시각, 결과, invalid-run 사유, 복구 확인

Scope가 없는 실행은 controller와 packet 결과까지 `Provisional`로 판정합니다. C가 주입한 실제 bit 위치를 장비 trace나 logic capture로 확인하지 못한 CAN-BENCH-03은 `Unverified`입니다. CAN-BENCH-01을 다시 통과해야 고장 시험 입력을 다음 회차에 사용할 수 있습니다.
