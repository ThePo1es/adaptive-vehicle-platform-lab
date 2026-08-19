# Traceability Matrix

92개 요구사항은 설계 배정과 검증 계획을 연결해 `Baselined`로 올렸습니다. 관측·성능·도구·공통 품질 요구사항 6개는 상세 설계가 정해질 때까지 `Draft`로 둡니다. 구현 링크는 실제 code가 생긴 PR에서 채우고, `Verified`에는 전체 commit SHA 또는 CI 실행과 검토자를 기록합니다.

| Requirement | Design / ADR | Implementation | Verification | Result | Reviewer |
| --- | --- | --- | --- | --- | --- |
| REQ-MCU-START-001 | [G4 contract](../gates/g04/contract.md) | Planned | [Sprint 4.1](../gates/g04/sprint-4.1.md) | Not run | — |
| REQ-MCU-TIME-001 | [G4 contract](../gates/g04/contract.md) | Planned | [Sprint 4.2](../gates/g04/sprint-4.2.md) | Not run | — |
| REQ-MCU-IRQ-001 | [G4 contract](../gates/g04/contract.md) | Planned | [Sprint 4.3](../gates/g04/sprint-4.3.md) | Not run | — |
| REQ-MCU-FAULT-001 | [G4 contract](../gates/g04/contract.md) | Planned | [Sprint 4.4](../gates/g04/sprint-4.4.md) | Not run | — |
| REQ-MCU-DRV-001 | [G4 contract](../gates/g04/contract.md) | Planned | [Sprint 4.5](../gates/g04/sprint-4.5.md) | Not run | — |
| REQ-MCU-WDG-001 | [G4 contract](../gates/g04/contract.md) | Planned | [Sprint 4.6](../gates/g04/sprint-4.6.md) | Not run | — |
| REQ-RTOS-001 | [G5 contract](../gates/g05/contract.md) | Planned | [Sprint 5.5](../gates/g05/sprint-5.5.md) | Not run | — |
| REQ-RTOS-002 | [G5 contract](../gates/g05/contract.md) | Planned | [Sprint 5.1](../gates/g05/sprint-5.1.md) | Not run | — |
| REQ-RTOS-003 | [G5 contract](../gates/g05/contract.md) | Planned | [Sprint 5.2](../gates/g05/sprint-5.2.md) | Not run | — |
| REQ-RTOS-004 | [G5 contract](../gates/g05/contract.md) | Planned | [Sprint 5.4](../gates/g05/sprint-5.4.md) | Not run | — |
| REQ-RTOS-005 | [G5 contract](../gates/g05/contract.md) | Planned | [Sprint 5.4](../gates/g05/sprint-5.4.md) | Not run | — |
| REQ-RTOS-006 | [G5 contract](../gates/g05/contract.md) | Planned | [Sprint 5.6](../gates/g05/sprint-5.6.md) | Not run | — |
| REQ-FALLBACK-001 | [G4 contract](../gates/g04/contract.md) / [G5 contract](../gates/g05/contract.md) | Planned | [Sprint 4.6](../gates/g04/sprint-4.6.md) / [Sprint 5.4](../gates/g05/sprint-5.4.md) | Not run | — |
| REQ-CAN-001 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.7](../gates/g06/sprint-6.7.md) | Not run | — |
| REQ-CAN-002 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.1](../gates/g06/sprint-6.1.md) | Not run | — |
| REQ-CAN-003 | [G6 bench contract](../gates/g06/bench-contract.md) | Planned | [Sprint 6.2](../gates/g06/sprint-6.2.md) | Not run | — |
| REQ-CAN-004 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.3](../gates/g06/sprint-6.3.md) | Not run | — |
| REQ-CAN-005 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.1](../gates/g06/sprint-6.1.md) | Not run | — |
| REQ-CAN-006 | [G6 bench contract](../gates/g06/bench-contract.md) | Planned | [Sprint 6.2](../gates/g06/sprint-6.2.md) | Not run | — |
| REQ-CAN-007 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.3](../gates/g06/sprint-6.3.md) | Not run | — |
| REQ-ECU-DIAG-001 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.6](../gates/g06/sprint-6.6.md) | Not run | — |
| REQ-ECU-DIAG-002 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.5](../gates/g06/sprint-6.5.md) | Not run | — |
| REQ-ECU-DIAG-003 | [G6 contract](../gates/g06/contract.md) | Planned | [Sprint 6.7](../gates/g06/sprint-6.7.md) | Not run | — |
| REQ-DTC-001 | [G7 contract](../gates/g07/contract.md) | Planned | [Sprint 7.4](../gates/g07/sprint-7.4.md) | Not run | — |
| REQ-DTC-002 | [G7 contract](../gates/g07/contract.md) | Planned | [Sprint 7.4](../gates/g07/sprint-7.4.md) | Not run | — |
| REQ-CP-OS-001 | [G7 contract](../gates/g07/contract.md) | Planned | [Sprint 7.1](../gates/g07/sprint-7.1.md) | Not run | — |
| REQ-CP-COM-001 | [G7 contract](../gates/g07/contract.md) | Planned | [Sprint 7.2](../gates/g07/sprint-7.2.md) | Not run | — |
| REQ-CP-DIAG-001 | [G7 contract](../gates/g07/contract.md) | Planned | [Sprint 7.3](../gates/g07/sprint-7.3.md) | Not run | — |
| REQ-CP-MEM-001 | [G7 contract](../gates/g07/contract.md) | Planned | [Sprint 7.4](../gates/g07/sprint-7.4.md) | Not run | — |
| REQ-CP-MODE-001 | [G7 contract](../gates/g07/contract.md) | Planned | [Sprint 7.5](../gates/g07/sprint-7.5.md) | Not run | — |
| REQ-CP-SEC-001 | [G7 R25-11 ledger](../gates/g07/source-ledger.md) | Planned | [Sprint 7.5](../gates/g07/sprint-7.5.md) | Not run | — |
| REQ-SI-001 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.2](../gates/g09/sprint-9.2.md) | Not run | — |
| REQ-SI-002 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.3](../gates/g09/sprint-9.3.md) | Not run | — |
| REQ-SI-003 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.3](../gates/g09/sprint-9.3.md) | Not run | — |
| REQ-SI-004 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.2](../gates/g09/sprint-9.2.md) | Not run | — |
| REQ-COM-001 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.6](../gates/g09/sprint-9.6.md) | Not run | — |
| REQ-COM-002 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.7](../gates/g09/sprint-9.7.md) | Not run | — |
| REQ-COM-003 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.7](../gates/g09/sprint-9.7.md) | Not run | — |
| REQ-COM-004 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.6](../gates/g09/sprint-9.6.md) | Not run | — |
| REQ-COM-005 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.10](../gates/g09/sprint-9.10.md) | Not run | — |
| REQ-GW-DIAG-001 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 9.8](../gates/g09/sprint-9.8.md) | Not run | — |
| REQ-GW-DIAG-002 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 9.8](../gates/g09/sprint-9.8.md) | Not run | — |
| REQ-GW-DIAG-003 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 9.8](../gates/g09/sprint-9.8.md) | Not run | — |
| REQ-EXEC-001 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.3](../gates/g10/sprint-10.3.md) | Not run | — |
| REQ-EXEC-002 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 8.1](../gates/g08/sprint-8.1.md) | Not run | — |
| REQ-EXEC-003 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 8.2](../gates/g08/sprint-8.2.md) | Not run | — |
| REQ-EXEC-004 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.9](../gates/g10/sprint-10.9.md) | Not run | — |
| REQ-STATE-001 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.4](../gates/g10/sprint-10.4.md) | Not run | — |
| REQ-STATE-002 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.4](../gates/g10/sprint-10.4.md) | Not run | — |
| REQ-HEALTH-001 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.5](../gates/g10/sprint-10.5.md) | Not run | — |
| REQ-PLAT-001 | [G8 plan](gate-playbook.md) | Planned | [Sprint 8.6](../gates/g08/sprint-8.6.md) | Not run | — |
| REQ-PLAT-002 | [G8 plan](gate-playbook.md) | Planned | [Sprint 8.5](../gates/g08/sprint-8.5.md) | Not run | — |
| REQ-PLAT-003 | [G8 plan](gate-playbook.md) | Planned | [Sprint 8.4](../gates/g08/sprint-8.4.md) | Not run | — |
| REQ-PLAT-004 | [G8 plan](gate-playbook.md) | Planned | [Sprint 8.6](../gates/g08/sprint-8.6.md) | Not run | — |
| REQ-LINUX-RT-001 | [G8 plan](gate-playbook.md) | Planned | [Sprint 8.8](../gates/g08/sprint-8.8.md) | Not run | — |
| REQ-LINUX-RT-002 | [G8 plan](gate-playbook.md) | Planned | [Sprint 8.8](../gates/g08/sprint-8.8.md) | Not run | — |
| REQ-LINUX-RT-003 | [G8 plan](gate-playbook.md) | Planned | [Sprint 8.9](../gates/g08/sprint-8.9.md) | Not run | — |
| REQ-AD-DIAG-001 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.7](../gates/g10/sprint-10.7.md) | Not run | — |
| REQ-AD-DIAG-002 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.7](../gates/g10/sprint-10.7.md) | Not run | — |
| REQ-AD-DIAG-003 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.7](../gates/g10/sprint-10.7.md) | Not run | — |
| REQ-AD-DIAG-004 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.7](../gates/g10/sprint-10.7.md) | Not run | — |
| REQ-IAM-001 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.8](../gates/g10/sprint-10.8.md) | Not run | — |
| REQ-IAM-002 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.8](../gates/g10/sprint-10.8.md) | Not run | — |
| REQ-IAM-003 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.8](../gates/g10/sprint-10.8.md) | Not run | — |
| REQ-IAM-004 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.8](../gates/g10/sprint-10.8.md) | Not run | — |
| REQ-BOOT-001 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.6](../gates/g11/sprint-11.6.md) | Not run | — |
| REQ-BOOT-002 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.6](../gates/g11/sprint-11.6.md) | Not run | — |
| REQ-BOOT-003 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.6](../gates/g11/sprint-11.6.md) | Not run | — |
| REQ-UCM-001 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.2](../gates/g11/sprint-11.2.md) | Not run | — |
| REQ-UCM-002 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.2](../gates/g11/sprint-11.2.md) | Not run | — |
| REQ-UCM-003 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.6](../gates/g11/sprint-11.6.md) | Not run | — |
| REQ-UCM-004 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.4](../gates/g11/sprint-11.4.md) | Not run | — |
| REQ-UCM-005 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.4](../gates/g11/sprint-11.4.md) | Not run | — |
| REQ-UCM-006 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.2](../gates/g11/sprint-11.2.md) | Not run | — |
| REQ-UCM-007 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.2](../gates/g11/sprint-11.2.md) | Not run | — |
| REQ-UCM-008 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.3](../gates/g11/sprint-11.3.md) | Not run | — |
| REQ-UCM-009 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.3](../gates/g11/sprint-11.3.md) | Not run | — |
| REQ-UCM-010 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.4](../gates/g11/sprint-11.4.md) | Not run | — |
| REQ-TIME-001 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.9](../gates/g09/sprint-9.9.md) | Not run | — |
| REQ-TIME-002 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.9](../gates/g09/sprint-9.9.md) | Not run | — |
| REQ-TIME-003 | [P02 design](../projects/02-vehicle-state-service/README.md) | Planned | [Sprint 9.9](../gates/g09/sprint-9.9.md) | Not run | — |
| REQ-ARCH-001 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 12.4](../gates/g12/sprint-12.4.md) | Not run | — |
| REQ-ARCH-002 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 12.4](../gates/g12/sprint-12.4.md) | Not run | — |
| REQ-ARCH-003 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 12.10](../gates/g12/sprint-12.10.md) | Not run | — |
| REQ-ARCH-004 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 12.9](../gates/g12/sprint-12.9.md) | Not run | — |
| REQ-ARCH-005 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 12.2](../gates/g12/sprint-12.2.md) | Not run | — |
| REQ-ARCH-006 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 12.3](../gates/g12/sprint-12.3.md) | Not run | — |
| REQ-SAFE-001 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 11.5](../gates/g11/sprint-11.5.md) | Not run | — |
| REQ-SAFE-002 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 11.5](../gates/g11/sprint-11.5.md) | Not run | — |
| REQ-SEC-001 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 11.1](../gates/g11/sprint-11.1.md) | Not run | — |
| REQ-SEC-002 | [P04 design](../projects/04-secure-update-manager/README.md) | Planned | [Sprint 10.8](../gates/g10/sprint-10.8.md) | Not run | — |
| REQ-OBS-001 | Planned | Planned | Planned | Not run | — |
| REQ-PERF-001 | Planned | Planned | Planned | Not run | — |
| REQ-TOOL-001 | Planned | Planned | Planned | Not run | — |
| REQ-QUAL-001 | Planned | Planned | Planned | Not run | — |
| REQ-QUAL-002 | Planned | Planned | Planned | Not run | — |
| REQ-QUAL-003 | Planned | Planned | Planned | Not run | — |
| REQ-QUAL-004 | [P06 design](../projects/06-heterogeneous-vehicle-platform/README.md) | Planned | [Sprint 12.11](../gates/g12/sprint-12.11.md) | Not run | — |

## Link format

```markdown
| REQ-EXEC-001 | [P03 design](../projects/03-execution-manager/README.md) | Planned | [Sprint 10.3](../gates/g10/sprint-10.3.md) | Not run | — |
```

`Pass`에는 검증한 전체 commit SHA 또는 CI 실행 URL을 붙입니다. 상태별 필수 링크와 결과 형식은 `scripts/check_traceability.py`가 검사하고, Markdown 링크의 실제 대상은 `scripts/check_internal_links.py`가 확인합니다.
