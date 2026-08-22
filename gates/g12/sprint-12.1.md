# Sprint 12.1 — P06 범위와 성공 장면 고정

모든 G12 과제는 [P06 통합 계약](contract.md)과 [고정 입력](../../fixtures/g12/integration-contract-v1.json)을 이어서 사용합니다.

## 시간과 시작 조건

20–24시간. P00-C, P01, P02, P03, P04-T2 이상, P05-HW의 tag와 전체 commit SHA를 모으는 데 4–6시간, stakeholder·use case 작업 6시간, system context와 claim boundary 6시간, 검토와 변경 문제 4–6시간을 씁니다.

필수 릴리스가 아직 나오지 않았다면 해당 칸에 owner와 준비 조건을 적습니다. 장비는 RTOS MCU 한 대, Linux target 한 대, 격리된 CAN/CAN FD와 Ethernet, 전원 제어·log 수집 경로를 기준으로 합니다.

## 안내 실습

운전자, 정비 도구, 업데이트 운영자, 개발자, 두 node, 외부 시간원, 전원, 네트워크를 system context에 놓습니다. `Driving-ready`, 진단 읽기, 업데이트 후 복구 세 장면에 대해 시작 조건, 사용자에게 보이는 결과, 실패 시 안전한 상태를 적습니다.

각 claim에는 SIM·HW·EXT 중 필요한 증거 등급을 붙입니다. demo에 보이는 항목과 내부 품질 지표도 분리해 합격 조건을 숫자로 씁니다.

## 독립 실습

`scope.yml`과 `release-lock.yml`을 작성합니다. 전자는 포함 기능, 외부 의존성, 가정, 알려진 제한, 실제 차량으로 확장할 때 필요한 추가 검증을 담습니다. 후자는 tag, commit, interface version, image·firmware·toolchain hash를 고정합니다. system context의 모든 화살표가 어느 릴리스 계약에 닿는지 확인합니다.

## 전이 과제

검토자가 “운행 중 update 준비를 허용하고 activation은 정차 상태에서만 수행”이라는 변경을 줍니다. 두 시간 안에 범위, use case, 상태 owner, 필요한 G11 회귀 시험을 고쳐 영향 목록을 냅니다.

## 판정 기준

- 여섯 선행 릴리스의 tag·전체 SHA·interface version과 context diagram의 actor·두 node·trust boundary가 고정됨
- 세 성공 장면마다 시작 조건·관찰 결과·실패 상태·증거 등급이 정해짐
- 포함 범위와 외부 의존성의 owner가 확인됨
- demo 지표와 내부 timing·recovery 지표가 구분되고 변경 요청이 activation 조건과 회귀 시험까지 전파됨
- claim 문구가 교육용 bench에서 얻은 근거 범위를 유지함

## 범위를 다시 잡는 신호

비어 있는 선행 릴리스는 범위 표에 차단 사유와 담당자를 적습니다. `Driving-ready` 장면의 실제 tag 두 개와 SIM 근거가 모이면 다음 장면의 일정을 다시 잡습니다.
