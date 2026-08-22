# 실습 3-1 — ARM32 함수 호출 경로 추적하기

> 상태: `Runnable` · [장 안내](README.md) · [실행 계약](contract.md)

## 시간과 기준 자료

능동 작업 15시간, 도구 실행 3시간, 검토와 재시험 대기 4시간으로 모두 22시간을 잡습니다. [Arm ABI 저장소](https://github.com/ARM-software/abi-aa)의 `aapcs32`와 `aaelf32` 문서를 릴리스 태그로 고정해 읽습니다. Cortex-M 대상 삼중항, CPU, FPU, float ABI, GCC·Clang 버전과 선택 사항을 명세에 적습니다.

## 입력 함수

```c
uint32_t mix4(uint8_t a, uint16_t b, uint32_t c, uint8_t d);
uint64_t sum64(uint64_t a, uint32_t b);
struct Pair { uint32_t x; uint16_t y; };
struct Pair adjust(struct Pair p, uint32_t delta);
uint32_t variadic_sum(unsigned count, ...);
```

## 안내 실습

`-O0`과 `-O2` 어셈블리를 만든 뒤 매개변수, 반환값, 스택 정렬, 호출자·피호출자 보존 레지스터를 표시합니다. 디버거를 쓸 수 있다면 함수 진입 전후의 레지스터 값도 저장합니다.

## 독립 실습

함수 원형을 보지 않은 어셈블리 세 개에서 C 함수 선언 후보를 작성합니다. 확정할 수 없는 부호 유무와 형식 너비는 따로 표시하고, 심벌과 디버그 정보로 확인합니다.

## 전이 과제

구조체 크기와 필드 조합을 바꾼 함수 하나를 검토자가 제공합니다. 60분 안에 전달 방식과 숨은 반환 포인터 여부를 설명하고 어셈블리 검사를 추가합니다.

## 판정 기준

- AAPCS32 절 번호와 실제 명령을 연결
- float ABI와 최적화 설정을 섞지 않음
- 레지스터만 보고 확정할 수 없는 원본 코드 속성을 명확히 표시
- 두 컴파일러에서 ABI 계약이 유지되는지 자동 검사 또는 역어셈블 검사로 확인

## 역추적 순서

1. 먼저 함수 경계에서 살아 있는 값을 표시합니다.
2. prologue의 stack 변화와 call site의 argument 준비를 함께 봅니다.
3. debug 정보는 결론 확인에 쓰고 첫 추론에는 숨깁니다.

## 판정을 보류하는 경우

대상과 float ABI가 기록되지 않았거나 한 컴파일 결과의 register 배치를 ABI 전체 규칙으로 일반화했다면 결론을 보류합니다. 정수 인자만 가진 두 함수로 줄여 호출 지점부터 다시 추적합니다.
