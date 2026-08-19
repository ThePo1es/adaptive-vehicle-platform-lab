# G10.1 실행 증거

`run-manifest.json`은 시작 커밋 `1dfdf95770be0e77ee591a537c8998c545e1dd83`을 `git archive`로 꺼낸 뒤 실행한 결과입니다. 공개 양성·음성 입력, 검사기, 시작 파일의 SHA-256과 기준 출력을 묶었습니다.

```bash
python3 scripts/check_runnable_evidence.py
```

검사는 현재 파일과 시작 커밋의 파일을 모두 해시하고, 같은 명령을 다시 실행해 표준 출력과 종료 코드를 비교합니다. 검사기 실행에는 0.038초가 걸렸습니다. Sprint 10.1 학습 시간은 첫 학습 실행에서 별도로 기록합니다.
