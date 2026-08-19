# Development Environment

저장소 기본 조합은 [ADR-0001](adr/0001-mcu-rtos-baseline.md)에 고정했습니다. G0에서는 실제 보유 장비와 host에서 version·revision·SHA를 다시 확인해 release manifest로 옮깁니다. 동급 장비로 바꿀 때는 equivalence test와 새 ADR이 필요합니다.

## 기본 재현 경로

| Area | 기본 선택 | 통과 증거 |
| --- | --- | --- |
| Host | 지원 중인 Ubuntu LTS | clean VM build |
| Language | C17, C++20, Python test/tool | compiler matrix |
| Build | CMake + Ninja + CTest | one-command build/test |
| Host compiler | GCC와 Clang, 정확한 version 고정 | warning-clean logs |
| MCU target | NUCLEO-G474RE, STM32G474RE Cortex-M4F | board ADR, schematic, RM0440, errata |
| RTOS | Zephyr v4.4.0, `nucleo_g474re/stm32g474xx` | west manifest SHA와 config |
| Simulator | Zephyr v4.4.0 `native_sim`과 host-side virtual clock | contract test |
| CAN bench | Cortex-M node 2대, transceiver, termination. 결정적 bus-off 판정에는 기록 가능한 격리형 error injector 추가 | physical bus trace와 injection log |
| Linux target | x86_64 VM/host + AArch64 QEMU `virt`; board는 Industrial Bridge | image hash와 boot log |
| Linux image | Core는 Buildroot, 이후 Yocto 이식 | clean image build, SBOM |
| SOME/IP | COVESA vsomeip | two-node packet trace |
| Debug | GDB, OpenOCD/J-Link, core dump, strace | fault report |
| Measurement | monotonic trace, cycle counter, logic analyzer; CAN analog 판정에는 oscilloscope·differential probe | calibration record |
| CI | GitHub Actions | docs와 code job 분리 |

Zephyr tag, west module commit, SDK, compiler, OpenOCD와 vendor 문서 revision은 G0.2에서 hash를 포함해 잠급니다. v4.4.0은 2026-08-19 기준 지원 중인 stable release이며 이 과정은 G7까지 같은 기준선을 유지합니다.

## 바로 시작할 수 있는 기준 장비 조합

이미 가진 동급 장비가 있으면 그대로 써도 됩니다. 새로 맞출 때의 기준 조합은 아래와 같습니다. 구매 전에는 재고, 전압, connector, transceiver 호환성을 직접 확인합니다.

