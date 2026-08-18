# Development Environment

초기에는 Ubuntu 네이티브 프로세스로 통신과 lifecycle을 검증합니다. SOME/IP-SD의 multicast와 network interface 문제를 애플리케이션 문제와 분리한 뒤 컨테이너 또는 다른 배포 방식을 도입합니다.

## 기본 도구

| Area | Choice | Purpose |
| --- | --- | --- |
| OS | Ubuntu 22.04 or 24.04 | POSIX/Linux baseline |
| Language | C++20, Python for test/tools | middleware and automation |
| Build | CMake + Ninja | reproducible builds |
| Test | GoogleTest + CTest | unit/integration orchestration |
| Static checks | compiler warnings, clang-tidy, cppcheck | defect candidates |
| Dynamic checks | ASan, UBSan, TSan where applicable | memory/UB/race evidence |
| Coverage | llvm-cov or lcov | test gap evidence |
| Communication | COVESA vsomeip | SOME/IP and SD experiments |
| CAN | SocketCAN + can-utils + vcan | safe local vehicle network simulation |
| Packet analysis | Wireshark + tcpdump | wire-level evidence |
| Runtime analysis | perf, strace, heaptrack | CPU/syscall/memory analysis |
| CI | GitHub Actions | clean-environment verification |
| Deployment | native process → systemd → optional container/Yocto | staged complexity |

의존성 버전은 구현 시점의 upstream 문서와 지원 범위를 확인하고, 각 프로젝트의 build 문서에 고정합니다. 전역적으로 “최신 버전”만 적지 않습니다.

## 도입 순서

### Stage 1 — Local native

- 한 Ubuntu 호스트
- loopback 또는 명시적 network interface
- vcan과 합성 데이터
- Debug + sanitizer build

### Stage 2 — Two nodes

- 노트북과 Raspberry Pi 또는 두 Linux VM
- multicast route/interface 명시
- clock 차이와 packet loss 관찰
- Release build 성능 측정

### Stage 3 — Deployment control

- systemd 또는 자체 Execution Manager
- config/Manifest 설치 경로
- 로그 rotation과 crash artifacts
- clean-machine setup script

### Stage 4 — Optional container/Yocto

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

서로 다른 sanitizer를 무리하게 한 실행에 모두 결합하지 않습니다. 성능 수치는 sanitizer build가 아닌 명시된 Release 조건에서 측정합니다.

## 증거 보관

- 작은 텍스트 로그와 비식별화한 캡처만 Git에 포함합니다.
- raw data에서 보고서를 다시 만드는 script를 함께 둡니다.
- 대용량 원본은 release asset 또는 별도 보관소를 사용할 수 있지만, README에 hash와 생성 절차를 남깁니다.
- 실제 키·인증서·VIN·위치·OEM 비공개 데이터는 크기와 무관하게 커밋하지 않습니다.

