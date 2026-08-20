# 실습 1-3 — 고정 용량 큐와 메모리 풀 만들기

> - 준비 상태: `Runnable`
> - 시작 커밋: `e048adcb655db789e9a6c10382f55afc9f68bbba`
> - 공개 입력 SHA-256: `966b9ef4e5c93dfbaa6cb4131a55f96fbe37eb3c935d6f15a79dec5e37f801f1`
> - 실행 기록: [G1.3 실행 명세 v1](../../evidence/runnable/g1.3/run-manifest-v1.json)

> 소속 챕터: [안전한 C로 데이터와 메모리 다루기](README.md) · 관리 코드: G1.3

## 시간과 자료

26–34시간입니다. 수명·배열 규칙 3–4시간, 큐 상태 설계 5–6시간, 풀과 핸들 6–8시간, 기준 모델·결함 주입 시험 6–8시간, 전이·기록 6–8시간으로 나눕니다. N1570 6.2.4, 6.5.6, 6.5.8, 7.22를 읽고 선택한 코딩 규칙에서 배열 범위와 정수 되감기 항목을 찾습니다.

## 시작 계약

저장 배열의 최대 크기는 compile time에 정하고 동적 할당을 사용하지 않습니다. 논리 용량은 1 이상이며 0은 compile-fail 입력으로 거부합니다. Ring buffer는 `reject-new`와 `overwrite-oldest` 정책을 별도 instance로 지원합니다. 공개 연산열과 seed는 [sprint-1.3-v1.h](../../fixtures/g01/sprint-1.3-v1.h)에 고정합니다.

```bash
G01_LAB_ID=G1.3 uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 python -m labs.g01_safe_c.run_harness
```

## 안내 실습

head, tail, count 중 어떤 상태를 저장할지 ADR로 결정합니다. Empty/full invariant, wrap, push/pop 실패 후 state를 test합니다.

## 독립 실습

원소 32개를 가진 고정 크기 메모리 풀을 작성합니다. 원시 포인터를 반환하지 않고 `index + generation` 핸들의 `get/set` 함수로만 값을 다룹니다. 이중 해제, 오래된 핸들, 공간 고갈을 탐지하고 진단 계수를 제공합니다. 세대값이 최댓값에 닿은 칸은 영구 은퇴시킵니다.

## 전이 과제

90분 동안 DMA descriptor queue를 구현합니다. Producer와 consumer 소유권, publish/consume 시점, 가득 참 정책을 설명합니다. DMA visibility와 cache maintenance는 C thread 동기화와 분리해 미해결 가정으로 남깁니다.

## 판정 기준

- capacity 0 compile-fail, 논리 용량 1/2/power-of-two/non-power-of-two 실행 시험
- 고정 난수 씨앗의 100만 연산 기준 모델 시험에서 기준 덱과 결과 일치
- 실패 operation 뒤 invariant 유지
- integer wrap과 index 범위가 sanitizer·property test를 통과
- 오래된 세대값, 이중 해제, 범위 밖 핸들이 데이터·소유권 상태를 바꾸지 않음
- 진단 계수는 `UINT32_MAX`에서 포화하며 되감기지 않음

## 구현 전 확인

1. 상태 표현 하나를 고르고 모든 operation의 pre/post condition을 적습니다.
2. Capacity와 index type의 표현 범위를 확인합니다.
3. 풀 소유권은 원시 포인터 관계 비교가 아니라 형식이 정해진 칸의 동일성 또는 세대 번호 핸들로 확인합니다.

## 통과를 미루는 경우

`full`과 `empty`가 같은 상태로 보이거나 잘못된 handle이 free list를 손상시키면 아직 닫지 않습니다. 용량 3으로 줄여 가능한 짧은 연산열을 전부 실행하고 깨진 불변 조건부터 고친 뒤 다른 seed로 재시험합니다.
