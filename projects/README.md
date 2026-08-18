# Projects

프로젝트는 앞 단계의 결과물을 재사용하며, 각 프로젝트가 독립적으로 빌드·테스트될 수 있도록 유지합니다. P00에서 MCU의 시간·메모리 제약을 먼저 증명하고, P01–P05에서 Linux/Adaptive-style 플랫폼을 만든 뒤, P06에서 두 영역의 contract와 failure propagation을 통합합니다.

| ID | Project | Primary proof | Depends on |
| --- | --- | --- | --- |
| P00 | [MCU/RTOS ECU Node](00-mcu-rtos-ecu/README.md) | deadline, jitter, stack, CAN/UDS, watchdog, boot | G1–G5 foundations |
| P01 | [Process Supervisor](01-process-supervisor/README.md) | lifecycle and bounded recovery | G7 Linux foundation |
| P02 | [Vehicle State Service](02-vehicle-state-service/README.md) | discovery, event, reconnection | Network fundamentals |
| P03 | [Execution Manager](03-execution-manager/README.md) | manifest, dependency, state, health | P01 |
| P04 | [Secure Update Manager](04-secure-update-manager/README.md) | verification, activation, rollback | P01/P03 lifecycle hooks |
| P05 | [Secure Adaptive Gateway](05-secure-adaptive-gateway/README.md) | integrated platform behavior | P01–P04 + CAN/diagnostics |
| P06 | [Mixed-Criticality Vehicle Platform](06-mixed-criticality-platform/README.md) | MCU–Linux timing, state, update and recovery contracts | P00–P05 |

각 프로젝트는 정상 데모만이 아니라 요구사항, architecture decision, 자동화된 fault campaign, raw measurement, clean-room reproduction과 mastery review까지 완료해야 통과합니다.

## 공통 디렉터리 권장안

구현을 시작할 때 다음 구조를 사용합니다.

```text
project-name/
├── README.md
├── CMakeLists.txt
├── include/
├── src/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fault/
├── config/
├── scripts/
└── evidence/
    └── README.md
```

프로젝트마다 구조가 달라져야 할 이유가 있으면 ADR에 남깁니다.
