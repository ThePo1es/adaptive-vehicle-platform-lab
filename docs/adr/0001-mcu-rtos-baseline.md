# ADR-0001 — G4–G7 MCU/RTOS 기준선

- 상태: 커리큘럼 명세 기준선으로 채택
- 날짜: 2026-08-19
- 적용 범위: G4부터 G7 P00-C까지

## 결정

| 항목 | 고정한 기준 |
| --- | --- |
| 보드 | ST NUCLEO-G474RE. 실제 보드의 revision은 G0에서 기록 |
| MCU | STM32G474RE LQFP64, Arm Cortex-M4F, flash 512 KiB, SRAM 128 KiB |
| Zephyr target | `nucleo_g474re/stm32g474xx` |
| RTOS | Zephyr v4.4.0 release tag |
| SDK | Zephyr SDK 1.0.0. 설치 archive의 SHA-256은 G0에서 기록 |
| Bare-metal 도구 | 같은 SDK의 GNU Arm toolchain. compiler/linker 전체 version과 flag를 기록 |
| Debug | 보드 내장 ST-LINK/V3E와 G0에서 고정한 OpenOCD 또는 STM32CubeProgrammer |
| CAN | MCU 내장 FDCAN과 MCP2562FD. VDD 5 V, VIO 3.3 V, 최대 propagation delay 120 ns 조건 사용 |
| Classic 기준 | AUTOSAR Classic R25-11 |

실물을 확인해야 알 수 있는 보드·silicon revision, transceiver model, probe firmware는 G0.2에서 기록합니다. 이 값과 west manifest의 실제 commit이 채워져야 Lab Pack을 `Runnable`로 올릴 수 있습니다.

## 선택 이유

Zephyr가 이 보드를 관리 대상으로 지원하고, MCU에는 FDCAN이 있으며, 보드에는 debug probe가 달려 있습니다. 부팅·interrupt·RTOS·CAN FD·Classic 개념 실습을 G7까지 한 target에서 이어 갈 수 있습니다. Cortex-M4F에는 data cache가 없으므로 G4.5의 cache 처리는 `Not applicable`로 기록합니다. M7/M33 이식 때는 cache, MPU, TrustZone 계약을 새로 추가합니다.

## 확인한 자료

- [ST NUCLEO-G474RE product page](https://www.st.com/en/evaluation-tools/nucleo-g474re.html)
- [Zephyr NUCLEO-G474RE board documentation](https://docs.zephyrproject.org/4.4.0/boards/st/nucleo_g474re/doc/index.html)
- [Zephyr v4.4.0 release](https://github.com/zephyrproject-rtos/zephyr/releases/tag/v4.4.0)
- [Microchip MCP2562FD product page와 datasheet](https://www.microchip.com/en-us/product/MCP2562FD)
- [AUTOSAR Classic R25-11](https://www.autosar.org/standards/classic-platform/)

## 변경 규칙

대체 보드에는 CAN FD controller, 복구 가능한 debug 경로, timer·fault·watchdog 계측 경로가 필요합니다. 변경 PR은 기존 결과를 보존하고 capability matrix를 추가한 뒤 G4.1–G4.6과 G6.1–G6.3을 새 target에서 다시 실행합니다. 확인하지 못한 항목은 `Unverified`로 남깁니다.
