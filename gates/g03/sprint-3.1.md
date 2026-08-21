# 실습 3-1 — ARM32 함수 호출 경로 추적하기

> 상태: `Runnable` · [장 안내](README.md) · [실행 계약](contract.md)

## 시간과 기준 자료

24–30시간. [Arm ABI repository](https://github.com/ARM-software/abi-aa)의 `aapcs32`와 `aaelf32` 문서를 release tag로 고정해 읽습니다. Cortex-M target triple, CPU, FPU, float ABI, GCC·Clang version과 flags를 manifest에 적습니다.

## 입력 함수

```c
uint32_t mix4(uint8_t a, uint16_t b, uint32_t c, uint8_t d);
uint64_t sum64(uint64_t a, uint32_t b);
struct Pair { uint32_t x; uint16_t y; };
struct Pair adjust(struct Pair p, uint32_t delta);
uint32_t variadic_sum(unsigned count, ...);
```

## 안내 실습

`-O0`와 `-O2` assembly를 만들고 parameter, return value, stack alignment, caller/callee-saved register를 표시합니다. debugger가 있으면 함수 진입 직전과 직후 register를 캡처합니다.

## 독립 실습

prototype을 보지 않은 assembly 세 개에서 C signature 후보를 작성합니다. 확정할 수 없는 signedness와 type width는 따로 표시하고, symbol·debug info로 확인합니다.

## 전이 과제

구조체 크기와 field 조합을 바꾼 함수 하나를 검토자가 제공합니다. 60분 안에 전달 방식과 hidden return pointer 여부를 설명하고 assembly assertion을 추가합니다.

## 판정 기준

- AAPCS32 절 번호와 실제 instruction을 연결
- float ABI와 optimization profile을 섞지 않음
- register만 보고 확정할 수 없는 source 속성을 명확히 표시
- compiler 두 개에서 ABI 계약이 유지되는지 자동 assertion 또는 disassembly test로 확인

## 역추적 순서

1. 먼저 함수 경계에서 살아 있는 값을 표시합니다.
2. prologue의 stack 변화와 call site의 argument 준비를 함께 봅니다.
3. debug 정보는 결론 확인에 쓰고 첫 추론에는 숨깁니다.

## 판정을 보류하는 경우

대상과 float ABI가 기록되지 않았거나 한 컴파일 결과의 register 배치를 ABI 전체 규칙으로 일반화했다면 결론을 보류합니다. 정수 인자만 가진 두 함수로 줄여 호출 지점부터 다시 추적합니다.
