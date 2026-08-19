# G4 실행 계약

각 Sprint는 이 표의 입력과 판정을 issue에 복사한 뒤 동결합니다. 실제 board·tool revision과 파일 SHA-256이 채워지기 전 상태는 `Specified`입니다.

## 공통 환경

- 기준: [ADR-0001](../../docs/adr/0001-mcu-rtos-baseline.md)
- target: NUCLEO-G474RE / STM32G474RE / Cortex-M4F
- bare-metal compiler·linker·GDB·OpenOCD 전체 version과 flag를 한 manifest에 기록
- build·flash 소요, 장비 대기, 검토자 대기는 아래 active time과 따로 기록

## 시간 배분

| Sprint | Core | Gate 근거 | Stretch | Active 합계 | 별도 wall time |
| --- | ---: | ---: | ---: | ---: | --- |
| 4.1 | 15–18h | 7–8h | 0–2h | 22–28h | 빈 환경 build·flash 3회 |
| 4.2 | 16–20h | 8h | 0–2h | 24–30h | 10,000-edge capture |
| 4.3 | 15–18h | 7–8h | 0–2h | 22–28h | storm run 30분 이하 |
| 4.4 | 18–21h | 8–9h | 0–2h | 26–32h | fault/power-cycle matrix |
| 4.5 | 16–20h | 8h | 0–2h | 24–30h | 1,000-phase run |
| 4.6 | 18–21h | 8–9h | 0–2h | 26–32h | reset matrix·새 환경 재현 |

## 입력, 판정, 계보

| Sprint | 시작 파일·입력 | 기대 결과와 허용 범위 | 산출물 계보 |
| --- | --- | --- | --- |
| 4.1 | 빈 target, `startup.c`, `vectors.c`, `stm32g474.ld`; vendor startup은 읽기 전용 비교본 | vector[0]은 선언 SRAM 범위·8-byte 정렬, vector[1]은 flash의 Thumb 주소; `.data/.bss` pattern 100% 일치; region overflow는 link 실패 | G3 ELF/map 해석 → `board-runtime/boot-v1`; vendor startup object는 배포용 link에서 제거 |
| 4.2 | 4.1 image, 1 kHz timer 시험 입력, wrap 직전 counter vector | 10,000개 edge의 평균 주기 오차 ±1.5% 이내, timestamp 역행 0회, event count 차이 0 | boot-v1에 calibrated timebase 추가 → G5 추적 clock |
| 4.3 | G1 SPSC 큐, 두 timer 입력, rate/capacity/storm seed 표 | `produced = consumed + queued + dropped`; ISR 최대 20 µs, unbounded wait·allocation 0 | G1 큐를 target에 이식 → G5 ISR-to-task 큐 |
| 4.4 | 통제된 UDF/div0/bad-address image, MSP/PSP synthetic frame, 봉인 fault 1개 | debugger와 기록의 PC/LR/xPSR·valid SCB field 일치; bad magic/CRC 채택 0; 재귀 fault 0 | G3 frame 분석 → `.noinit` 기록과 versioned decoder → G5/G7 incident 기록 |
| 4.5 | polling driver, DMA 상태 표, late IRQ/timeout/alignment seed | 1,000 phase run의 duplicate·loss·corruption 0; cancel 뒤 old completion의 상태 write 0; timeout 2 ms 이내 | board runtime에 driver boundary 추가 → G6 CAN driver shell |
| 4.6 | 4.1–4.5 image, health vote 표, 100 ms watchdog window, 상태별 reset matrix | stale/missing vote에서 feed 0; fault 감지부터 reset까지 150 ms 이내; 다음 boot의 reset reason·기록 일치 | `board-runtime-v1`; startup/time/IRQ/fault/watchdog를 P00-A가 그대로 사용 |

## 근거 묶음

ELF·map·disassembly, 원시 edge/interrupt 추적 기록, GDB transcript, reset log, board ID, image SHA-256, 실행 명령 기록이 모두 있어야 G4를 닫습니다. 장비나 clock이 바뀐 run은 기존 결과를 보존한 채 다른 manifest로 다시 시험합니다.

Crash handler는 flash를 쓰지 않고 `.noinit` RAM record만 commit합니다. reset-class retention matrix로 보존 범위를 밝히고, 유효한 record를 flash journal에 옮기는 작업은 다음 boot의 정상 context에서 수행합니다.
