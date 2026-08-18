# AUTOSAR Concept Mapping

이 표는 프로젝트 구성요소가 Adaptive AUTOSAR의 어떤 개념을 학습하기 위해 만들어졌는지 설명합니다. 이름이 비슷하다는 이유만으로 API 호환성이나 규격 적합성을 의미하지 않습니다.

| Local component | Related Adaptive concept | Implemented scope | Deliberate difference | Evidence |
| --- | --- | --- | --- | --- |
| `vehicle-state-service` | Communication Management / `ara::com` | service, method, event, discovery, reconnection | vsomeip API 사용, `ara::com` API·generator 미구현 | Planned |
| `execution-manager` | Execution Management | process spawn/stop, dependency order, restart policy | YAML manifest, `ara::exec` 미구현 | Planned |
| `state-manager` | State Management | Startup/Driving/Diagnostic/Update/Shutdown 결정 | Function Group 모델을 단순 enum/YAML로 표현 | Planned |
| `health-monitor` | Platform Health Management | alive/deadline supervision, recovery trigger | supervision 종류와 recovery policy 일부만 구현 | Planned |
| `persistency-service` | Persistency | version/config/journal 저장과 복구 | `ara::per` API, redundancy 정책 미구현 | Planned |
| `diagnostic-gateway` | Diagnostics | DoIP–UDS–ISO-TP read-only routing, policy | 전체 diagnostic conversation·DEM 모델 미구현 | Planned |
| `update-manager` | Update and Configuration Management | 검증, staging, activation, health check, rollback | 공식 package/manifest 모델 대신 자체 최소 형식 | Planned |
| `crypto-adapter` | Cryptography | hash/signature verification, key abstraction | `ara::crypto` API·key slot 모델 미구현 | Planned |
| `audit-service` | Log and Trace / IAM-related auditing | 구조화 이벤트와 상태 변경 추적 | `ara::log`가 아닌 자체 logger 또는 DLT 도구 | Planned |
| `policy-engine` | Identity and Access Management | caller/service/action allow-list | 공식 identity/credential model 미구현 | Planned |

## 매핑 갱신 규칙

각 프로젝트 PR에서 다음을 확인합니다.

1. 관련 Functional Cluster의 책임을 공식 문서에서 다시 확인했는가?
2. 구현한 범위와 의도적으로 생략한 범위가 분리되어 있는가?
3. 비슷한 이름만 차용하고 동작이 다른 부분을 명시했는가?
4. 코드와 자동 테스트 링크가 `Evidence`에 연결되어 있는가?
5. “AUTOSAR compliant”, “complete Adaptive Platform”처럼 검증하지 못한 표현을 쓰지 않았는가?

