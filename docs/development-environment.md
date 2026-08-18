# Development Environment

초기에는 host-native test와 MCU simulator로 contract를 빠르게 검증하고, 같은 test를 실제 Cortex-M board와 Linux node에서 다시 실행합니다. hardware timing과 network interface 문제를 애플리케이션 문제와 분리한 뒤 두 노드를 통합합니다.

## 기본 도구

| Area | Choice | Purpose |
| --- | --- | --- |
| Host OS | Supported Ubuntu LTS release | POSIX/Linux baseline and CI parity |
| Language | C17, C++20, Python for test/tools | MCU, platform and automation |
| Build | CMake + Ninja | reproducible builds |
| Test | GoogleTest + CTest | unit/integration orchestration |
| Cross toolchain | GCC/Clang host + ARM GNU/LLVM target tools | Cortex-M/AArch64 build comparison |
| MCU execution | QEMU or native simulator → owned Cortex-M board | fast fault tests, then hardware evidence |
| RTOS | Zephyr or FreeRTOS, selected per Gate ADR | task/ISR/timing experiments |
| Debug | GDB, OpenOCD/J-Link where authorized | register, fault and board debugging |
| Binary analysis | `readelf`, `objdump`, `nm`, `size`, linker map | section, ABI and generated-code evidence |
| Static checks | compiler warnings, clang-tidy, cppcheck | defect candidates |
| Dynamic checks | ASan, UBSan, TSan where applicable | memory/UB/race evidence |
| Coverage | llvm-cov or lcov | test gap evidence |
| Communication | COVESA vsomeip | SOME/IP and SD experiments |
| CAN | SocketCAN + can-utils + vcan | safe local vehicle network simulation |
| Packet analysis | Wireshark + tcpdump | wire-level evidence |
| Runtime analysis | perf, strace, heaptrack | CPU/syscall/memory analysis |
| Timing analysis | monotonic trace, cycle counter where available, optional logic analyzer | release, execution, ISR and end-to-end timing |
| CI | GitHub Actions | clean-environment verification |
| Deployment | native process → systemd → optional container/Yocto | staged complexity |

의존성 버전은 구현 시점의 upstream 문서와 지원 범위를 확인하고, 각 프로젝트의 build 문서에 고정합니다. 전역적으로 “최신 버전”만 적지 않습니다.

선택한 board·RTOS·compiler version은 Gate 시작 ADR에 고정합니다. QNX는 정식 접근 권한과 환경이 있을 때 Linux contract를 이식하는 선택 트랙이며, QNX가 없어도 핵심 학습을 중단하지 않습니다.

## 도입 순서

### Stage 0 — Host-native low-level tests

- C/C++ parser, queue, state machine을 host에서 sanitizer/fuzz test
- Cortex-M cross compile과 linker map/assembly 생성
- simulator에서 startup, interrupt, RTOS task contract 확인
- hardware-only 가정은 `Unverified`로 표시

### Stage 1 — MCU board

- 본인 소유 또는 허가된 Cortex-M 개발 보드
- timer/UART/CAN loopback과 fault handler
- RTOS timing, stack high-water mark, watchdog reset 측정
- 실제 actuator 없이 synthetic sensor/output 사용

### Stage 2 — Local Linux native

- 한 Ubuntu 호스트
- loopback 또는 명시적 network interface
- vcan과 합성 데이터
- Debug + sanitizer build

### Stage 3 — Two Linux nodes

- 노트북과 Raspberry Pi 또는 두 Linux VM
- multicast route/interface 명시
- clock 차이와 packet loss 관찰
- Release build 성능 측정

### Stage 4 — Deployment control

- systemd 또는 자체 Execution Manager
- config/Manifest 설치 경로
- 로그 rotation과 crash artifacts
- clean-machine setup script

### Stage 5 — MCU–Linux integration

- physical MCU board + Raspberry Pi/laptop 또는 equivalent simulator pair
- CAN/CAN FD, ISO-TP/UDS, SOME/IP/DoIP contract tests
- timestamp/sequence/quality로 end-to-end freshness 측정
- task overrun, bus-off, process crash, network loss의 state propagation 검증

### Stage 6 — Optional container/Yocto/QNX

- native 결과와 동일한 contract test 재사용
- host network/bridge/multicast 차이 기록
- 이미지 생성과 runtime behavior를 분리해 디버깅

## 빌드 프로필 권장안

| Profile | Compiler flags / tools | Use |
| --- | --- | --- |
| Debug | warnings as errors, symbols | daily development |
| ASan+UBSan | address + undefined behavior sanitizer | memory and UB tests |
| TSan | thread sanitizer, separate run | concurrency-focused tests |
| Coverage | instrumentation, no performance claims | test gap review |
| Release | optimized, symbols retained separately | benchmark and demo |
| Size | `-Os`/`-Oz` candidate plus map/section diff | flash/code-size decision |
| Target analysis | Cortex-M/AArch64 assembly and LLVM IR | ABI/codegen evidence |

서로 다른 sanitizer를 무리하게 한 실행에 모두 결합하지 않습니다. 성능 수치는 sanitizer build가 아닌 명시된 Release 조건에서 측정합니다.

## 증거 보관

- 작은 텍스트 로그와 비식별화한 캡처만 Git에 포함합니다.
- raw data에서 보고서를 다시 만드는 script를 함께 둡니다.
- 대용량 원본은 release asset 또는 별도 보관소를 사용할 수 있지만, README에 hash와 생성 절차를 남깁니다.
- 실제 키·인증서·VIN·위치·OEM 비공개 데이터는 크기와 무관하게 커밋하지 않습니다.
- board model, clock, probe, RTOS config, compiler, optimization과 measurement clock source를 raw data metadata에 기록합니다.
- simulator 결과와 hardware 결과를 같은 표의 숫자로 섞지 않고 각각 표시합니다.
