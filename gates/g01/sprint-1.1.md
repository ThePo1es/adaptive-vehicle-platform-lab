# 실습 1-1 — 정수와 바이트를 안전하게 변환하기

> 소속 챕터: [안전한 C로 데이터와 메모리 다루기](README.md) · 관리 코드: G1.1

## 시간과 자료

18–24시간을 다음처럼 나눕니다.

| 활동 | 계획 시간 |
| --- | ---: |
| 정수 변환·표현 규칙 읽기 | 3–4시간 |
| 안내 디코더 구현 | 4–5시간 |
| 인코더와 속성 시험 | 4–5시간 |
| 경계·오류·mutant 검사 | 3–4시간 |
| 전이 과제와 기록 | 4–6시간 |

[WG14 N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) 3.4, 5.2.4.2.1, 6.2.5, 6.2.6, 6.3.1, 6.5.7, 7.20.1을 읽습니다. 공개 초안과 C17의 차이는 접근 가능한 ISO/IEC 9899:2018 및 사용한 compiler 문서에서 확인해 절 번호를 기록합니다.

## 입력 계약

고정 입력은 [sprint-1.1-v1.h](../../fixtures/g01/sprint-1.1-v1.h), 공통 전제는 [G1 계약](contract.md#실습-1-1-wire-정수-계약)을 사용합니다. `CHAR_BIT == 8`과 exact-width unsigned type 지원을 컴파일할 때 확인합니다.

8바이트 payload를 사용합니다.

- byte 0–1: little-endian unsigned speed, scale 0.01 km/h
- byte 2–3: little-endian signed temperature, scale 0.1 °C
- byte 4 low nibble: rolling counter 0–15
- byte 4 high nibble와 byte 5–7: zero reserved

기준 벡터 `10 27 D7 00 03 00 00 00`은 속도 100.00 km/h, 온도 21.5 °C, counter 3입니다. signed 경계 `0x0000`, `0x7FFF`, `0x8000`, `0xFFFF`와 application 범위 -40.0–215.0 °C를 따로 검사합니다.

```bash
G01_LAB_ID=G1.1 python3 labs/g01_safe_c/run_harness.py
```

## 안내 실습

고정 폭 unsigned 정수, 명시적인 byte 조립, 입력 길이, reserved bit 검사로 디코더를 만듭니다. signed 값은 signed shift나 범위 밖 signed cast 대신 unsigned raw에서 수학적으로 변환합니다. 오류 경로는 출력 구조체를 변경하지 않습니다.

## 독립 실습

인코더를 작성하고 `decode(encode(raw)) == raw`가 유효한 raw 범위에서 성립하는지 속성 시험으로 확인합니다. 공학 단위의 부동소수점 표시와 raw round trip은 별도 계약으로 둡니다.

## 전이 과제

12비트 unsigned 신호와 12비트 signed two's-complement 신호가 byte 경계를 넘는 새 배치를 90분 안에 구현합니다. 평가자가 제공한 byte order, bit numbering, application 범위를 먼저 표로 고정합니다.

## 판정 기준

- golden vector와 min/max vector 통과
- length 0–7, null, reserved bit, out-of-range input 거부
- signed shift·promotion·overflow UB 없음
- 오류 뒤 출력 불변을 속성 시험으로 확인
- 필수 mutant인 길이 선검사 제거, reserved mask 반전, signed 경계 `>=` 오류, byte order 반전을 모두 검출

## 구현 메모

1. byte를 넓은 unsigned type으로 변환한 뒤 shift합니다.
2. signed 신호의 폭을 먼저 분리하고 unsigned raw에서 값을 계산합니다.
3. 부동소수점 표시와 raw 정수 계약을 나눕니다.

## 다시 볼 조건

정렬되지 않은 payload를 typed pointer cast로 읽었거나 오류 뒤 출력 일부가 바뀌었다면 완료 처리를 미룹니다. 16비트 raw 디코더 하나로 범위를 줄여 `memcpy` 방식과 byte 조립 방식을 비교한 뒤 공개 입력 B로 재시험합니다.
