# G1 공개 검사기

이 디렉터리는 “안전한 C로 데이터와 메모리 다루기(G1)”의 시작 코드와 공개 검사를 제공합니다. 검사기는 C17 기준 구현을 먼저 실행해 fixture와 판정 자체가 작동하는지 확인합니다.

## 기준 구현 확인

```bash
G01_LAB_ID=G1.ALL python3 labs/g01_safe_c/run_harness.py
```

성공하면 다섯 실습과 필수 mutant가 모두 `PASS`로 출력됩니다. `G1.1`부터 `G1.5` 중 하나만 지정할 수도 있습니다.

## 내 구현 확인

```bash
mkdir -p study/g01/src
cp labs/g01_safe_c/starter/*.c study/g01/src/

G01_SUBMISSION_ROOT=study/g01/src \
G01_LAB_ID=G1.1 \
python3 labs/g01_safe_c/run_harness.py
```

시작 코드는 의도적으로 공개 검사를 통과하지 않습니다. 실습을 진행하며 해당 함수만 구현합니다. `G1.5`는 이전 실습의 `storage.c`에 SPSC queue 구현이 있어야 합니다.

## 검사 범위

| 실습 | 공개 검사가 보는 것 | 별도 검증이 필요한 것 |
| --- | --- | --- |
| G1.1 | 신호 벡터, 길이, reserved bit, 출력 불변 | 새 bit layout 전이 과제 |
| G1.2 | offset 0–7의 safe read와 native endian 비교 | Cortex-M 정렬 fault·assembly |
| G1.3 | 100만 operation model, full 정책, generation handle | DMA ownership |
| G1.4 | CRC, 고정 corpus, stream 복구, 결정적 입력 10만 개 | 장시간 libFuzzer/AFL++ |
| G1.5 | register access log, W1C, timeout wrap, SPSC 값 전달 | target lock-free·barrier·DMA cache |

공개 검사는 봉인된 종합 평가가 아닙니다. 실제 target에서 확인하지 않은 성질과 학습자가 직접 수행하지 않은 결과를 완료로 표시하지 않습니다.
