# Study Logs

주차별 기록에는 질문, 근거, 직접 실험, 실패 원인을 남깁니다. Gate 판정은 주차 수와 별도로 관리합니다.

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

Git에는 재현 script와 작고 비식별화된 증거를 둡니다. 대용량 로그와 packet은 hash·보관 위치·생성 절차를 기록합니다.

## 새 주차 만들기

```bash
./scripts/new-study-log.sh 2 "POSIX process lifecycle"
```

생성된 `study/week-02/README.md`의 질문부터 작성합니다.

각 기록의 `Current gate`에 G0–G12를 적고, Gate 종료 시 [mastery review](../docs/templates/mastery-review.md)를 별도로 작성합니다.

## 좋은 기록의 기준

```markdown
Claim: State Management decides the requested Function Group State,
while Execution Management performs the resulting process lifecycle changes.

Source: AUTOSAR AP Software Architecture R25-11, relevant sections
My evidence: state-controller test and execution-manager transition log
Confidence: Partially confirmed — public prototype does not implement ara::exec
```

좋은 기록은 source의 주장과 내 실험을 연결합니다. 설명, 코드, packet, test 중 두 가지 이상으로 확인합니다.

AI 도움을 사용했다면 범위를 metadata에 남깁니다. 독립·전이·비공개 고장 평가는 초기 도움 없이 진행합니다.
