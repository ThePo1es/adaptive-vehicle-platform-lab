# Sprint 12.3 — 데이터·상태·시간·버전 계약

Sprint 12.2 요구사항을 두 node가 구현할 수 있는 interface pack으로 내립니다. 공통 수치와 세 version 사례는 [integration-contract-v1.json](../../fixtures/g12/integration-contract-v1.json)에 고정돼 있습니다.

## 시간과 결과물

24–30시간. data schema와 단위 6시간, 상태·오류 5–7시간, 시간·freshness 5–7시간, version·부분 배포 시험 6–8시간입니다. 결과는 `interfaces/` 아래 machine-readable schema와 사람이 읽는 결정 표로 묶습니다.

## 계약 표

VehicleState에는 value, unit, range, source session, rolling counter, source timestamp, receive timestamp, clock uncertainty, quality, schema version을 둡니다. 진단 결과는 transport 거부, gateway/backend 실패, ECU NRC, 정상 응답을 서로 다른 code family로 유지합니다.

## 안내 실습

CAN signal 하나를 local gateway object와 SOME/IP event로 옮기며 scale, endianness, invalid raw value, update policy를 추적합니다. 새 MCU session이 들어왔을 때 counter와 freshness baseline을 초기화하는 순서를 상태 표로 작성합니다.

세 version 조합을 실행하는 작은 contract test를 만듭니다. service 2·gateway 1·fallback 없음은 `Block activation`, service 2·gateway 2·MCU 1·translation 있음은 `Degraded read-only`를 내야 합니다.

## 독립 실습

speed 외에 quality 또는 diagnostic status 하나를 골라 같은 계약을 만듭니다. schema field 제거, 단위 변경, unknown enum, 오래된 source session, uncertainty 초과를 입력하고 producer·gateway·consumer의 관찰 결과를 비교합니다.

## 전이 과제

Linux 쪽만 새 schema로 배포된 상태를 받습니다. 90분 동안 offer 허용 여부, 읽기·쓰기 권한, translation 위치, audit event, 정상 version으로 돌아가는 절차를 결정합니다.

## 판정 기준

- field마다 type·단위·범위·invalid 값·owner·version 규칙이 있음
- 새 source session 전에는 이전 counter와 값을 이어 쓰지 않음
- uncertainty 초과 시 quality와 latency 판정이 동결된 결과를 냄
- 세 version 사례가 fixture의 결정과 일치함
- 진단의 네 결과군이 wire와 application 결과에서 보존됨
- schema 생성물과 consumer test가 같은 commit에 고정됨
- 부분 배포에서 쓰기 권한과 degraded 동작이 명시됨

## 계약을 다시 펼칠 때

consumer가 모르는 enum을 정상값으로 받거나 version 불일치가 연결 실패 하나로만 보이면 field 하나와 client 하나로 범위를 줄입니다. raw frame부터 API 결과까지 다시 추적하고 다섯 음성 입력을 재시험합니다.
