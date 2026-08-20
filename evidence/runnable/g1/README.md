# G1 실행 증거

“안전한 C로 데이터와 메모리 다루기”의 다섯 실습을 시작 커밋 `e048adcb655db789e9a6c10382f55afc9f68bbba`에서 각각 다시 실행했습니다.

| 실습 | 실행 명세 | 확인한 경계 |
| --- | --- | --- |
| G1.1 | [v1](../g1.1/run-manifest-v1.json) | 길이·부호·예약 비트·바이트 순서 |
| G1.2 | [v1](../g1.2/run-manifest-v1.json) | 정렬·별칭·native endian 의존 |
| G1.3 | [v1](../g1.3/run-manifest-v1.json) | 가득 참·오래된 handle·0용량 거부 |
| G1.4 | [v1](../g1.4/run-manifest-v1.json) | CRC·소비 길이·재동기화 |
| G1.5 | [v1](../g1.5/run-manifest-v1.json) | MMIO 부작용·W1C·timeout·release/acquire |

```bash
python3 -m scripts.check_runnable_evidence
```

검사는 각 명세의 시작 커밋을 `git archive`로 새 임시 경로에 풀고, 고정된 Python 3.12.13 환경에서 실행 명령과 저장소 검사를 다시 수행합니다. 텍스트 출력은 운영체제 줄바꿈만 LF로 맞춘 뒤 종료 코드·전체 내용·SHA-256을 비교합니다. 기계 재현은 학습자가 독립 과제를 수행했다는 뜻이 아니며, 학습 시간과 Cortex-M 확인은 별도 기록으로 남습니다.
