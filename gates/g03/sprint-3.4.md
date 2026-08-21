# 실습 3-4 — 같은 ARM 대상에서 GCC와 Clang 공정하게 비교하기

> 상태: `Provisional` · 공식 GNU 아카이브가 검증되면 `Runnable` · [장 안내](README.md) · [실행 계약](contract.md)

## 시간과 기준 자료

24–30시간. [GCC developer options](https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html), [LLVM optimization remarks](https://llvm.org/docs/Remarks.html), 두 compiler의 현재 command reference를 읽습니다. 지원 flag는 실제 `--help`와 build log로 확인합니다.

## 실험 행렬

같은 C corpus와 같은 target CPU·ABI를 사용합니다.

| Compiler | 중간 표현 자료 | 공통 비교 자료 |
| --- | --- | --- |
| GCC | GIMPLE/RTL dump | assembly, map, text/data/bss, runtime/cycle |
| Clang | LLVM IR과 optimization remarks | assembly, map, text/data/bss, runtime/cycle |

`-O0`, `-O2`, 지원되는 size profile, LTO off/on을 시험합니다. 모든 조합을 한 번에 돌리기 어렵다면 corpus 두 함수와 profile 세 개를 Core로 고정합니다.

## 안내 실습

CRC 또는 parser loop에서 두 compiler가 만든 branch, call, load/store를 표시합니다. optimization remark와 dump는 각 compiler의 판단을 이해하는 자료로 씁니다.

## 독립 실습

size와 runtime이 크게 달라지는 함수 하나를 고릅니다. warm-up, sample count, clock, cache 조건, binary hash를 기록하고 원인을 최소 fixture로 줄입니다.

## 전이 과제

compiler version 하나를 바꿔 regression 여부를 재시험합니다. 통계 변동, code layout 변화, 실제 semantic change를 나눠 결론을 냅니다.

## 판정 기준

- GCC와 Clang의 중간 표현 이름과 도구를 정확히 구분
- 같은 target·ABI·workload 안에서 size와 runtime 비교
- raw result, 생성 명령, compiler·linker version을 보존
- 차이가 없는 결과도 그대로 기록하고 과장된 원인을 만들지 않음

## 힌트

1. 먼저 binary와 workload가 정말 같은 계약인지 확인합니다.
2. 작은 시간 차이는 반복 순서와 frequency scaling의 영향을 받습니다.
3. LTO 비교에는 linker와 plugin version도 필요합니다.

## 측정을 버리고 다시 할 때

서로 다른 대상의 수치를 한 순위에 넣었거나 GCC가 LLVM IR을 만들었다고 기록했다면 그 결과는 사용하지 않습니다. 함수와 대상을 하나로 고정하고 네 빌드만 다시 측정합니다.
