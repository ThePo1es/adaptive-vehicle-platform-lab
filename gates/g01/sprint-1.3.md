# Sprint 1.3 — Bounded Storage

## 시간과 자료

24–30시간. N1570 6.2.4, 6.5.6, 7.22를 읽고, 선택한 coding rule에서 array bounds와 integer wrap 관련 항목을 찾습니다.

## 시작 계약

Capacity는 compile time에 정하고 dynamic allocation을 사용하지 않습니다. Ring buffer는 `reject-new`와 `overwrite-oldest` 정책을 별도 instance로 지원합니다.

## 안내 실습

head, tail, count 중 어떤 상태를 저장할지 ADR로 결정합니다. Empty/full invariant, wrap, push/pop 실패 후 state를 test합니다.

## 독립 실습

Element 32개를 가진 fixed-size object pool을 작성합니다. Double free, foreign pointer, exhaustion을 탐지하고 counter를 제공합니다.

## 전이 과제

90분 동안 DMA descriptor queue를 구현합니다. Producer와 consumer ownership, publish/consume 시점, full policy를 설명합니다.

## 판정 기준

- capacity 0/1/2/power-of-two/non-power-of-two test
- 100만 operation model test에서 reference deque와 결과 일치
- 실패 operation 뒤 invariant 유지
- integer wrap과 index 범위가 sanitizer·property test를 통과

## 구현 전 확인

1. 상태 표현 하나를 고르고 모든 operation의 pre/post condition을 적습니다.
2. Capacity와 index type의 표현 범위를 확인합니다.
3. Pool pointer validation은 alignment와 range를 모두 확인합니다.

## 통과를 미루는 경우

`full`과 `empty`가 같은 상태로 보이거나 외부 포인터가 free list를 손상시키면 아직 닫지 않습니다. 용량 3으로 줄여 가능한 짧은 연산열을 전부 실행하고 깨진 불변 조건부터 고칩니다.
