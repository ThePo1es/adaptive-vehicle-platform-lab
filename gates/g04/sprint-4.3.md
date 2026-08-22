# Sprint 4.3 — NVIC, ISR, 상한이 있는 큐

추적 대상: `OUT-XCUT-G4`, `REQ-MCU-IRQ-001`, `REQ-RTOS-005`. `FATAL-G4.3-IRQ`는 무한 ISR, interrupt context의 blocking, 설명되지 않은 event loss입니다.

## 시간과 기준 자료

22–28시간. Arm exception entry/return·NVIC priority 절, MCU의 implemented priority bits, UART 또는 timer interrupt 절을 읽습니다. CMSIS helper가 실제 register에 쓰는 값도 disassembly와 debugger로 확인합니다.

큐 보존식, ISR 예산, 이전·다음 산출물은 [G4 실행 계약](contract.md) 4.3을 따릅니다.

## 선수 진단

동일한 numeric priority 값이 library API와 NVIC register에서 어떻게 표현되는지 계산합니다. `PRIGROUP`, preemption priority, subpriority를 섞어 설명하면 작은 두-interrupt 실험부터 시작합니다.

## 안내 실습

두 timer interrupt에 다른 우선순위를 주고 GPIO edge로 entry·exit·nesting을 표시합니다. ISR에서는 timestamp와 event만 fixed-capacity SPSC 큐에 넣고, parsing과 logging은 foreground에서 처리합니다. 큐가 찼을 때 newest drop 또는 oldest drop 가운데 한 정책을 고르고 counter 보존식을 둡니다.

memory ordering과 shared state를 최소화한 뒤 interrupt storm을 주입합니다. 최대 ISR 실행 시간, foreground service rate, 큐 high-water mark, drop 수를 같은 monotonic clock으로 기록합니다.

## 독립 실습

UART RX 또는 GPIO edge를 두 번째 source로 연결합니다. priority 설정, clear 순서, edge/level 특성을 reference manual에서 찾아 driver contract에 반영합니다. spurious 또는 재진입 가능 경로를 시험 corpus에 넣습니다.

## 전이 과제

seed patch 세 개에는 priority 역전, 늦은 status clear, 큐 index race가 하나씩 들어 있습니다. 임의 delay로 증상을 가리지 말고 event trace와 최소 재현으로 원인을 특정합니다.

## 판정 기준

- 실제 implemented priority bit 수와 `PRIGROUP` 설정을 register dump로 확인
- ISR에 동적 할당, 무한 대기, blocking log가 없음
- 큐 포화 전후 `produced = consumed + queued + dropped`가 성립
- storm 중 최대 ISR 시간과 drop 정책이 정한 budget 안에 있음
- nested entry 순서가 GPIO trace와 software event log에서 일치
- unknown interrupt가 원인과 횟수를 남기고 정한 시간 안에 끝남

## 간헐 재현 기록

race가 드물게 나타나면 최적화 수준과 phase를 바꾼 실행을 추가합니다. 기록에는 seed, image hash, interrupt 수, 처음 어긋난 큐 식을 남깁니다.

`volatile` 추가나 넓은 전역 interrupt 차단은 원인 설명이 될 수 없습니다. interrupt 입력 하나와 큐 하나에서 보존식을 다시 맞춘 다음 수정 범위를 정합니다.
