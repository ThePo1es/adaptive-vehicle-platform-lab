# Sprint 2.2 — 제한된 Runtime

## 시간과 기준 자료

24–30시간. C++ working draft의 [`[container.requirements]`](https://eel.is/c++draft/container.requirements), [`[span]`](https://eel.is/c++draft/span), [`[optional]`](https://eel.is/c++draft/optional), [`[variant]`](https://eel.is/c++draft/variant)를 읽습니다. 선택한 compiler의 linker map과 size 도구 문서도 manifest에 고정합니다.

## 입력 계약

Event는 16바이트 payload, 16-bit type, 32-bit sequence를 갖습니다. Runtime은 시작할 때 저장 공간을 준비한 뒤 다음 계약을 지킵니다.

- capacity 32
- full policy는 `RejectNewest` 또는 `DropOldest` 중 하나를 설정에서 선택
- event dispatch 중 heap allocation 0회
- callback 8개까지 등록
- 오류는 exception 없이 호출자에게 전달

## 안내 실습

고정 용량 event queue와 callback table을 만듭니다. 전역 `operator new` 계수기 또는 allocator hook으로 초기화 뒤 allocation을 감시합니다.

## 독립 실습

두 full policy를 같은 test suite로 검증합니다. callback이 event를 다시 넣는 경우, callback 제거, sequence wrap 근처를 포함합니다. Release map에서 text/data/bss와 template instantiation을 기록합니다.

## 전이 과제

같은 계약으로 고정 크기 timer wheel 또는 message router를 만듭니다. 새 구현은 event queue source를 복사하지 않고 공통 policy만 재사용합니다.

## 판정 기준

- 초기화 뒤 정상·full·reentrant 경로의 allocation count가 0
- capacity를 넘는 상태가 없고 선택한 full policy의 counter가 정확함
- 모든 public operation이 bounded loop 또는 명시한 상한을 가짐
- GCC·Clang Release 결과의 text/data/bss를 같은 target과 flags 범위에서 기록

## 힌트

1. 저장 공간, 현재 개수, head/tail invariant부터 적습니다.
2. callback 실행 중 container를 직접 수정하면 iterator와 순회 정책이 필요합니다.
3. code size는 compiler·linker·target이 같을 때 비교합니다.

## 재검증 조건

가득 찬 상태에서 메모리를 덮어쓰거나 금지 구간에서 할당이 한 번이라도 발생하면 단일 producer/consumer로 줄입니다. 저장 공간, 인덱스, 원소 수의 불변 조건을 고정하고 다시 확장합니다.
