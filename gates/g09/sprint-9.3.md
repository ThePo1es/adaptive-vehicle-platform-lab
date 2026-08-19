# Sprint 9.3 — SOME/IP Service Discovery 생명주기

## 시간과 기준 자료

24–30시간. [AUTOSAR Foundation R25-11](https://www.autosar.org/standards/foundation)의 `SOME/IP Service Discovery Protocol Specification`에서 entry, option, timer, Offer/Find, SubscribeEventgroup 절을 읽습니다. [vsomeip configuration guide](https://github.com/COVESA/vsomeip/blob/master/documentation/vsomeipConfiguration.md)는 고정한 vsomeip tag의 파일을 사용합니다.

## 시작 조건과 model

provider와 consumer의 SD 상태를 표로 작성합니다. Service/Instance/Major/Minor, eventgroup, multicast address, initial delay 범위, repetition, cyclic offer, TTL, subscription TTL을 config와 `sd-contract.md`에 한 번만 선언합니다. timer test는 virtual clock을 씁니다.

## 안내 실습

provider가 늦게 시작되는 경우 `FindService → OfferService → SubscribeEventgroup → SubscribeEventgroupAck → event` 흐름을 capture합니다. 각 packet의 entry와 option run을 해석하고 local availability callback 시점과 나란히 놓습니다.

## 독립 실습

StopOffer, TTL expiry, consumer restart, provider restart, subscription renewal을 상태 머신으로 검증합니다. randomized initial delay는 범위 안에서 seed를 기록합니다. 이미 사라진 service의 오래된 event를 consumer가 current data로 쓰지 않도록 availability와 freshness 정책을 연결합니다.

## 전이 과제

검토자가 provider를 지연시키거나 TTL·eventgroup·major version 하나를 바꿉니다. packet과 local state를 함께 보고 unavailable 원인을 90분 안에 찾습니다. 수정 뒤 동일 fault를 자동 재생합니다.

## 판정 기준

- 핵심 SD state와 timer transition이 공식 문서 절에 연결됨
- delay와 TTL test가 실제 sleep 없이 결정론적으로 통과
- packet entry/option과 availability/subscription state가 한 timeline에 표시됨
- provider restart 뒤 bounded time 안에 재탐색·재구독
- TTL expiry 뒤 stale event를 current로 전달하지 않음
- 같은 config source에서 vsomeip 설정과 test oracle을 생성하거나 일치 검사

## 힌트

1. service availability와 eventgroup subscription 성공은 별도 상태입니다.
2. TTL 단위와 0 값의 의미를 선택한 release 문서에서 직접 확인합니다.
3. packet이 안 보이면 routing manager와 multicast interface 설정부터 봅니다.

## 치명적 실패와 보충

hard-coded sleep으로만 discovery를 통과하거나, Offer만 보고 subscription 성공으로 처리하거나, TTL 뒤 stale 값을 계속 노출하면 실패입니다. 보충 과제는 단일 provider/consumer와 virtual timer model만 다시 구성하는 것입니다.
