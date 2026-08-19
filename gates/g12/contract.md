# G12 P06 통합 계약

G12에서는 새 기능을 늘리는 대신 P00–P05 릴리스의 계약을 두 node에서 재생합니다. 기준 구성은 RTOS MCU 한 대, Linux 차량 컴퓨터 한 대, 격리된 CAN/CAN FD와 Ethernet 네트워크입니다. host·simulator 결과와 물리 장비 결과는 같은 표에 합치지 않습니다.

## 시간 합계

12개 Sprint의 집중시간은 288–360시간입니다.

| Sprint | 시간 | Sprint | 시간 |
| --- | ---: | --- | ---: |
| 12.1 | 20–24h | 12.7 | 24–30h |
| 12.2 | 22–28h | 12.8 | 26–34h |
| 12.3 | 24–30h | 12.9 | 26–34h |
| 12.4 | 26–34h | 12.10 | 28–36h |
| 12.5 | 24–30h | 12.11 | 20–24h |
| 12.6 | 26–32h | 12.12 | 22–24h |

## 동결할 릴리스

P00-C, P01, P02, P03, P04-T2 이상, P05-HW의 tag와 전체 commit SHA를 `release-lock.yml`에 기록합니다. 각 구성요소가 내보내는 인터페이스, 저장 상태, toolchain과 image hash도 함께 고정합니다. 필요한 릴리스가 비어 있으면 해당 Sprint는 `Specified`에 머뭅니다.

## 기준 계약

[integration-contract-v1.json](../../fixtures/g12/integration-contract-v1.json)에 20 ms VehicleState 예산, 세 가지 version 조합, 두 lifecycle 순서, 열두 고장을 고정했습니다. 이 수치는 P06 교육용 기준선이며 실제 차량 목표값으로 사용하지 않습니다.

20 ms data path 예산:

| 구간 | 예산 |
| --- | ---: |
| MCU sampling and processing | 3 ms |
| RTOS queue and CAN scheduling | 4 ms |
| CAN transmission and gateway | 5 ms |
| Linux decode and service publish | 4 ms |
| network and client | 2 ms |
| margin | 2 ms |

예산은 합이 맞는지와 실제 owner가 있는지를 먼저 검사합니다. 한 구간의 실측이 예산을 넘으면 다른 구간의 여유를 몰래 옮기지 않고 ADR로 재배정합니다.

## 종단 불변 조건

- 새로운 MCU boot/session ID를 보기 전에는 이전 source의 값과 rolling counter를 이어 쓰지 않는다.
- clock uncertainty가 freshness threshold를 넘으면 one-way latency와 fresh 판정을 내리지 않는다.
- version 조합은 `Compatible`, `Block activation`, `Degraded read-only` 중 동결된 결과를 낸다.
- diagnostic transport 실패, backend 실패, ECU NRC를 서로 다른 결과로 유지한다.
- 단일 lifecycle owner가 restart를 명령하고 나머지 구성요소는 요청·관찰만 한다.
- update health check가 실패하면 알려진 정상 버전과 저장 상태를 함께 복구한다.

## 증거 등급

| 등급 | 환경 | 가능한 주장 |
| --- | --- | --- |
| SIM | host, vcan, 합성 시계·저장소 | 상태와 protocol 흐름, 결정형 oracle |
| HW | 실제 MCU, CAN transceiver, Linux target | controller 상태, 파형, reset, power-cut, target timing |
| EXT | 새 환경의 재현 담당자가 실행 | 문서와 릴리스의 재현성 |

상위 등급은 하위 결과를 지우지 않습니다. 환경마다 manifest와 원본 자료 hash를 따로 둡니다.

## 고장 campaign

F01–F12는 task overrun, watchdog reset, bus-off, CAN flood, malformed UDS, Linux service crash, SOME/IP loss, version mismatch, 변조 update, activation 중 전원 차단, 두 node 동시 고장, clock uncertainty overflow입니다. 각 결과에는 최초 관찰자, containment 경계, 상태, 복구 제한 시간, 관련 regression test를 남깁니다.

## Gate 종료 조건

- requirement → architecture → interface/budget → code → test → result 연결
- 열두 고장의 자동 실행과 비공개 고장 한 건의 독립 진단
- 물리 node에서 필요한 고장과 simulator 고장의 증거 분리
- 새 환경 재현 담당자와 도메인 검토자의 기록
- release tag, image·firmware·SBOM hash, 5–10분 demo

통합 실패가 생기면 최초로 달라진 계약과 책임 경계를 먼저 찾습니다. 전체 system reset으로 증상을 덮은 결과는 Gate 근거에 넣지 않습니다.
