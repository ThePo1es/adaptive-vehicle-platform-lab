# Projects

프로젝트는 앞 단계의 결과물을 재사용하며, 각 프로젝트가 독립적으로 빌드·테스트될 수 있도록 유지합니다.

| ID | Project | Primary proof | Depends on |
| --- | --- | --- | --- |
| P01 | [Process Supervisor](01-process-supervisor/README.md) | lifecycle and bounded recovery | None |
| P02 | [Vehicle State Service](02-vehicle-state-service/README.md) | discovery, event, reconnection | Network fundamentals |
| P03 | [Execution Manager](03-execution-manager/README.md) | manifest, dependency, state, health | P01 |
| P04 | [Secure Update Manager](04-secure-update-manager/README.md) | verification, activation, rollback | P01/P03 lifecycle hooks |
| P05 | [Secure Adaptive Gateway](05-secure-adaptive-gateway/README.md) | integrated platform behavior | P01–P04 + CAN/diagnostics |

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

