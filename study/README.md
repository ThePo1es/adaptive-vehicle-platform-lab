# Study Logs

주차별 학습 기록은 “요약”보다 **질문, 근거, 직접 실험, 실패 기록**을 중심으로 남깁니다.

## 디렉터리 규칙

```text
study/
└── week-NN/
    ├── README.md
    ├── experiments/
    │   └── short-name.md
    ├── diagrams/
    └── evidence/
        └── README.md
```

대용량 로그와 원본 패킷 캡처를 무조건 Git에 넣지 않습니다. 재현 스크립트와 최소화·비식별화한 증거를 우선합니다.

## 새 주차 만들기

```bash
./scripts/new-study-log.sh 2 "POSIX process lifecycle"
```

생성된 `study/week-02/README.md`의 질문부터 작성합니다.

## 좋은 기록의 기준

```markdown
Claim: State Management decides the requested Function Group State,
while Execution Management performs the resulting process lifecycle changes.

Source: AUTOSAR AP Software Architecture R25-11, relevant sections
My evidence: state-controller test and execution-manager transition log
Confidence: Partially confirmed — public prototype does not implement ara::exec
```

나쁜 기록은 출처 문장을 복사한 뒤 “이해했다”고 끝나는 기록입니다. 설명, 코드, 패킷 또는 테스트 중 최소 두 가지 방식으로 교차 검증합니다.

