# G3 공개 입력

`input-a.tsv`는 구현 중 쓰는 공개 입력 A, `input-b.tsv`는 값과 경계를 바꾼 재시험 입력 B입니다. 일반 실행은 A만, `.RETEST` 실행은 B만 사용합니다. `defined=true` 행은 학습자 함수를 `-O0`과 `-O2`로 실제 실행해 독립 기대값과 비교하고, `defined=false` 행은 UB 관찰로 명시해 동등성 판정에서 제외합니다.

`comparison-a.tsv`는 같은 C17 원본·입력 해시와 Cortex-M4/Thumb/AAPCS32/soft-float 계약을 고정합니다. `comparison-b.tsv`는 대상 변경, 원본·입력 변경, GCC 덤프를 LLVM IR로 잘못 부른 경우, 서로 다른 LTO 순위 주장을 각각 거부하는 재시험 자료입니다. 평가용 입력 C는 저장소 밖에서 보관합니다.
