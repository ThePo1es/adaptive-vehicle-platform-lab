# 실습 1-4 — 깨진 입력에도 안전한 파서 만들기

> - 준비 상태: `Runnable`
> - 시작 커밋: `e048adcb655db789e9a6c10382f55afc9f68bbba`
> - 공개 입력 SHA-256: `4a854226b4d82abf04ceca2d3fb4fbdc744b2f1433b6fae4686fa62f3ed5f350`
> - 실행 기록: [G1.4 실행 명세 v1](../../evidence/runnable/g1.4/run-manifest-v1.json)

> 소속 챕터: [안전한 C로 데이터와 메모리 다루기](README.md) · 관리 코드: G1.4

## 시간과 자료

32–44시간입니다. 상태 머신·CRC 자료 5–6시간, 두 parser와 reference encoder 8–10시간, differential·truncation 검사 6–8시간, fuzz·mutation 6–8시간, TLV 전이와 기록 7–12시간으로 나눕니다. N1570 6.5.6, 6.5.7, 7.20.1과 [libFuzzer](https://llvm.org/docs/LibFuzzer.html) 문서의 Fuzz Target, Corpus, Options를 읽습니다.

## Frame 형식

```text
[0xA5 magic][0x01 version][length 0..16][payload][CRC-8/ATM]
```

CRC는 magic부터 payload 마지막 byte까지 계산합니다. Polynomial `0x07`, init `0x00`, refin/refout false, xorout `0x00`으로 고정하고 ASCII `123456789 → 0xF4`를 먼저 확인합니다. 파서는 `complete`, `need-more`, `rejected`와 소비한 byte 수를 반환합니다. 정확한 재동기화 규칙은 [G1 계약](contract.md#실습-1-4-프레임-파서-계약)을 따릅니다.

고정 입력은 [sprint-1.4-v1.h](../../fixtures/g01/sprint-1.4-v1.h)입니다.

```bash
G01_LAB_ID=G1.4 python3 labs/g01_safe_c/run_harness.py
```

## 안내 실습

Byte-at-a-time 상태 머신, full-buffer parser, 작은 reference encoder를 만듭니다. 두 parser가 같은 입력 모음에서 status·consumed·payload까지 일치하는지 differential test합니다.

## 독립 실습

libFuzzer harness와 seed corpus를 작성합니다. Truncation, repeated magic, bad length, bad CRC, extra bytes를 포함합니다. 결정적 검사는 최대 64바이트, 고정 seed, 100,000회, 각 실행 전 상태 초기화로 고정합니다.

## 전이 과제

처음 보는 TLV 형식에 maximum nesting 2와 total decoded size 64를 적용합니다. Resource exhaustion 조건을 test합니다.

## 판정 기준

- 모든 0–20 byte truncation 위치에서 crash·state corruption 없음
- accepted frame은 reference encoder round trip 통과
- rejected frame 뒤 다음 valid frame parsing 가능
- length 선검사 제거, CRC 범위 축소, 오류 뒤 output write, consumed off-by-one mutant를 모두 검출
- coverage와 equivalent mutant, 남은 blind spot 기록

## 힌트

1. Length 검증과 buffer indexing 순서를 확인합니다.
2. Error state에서 소비한 byte 수를 계약에 넣습니다.
3. CRC test는 parser logic과 독립된 reference를 사용합니다.

## 축소해서 다시 풀기

길이 필드 때문에 범위 밖 접근이 생기거나 거부된 입력이 application 상태를 바꿨다면 최대 payload 2인 parser로 줄입니다. 가능한 짧은 입력을 전부 실행해 두 문제가 사라진 뒤 원래 형식과 공개 입력 B로 확장합니다.
