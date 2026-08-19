# Sprint 3.3 — Clang과 LLVM IR

## 시간과 기준 자료

24–30시간. [LLVM Language Reference](https://llvm.org/docs/LangRef.html)의 module, Data Layout, integer operations, `poison`, memory와 [opt command guide](https://llvm.org/docs/CommandGuide/opt.html)를 읽습니다. Clang·LLVM version과 target triple을 고정합니다.

## 분석 corpus

- endian-safe signal decoder
- bounded queue index update
- CRC loop
- range-checked parser state transition

각 함수에는 유효 input domain과 C/C++의 UB 가능 지점을 먼저 적습니다.

## 안내 실습

Clang으로 optimization 전후 LLVM IR을 만들고 `zext/sext`, `getelementptr`, `phi`, branch, load/store 변화를 source에 연결합니다. `DataLayout`과 target triple도 보고서에 넣습니다.

## 독립 실습

parser 한 함수의 source, LLVM IR, target assembly, 정상·경계 test를 한 문서에서 추적합니다. UB를 넣은 별도 fixture는 sanitizer와 IR 변화로 관찰하고 production corpus와 섞지 않습니다.

## 전이 과제

검토자가 새 C 함수와 input contract를 줍니다. 90분 안에 optimizer가 제거한 check가 유효한지 판단하고 작은 executable test를 만듭니다.

## 판정 기준

- LLVM IR은 Clang에서 생성했다고 기록
- `poison`, `undef`, wrap flag를 문서 정의와 실제 instruction에 맞게 설명
- defined input domain에서 optimization 전후 결과를 differential test
- IR 모양만 보고 성능을 확정하지 않고 target assembly와 측정으로 확인

## 비교할 때 주의할 점

1. source contract에 없는 input은 equivalence test 결과 해석에서 분리합니다.
2. `-O0` IR에도 frontend가 만든 구조가 남습니다.
3. pass 이름은 해당 LLVM version의 pipeline 출력으로 확인합니다.

## 다시 분리할 문제

GCC 출력물을 LLVM IR로 기록했거나 UB 입력의 차이를 컴파일러 결함으로 확정했다면 unsigned 덧셈과 signed overflow 입력을 따로 만듭니다. 정의된 동작에서만 동등성을 판정한 뒤 UB 결과는 관찰로 남깁니다.
