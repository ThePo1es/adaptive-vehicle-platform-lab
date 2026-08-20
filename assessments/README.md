# Frozen Assessment Contracts

시험 문제를 보기 전에 이 문서의 기준과 시험 manifest를 동결합니다. 시험이 끝난 뒤 난이도나 합격선을 바꾸지 않습니다. 채점 오류가 발견되면 기존 기록을 보존하고 새 버전으로 재시험합니다.

## Gate별 고정 기준

모든 관찰 항목은 `통과` 이상이어야 하고, 아래 두 중점 항목은 `강한 통과`를 받아야 합니다. Fatal 열의 요구사항을 깨뜨리거나 해당 Gate의 치명적 실패 조건을 밟으면 총점과 관계없이 재시험합니다.

| Gate | 중점 항목 | Fatal requirement / invariant |
| --- | --- | --- |
| G0 | Reproducibility, Diagnosis | `FATAL-G0-REPRO`: 새 환경 build 불가 또는 결함 원인 오판 |
| G1 | Correctness, Independence | `REQ-C-SER-001`, `REQ-C-MEM-001`, `REQ-C-STOR-001`, `REQ-C-PARSE-001`, `REQ-C-ISR-001`; UB, 오류 뒤 출력·상태 훼손, 실행 모델 과장 |
| G2 | Correctness, Design | `REQ-QUAL-001`, `REQ-QUAL-002`; dangling owner/view, data race, 금지된 동적 할당 |
| G3 | Diagnosis, Measurement | `REQ-TOOL-001`; GCC를 LLVM IR 근거로 설명, target·ABI가 다른 수치 비교 |
| G4 | Diagnosis, Reliability | `REQ-MCU-START-001`, `REQ-MCU-TIME-001`, `REQ-MCU-IRQ-001`, `REQ-MCU-FAULT-001`, `REQ-MCU-DRV-001`, `REQ-MCU-WDG-001`, `REQ-OBS-001`; fault 원인 유실, 무한 ISR, 정의하지 않은 reset 상태 |
| G5 | Measurement, Reliability | `REQ-RTOS-003`, `REQ-RTOS-004`, `REQ-RTOS-005`, `REQ-RTOS-006`; blocking·jitter 누락, queue·stack overflow 미탐지 |
| G6 | Correctness, Diagnosis | `REQ-CAN-002`, `REQ-CAN-003`, `REQ-CAN-004`, `REQ-ECU-DIAG-002`, `REQ-ECU-DIAG-003`; malformed 입력이 application state를 훼손 |
| G7 | Design, Correctness | `REQ-DTC-001`, `REQ-DTC-002`, `REQ-CP-OS-001`, `REQ-CP-COM-001`, `REQ-CP-DIAG-001`, `REQ-CP-MEM-001`, `REQ-CP-MODE-001`, `REQ-CP-SEC-001`; 책임 경계 오배치, corruption 뒤 잘못된 DTC 복구 |
| G8 | Diagnosis, Reproducibility | `REQ-PLAT-001`, `REQ-PLAT-002`, `REQ-PLAT-003`, `REQ-PLAT-004`, `REQ-LINUX-RT-001`, `REQ-LINUX-RT-002`, `REQ-LINUX-RT-003`; 재현 불가능한 image, descendant 잔류, VM timing 과장 |
| G9 | Correctness, Measurement | `REQ-SI-001`, `REQ-SI-002`, `REQ-SI-003`, `REQ-SI-004`, `REQ-COM-002`, `REQ-COM-003`, `REQ-COM-004`, `REQ-COM-005`, `REQ-TIME-001`, `REQ-TIME-002`, `REQ-TIME-003`; generated boundary 우회, clock uncertainty 없는 one-way latency 주장 |
| G10 | Design, Reliability | `REQ-EXEC-001`, `REQ-EXEC-002`, `REQ-EXEC-003`, `REQ-EXEC-004`, `REQ-STATE-001`, `REQ-STATE-002`, `REQ-HEALTH-001`, `REQ-AD-DIAG-001`, `REQ-AD-DIAG-002`, `REQ-AD-DIAG-003`, `REQ-AD-DIAG-004`, `REQ-IAM-001`, `REQ-IAM-002`, `REQ-IAM-003`, `REQ-IAM-004`; 중복 restart owner, 저장된 운행 상태 자동 적용, transport ID를 principal로 사용 |
| G11A | Reliability, Design | `REQ-UCM-001`, `REQ-UCM-002`, `REQ-UCM-003`, `REQ-UCM-004`, `REQ-UCM-005`, `REQ-UCM-006`, `REQ-UCM-007`, `REQ-UCM-008`, `REQ-UCM-009`, `REQ-UCM-010`, `REQ-BOOT-001`, `REQ-BOOT-002`, `REQ-BOOT-003`, `REQ-SEC-001`, `REQ-SEC-002`; health 전 commit, tier를 넘는 보장 표기 |
| G11B | Design, Reliability | `REQ-SAFE-001`, `REQ-SAFE-002`, `REQ-SEC-001`, `REQ-SEC-002`, `REQ-BOOT-001`, `REQ-BOOT-002`, `REQ-BOOT-003`; 가정 없는 safety/security claim |
| G12 | Design, Reproducibility | `REQ-ARCH-001`, `REQ-ARCH-002`, `REQ-ARCH-003`, `REQ-ARCH-004`, `REQ-ARCH-005`, `REQ-ARCH-006`, `REQ-QUAL-004`; 기준선 요구 누락, 제3자 재현 실패 |

## 시험 manifest

검토자는 아래 내용을 채운 private manifest를 만들고 SHA-256을 mastery review에 기록합니다.

| Field | 기록할 값 |
| --- | --- |
| Assessment version | 이 파일의 commit SHA |
| Candidate commit | 시험 대상 전체 40자리 SHA |
| Task IDs | 공개 과제와 비공개 고장 ID |
| Task manifest hash | private manifest의 SHA-256 |
| Fixed inputs | corpus, seed, target, compiler, 장비 |
| Time and tools | 제한 시간, 문서·인터넷·AI 사용 범위 |
| Expected observations | invariant, output, tolerance, reference result |
| Fatal checks | 위 표와 lab pack의 치명적 실패 ID |
| Reviewers | 이름 또는 handle, 관련 경험, 이해관계 |
| Freeze time | ISO 8601 시각과 timezone |

G11B의 `Validated` 판정에는 safety와 security 검토자 두 사람이 필요합니다. G7과 G10의 AUTOSAR 매핑은 해당 플랫폼 경험 또는 선택한 공식 release 문서의 직접 검토 기록이 없으면 `Provisional`입니다.

## 변경 절차

1. 공개 기준 변경은 시험 전에 PR로 검토합니다.
2. private task의 정답·seed·허용 오차를 실행해 확인합니다.
3. manifest hash를 mastery review에 적고 응시자와 검토자가 동결 시각을 확인합니다.
4. 시험 뒤에는 같은 hash로 채점합니다.
5. 문제 결함이 확인되면 `Invalid assessment`로 남기고 새 manifest로 재시험합니다.
