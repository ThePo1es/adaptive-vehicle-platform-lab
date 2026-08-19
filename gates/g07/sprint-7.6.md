# Sprint 7.6 — P00-C 생성, 세 slice, 설계 방어

추적 대상: `OUT-XCUT-G7`, `REQ-CP-OS-001`–`REQ-CP-SEC-001`. `FATAL-G7.6-RELEASE`는 생성 파일 수동 변경, 검토 없는 적합성 주장, G4–G6 fatal regression입니다.

## 시간과 기준 자료

22–28시간. [R25-11 자료 장부](source-ledger.md), 책임 표, P00-B 릴리스, 세 vertical slice의 기준 시험 입력을 동결합니다. 깨끗한 환경의 생성·195분 시험·릴리스 근거 묶음은 [G7 실행 계약](contract.md) 7.6을 따릅니다.

## 생성 대상

한 schema에서 runnable/event/port, CAN/PDU/signal route, diagnostic route, event/DTC, mode rule을 생성합니다. 생성 결과에는 직접 작성한 애플리케이션 logic과 secret을 넣지 않습니다. 같은 canonical input은 byte 단위로 같은 결과를 만들어야 합니다.

## 안내 실습

RX frame→RTE-like port, UDS read→provider, event→DTC journal 세 slice를 새 build directory에서 생성한 뒤 재생합니다. packet/call/상태 추적 기록을 책임 표와 대조하고, G4 watchdog·G5 timing·G6 protocol regression을 함께 실행합니다.

## 독립 실습

빈 build directory와 새 host에서 P00-C를 생성·build·flash합니다. E2E/SecOC 보장 표, 자료 접근 장부, 로컬-to-AUTOSAR mapping을 검토자에게 넘깁니다. 문서 절을 직접 확인하지 못한 mapping은 `Provisional`로 남깁니다.

## 전이 과제

195분 시험에서 처음 보는 configuration 변경과 봉인 책임 경계 고장을 받습니다. generator input, 생성 결과, 직접 작성한 adapter 가운데 처음 잘못된 경계를 찾고 세 slice regression을 다시 돌립니다. 마지막에는 packet과 상태 추적 기록으로 설계를 설명합니다.

## 판정 기준

- canonical config에서 생성 결과 hash가 반복 build마다 같음
- 세 slice가 각자의 packet/call/상태 oracle을 통과
- 생성 파일 직접 수정이 검사에서 0건
- G4–G6 safety·timing·protocol regression이 모두 통과
- E2E/SecOC 보장과 key/freshness 가정이 주장 표에 있음
- R25-11 mapping 검토자와 확인한 절 또는 `Provisional` 사유가 기록됨
- 새 host 재현, 봉인 고장, 구술 검토 결과가 릴리스 근거 묶음에 있음

## P00-C를 넘길 때 묶을 자료

생성 입력·결과 hash, 세 slice 추적 기록, 책임 매핑 검토, G4–G6 regression, 구술 검토표를 한 manifest에 묶습니다. 로컬 adapter를 AUTOSAR 구현으로 소개했거나 생성 파일을 손으로 고친 실행은 태그 후보에서 제외합니다.

빠진 자료가 있으면 관련 slice만 새 build directory에서 다시 생성하고 다른 봉인 고장으로 확인합니다. 기존 실패 manifest는 삭제하지 않습니다.
