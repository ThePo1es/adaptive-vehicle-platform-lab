# Sprint 4.5 — Peripheral driver와 DMA 소유권

추적 대상: `OUT-XCUT-G4`, `REQ-MCU-DRV-001`. `FATAL-G4.5-DMA`는 이전 transfer의 completion이 새 request의 buffer나 state를 바꾼 경우입니다.

## 시간과 기준 자료

24–30시간. 기본 실습은 UART RX circular DMA 또는 timer-triggered ADC DMA입니다. 선택 peripheral, DMA/DMAMUX, interrupt, bus clock, errata 절을 같은 silicon revision으로 고정합니다. STM32G474RE에는 data cache가 없으므로 cache maintenance를 흉내 내지 않습니다.

1,000-phase 입력, timeout, 산출물 이동은 [G4 실행 계약](contract.md) 4.5에 고정합니다.

## 설계 메모

buffer 책임 주체, DMA가 읽거나 쓰는 구간, CPU가 접근해도 되는 시점, timeout·cancel 뒤 상태를 간단한 상태도로 그립니다. alignment와 memory accessibility는 linker section과 reference manual로 확인합니다.

## 안내 실습

polling driver를 먼저 만들어 peripheral 자체 설정을 검증한 뒤 DMA 경로를 추가합니다. half/full/idle event의 의미를 분리하고, producer cursor를 읽는 순간 DMA가 움직여도 unread length가 깨지지 않게 합니다. 모든 대기에는 deadline과 명시적인 recovery가 있습니다.

DMA transfer error, peripheral overrun, short transfer, late interrupt를 fault hook으로 주입합니다. disable·flag clear·descriptor 재설정의 순서를 register trace로 확인합니다.

## 독립 실습

처음 구현과 다른 peripheral 또는 TX/RX 반대 방향으로 driver shell을 옮깁니다. 기존 API에서 재사용한 부분과 target-specific contract를 나눠 적고, zero-copy를 선택했다면 buffer lifetime을 test로 고정합니다.

## 전이 과제

alignment, buffer reuse, cancel race를 바꾼 세 fixture를 순서 없이 받습니다. 1,000회 phase sweep과 sequence가 들어간 payload로 corruption 위치를 찾습니다.

## 판정 기준

- polling과 DMA 경로가 같은 기준 payload를 전달
- CPU/DMA 소유권 전환이 diagram, code assertion, test에서 일치
- timeout 뒤 channel과 peripheral이 다음 요청을 받을 수 있는 상태로 복구
- overrun·DMA error·cancel마다 서로 다른 counter와 결과가 남음
- target의 cache 유무와 DMA-accessible memory 조건을 capability 표에 기록
- 1,000회 phase sweep에서 중복·누락·순서 뒤바뀜이 없음

## DMA 결함 격리표

| 남은 현상 | 먼저 실행할 경로 | 다시 붙일 기능 |
| --- | --- | --- |
| 데이터가 달라짐 | 고정 패턴 memory-to-memory | 실제 주변 장치 |
| 완료가 오지 않음 | polling | interrupt와 DMA |
| 취소 뒤 재사용 실패 | channel 하나, 요청 하나 | 동시 요청 |

각 단계에서는 소유권 assertion이 처음 깨지는 시점을 적습니다. 주변 장치와 DMA를 동시에 고치지 않습니다.
