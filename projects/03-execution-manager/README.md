# P03 — Manifest-driven Execution Manager

Status: Planned

## 문제

프로세스별 실행 조건, 의존성, 상태, 재시작 및 건강 정책을 Manifest로 표현하고, 상태 결정과 프로세스 실행 책임을 분리합니다.

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
| Process controller | lifecycle action execution | Execution Management |
| Health monitor | alive/deadline observation and recovery trigger | Platform Health Management |
| Audit logger | state/action/reason record | Log and Trace / audit |

## 범위

### 구현

- YAML schema validation
- DAG dependency resolution와 cycle rejection
- Startup/Driving/Diagnostic/Update/Shutdown 상태
- 상태별 start/stop plan
- heartbeat/deadline supervision
- restart/degraded policy
- last-known state/config persistency

### 제외

- AUTOSAR ARXML과 공식 Manifest schema
- `ara::exec`, `ara::per` API
- 전체 Function Group/Platform State 모델
- safety-certified scheduling 및 resource management

## 관련 요구사항

- `REQ-EXEC-001`–`REQ-EXEC-003`
- `REQ-STATE-001`
- `REQ-HEALTH-001`
- `REQ-OBS-001`

## 마일스톤

- [ ] P03-M1: Manifest schema와 negative tests
- [ ] P03-M2: DAG start/stop plan
- [ ] P03-M3: state controller와 process controller 분리
- [ ] P03-M4: heartbeat/deadline supervision
- [ ] P03-M5: P01/P02 통합 및 재부팅 복구

## 필수 장애 테스트

| Scenario | Expected result |
| --- | --- |
| cyclic dependencies | 실행 전에 명확한 validation error |
| dependency fails to start | dependent application을 시작하지 않음 |
| service crash | 제한된 restart 뒤 degraded 또는 failed 상태 |
| heartbeat stops | deadline 뒤 정책에 따른 recovery action |
| illegal state transition | transition 거부와 audit reason |
| corrupted persisted state | 안전한 default로 복구하고 오류 기록 |

## 완료 증거

- Manifest schema, 예제, invalid corpus
- dependency/state/health deterministic tests
- 부팅·상태 전환·장애 복구 시퀀스
- EM/SM/PHM 책임 분리 설명
- [AUTOSAR mapping](../../docs/autosar-mapping.md) 갱신
- 선택한 AUTOSAR release의 Execution, Service Interface, Service Instance, Machine Manifest 요소 매핑
