# Sprint 1.4 — 방어적 Parser

## 시간과 자료

24–30시간. N1570 6.5.6, 6.5.7, 7.20.1과 [libFuzzer](https://llvm.org/docs/LibFuzzer.html) 문서의 Fuzz Target, Corpus, Options를 읽습니다.

## Frame 형식

```text
[0xA5 magic][0x01 version][length 0..16][payload][CRC-8/ATM]
```

CRC는 polynomial `0x07`, init `0x00`, refin/refout false, xorout `0x00`으로 고정합니다. Parser는 complete, need-more, rejected 상태를 반환합니다.

## 안내 실습

Byte-at-a-time state machine, full-buffer parser, 작은 reference encoder를 만듭니다. 두 parser가 같은 corpus에서 일치하는지 differential test합니다.

## 독립 실습

libFuzzer harness와 seed corpus를 작성합니다. Truncation, repeated magic, bad length, bad CRC, extra bytes를 포함합니다.

## 전이 과제

처음 보는 TLV 형식에 maximum nesting 2와 total decoded size 64를 적용합니다. Resource exhaustion 조건을 test합니다.

## 판정 기준

- 모든 0–20 byte truncation 위치에서 crash·state corruption 없음
- accepted frame은 reference encoder round trip 통과
- rejected frame 뒤 다음 valid frame parsing 가능
- coverage와 mutation 결과, 남은 blind spot 기록

## 힌트

1. Length 검증과 buffer indexing 순서를 확인합니다.
2. Error state에서 소비한 byte 수를 계약에 넣습니다.
3. CRC test는 parser logic과 독립된 reference를 사용합니다.

## 치명적 실패와 보충

길이 field로 out-of-bounds가 발생하거나 rejected input이 application state를 바꾸면 실패입니다. 보충 과제는 모든 4-byte input을 exhaustive하게 실행하는 축소 parser입니다.

