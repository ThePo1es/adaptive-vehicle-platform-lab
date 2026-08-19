# Sprint 7.1 — AUTOSAR OS와 RTE 책임 읽기

추적 대상: `OUT-XCUT-G7`, `REQ-CP-OS-001`. `FATAL-G7.1-OSRTE`는 로컬 RTOS/API를 AUTOSAR OS/RTE 구현으로 표기하거나 scheduling 책임을 RTE-like adapter에 둔 경우입니다.

## 시간과 기준 자료

22–28시간. [R25-11 자료 장부](source-ledger.md)의 OS, RTE, methodology 절에서 task, ISR, event, resource, runnable, port, sender/receiver 의미를 읽습니다. 입력·수치 판정·시간 분해는 [G7 실행 계약](contract.md) 7.1에 고정했습니다.

## 판정 범위

P00-C는 `Classic concept-aligned prototype`입니다. Zephyr thread를 AUTOSAR OS Task라고 표기하거나 로컬 adapter를 실제 RTE 구현이라고 배포하지 않습니다. 책임 매핑은 공식 문서 검토 전까지 `Provisional`입니다.

## 안내 실습

P00-A task model을 OS task/ISR/event/resource 표로 옮기고, 애플리케이션 runnable과 data access를 별도 표로 만듭니다. static configuration에서 runnable→event→task mapping과 port type을 생성해 로컬 scheduler/adapter에 연결합니다.

RX data, operation invocation, periodic runnable 세 경로의 call trace를 남깁니다. RTE-like adapter는 typed port와 last-valid/quality contract를 제공하고 scheduling policy를 소유하지 않습니다.

## 독립 실습

mode-dependent runnable과 inter-runnable variable 하나를 추가합니다. activation count, reentrancy, exclusive area, data age를 설정 lint와 runtime assertion으로 확인합니다. 직접 작성한 애플리케이션 logic은 생성 파일에 넣지 않습니다.

## 전이 과제

잘못된 task에 runnable을 배정한 config와 event/resource mapping을 뒤튼 config를 비교합니다. 로컬 동작 결과와 R25-11 책임 매핑 오류를 따로 진단하고 generator input에서 수정합니다.

## 판정 기준

- ISR, OS-like task, runnable, event, resource owner가 표에서 구분됨
- typed port contract에 data·unit·range·freshness·error가 있음
- static config와 runtime call trace의 runnable activation이 일치
- 생성 파일 구성이 같은 input에서 결정적으로 재생됨
- Zephyr/로컬 구현과 AUTOSAR 책임 매핑의 주장 수준을 분리
- R25-11 문서 ID·절·접근 상태가 ledger에 기록됨

## 책임 경계 점검표

- thread 생성: OS-like layer
- runnable 호출 시점 결정: RTE-like adapter의 정적 매핑
- driver 접근: BSW-like interface

실행 trace가 이 표를 벗어나면 periodic runnable과 port 하나로 돌아가 다시 확인합니다. 어긋난 책임은 generator input에서 고치고 생성 파일은 손대지 않습니다.
