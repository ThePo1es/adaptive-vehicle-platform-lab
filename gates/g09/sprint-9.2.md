# Sprint 9.2 — Service Interface 계약

## 시간과 기준 자료

22–30시간을 잡습니다. R25-11 `Communication Management`와 `Explanation of Adaptive Platform Software Architecture`, COVESA의 [CommonAPI C++ specification](https://github.com/COVESA/capicxx-core-tools/tree/master/docx)을 읽습니다. 시작 전에 AUTOSAR PDF의 document ID, revision, Service Interface 관련 section title을 `standards-ledger.md`에 적습니다. 이 정보가 비어 있으면 과제 상태는 `Specified`에 머뭅니다.

## 시작 조건과 선수 진단

`GetSnapshot`, `VehicleSpeedChanged`, `IgnitionState`를 보고 method, 이벤트, field의 호출 방향과 실패를 도움 없이 적어 봅니다. Service Interface에는 단위·범위·오류 의미를 두고, Service/Instance ID와 IP·port 같은 배포 정보는 별도 문서로 분리합니다.

## 안내 실습

`VehicleState`의 언어 중립 계약을 작성합니다. 각 요소에 이름, 입력·출력 type, 단위, 범위, invalid 표현, 동기·비동기 여부, 오류 집합, major/minor 변경 규칙을 붙입니다. 정상 호출 세 개와 오류 호출 세 개를 transport를 쓰지 않는 golden vector로 먼저 고정합니다.

## 독립 실습

snapshot의 원자성, 이벤트 순서, field getter·setter·notifier 조합을 결정합니다. 서비스가 unavailable일 때 호출이 실패하는 방식, stale data를 반환할 수 있는 조건, client가 재시도해도 되는 operation을 표로 남깁니다. 같은 type을 C++ struct, JSON fixture, 문서 표에서 생성하거나 일치 검사하는 단일 원천도 정합니다.

## 전이 과제

검토자가 `BatteryState` 추가, `VehicleSpeed` 단위 변경, method의 필수 인자 추가 중 하나를 제시합니다. 호환 가능한 변경과 major 증가가 필요한 변경을 판정하고, old/new client·서비스 네 조합의 예상 결과를 계약 시험으로 만듭니다.

## 판정 기준

- 인터페이스 의미와 배포·binding 설정이 다른 파일과 검토 단위를 가짐
- method, 이벤트, field의 호출·갱신·오류 의미가 시험 가능한 문장으로 고정됨
- 모든 수치에 type, 단위, 범위, invalid·stale 표현이 있음
- major/minor 호환 표가 old/new 조합 네 개를 다룸
- transport 없이 실행하는 golden vector가 정상·경계·오류 결과를 고정함
- AUTOSAR와 CommonAPI 용어를 로컬 계약과 섞지 않고 mapping 상태를 표시함
- 새 요소 전이 과제에서 바뀐 계약과 유지되는 계약을 구분함

## 힌트

1. wire ID는 다음 Sprint 이후의 배포·binding 관심사입니다.
2. field에는 계약에 필요한 getter, setter, notifier만 둡니다.

## 재시험 조건

단위나 오류 의미가 코드 작성 뒤에 정해졌거나, IP·port 변경이 Service Interface major 변경으로 처리됐거나, 호환 표 없이 버전만 올렸다면 다시 봅니다. 보강할 때는 `GetSnapshot`과 이벤트 하나만 남기고 여섯 golden vector부터 고정합니다.
