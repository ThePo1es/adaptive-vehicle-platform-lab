# Sprint 12.9 — 두 node 버전과 update 복구

P04 updater를 MCU–Linux release 조합에 적용합니다. version 결정 세 건과 power interruption 고장은 [P06 통합 계약](contract.md)에 고정돼 있습니다.

## 시간과 릴리스 후보

26–34시간. compatibility matrix 5–7시간, activation plan 6–8시간, 중단·health 고장 9–11시간, 원복과 자료 정리 6–8시간입니다. 현재 known-good와 candidate의 firmware, image, manifest, SBOM hash를 각각 잠급니다.

## 안내 실습

service·gateway·MCU major version과 fallback translation 유무로 `Compatible`, `Block activation`, `Degraded read-only`를 계산합니다. activation policy가 두 node의 상태, 차량 조건, package authenticity, storage 여유, rollback counter를 확인하는 순서를 기록합니다.

Linux image만 바뀌는 경우와 MCU firmware까지 바뀌는 경우를 나눠 staging, activation, reboot, version handshake, health check, commit을 실행합니다. lifecycle coordinator가 프로세스·node 재시작 순서를 소유합니다.

## 독립 실습

새 service가 시작되지만 VehicleState freshness가 실패하는 candidate를 만듭니다. health window 전·중·후에 process kill을 넣고, 실제 장비에서는 선택한 write boundary에 power interruption을 넣습니다. known-good version과 persisted schema가 함께 복구되는지 확인합니다.

## 전이 과제

service 2·gateway 2·MCU 1 조합에서 translation module이 시작 뒤 crash합니다. 120분 안에 read-only 유지, service withdraw, 전체 rollback 중 하나를 선택하고 요구사항·상태·시험을 갱신합니다.

## 판정 기준

- 세 version 조합의 결정, activation 전 조건, decision owner가 fixture와 실행 기록에서 일치함
- health check가 data freshness와 lifecycle 상태까지 확인함
- kill 지점마다 known-good·candidate·recovery 상태 중 하나로 수렴함
- 물리 power interruption과 process kill 결과가 구분됨
- rollback 뒤 firmware·image·persisted schema의 호환성이 다시 검사됨
- signature, version, health 실패가 서로 다른 audit reason을 냄

## update를 다시 묶을 조건

slot, MCU version, 저장 schema가 함께 돌아오지 않은 실행은 부분 rollback 결함으로 남깁니다. 상태 차이와 마지막 durable write를 붙여 다음 후보의 재시험 조건으로 사용합니다.
