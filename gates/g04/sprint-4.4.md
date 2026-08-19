# Sprint 4.4 — Fault frame과 crash 기록

추적 대상: `OUT-XCUT-G4`, `REQ-MCU-FAULT-001`, `REQ-OBS-001`. `FATAL-G4.4-FAULT`는 invalid frame dereference, unbounded fault loop, image identity 없는 오진입니다.

## 시간과 기준 자료

26–32시간. Arm fault handling·exception stack frame·SCB 절과 MCU reset flags, `.noinit` RAM의 reset-class별 보존 범위를 확인합니다. 시험할 fault는 교육용 image와 격리된 보드에서만 발생시킵니다.

fault 시험 입력과 기록 판정, 근거 시간은 [G4 실행 계약](contract.md) 4.4에서 동결합니다.

## 고장 표 만들기

UsageFault, BusFault, MemManage fault의 enable 조건과 escalation 경로를 표로 정리합니다. target에 MPU나 별도 보존 영역이 없으면 그 경로는 `Not applicable`로 표시하고 근거를 붙입니다.

## 안내 실습

fault handler가 MSP/PSP와 EXC_RETURN을 보고 올바른 stacked frame을 고르게 합니다. PC, LR, xPSR, CFSR, HFSR, MMFAR, BFAR, active exception, reset reason을 고정 크기 `.noinit` record에 저장합니다. record는 magic, schema version, length, sequence, CRC와 two-phase commit marker를 갖습니다. fault context에서는 flash를 쓰지 않습니다.

divide-by-zero, undefined instruction, invalid address 같은 통제된 fault를 하나씩 만들고 debugger의 live register와 reboot 뒤 출력된 record를 비교합니다. handler 안의 작업은 정해진 cycle 또는 watchdog window 안에 끝나야 합니다.

## 독립 실습

startup code가 이전 crash record를 읽어 유효성을 검사하고 한 번만 보고한 뒤 소비 상태를 남기게 합니다. 장기 보관이 필요하면 정상 boot context에서 flash journal로 복사합니다. torn write, bad CRC, 오래된 schema, sequence wrap corpus를 만들어 잘못된 record가 정상 진단처럼 보이지 않게 합니다.

## 전이 과제

source가 없는 faulting image를 받아 처음 잘못된 instruction과 호출 경로를 찾습니다. 원시 기록, ELF build ID, symbolization 명령, 판단 근거를 함께 제출합니다.

## 판정 기준

- MSP와 PSP 양쪽 synthetic frame을 올바르게 해석
- debugger register와 persisted record의 필수 필드가 일치
- reset 도중 끊긴 record와 CRC 오류를 유효한 crash로 채택하지 않음
- fault handler가 재귀 fault에 빠지지 않고 정한 reset 경로로 종료
- ELF/image identity 없이 symbolized address를 보고하지 않음
- 처음 보는 fault에서 register→instruction→root cause 설명이 이어짐
- secret, key, 전체 payload를 crash record에 복사하지 않음

## fault handler 복구 순서

기록 저장 중 fault가 겹치면 flash 쓰기와 문자열 출력을 제거하고 `.noinit` RAM에 raw frame만 남깁니다. 이 최소 handler가 연속 세 번 같은 종료 경로를 보이면 build ID, status register, CRC 순으로 필드를 되붙입니다.

재현되지 않은 추정은 별도 메모에 두고 판정 근거에는 넣지 않습니다. 다음 시험자가 raw record와 ELF만으로 같은 instruction을 찾는 시험을 다시 수행할 수 있어야 복구가 끝납니다.
