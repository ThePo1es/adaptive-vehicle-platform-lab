# Sprint 12.8 — 시작·종료·동시 고장 순서

[통합 fixture](../../fixtures/g12/integration-contract-v1.json)의 lifecycle 두 사례를 기준으로 P01·P03·G11A의 상태 전이를 한 owner 아래에 연결합니다.

## 시간과 상태 준비

26–34시간. 상태·event 표 6–8시간, 시작과 종료 구현 6–8시간, 동시 고장 runner 8–10시간, 반복 실행과 리뷰 6–8시간입니다. virtual clock 회귀와 실제 target 측정을 모두 준비합니다.

## 안내 실습

`Cold → Starting → Driving-ready → Degraded read-only/Unavailable → Stopping → Off` 상태를 정의합니다. lifecycle coordinator가 상태 결정을 내리고 process supervisor, gateway, service, MCU session tracker는 event와 실행 결과를 보고합니다. 각 transition에 중복 요청 처리와 timeout을 적습니다.

fixture의 정상 시작 event 다섯 개를 순서대로 재생합니다. 이어 MCU reset과 Linux service crash를 같은 virtual timestamp에 넣어 service withdraw부터 새 session 확인, version 재검사, degraded 재개까지 expected order를 확인합니다.

## 독립 실습

두 고장의 순서를 바꾸고 0·10·100 ms 간격을 줍니다. startup 도중 shutdown, recovery 도중 두 번째 crash, event 중복, event 유실을 추가합니다. 모든 run에서 transition ID, decision owner, executor, terminal state를 저장합니다.

## 전이 과제

process supervisor와 P03이 동시에 restart를 요청하는 기록을 받습니다. 90분 안에 최초 중복 owner를 찾아 하나의 실행 권한으로 정리하고, 기존 reporter 역할과 audit trail을 보존합니다.

## 판정 기준

- 상태와 event마다 decision owner·executor·reporter가 명시됨
- 정상 시작이 fixture의 `Driving-ready`에 도달함
- dual fault의 여섯 expected event가 고정 순서로 나타남
- 고장 순서와 간격이 바뀌어도 허용된 terminal state로 수렴함
- 새 MCU session 확인 전 VehicleState가 재공개되지 않음
- 중복·유실 event가 무한 restart나 queue 증가를 만들지 않음
- 실제 target 전이 시간과 virtual clock 판정이 별도 자료로 남음

## 순서가 흔들리면

동일 seed에서 terminal state가 달라지면 dual fault를 단일 MCU reset과 단일 service crash로 분리합니다. event ledger와 owner를 다시 맞추고 두 고장 간격을 100 ms부터 줄여 가며 재시험합니다.
