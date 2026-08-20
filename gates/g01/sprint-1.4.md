# 실습 1-4 — 깨진 입력에도 안전한 파서 만들기

> - 준비 상태: `Runnable`
> - 시작 커밋: `4183399dc32bc69177a1cd0d18f81ac3b2877138`
> - 공개 입력 SHA-256: `4a854226b4d82abf04ceca2d3fb4fbdc744b2f1433b6fae4686fa62f3ed5f350`
> - 재시험 입력 SHA-256: `198e4f648ad29624e716d72047db760663ea347a839800156d0d9f7f0db5c029`
> - 실행 기록: [G1.4 실행 명세 v2](../../evidence/runnable/g1.4/run-manifest-v2.json)

> 소속 챕터: [안전한 C로 데이터와 메모리 다루기](README.md) · 관리 코드: G1.4

## 시간과 자료

32–44시간입니다. 상태 머신·CRC 자료 5–6시간, 두 파서와 기준 인코더 8–10시간, 차이 비교·잘림 검사 6–8시간, 퍼징·결함 주입 6–8시간, TLV 전이와 기록 7–12시간으로 나눕니다. N1570 6.5.6, 6.5.7, 7.20.1과 [libFuzzer](https://llvm.org/docs/LibFuzzer.html) 문서의 Fuzz Target, Corpus, Options를 읽습니다.

## Frame 형식

```text
[0xA5 시작 표식][0x01 버전][길이 0..16][데이터][CRC-8/ATM]
```

CRC는 시작 표식부터 데이터 마지막 바이트까지 계산합니다. 다항식 `0x07`, 초깃값 `0x00`, refin/refout false, xorout `0x00`으로 고정하고 ASCII `123456789 → 0xF4`를 먼저 확인합니다. 파서는 `complete`, `need-more`, `rejected`와 소비한 바이트 수를 반환합니다. 정확한 재동기화 규칙은 [G1 계약](contract.md#실습-1-4-프레임-파서-계약)을 따릅니다.

고정 입력은 [sprint-1.4-v1.h](../../fixtures/g01/sprint-1.4-v1.h)입니다.

```bash
G01_LAB_ID=G1.4 uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 python -m labs.g01_safe_c.run_harness
```

## 안내 실습

바이트 단위 상태 머신, 전체 버퍼 파서, 작은 기준 인코더를 만듭니다. 두 파서가 같은 입력 모음에서 판정·소비 길이·데이터까지 일치하는지 차이 비교 시험을 합니다.

## 독립 실습

libFuzzer harness와 seed corpus를 작성합니다. Truncation, repeated magic, bad length, bad CRC, extra bytes를 포함합니다. 결정적 검사는 최대 64바이트, 고정 seed, 100,000회, 각 실행 전 상태 초기화로 고정합니다.

## 전이 과제

처음 보는 TLV 형식에 maximum nesting 2와 total decoded size 64를 적용합니다. Resource exhaustion 조건을 test합니다.

## 판정 기준

- 최대 프레임의 길이 0–19 잘림과 20바이트 완성본에서 충돌·상태 손상 없음
- 받아들인 프레임은 기준 인코더 왕복 통과
- rejected frame 뒤 다음 valid frame parsing 가능
- 길이 선검사 제거, CRC 범위 축소, 오류 뒤 출력 쓰기, 소비 길이 한 칸 오류, 시작 표식 재사용 제거 결함을 모두 검출
- 검사 범위와 동등한 결함 주입, 남은 사각지대 기록

## 힌트

1. Length 검증과 buffer indexing 순서를 확인합니다.
2. Error state에서 소비한 byte 수를 계약에 넣습니다.
3. CRC test는 parser logic과 독립된 reference를 사용합니다.

## 축소해서 다시 풀기

길이 필드 때문에 범위 밖 접근이 생기거나 거부된 입력이 응용 상태를 바꿨다면 최대 데이터 길이 2인 파서로 줄입니다. 가능한 짧은 입력을 전부 실행해 두 문제가 사라진 뒤 원래 형식과 공개 입력 B로 확장합니다.
