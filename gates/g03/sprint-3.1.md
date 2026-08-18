# Sprint 3.1 — AAPCS32

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

## 힌트

1. 먼저 함수 경계에서 살아 있는 값을 표시합니다.
2. prologue의 stack 변화와 call site의 argument 준비를 함께 봅니다.
3. debug 정보는 결론 확인에 쓰고 첫 추론에는 숨깁니다.

## 치명적 실패와 보충

target·float ABI를 기록하지 않거나 compiler가 우연히 만든 register 배치를 ABI 규칙 전체로 일반화하면 실패입니다. 보충 과제는 정수 인자만 가진 두 함수로 줄여 call site부터 다시 추적하는 것입니다.
