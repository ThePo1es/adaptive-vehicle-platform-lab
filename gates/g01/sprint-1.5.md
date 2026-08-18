# Sprint 1.5 — MMIO와 동시성 경계

## 시간과 자료

24–30시간. N1570 5.1.2.3, 6.7.3, 7.17과 선택한 Arm architecture/compiler의 barrier intrinsic 문서를 읽습니다.

## Register model

```text
STATUS bit0 RX_READY, bit1 ERROR
CONTROL bit0 ENABLE, bit1 IRQ_ENABLE
RX_DATA bits0..7
IRQ_ACK write-one-to-clear bit0
```

Host fixture는 read/write log와 side effect를 기록합니다.

## 안내 실습

Register access, bit update, polling timeout, write-one-to-clear API를 만듭니다. Read-modify-write가 위험한 register를 구분합니다.

## 독립 실습

ISR은 byte를 bounded queue에 넣고 task가 parser를 실행하는 driver shell을 작성합니다. Queue full policy와 counter를 test합니다.

## 전이 과제

DMA completion flag와 descriptor ownership을 가진 새 peripheral shell을 설계합니다. Compiler barrier, CPU memory barrier, cache maintenance의 필요 조건을 나눕니다.

## 판정 기준

- `volatile`의 역할과 동기화 한계를 source·assembly로 설명
- ISR에 allocation·unbounded wait·parser 없음
- register side effect와 timeout negative test 통과
- single-core ISR/task와 multi-core/thread contract를 분리

## 힌트

1. Device ordering, compiler reordering, language data race는 서로 다른 문제입니다.
2. ISR과 task가 공유하는 상태의 writer/reader를 표로 적습니다.
3. Host mock이 실제 hardware ordering을 보장하지 않는다는 한계를 기록합니다.

## 치명적 실패와 보충

`volatile`만으로 atomicity와 happens-before를 주장하거나 ISR에서 무한 loop를 돌면 실패입니다. 보충 과제는 single-producer/single-consumer queue contract를 state diagram으로 다시 작성하는 것입니다.
