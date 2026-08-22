# 실습 3-3 — C에서 LLVM IR과 기계어까지 연결하기

> 상태: `Runnable` · [장 안내](README.md) · [실행 계약](contract.md)

## 시간과 기준 자료

능동 작업 18시간, 도구 실행 5시간, 검토 대기 3시간으로 모두 26시간을 잡습니다. [LLVM 언어 참조](https://llvm.org/docs/LangRef.html)의 모듈, Data Layout, 정수 연산, `poison`, 메모리 절과 [opt 명령 안내](https://llvm.org/docs/CommandGuide/opt.html)를 읽습니다. Clang·LLVM 버전과 대상 삼중항을 고정합니다.

## 분석 대상 코드

- 바이트 순서에 안전한 신호 해석기
- 범위를 제한한 큐 색인 갱신
- CRC 반복문
- 범위를 확인하는 파서 상태 전이

각 함수에는 유효한 입력 범위와 C/C++의 UB 가능 지점을 먼저 적습니다.

## 안내 실습

Clang으로 최적화 전후 LLVM IR을 만들고 `zext/sext`, `getelementptr`, `phi`, 분기, 읽기와 쓰기의 변화를 원본 코드에 연결합니다. `DataLayout`과 대상 삼중항도 보고서에 넣습니다.

## 독립 실습

파서 함수 하나를 골라 원본 C 코드, LLVM IR, 대상 어셈블리, 정상·경계값 시험을 한 문서에서 이어 봅니다. UB를 일으키는 입력은 별도 시험 자료에서 관찰하고 정상 분석 대상과 섞지 않습니다.

## 전이 과제

검토자가 새 C 함수와 입력 계약을 줍니다. 90분 안에 최적화기가 제거한 검사가 타당한지 판단하고 작은 실행 시험을 만듭니다.

## 판정 기준

- LLVM IR은 Clang에서 생성했다고 기록
- `poison`, `undef`, wrap flag를 문서 정의와 실제 instruction에 맞게 설명
- 정의된 입력 범위에서 `-O0`과 `-O2` 실행 결과를 독립 기대값과 비교
- IR 모양만 보고 성능을 확정하지 않고 target assembly와 측정으로 확인

## 비교할 때 주의할 점

1. source contract에 없는 input은 equivalence test 결과 해석에서 분리합니다.
2. `-O0` IR에도 frontend가 만든 구조가 남습니다.
3. pass 이름은 해당 LLVM version의 pipeline 출력으로 확인합니다.

## 다시 분리할 문제

GCC 출력물을 LLVM IR로 기록했거나 UB 입력의 차이를 컴파일러 결함으로 확정했다면 unsigned 덧셈과 signed overflow 입력을 따로 만듭니다. 정의된 동작에서만 동등성을 판정한 뒤 UB 결과는 관찰로 남깁니다.
