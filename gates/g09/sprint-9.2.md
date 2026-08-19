# Sprint 9.2 — SOME/IP message와 parser

## 시간과 기준 자료

24–30시간. [AUTOSAR Foundation R25-11](https://www.autosar.org/standards/foundation)에서 `SOME/IP Protocol Specification`을 받아 release와 document ID를 기록합니다. [COVESA vsomeip](https://github.com/COVESA/vsomeip)의 pinned tag도 함께 사용합니다. AUTOSAR 문서의 SOME/IP header, serialization, message type, error handling 절을 읽습니다.

## 시작 조건과 corpus

고정된 Service/Method/Event ID와 major interface version을 `interface.md`에 선언합니다. corpus에는 정상 request/response/notification 각 3개, 경계 length, 잘린 header, 잘못된 protocol version, 알 수 없는 message type, 큰 payload를 넣습니다. byte sequence와 expected parse result는 사람이 먼저 작성합니다.

## 안내 실습

SOME/IP 16-byte header를 bounds-checking parser로 읽습니다. Service ID, Method/Event ID, Length, Client ID, Session ID, Protocol Version, Interface Version, Message Type, Return Code를 network byte order에서 변환합니다. Length가 포함하는 범위를 문서 절과 test vector로 고정합니다.

## 독립 실습

Vehicle State의 `GetSnapshot` request/response와 `VehicleSpeedChanged` notification payload를 serialize/deserialize합니다. malformed input은 정확한 offset과 reason으로 거부합니다. parser는 payload allocation 전에 최대 길이를 확인하고 trailing bytes 처리 규칙을 갖습니다.

## 전이 과제

vsomeip 두 process가 만든 packet을 parser corpus로 가져오고, 직접 만든 정상 message를 test peer가 읽게 합니다. 검토자는 length, interface version, message type 중 하나를 바꾼 packet을 줍니다. parser와 service가 합의한 error path를 보여 줍니다.

## 판정 기준

- 공식 header 정의의 모든 field에 positive/negative test 존재
- truncated input 모든 byte 위치에서 crash와 out-of-bounds 0건
- 최대 payload와 allocation 상한이 contract에 명시됨
- byte vector, decoded field, packet capture가 서로 일치
- libFuzzer 또는 동등한 fuzz run을 30분 이상 수행하고 sanitizer 오류 0건
- vsomeip 정상 traffic과 최소 한 방향 상호 운용

## 힌트

1. C++ struct를 wire buffer에 그대로 cast하지 않습니다.
2. Method ID와 Event ID가 같은 16-bit field를 공유하는 방식을 확인합니다.
3. return code의 의미는 message type과 함께 해석합니다.

## 치명적 실패와 보충

host endian에 따라 결과가 바뀌거나, length 검증 전에 allocation·copy를 하거나, 자체 vector만 통과하고 packet 대조가 없으면 실패입니다. 보충 과제는 header parser만 남겨 정상 3개와 잘린 입력 17개를 다시 검증하는 것입니다.
