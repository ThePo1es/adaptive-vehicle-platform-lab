# Sprint 5.7 — P00-A 릴리스와 실시간 설계 시험

추적 대상: `OUT-XCUT-G5`, `REQ-RTOS-001`–`REQ-RTOS-006`, `REQ-FALLBACK-001`. `FATAL-G5.7-RELEASE`는 분석 input과 실행 image가 다르거나 raw timing 근거 없이 release한 경우입니다.

## 시간과 기준 자료

24–28시간. P00-A release candidate, Sprint 5.1 task model, 5.2 RTA, 5.5 calibration, 5.6 raw campaign을 동결합니다. 시험용 change set과 fault는 응시자에게 공개하지 않은 별도 hash로 관리합니다.

릴리스 입력·oracle·210분 시험·산출물 계보는 [G5 실행 계약](contract.md) 5.7을 따릅니다.

## 릴리스 준비

새 checkout의 build, flash, smoke, phase sweep, report 생성 명령을 한 순서로 정리합니다. manifest에는 코드 commit, Zephyr revision, SDK/toolchain, board revision/ID, 설정 hash, image hash, active/wall time을 넣습니다.

## 안내 실습

기존 task set에 requirement 변경 하나를 적용하고 analysis→configuration→measurement→fallback evidence를 끝까지 갱신합니다. 오래된 RTA 또는 summary가 남으면 checker가 실패하도록 artifact 관계를 검사합니다.

## 독립 실습

새 host에서 P00-A를 build·flash하고 정상, 큐 포화, deadline overrun, watchdog reset 시험을 실행합니다. README만 본 동료가 같은 결과 형식을 만들 수 있는지 관찰하고 빠진 전제를 고칩니다.

## 전이 과제

90분 practical에서 처음 보는 task-set 변경과 봉인 fault를 받습니다. 분석 가능한 범위, 즉시 계측할 항목, 안전하게 줄일 기능을 설명한 뒤 수정합니다. 마지막 20분에는 trace와 RTA를 근거로 설계 질의에 답합니다.

## 판정 기준

- 새 host에서 문서 순서만으로 build·flash·시험 재현 완료
- task model, RTA, RTOS 설정, 추적 schema가 같은 release identity를 가짐
- 봉인 fault의 첫 잘못된 invariant와 수정 이유를 설명
- deadline miss·큐 포화·watchdog에 정한 대응이 실행
- 검토자가 raw trace에서 주요 summary를 독립 재계산
- 공개 claim마다 artifact와 관찰 범위가 연결됨

## P00-A 판정표

| 확인 항목 | 판정 |
| --- | --- |
| 분석 입력과 실행 image가 다름 | 보류 |
| 원시 추적 기록 없이 요약만 있음 | 보류 |
| 봉인 고장의 첫 불변 조건을 설명하지 못함 | 재응시 |

불일치한 산출물부터 다시 동결합니다. 재응시는 새 변경 묶음과 다른 고장을 사용하며, 기존 실패 기록도 함께 보관합니다.
