# Traceability Matrix

요구사항이 코드와 테스트로 연결될 때 이 표를 갱신합니다. `Planned` 링크를 실제 상대 경로와 테스트 이름으로 교체합니다.

| Requirement | Design / ADR | Implementation | Verification | Result |
| --- | --- | --- | --- | --- |
| REQ-COM-001 | Planned | Planned | Planned | Not run |
| REQ-COM-002 | Planned | Planned | Planned | Not run |
| REQ-COM-003 | Planned | Planned | Planned | Not run |
| REQ-COM-004 | Planned | Planned | Planned | Not run |
| REQ-EXEC-001 | Planned | Planned | Planned | Not run |
| REQ-EXEC-002 | Planned | Planned | Planned | Not run |
| REQ-EXEC-003 | Planned | Planned | Planned | Not run |
| REQ-STATE-001 | Planned | Planned | Planned | Not run |
| REQ-HEALTH-001 | Planned | Planned | Planned | Not run |
| REQ-DIAG-001 | Planned | Planned | Planned | Not run |
| REQ-DIAG-002 | Planned | Planned | Planned | Not run |
| REQ-CAN-001 | Planned | Planned | Planned | Not run |
| REQ-CAN-002 | Planned | Planned | Planned | Not run |
| REQ-UCM-001 | Planned | Planned | Planned | Not run |
| REQ-UCM-002 | Planned | Planned | Planned | Not run |
| REQ-UCM-003 | Planned | Planned | Planned | Not run |
| REQ-UCM-004 | Planned | Planned | Planned | Not run |
| REQ-UCM-005 | Planned | Planned | Planned | Not run |
| REQ-OBS-001 | Planned | Planned | Planned | Not run |
| REQ-PERF-001 | Planned | Planned | Planned | Not run |
| REQ-QUAL-001 | Planned | Planned | Planned | Not run |
| REQ-QUAL-002 | Planned | Planned | Planned | Not run |

## 링크 형식 예시

```markdown
| REQ-EXEC-001 | [ADR-0002](architecture/adr-0002-manifest-dag.md) | [`DependencyGraph`](../projects/03-execution-manager/src/dependency_graph.cpp) | `DependencyGraphTest.RejectsCycle` | Pass @ `abcdef1` |
```

`Result`에는 단순히 Pass를 쓰지 말고 검증한 commit SHA 또는 CI run 링크를 함께 둡니다.