| 수량 | 장비 | 선택 이유와 확인할 점 |
| ---: | --- | --- |
| 2 | [NUCLEO-G474RE](https://docs.zephyrproject.org/latest/boards/st/nucleo_g474re/doc/index.html) | Cortex-M4F, FDCAN controller, onboard ST-LINK. CAN transceiver는 별도 필요 |
| 2 | MCP2562FD를 사용한 transceiver board | VDD 5 V, VIO 3.3 V, standby pin, common ground, 최대 120 ns propagation delay 확인 |
| 1 | frame ID·bit 위치·횟수를 기록하는 격리형 CAN error injector 또는 별도 검증한 timer/TXD jig | ACK 부재가 아닌 data-bit error로 bus-off를 재현. 없으면 CAN-BENCH-03은 `Unverified` |
| 1 set | twisted pair, 분리 가능한 120Ω 종단 저항 2개 | 양 끝 종단과 무종단·오종단 고장 시험에 사용 |
| 1 | 8-channel 이상 logic analyzer | UART, GPIO marker, interrupt timing 관찰. 측정 한계를 기록 |
| 1 optional | CAN FD bit rate에 맞는 oscilloscope와 differential probe | differential voltage, edge, ringing, termination 관찰. 없으면 analog acceptance는 `Unverified` |
| 1 | current-limited bench supply와 즉시 차단 수단 | termination·bit-rate mismatch 시험의 고장 시간과 전류 제한 |
| 1 | [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/) 4GB 또는 동급 AArch64 Ethernet SBC | Buildroot image, service 배포, MCU–Linux 통합에 사용 |

기본 소프트웨어 경로는 Zephyr와 Buildroot입니다. 다른 RTOS를 쓰거나 Yocto를 core로 대체하면 G0 ADR에 문서 품질, 지원 상태, 재현 경로와 equivalence test를 적습니다. 이 문서는 장비 구매를 대신하지 않으며, G0.2에서 실제 보유·접근 상태를 확인합니다.

## G0 Hardware and Access ADR

| Item | Required field |
| --- | --- |
| MCU board | model, core, RAM/flash, CAN/FDCAN, clock, quantity |
| Probe | SWD/JTAG model과 사용 권한 |
| CAN | transceiver, termination, second node, USB-CAN |
| Measurement | logic analyzer, oscilloscope, differential probe의 availability·bandwidth·calibration |
| Linux node | CPU, RAM, network interfaces, storage |
| RTOS/toolchain | version과 supported target |
| Standards | document, edition/release, access status |
| QNX/commercial tool | license·문서 접근 기간 또는 `Unavailable` |
| Budget | 구매 상한과 대체 경로 |

장비가 늦어지면 simulator에서 contract를 먼저 완성합니다. Hardware-dependent acceptance는 `Unverified`로 두고 Gate 최종 통과 전에 실제 장비에서 실행합니다.

## 도구

| 용도 | 도구 후보 |
| --- | --- |
| Static analysis | compiler warnings, clang-tidy, cppcheck |
| Dynamic analysis | ASan, UBSan, TSan where applicable |
| Fuzz/property | libFuzzer/AFL++, RapidCheck 또는 자체 generator |
| Coverage/mutation | llvm-cov/lcov, Mull 또는 동등 도구 |
| Binary | readelf, objdump, nm, size, linker map |
| CAN | SocketCAN, can-utils, Linux ISO-TP |
| Ethernet | Wireshark, tcpdump, iproute2 |
| Runtime | perf, strace, heaptrack, systemd tools |
| Time sync | chrony/ptp4l where supported, timestamp calibration script |
| Image | Buildroot core, Yocto Industrial Bridge, pinned configuration |

compiler와 도구 version은 각 release에 고정합니다. GCC와 Clang의 optimization flag 지원 범위도 version별로 기록합니다.

## 단계별 도입

### Stage 0 — Host contract tests

- parser, queue, state machine, manifest를 host에서 시험
- sanitizer, fuzz, property, mutation test
- Cortex-M/AArch64 cross compile과 binary inspection
- simulator-only 가정 표시

### Stage 1 — MCU bring-up

- schematic, reference manual, errata 검토
- clock, reset, timer, UART, fault, watchdog
- 실제 clock source와 probe overhead 측정
- synthetic sensor와 defined output 사용

### Stage 2 — Physical CAN bench

- 두 CAN node, 올바른 termination, 승인한 error injector
- bit timing, load, arbitration, error counter
- bit-rate mismatch와 termination 관찰, data-bit error 기반 bus-off 시험
- vcan 결과와 physical 결과 분리

### Stage 3 — Linux platform

- x86_64 host/VM에서 process·network contract 시험
- AArch64 QEMU image build와 service packaging; 실제 board는 별도 결과
- kernel config와 Device Tree 읽기; 작은 module·driver는 Industrial Bridge
- cgroup, capability, seccomp, logging, crash artifact

### Stage 4 — Two Linux nodes

- multicast interface와 route 고정
- SOME/IP/SD, DoIP packet capture
- clock offset·drift·uncertainty 측정
- network loss와 service restart

### Stage 5 — MCU–Linux integration

- physical CAN 또는 명시된 simulator pair
- timestamp, sequence, quality가 포함된 data contract
- task overrun, bus-off, process crash, network loss 전파
- 두 node의 version·startup·update policy

## Build profile

| Profile | 구성 | 사용처 |
| --- | --- | --- |
| Debug | symbols, warnings as errors | 일상 개발 |
| ASan+UBSan | address·undefined sanitizer | host memory/UB 시험 |
| TSan | 별도 실행 | host concurrency 시험 |
| Fuzz | sanitizer + corpus instrumentation | parser·manifest |
| Coverage | instrumentation | test gap 검토 |
| Release | optimized, symbols 별도 보존 | benchmark·demo |
| Size | GCC `-Os` 또는 지원 시 `-Oz`, Clang `-Oz` 후보 | flash/code-size 결정 |
| Target analysis | target triple·CPU·ABI 고정 | IR·assembly·ABI 보고서 |

성능 보고서는 Release build와 target별 metric을 사용합니다. Sanitizer 결과는 correctness evidence에 둡니다.

## QNX 선택 Gate

QNX 실습은 정식 SDP와 문서 접근 권한이 있을 때 진행합니다. 같은 P01 contract를 아래 기능으로 이식합니다.

- `MsgSend/MsgReceive/MsgReply`
- channel, connection, pulse
- synchronous IPC와 thread priority behavior
- resource manager
- procnto, tracing, crash diagnosis

Portability report에는 Linux와 QNX의 API, scheduling, IPC, failure 차이를 target별 evidence로 기록합니다.

## Evidence 보관

- 작은 로그, 비식별화한 packet, 재생성 script를 Git에 둡니다.
- 대용량 원본은 release asset 등에 보관하고 hash와 생성 절차를 남깁니다.
- board, clock, probe, RTOS config, compiler, flags, measurement source를 metadata에 넣습니다.
- 키, 인증서, VIN, 위치 정보, OEM 비공개 자료는 커밋하지 않습니다.
