# Architecture Decision Records

중요한 설계 결정은 ADR로 남깁니다. 결정 당시의 맥락과 대안을 보존하는 것이 목적이며, 현재 코드 설명서로 사용하지 않습니다.

## 상태

- `Proposed`: 검토 중
- `Accepted`: 현재 적용
- `Superseded`: 다른 ADR로 대체
- `Rejected`: 검토했지만 채택하지 않음

## 파일명

```text
adr-0001-use-posix-spawn.md
adr-0002-manifest-dependency-dag.md
adr-0003-update-slot-layout.md
```

새 ADR은 [ADR 템플릿](../templates/adr.md)을 복사해 작성합니다.

## 초기 결정 후보

| ADR | Decision | Status |
| --- | --- | --- |
| ADR-0001 | `fork/exec`와 `posix_spawn` 중 기본 실행 방식 | Proposed |
| ADR-0002 | Manifest dependency를 DAG로 제한 | Proposed |
| ADR-0003 | heartbeat transport와 virtual-time test strategy | Proposed |
| ADR-0004 | A/B slot metadata와 transaction journal 저장 방식 | Proposed |
| ADR-0005 | SOME/IP adapter와 domain model 분리 | Proposed |
| ADR-0006 | MCU task/ISR와 Linux process 사이 timing budget 분할 | Proposed |
| ADR-0007 | bus-off·watchdog·process crash의 cross-node state propagation | Proposed |
| ADR-0008 | MCU/Linux version compatibility와 coordinated rollback | Proposed |
| ADR-0009 | simulator와 hardware에서 재사용할 transport/clock contract | Proposed |
| ADR-0010 | Classic-like adapter와 Adaptive domain model의 경계 | Proposed |
