# P03 — Manifest-driven Execution Manager

Status: Planned

## 문제

프로세스별 실행 조건, 의존성, 상태, 재시작 및 건강 정책을 Manifest로 표현하고, 상태 결정과 프로세스 실행 책임을 분리합니다.

G9에서 read-only DoIP transport와 diagnostic router를 먼저 만듭니다. G10에서는 이 조각을 Diagnostic Manager, 인증 주체 정책, 프로세스 생명주기와 연결합니다. 따라서 G9의 DoIP 결과물도 P03에서 소유합니다.

## Manifest 초안

```yaml
applications:
  - name: vehicle-state-service
    executable: ./bin/vehicle-state-service
    dependencies:
      - persistency-service
    start_states:
      - Driving
    restart_policy:
      mode: on-failure
      max_attempts: 3
      initial_backoff_ms: 500
      max_backoff_ms: 4000
    health:
      heartbeat_period_ms: 500
      deadline_ms: 1500
```

## 구성요소

| Component | Responsibility | Related concept |
| --- | --- | --- |
| Manifest loader | schema validation and immutable model | Application/Execution Manifest |
| Dependency graph | cycle detection and start/stop order | Execution configuration |
| State controller | requested platform/function state decision | State Management |
| Process controller | desired process set, restart decision, P01 action request | Execution Management |
| P01 action adapter | spawn/stop/kill execution and observed exit | local Linux mechanism |
| Health monitor | alive/deadline/logical observation and recovery request | Platform Health Management |
| Diagnostic manager | request routing, provider availability, read-only service policy | Diagnostics |
| Policy engine | authenticated principal authorization and policy audit | IAM/Cryptography boundary |
| Audit logger | state/action/reason record | Log and Trace / audit |

## 범위

### 구현

- YAML schema validation
- DAG dependency resolution와 cycle rejection
- Startup/Driving/Diagnostic/Update/Shutdown 상태
- 상태별 start/stop plan
- heartbeat/deadline supervision
- restart/degraded policy
- last accepted request/config persistency와 `Startup` boot reconciliation
- read-only diagnostic routing과 Unix credential 기반 authorization

### 제외

- AUTOSAR ARXML과 공식 Manifest schema
- `ara::exec`, `ara::per` API
- 전체 Function Group/Platform State 모델
- safety-certified scheduling 및 resource management

## 관련 요구사항

- `REQ-EXEC-001`–`REQ-EXEC-003`
- `REQ-STATE-001`
- `REQ-HEALTH-001`
- `REQ-AD-DIAG-001`–`REQ-AD-DIAG-004`
- `REQ-IAM-001`–`REQ-IAM-004`
- `REQ-OBS-001`

## 마일스톤

- [ ] P03-D0 (G9): namespace 안의 DoIP activation·alive check·DID read와 합성 패킷 근거
- [ ] P03-M1: Manifest schema와 negative tests
- [ ] P03-M2: DAG start/stop plan
- [ ] P03-M3: state controller와 process controller 분리
- [ ] P03-M4: heartbeat/deadline supervision
- [ ] P03-M5: Diagnostics/IAM과 P01/P02 통합
- [ ] P03-M6: `Startup` reconciliation과 재부팅 복구

## 필수 장애 테스트

| Scenario | Expected result |
| --- | --- |
| cyclic dependencies | 실행 전에 명확한 validation error |
| dependency fails to start | dependent application을 시작하지 않음 |
| service crash | 제한된 restart 뒤 degraded 또는 failed 상태 |
| heartbeat stops | deadline 뒤 정책에 따른 recovery action |
| illegal state transition | transition 거부와 audit reason |
| corrupted persisted state | `Startup`에서 안전한 default로 복구하고 오류 기록 |
| stored `Driving` conflicts with boot condition | 저장값을 바로 적용하지 않고 새 transition으로 재판정 |
| spoofed logical address | authenticated principal로 인정하지 않고 policy에서 거부 |
| DoIP request has no authenticated principal | G9-D0에서는 `unauthenticated endpoint`로 기록하고, G10 policy 연결 전까지 실차 접근을 허용하지 않음 |

## 완료 증거

- Manifest schema, 예제, invalid corpus
- DoIP 거부, backend timeout, ECU UDS NRC를 나눈 P03-D0 추적 기록
- dependency/state/health deterministic tests
- 부팅·상태 전환·장애 복구 시퀀스
- EM/SM/PHM 책임 분리 설명
- systemd/P01/P03/PHM/UCM [lifecycle owner 표](../../docs/lifecycle-ownership.md)
- [AUTOSAR mapping](../../docs/autosar-mapping.md) 갱신
- 선택한 AUTOSAR release의 Execution, Service Interface, Service Instance, Machine Manifest 요소 매핑
