# Projects

프로젝트는 작은 release를 차례로 재사용합니다. 각 release는 독립적으로 build·test할 수 있어야 합니다.

| ID | Project | Gate / release | Primary evidence |
| --- | --- | --- | --- |
| P00 | [MCU/RTOS ECU Node](00-mcu-rtos-ecu/README.md) | G5 P00-A, G6 P00-B, G7 P00-C | RTA, board timing, CAN/UDS, DTC |
| P01 | [Process Supervisor](01-process-supervisor/README.md) | G8 | process tree, crash diagnosis, bounded recovery |
| P02 | [Vehicle State Service](02-vehicle-state-service/README.md) | G9 | SOME/IP-SD, version, reconnect, latency |
| P03 | [Execution Manager](03-execution-manager/README.md) | G10 | manifest, dependency, state, health |
| P04 | [Update Assurance Lab](04-secure-update-manager/README.md) | G11 | crash consistency, authenticity, rollback |
| P05 | [CAN–SOME/IP Vertical Slice](05-can-ethernet-vertical-slice/README.md) | G9 | 첫 MCU–Linux walking skeleton |
| P06 | [Heterogeneous Vehicle Platform](06-heterogeneous-vehicle-platform/README.md) | G12 | end-to-end contract, budget, fault campaign |

P05는 통신 경로 하나를 완성합니다. P06은 P00–P05 release의 통합과 복구에 집중합니다.

## 공통 구조

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

## Release 완료 조건

- 측정 가능한 요구사항과 인수 예산
- 정상·오류·고장 주입 시험
- 원본 자료와 재생성 script
- 새 환경 재현
- 확인한 범위와 의도적으로 뺀 범위
- reviewer 의견과 수정 기록
- requirement → design → code → test → result link

프로젝트 구조를 바꾸면 ADR에 이유와 이관 비용을 남깁니다.
