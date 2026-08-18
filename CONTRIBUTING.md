# Working Agreement

개인 저장소지만 실제 개발 조직처럼 요구사항, 변경 범위, 검증 증거를 남기기 위한 규칙입니다.

## 작업 단위

- 한 이슈는 하나의 질문, 기능 또는 실험만 다룹니다.
- 한 PR은 리뷰 가능한 크기로 유지합니다.
- 리팩터링과 기능 변경을 가능하면 다른 커밋 또는 PR로 분리합니다.
- 학습 노트에 검증하지 않은 추측이 있으면 `Unverified`로 표시합니다.

## 브랜치

```text
study/gNN-wNN-short-topic
project/pNN-short-feature
gate/gNN-mastery-evidence
fix/pNN-short-bug
docs/short-topic
```

## 완료 정의

다음 항목이 모두 충족돼야 PR을 병합합니다.

- [ ] 이슈의 질문 또는 요구사항 ID가 명확하다.
- [ ] 구현 범위와 의도적으로 제외한 범위가 적혀 있다.
- [ ] 명령과 환경을 포함한 재현 절차가 있다.
- [ ] 정상 경로와 최소 하나의 오류 경로를 테스트했다.
- [ ] 테스트·패킷·로그·측정 중 하나 이상의 검증 증거가 있다.
- [ ] 민감 정보와 라이선스 문제가 없는지 확인했다.
- [ ] 관련 `PROGRESS.md`와 추적성 표를 갱신했다.
- [ ] Gate 승급을 주장한다면 AI-independent 시험과 clean-room 재현 증거가 있다.

## 측정 규칙

- 하드웨어, OS, compiler, build type, commit SHA를 함께 기록합니다.
- latency는 평균만 쓰지 않고 p50/p95/p99와 표본 수를 기록합니다.
- 비교 실험은 동일한 조건에서 반복하고 warm-up 여부를 명시합니다.
- 실패한 실험도 삭제하지 말고 원인과 다음 가설을 남깁니다.
- MCU/RTOS 결과는 simulator와 hardware, timer source와 probe overhead를 구분합니다.
- 관찰한 worst time을 검증된 WCET upper bound라고 부르지 않습니다.

## Gate 승급

- 주차나 프로젝트 milestone 완료만으로 승급하지 않습니다.
- [평가 기준](ASSESSMENTS.md)의 모든 dimension을 채운 `Mastery gate review` 이슈를 사용합니다.
- blank-page와 hidden-fault 시험은 초기 AI 힌트 없이 수행합니다.
- G11은 외부 reviewer의 architecture 질문과 clean environment 재현을 포함합니다.
