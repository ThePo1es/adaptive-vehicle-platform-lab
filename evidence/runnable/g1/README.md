# G1 실행 증거

“안전한 C로 데이터와 메모리 다루기”의 다섯 실습을 시작 커밋 `abf2aae90dfe739cc28b8fc3c08fa0729f541c34`에서 각각 다시 실행했습니다. Python 3.12.13, uv 0.12.3, Zig 0.15.2와 내장 C 표준 라이브러리를 고정하고 공개 입력 A·B를 모두 확인했습니다. v14는 잠금 파일로 도구 해시를 확인하고 Windows 재생 때 Git Bash 절대 경로를 사용해 WSL 실행기와 섞이지 않도록 고정합니다.

| 실습 | 실행 명세 | 확인한 경계 |
| --- | --- | --- |
| G1.1 | [v14](../g1.1/run-manifest-v14.json) | 길이·부호·예약 비트·바이트 순서·속성 왕복 |
| G1.2 | [v14](../g1.2/run-manifest-v14.json) | 위치 0–7·길이 0–8·호스트 바이트 순서 |
| G1.3 | [v14](../g1.3/run-manifest-v14.json) | 용량 1·2·3·4·8, 32칸 풀, 세대값 고갈 |
| G1.4 | [v14](../g1.4/run-manifest-v14.json) | 모든 최대 프레임 접두부·CRC·시작 표식 재사용 |
| G1.5 | [v14](../g1.5/run-manifest-v14.json) | 32비트 MMIO·W1C·시간 제한·release/acquire |

```bash
uv run --project toolchain --locked --offline \
  python -m scripts.check_runnable_evidence
```

검사는 각 명세의 시작 커밋을 `git archive`로 새 임시 경로에 풀고, 네트워크를 끈 고정 환경에서 실행 명령과 저장소 검사를 다시 수행합니다. 텍스트 출력은 운영체제 줄바꿈만 LF로 맞춘 뒤 종료 코드·전체 내용·SHA-256을 비교합니다. 기계 재현은 학습자가 독립 과제를 수행했다는 뜻이 아니며, 학습 시간과 Cortex-M 확인은 별도 기록으로 남습니다.
