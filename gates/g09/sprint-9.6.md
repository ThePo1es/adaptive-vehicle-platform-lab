# Sprint 9.6 — P02 Vehicle State Service

## 시간과 기준 자료

26–32시간. [P02 범위](../../projects/02-vehicle-state-service/README.md), [vsomeip 저장소](https://github.com/COVESA/vsomeip), 고정한 R25-11 SOME/IP·SD 문서를 사용합니다. vsomeip tag 또는 commit SHA와 빌드 옵션을 릴리스 명세에 남깁니다.

## 시작 조건과 interface

Sprint 9.2의 `VehicleStateService` 계약과 Sprint 9.3 generated Proxy/Skeleton을 그대로 사용합니다. Service/Instance/Method/Event ID, payload layout, SOME/IP major, SD·deployment compatibility는 binding 파일에 둡니다. Service Interface를 바꾸지 않고 transport adapter만 교체할 수 있어야 합니다.

## 안내 실습

generated Proxy와 Skeleton 뒤에 vsomeip adapter를 붙여 두 프로세스에서 method request/response와 이벤트 publish/subscribe를 실행합니다. consumer가 먼저 시작되는 sequence를 기본 테스트로 둡니다. availability callback, subscription 상태, 첫 이벤트의 순서를 이벤트 log와 packet capture로 대조합니다.

## 독립 실습

서비스 내부 입력은 Sprint 8.3 bounded IPC로 받습니다. 이벤트 queue capacity와 drop policy를 설정하고 snapshot은 한 시점의 일관된 상태를 반환합니다. major mismatch는 거부하고 minor 차이는 선언한 compatibility policy로 처리합니다.

## 전이 과제

봉인 입력으로 old consumer, unknown method, out-of-range 상태, sequence wrap 중 하나가 들어옵니다. wire 결과, 서비스 log, consumer-visible 결과를 한 표에 정리하고 contract 테스트를 추가합니다.

## 판정 기준

- 모든 ID와 version이 code/config/test에서 동일한 source를 따름
- generated file 수정 없이 in-memory binding과 SOME/IP binding이 같은 contract suite를 통과
- provider 늦은 시작과 restart 뒤 availability·재구독 시험 통과
- incompatible major가 조용히 연결되지 않음
- 이벤트 queue 상한과 drop counter 보존식이 성립
- snapshot field 간 일관성 규칙과 concurrency 테스트 존재
- 새 Linux node 두 대 또는 격리된 namespace 두 개에서 재현

## 어댑터 경계 점검

1. 서비스 instance와 프로세스 instance를 구분해 이름을 정합니다.
2. 값의 unit·scale·invalid 표현을 payload 밖 문서에만 두지 말고 테스트 data에도 넣습니다.
3. availability callback 안에서 오래 걸리는 작업을 하지 않습니다.

## 기능을 줄여 재시험하기

ID 충돌, 버전 불일치의 묵시적 허용, 무제한 이벤트 큐, 재시작 뒤 중복 구독이 나오면 `GetSnapshot`과 이벤트 하나만 남깁니다. 두 프로세스의 시작·종료·재연결을 다시 통과시킨 뒤 기능을 하나씩 복구합니다.
