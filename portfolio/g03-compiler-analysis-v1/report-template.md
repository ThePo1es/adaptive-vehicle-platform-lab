# G3 분석 보고서

## 재현 정보

| 항목 | 값 |
| --- | --- |
| 시작 커밋 | |
| 입력 A/B SHA-256 | |
| Python/Zig/Clang | |
| GNU 아카이브/해시/상태 | |
| CPU·ISA·ABI·float ABI | |

## ARM32 호출 경로

| source 값 | caller 준비 | 함수 진입 | 저장 책임 | 근거 명령 |
| --- | --- | --- | --- | --- |
| | | | | |

## AArch64 오류 주소 복원

| build ID | runtime 주소 | load bias | link 주소 | source 위치 |
| --- | ---: | ---: | ---: | --- |
| | | | | |

재배치→PLT→GOT 흐름:

## C→LLVM IR→기계어

| source 계약 | LLVM IR | Thumb 명령 | defined 입력 결과 | UB 관찰 |
| --- | --- | --- | --- | --- |
| | | | | |

## GCC·Clang 공정 비교

| compiler | 같은 대상 계약 | `.text` | 상태 |
| --- | --- | ---: | --- |
| Clang 20.1.2 | | | |
| Arm GCC 14.3.1 | | | Provisional/검증됨 |

## 이슈 보고 결정

| source contract | 재현 | 축소 | 기대 근거 | 중복 검색 | 결정 |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 확인하지 못한 범위

- 보드 실행:
- runtime/cycle/cache:
- cross-LTO:
- upstream 제출/검토:
