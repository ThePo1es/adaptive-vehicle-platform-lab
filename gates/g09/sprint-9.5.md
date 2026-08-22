# Sprint 9.5 — SOME/IP Service Discovery 생명주기

## 시간과 기준 자료

24–30시간. [AUTOSAR Foundation R25-11](https://www.autosar.org/standards/foundation)의 `SOME/IP Service Discovery Protocol Specification`에서 entry, option, timer, Offer/Find, SubscribeEventgroup 절을 읽습니다. [vsomeip configuration guide](https://github.com/COVESA/vsomeip/blob/master/documentation/vsomeipConfiguration.md)는 고정한 vsomeip tag의 파일을 사용합니다.

## 시작 조건과 model

provider와 consumer의 SD 상태를 표로 작성합니다. Service/Instance/Major/Minor, eventgroup, multicast address, initial delay 범위, repetition, cyclic offer, TTL, subscription TTL을 config와 `sd-contract.md`에 한 번만 선언합니다. timer 테스트는 virtual clock을 씁니다.

## 안내 실습

provider가 늦게 시작될 때 `FindService → OfferService → SubscribeEventgroup → SubscribeEventgroupAck → event` 흐름을 캡처합니다. 각 패킷의 entry와 option run을 해석하고 로컬 availability callback 시점과 나란히 놓습니다.

## 독립 실습

StopOffer, TTL expiry, consumer restart, provider restart, subscription renewal을 순수 상태 모델로 검증합니다. randomized initial delay는 범위 안에서 seed를 기록합니다. 실제 vsomeip packet 실험은 별도 실행으로 두고, 순수 모델이 증명하는 timer logic과 구현 상호 운용 근거를 구분합니다. 이미 사라진 서비스의 오래된 이벤트는 current data로 사용하지 않습니다.

## 전이 과제

봉인 fixture는 provider 지연, TTL·eventgroup·major version 변경 가운데 하나를 담습니다. packet과 로컬 상태를 함께 보고 unavailable 원인을 90분 안에 찾습니다. 수정 뒤 같은 고장을 자동 재생합니다.

## 판정 기준

- 핵심 SD 상태와 timer transition이 공식 문서 절에 연결됨
- delay와 TTL 테스트가 실제 sleep 없이 결정론적으로 통과
- packet entry/option과 availability/subscription 상태가 한 timeline에 표시됨
- provider restart 뒤 bounded time 안에 재탐색·재구독
- TTL expiry 뒤 stale 이벤트를 current로 전달하지 않음
- 같은 config source에서 vsomeip 설정과 테스트 oracle을 생성하거나 일치 검사

## 상태 추적 메모

1. 서비스 availability와 eventgroup subscription 성공은 별도 상태입니다.
2. TTL 단위와 0 값의 의미를 선택한 릴리스 문서에서 직접 확인합니다.
3. packet이 안 보이면 routing manager와 multicast interface 설정부터 봅니다.

## 재현부터 다시 할 조건

고정된 `sleep`으로 발견 절차를 맞췄거나 Offer만 보고 구독 성공으로 처리했거나 TTL 뒤 값을 계속 내보냈다면 단일 provider/consumer와 가상 시계 모델로 돌아갑니다. 사건 순서를 먼저 맞추고 실제 패킷 경로를 다시 연결합니다.
