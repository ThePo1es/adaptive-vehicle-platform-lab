# Sprint 9.4 — P02 Vehicle State Service

## 시간과 기준 자료

24–30시간. [P02 범위](../../projects/02-vehicle-state-service/README.md), [vsomeip repository](https://github.com/COVESA/vsomeip), 고정한 R25-11 SOME/IP·SD 문서를 사용합니다. vsomeip는 tag 또는 commit SHA와 build option을 release manifest에 남깁니다.

## 시작 조건과 interface

`VehicleStateService`에 `GetSnapshot`, `GetSoftwareVersion`, `VehicleSpeedChanged`, `GearPositionChanged`, `IgnitionState` contract를 작성합니다. ID, major/minor, payload layout, unit, range, invalid value, freshness, sequence wrap, timestamp clock을 표로 고정합니다. field를 구현할 때 getter/setter/notifier 중 실제로 제공하는 조합을 명시합니다.

## 안내 실습

두 process에서 method request/response와 event publish/subscribe를 실행합니다. consumer가 먼저 시작되는 sequence를 기본 test로 둡니다. availability callback, subscription state, 첫 event의 순서를 event log와 pcap으로 대조합니다.

## 독립 실습

service 내부 입력은 Sprint 8.3 bounded IPC로 받습니다. event queue capacity와 drop policy를 설정하고 snapshot은 한 시점의 일관된 state를 반환합니다. major mismatch는 거부하고 minor 차이는 선언한 compatibility policy로 처리합니다.

## 전이 과제

검토자가 old consumer, unknown method, out-of-range state, sequence wrap 중 하나를 투입합니다. wire 결과, service log, consumer-visible 결과를 한 표에 정리하고 contract test를 추가합니다.

## 판정 기준

- 모든 ID와 version이 code/config/test에서 동일한 source를 따름
- provider 늦은 시작과 restart 뒤 availability·재구독 시험 통과
- incompatible major가 조용히 연결되지 않음
- event queue 상한과 drop counter 보존식이 성립
- snapshot field 간 일관성 규칙과 concurrency test 존재
- 새 Linux node 두 대 또는 격리된 namespace 두 개에서 재현

## 힌트

1. service instance와 process instance를 구분해 이름을 정합니다.
2. 값의 unit·scale·invalid 표현을 payload 밖 문서에만 두지 말고 test data에도 넣습니다.
3. availability callback 안에서 오래 걸리는 작업을 하지 않습니다.

## 치명적 실패와 보충

ID 충돌, version mismatch silent acceptance, 무제한 event queue, 재시작 뒤 중복 subscription이 나오면 실패입니다. 보충 과제는 `GetSnapshot`과 단일 event만 남겨 두 process lifecycle을 다시 통과시키는 것입니다.
