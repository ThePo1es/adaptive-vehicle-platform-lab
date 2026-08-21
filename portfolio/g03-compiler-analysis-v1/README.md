# Arm 호출부터 기계어까지 분석 묶음 v1

이 폴더는 G3의 다섯 결과를 GitHub에서 재현할 수 있게 묶는 공개 포트폴리오 안내입니다. 기준 구현으로 만든 출력은 검사기 검증일 뿐 학습자 포트폴리오 완성이 아닙니다.

## 폴더 만들기

```bash
mkdir -p study/g03/src study/g03/results
cp labs/g03_compiler_analysis/starter/* study/g03/src/
cp portfolio/g03-compiler-analysis-v1/report-template.md study/g03/report.md
git switch -c study/g03-call-to-machine
```

각 실습을 통과할 때 `study/g03/results`에 원본 표준 출력, 생성 명령, 컴파일러 버전, 입력 A·B SHA-256을 남깁니다. 생성한 IR·어셈블리·ELF는 작은 핵심 산출물만 커밋하고, 다시 만들 수 있는 대용량 중간 파일은 명령과 해시만 기록합니다.

## 공개 검사

```bash
G03_TRUSTED_LOCAL_EXECUTION=1 \
G03_SUBMISSION_ROOT=study/g03/src \
G03_LAB_ID=G3.ALL \
uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g03_compiler_analysis.run_harness
```

공식 GNU 아카이브를 검증하지 못하면 G3.4는 실패합니다. 시스템의 다른 GCC 결과로 표를 채우지 말고 도구 준비 기록부터 고칩니다.

## PR에 넣을 것

- Cortex-M4/Thumb/AAPCS32/soft-float 호출 경로 표
- AArch64 build ID, load bias, 실행 중 주소→링크 주소 계산과 재배치→PLT→GOT→DWARF 흐름
- C 원본 코드, Clang LLVM IR, Thumb 기계어를 연결한 표
- defined 입력 A·B 결과와 별도로 둔 UB 관찰
- 같은 대상 계약의 GCC·Clang `.text*` 합계와 원본·입력 해시
- 이슈 후보의 양·음성 대조군과 `READY_FOR_PEER_REVIEW` 또는 중단 결정
- 개발 PC에서 실제 실행한 것, 재배치 ELF만 만든 것, 보드에서 실행하지 않은 것을 나눈 범위표
- [G3 종합 평가](../../assessments/g03-compiler-analysis.md)와 독립 검토 결과가 있다면 그 링크
- 실제 학습 시간, 실패한 시도나 오해, 결론을 바꾼 증거, 보완·재시험, 전이 결과, 검토자, 다음 간격 재시험을 채운 학습·검토 기록

PR 제목 예시는 `G3: ARM 호출부터 기계어까지 분석 묶음 v1`입니다. 실제 상위 프로젝트에 문제를 신고하지 않았다면 URL 자리를 만들지 말고 `제출하지 않음`으로 씁니다. 보드 측정이 없다면 실행 시간, 사이클, 캐시, 서로 다른 LTO 구성의 우열을 결론에 넣지 않습니다.
