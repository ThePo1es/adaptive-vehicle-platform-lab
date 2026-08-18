# Sprint 1.1 — 정수와 직렬화

## 시간과 자료

24–30시간. [WG14 N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) 3.4, 6.2.5, 6.2.6, 6.3.1, 6.5.7, 7.20.1을 읽습니다. C17 차이는 접근 가능한 ISO/IEC 9899:2018과 compiler 문서로 확인합니다.

## 입력 계약

8-byte payload를 사용합니다.

- byte 0–1: little-endian unsigned speed, scale 0.01 km/h
- byte 2–3: little-endian signed temperature, scale 0.1 °C
- byte 4 low nibble: rolling counter 0–15
- byte 4 high nibble와 byte 5–7: zero reserved

Golden vector `10 27 D7 00 03 00 00 00`은 speed 100.00 km/h, temperature 21.5 °C, counter 3입니다.

## 안내 실습

고정 폭 정수, explicit byte assembly, input length, reserved-bit 검사로 decoder를 만듭니다. Error path는 output을 변경하지 않습니다.

## 독립 실습

Encoder를 작성하고 `decode(encode(x)) == x`가 유효 범위에서 성립하는지 property test로 확인합니다.

## 전이 과제

12-bit unsigned signal과 12-bit signed two's-complement signal이 byte 경계를 넘는 새 layout을 90분 안에 구현합니다.

## 판정 기준

- golden vector와 min/max vector 통과
- length 0–7, null, reserved bit, out-of-range input 거부
- signed shift·promotion·overflow UB 없음
- output unchanged invariant를 property test로 확인

## 힌트

1. byte를 넓은 unsigned type으로 변환한 뒤 shift합니다.
2. signed 값의 width를 먼저 분리하고 sign extension을 정의합니다.
3. floating output과 raw integer contract를 나눕니다.

## 치명적 실패와 보충

Typed pointer cast로 unaligned payload를 읽거나, 오류 뒤 일부 output이 갱신되면 실패입니다. 보충 과제는 16-bit byte-aligned decoder를 `memcpy`와 explicit assembly 두 방식으로 구현해 비교하는 것입니다.

