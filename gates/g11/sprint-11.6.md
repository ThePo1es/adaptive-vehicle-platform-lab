# Sprint 11.6 — 부팅 신뢰점과 롤백 방지

[G11B 보증 계약](assurance-contract.md)의 T1/T2/T3 정의와 [TRUST-ROOT-001](../../fixtures/g11/assurance-change-v1.json)을 기준 입력으로 삼습니다.

## 시간과 장비

24–32시간. 서명·키 정책 5–7시간, verified boot와 recovery chain 7–9시간, monotonic state와 중단 시험 8–10시간, 근거 정리 4–6시간입니다. T3 후보에는 실제 MCU 또는 Linux target, 전원 차단 수단, 부팅 log 수집 경로, 보호 저장소의 vendor 문서가 필요합니다.

AUTOSAR R25-11 UCM·Cryptography·IAM 문서와 target의 boot ROM, secure boot, OTP/eFuse 또는 TPM 계열 설명서에서 판·절·접근 날짜를 기록합니다. 사용 장비가 제공하지 않는 기능은 T1/T2 설계 가정 표에 남깁니다.

## 안내 실습

package signer, boot verifier, activation policy, rollback counter writer, recovery image의 키와 결정 권한을 그립니다. 정상 image, 서명 변조 image, 이전 version, counter 쓰기 도중 전원 차단을 순서대로 실행합니다. serial log, boot measurement, storage dump, power event 시각을 하나의 run ID로 묶습니다.

중단 위치마다 이전 정상 slot, 새 정상 slot, recovery 상태 중 도달 가능한 상태를 먼저 적습니다. process kill과 물리 전원 차단은 별도 열에서 실행 횟수와 결과를 집계합니다.

## 독립 실습

MCU firmware 또는 Linux boot artifact 하나를 골라 immutable first verifier부터 application health commit까지 trust chain을 완성합니다. 최소 20회의 무작위 power-cut, 이전 signed image 재설치, key ID 불일치, 손상된 monotonic record를 넣습니다. 복구 뒤 version과 protected counter가 서로 어긋나는 조합도 확인합니다.

## 전이 과제

fixture의 `TRUST-ROOT-001`처럼 immutable trust root와 보호 monotonic state를 제거합니다. 기존 claim 가운데 유지되는 것, T2로 낮아지는 것, `Rejected`가 되는 것을 60분 안에 분류하고 recovery test를 다시 고릅니다.

## 판정 기준

- 서명 검증과 설치·활성화 권한의 owner가 각각 표시됨
- 부팅의 첫 검증자, key provisioning, recovery image 갱신 경계가 자료 절과 연결됨
- 이전 signed image와 counter corruption이 자동 시험에 포함됨
- 모든 power-cut 결과가 확정 slot 또는 명시된 recovery 상태로 수렴함
- version, rollback counter, application health의 commit 순서가 state model과 일치함
- T3 claim에는 같은 target에서 얻은 boot·보호 저장소·전원 차단 근거가 모두 붙음
- trust root 제거 사례의 상한이 T2로 계산됨

## 근거를 보강할 조건

serial log만으로 전원 차단 결과를 추정했거나 protected counter의 실제 저장 위치가 비어 있으면 현재 결과를 `Provisional`로 둡니다. T2 범위에서는 signature·journal oracle을 다시 돌리고, T3 재시험은 필요한 장비와 자료가 준비된 뒤 별도 run ID로 시작합니다.
