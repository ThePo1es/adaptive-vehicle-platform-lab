# 실습 1-5 — 레지스터·인터럽트·동시성 경계 다루기

> 소속 챕터: [안전한 C로 데이터와 메모리 다루기](README.md) · 관리 코드: G1.5

## 시간과 자료

30–42시간입니다. C17 volatile·atomic 5–6시간, register fake 5–7시간, ISR→task queue 7–9시간, assembly·target 검토 5–7시간, DMA 전이와 기록 8–13시간으로 나눕니다. N1570 5.1.2.3, 6.7.3, 7.17, Armv7-M Architecture Reference Manual의 memory model, CMSIS barrier intrinsic, 선택한 compiler의 ISR 확장 문서를 읽고 판본·절을 기록합니다.

## 레지스터 모델

```text
STATUS bit0 RX_READY, bit1 ERROR
CONTROL bit0 ENABLE, bit1 IRQ_ENABLE
RX_DATA bits0..7
IRQ_ACK write-one-to-clear bit0
```

Register별 offset·폭·RO/RW/W1C·reserved mask·부작용은 [G1 계약](contract.md#가짜-레지스터)에 고정합니다. Host fixture는 read/write 순서·폭·값과 side effect를 기록하며 입력은 [sprint-1.5-v1.h](../../fixtures/g01/sprint-1.5-v1.h)를 사용합니다.

```bash
G01_LAB_ID=G1.5 python3 labs/g01_safe_c/run_harness.py
```

## 안내 실습

Register access, bit update, modulo tick polling timeout, write-one-to-clear API를 만듭니다. W1C register는 literal write만 허용하고 read-modify-write가 섞이면 검사가 실패하게 합니다.

## 독립 실습

ISR을 단일 producer, task를 단일 consumer로 고정합니다. Producer는 non-atomic payload를 먼저 쓴 뒤 release로 index를 공개하고 consumer는 acquire 뒤 payload를 읽습니다. Queue full 정책과 counter를 검사하고, target에서 index atomic이 lock-free인지 macro와 assembly로 확인합니다.

## 전이 과제

DMA completion flag와 descriptor 소유권을 가진 새 peripheral shell을 설계합니다. C thread synchronization, compiler fence, CPU memory barrier, Device ordering, cache maintenance의 필요 조건을 각각 나눕니다. Host 검사로 DMA visibility를 증명했다고 쓰지 않습니다.

## 판정 기준

- `volatile`의 역할과 동기화 한계를 source·assembly로 설명
- ISR에 allocation·unbounded wait·parser 없음
- register side effect와 timeout negative test 통과
- single-core ISR/task, C thread, multi-core, DMA 계약을 분리
- W1C read-modify-write mutant, release/acquire 제거 mutant, timeout wrap 오류를 모두 검출

## 하드웨어 확인 사항

1. Device ordering, compiler reordering, language data race는 서로 다른 문제입니다.
2. ISR과 task가 공유하는 상태의 writer/reader를 표로 적습니다.
3. Host mock이 실제 hardware ordering을 보장하지 않는다는 한계를 기록합니다.

## 재시험

`volatile` 하나로 원자성과 happens-before를 설명했거나 ISR에 끝나지 않는 loop가 남았다면 SPSC queue 계약을 상태도로 다시 그립니다. Writer, reader, memory order를 표시한 뒤 다른 register sequence와 target assembly로 재시험합니다.
