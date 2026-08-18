# Vehicle Platform Competency Map

## Career thesis

```text
Primary
C/C++ → ARM/MCU → RTOS/Linux → CAN/Ethernet → AUTOSAR → Platform Integration

Differentiator
LLVM/Compiler → UB, ABI, code generation, code size, performance

Cross-cutting quality
Security → boot/update, access control, isolation, malformed input, recovery
```

목표는 관심 분야를 많이 나열하는 것이 아니라, **MCU ECU와 Linux vehicle computer를 요구사항부터 통합·복구까지 구현하는 차량 플랫폼 개발자**로 증거를 모으는 것입니다.

## Target roles

| Priority | Role family | Portfolio proof |
| --- | --- | --- |
| 1 | Vehicle platform / middleware SW | C++/Linux/QNX, SOME/IP, diagnostics, lifecycle, update |
| 2 | MCU / ECU / BSW development | C, Cortex-M, RTOS, CAN, UDS, watchdog, bootloader |
| 3 | SW integration | configuration, deployment, interface, traceability, fault recovery |
| Long-term | Component/System Architect | budgets, trade-offs, failure containment, design defense |

“Architect”는 첫 직무명보다 성장 방향으로 둡니다. 먼저 BSW·MCU·플랫폼·미들웨어·통합 개발에서 구현 책임을 경험하고, 이후 component/system architecture로 확장합니다.

## Two compute domains

| Dimension | ECU / MCU | HPC / Domain Controller |
| --- | --- | --- |
| Typical CPU | Cortex-M/R class | Cortex-A/x86/vehicle SoC |
| OS | Bare metal / RTOS | Linux / QNX |
| Main language | C, restricted C++ | Modern C++ |
| Network | CAN/CAN FD/LIN | Ethernet/SOME-IP/DoIP |
| AUTOSAR lens | Classic | Adaptive |
| Core constraint | determinism, interrupt, memory | process, service, distribution |
| Recovery | watchdog, safe state, reset | restart, degraded state, rollback |
| Evidence | jitter, WCET bound, stack | latency distribution, CPU/RSS, recovery |

한쪽을 먼저 깊게 배우되 최종 프로젝트에서는 timing, state, diagnostic, update contract로 둘을 연결합니다.

## Main gap this repository closes

리버싱·취약점·환경 구축 경험만으로는 개발 직무의 다음 질문에 충분히 답하기 어렵습니다.

- 요구사항을 검증 가능한 문장으로 정의했는가?
- interface와 state machine을 설계했는가?
- CPU, memory, timing, network budget을 정하고 측정했는가?
- 장애를 어느 boundary에서 격리하고 어떤 state로 복구하는가?
- code와 test가 requirement까지 추적되는가?
- target board와 distributed node에서 재현했는가?

따라서 모든 프로젝트는 분석 결과가 아니라 **정상 제품 경로 + 고장 경로 + 수치 + 설계 문서**를 완료 조건으로 둡니다.

## Time allocation

장기 평균 기준입니다. 특정 Gate에서는 비율이 달라질 수 있습니다.

| Track | Share | Rule |
| --- | ---: | --- |
| Vehicle embedded/platform implementation | 70% | 메인 시스템을 실제로 전진시킴 |
| LLVM and upstream OSS | 20% | 현재 Gate의 critical code와 연결 |
| Security research/CTF | 10% | 메인 프로젝트 기능을 밀어내지 않음 |

## Evidence map

| Claimed strength | Minimum credible evidence |
| --- | --- |
| Systems C | malformed corpus, sanitizer result, assembly/ABI explanation |
| Real-time | period/execution/jitter/stack/deadline raw data |
| Classic concepts | communication/diagnostic/DTC end-to-end trace |
| Linux platform | lifecycle faults, core/trace analysis, bounded recovery |
| SOME/IP/DoIP | packet capture, reconnection/version policy, latency/drops |
| Adaptive concepts | explicit mapping, state/health/update recovery tests |
| Security | negative corpus, trust boundary, last-known-good invariant |
| Architecture | budgets, ADRs, failure table, traceability, external review |
| LLVM | IR/assembly/code-size/runtime comparison tied to vehicle code |

## Portfolio positioning

나열식 표현보다 다음처럼 하나의 축으로 설명합니다.

> MCU 기반 실시간 ECU부터 Linux/QNX 기반 차량 컴퓨팅 플랫폼까지 구현하며, 차량 통신·진단·업데이트·고장 복구를 통합하는 임베디드 플랫폼 개발자를 목표로 한다. LLVM 기여 경험을 통해 컴파일러 최적화와 ARM 코드 생성까지 분석하고, 보안은 secure boot/update와 격리·접근 제어·복구 정책에 반영한다.

