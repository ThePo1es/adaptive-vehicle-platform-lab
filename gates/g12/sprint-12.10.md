# Sprint 12.10 — 열두 고장 자동 campaign

[integration-contract-v1.json](../../fixtures/g12/integration-contract-v1.json)의 F01–F12를 한 runner와 결과 schema로 실행합니다. 각 고장은 P06의 같은 release lock을 사용합니다.

## 시간과 실행 예산

28–36시간. adapter와 reset hook 7–9시간, oracle 작성 7–9시간, campaign 실행 8–10시간, triage와 비공개 고장 6–8시간입니다. seed, 반복 횟수, 최대 실행 시간, 중단 뒤 정리 시간을 manifest에 고정합니다.

## 결과 한 건의 모양

fault ID, injection point, trigger 확인, first observer, containment boundary, state sequence, recovery limit, terminal state, raw artifact hash, linked regression test를 필수 field로 둡니다. 주입이 실제로 일어나지 않은 run은 `INJECTION_MISSED`로 분류합니다.

## 안내 실습

F01 task overrun, F03 bus-off, F06 service crash, F10 activation power interruption을 먼저 연결합니다. 각 adapter는 주입 전 probe와 주입 후 observation을 내고 cleanup에서 다음 run의 상태를 초기화합니다. SIM 전용과 HW 필수 고장을 manifest가 구분하게 합니다.

## 독립 실습

F01–F12를 최소 10 seed로 실행합니다. 같은 first observer와 terminal state가 나오는지 비교하고, 차이가 난 run은 timing·event order·남은 상태를 보존합니다. campaign 도중 runner 자체를 종료한 뒤 이어서 실행해 중복·누락도 확인합니다.

## 전이 과제

검토자가 fault catalog에 없는 고장 하나를 고릅니다. 고장 이름만 받은 상태에서 90분 안에 관찰 경계, 주입 확인, 예상 state, cleanup을 설계하고 첫 run을 수행합니다.

## 판정 기준

- F01–F12가 고유 ID와 fixture의 first observer·expected state를 가짐
- 모든 run이 주입 성공 여부와 원본 자료 hash를 기록함
- HW 필수 고장에 실제 controller·reset·power 자료가 있음
- 열 seed에서 terminal state 차이가 설명되거나 결함으로 등록됨
- cleanup 실패가 다음 run을 오염시키면 campaign이 즉시 멈춤
- runner 재시작 뒤 run ID 중복과 누락이 없음
- 비공개 고장이 90분 안에 재현 가능한 regression으로 바뀜

## campaign을 멈출 때

주입 확인 probe가 없거나 cleanup 뒤 baseline smoke가 실패하면 뒤 고장을 이어서 돌리지 않습니다. 오염된 결과를 격리하고 마지막 정상 run부터 고장 하나씩 다시 실행합니다.
