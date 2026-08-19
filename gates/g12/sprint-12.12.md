# Sprint 12.12 — 설계 방어와 P06 릴리스

마지막 Sprint는 새 기능보다 P06의 주장, trade-off, 재현 자료를 한 릴리스로 잠그는 작업입니다. [P06 통합 계약](contract.md)의 Gate 종료 조건을 그대로 심사표로 사용합니다.

## 시간과 심사 구성

22–24시간. release candidate와 demo 7시간, change request 4시간, 설계 질의 5시간, 수정·tag·회고 6–8시간입니다. embedded/platform 검토자 한 명과 Sprint 12.11 재현 담당자가 참여합니다.

## 방어 자료

system context, 요구사항 추적, interface pack, timing·resource budget, lifecycle·version 결정, F01–F12 결과, assurance claim, EXT 기록을 15분 안에 찾을 수 있게 index를 만듭니다. 각 표는 release tag와 원본 artifact hash를 가리킵니다.

## 안내 실습

5–10분 demo에서 정상 startup, VehicleState, 진단 읽기, 선택한 고장과 복구를 보여 줍니다. 이어 “왜 이 owner인가”, “20 ms의 근거는 무엇인가”, “clock을 믿을 수 없을 때 어떤 claim이 남는가”, “update 뒤 어떤 상태를 다시 확인하는가”를 실제 자료로 답합니다.

## 독립 실습

검토자가 requirement 하나, interface field 하나, budget allocation 하나를 바꿉니다. 두 시간 안에 영향 graph를 만들고 수정할 component·test·claim과 유지되는 영역을 제시합니다. 선택한 regression 하나를 실행해 결과를 candidate에 반영합니다.

## 전이 과제

공개하지 않은 system fault 또는 설계 질문을 현장에서 받습니다. 90분 동안 관찰 자료를 모아 최초로 달라진 계약 경계를 찾고, 임시 대응과 릴리스 뒤 근본 수정을 나눠 설명합니다.

## 판정 기준

- requirement에서 code·test·result까지 표본 10개가 끊김 없이 추적됨
- demo가 한 release lock으로 정상과 고장 경로를 재생함
- 20 ms와 자원 예산을 raw 자료와 ADR로 방어함
- lifecycle·diagnostic·update owner 질문에 서로 모순 없는 답을 냄
- 변경 요청의 영향과 유지 영역이 regression 결과에 연결됨
- 비공개 문제에서 최초 계약 경계와 추가 관찰을 90분 안에 제시함
- 검토 의견, EXT 기록, SBOM·image·firmware hash가 P06 tag에 고정됨

## 릴리스를 미룰 조건

질문에 설명만 있고 result hash를 찾지 못하거나 변경 요청 뒤 회귀가 비어 있으면 tag 후보를 보존합니다. 해당 주장 한 개로 범위를 축소해 근거와 시험을 다시 연결한 뒤 같은 질문으로 재검토합니다.
