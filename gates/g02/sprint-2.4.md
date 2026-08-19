# Sprint 2.4 — ABI와 설계 선택

## 시간과 기준 자료

24–30시간. C++ working draft의 [`[class.virtual]`](https://eel.is/c++draft/class.virtual), [`[except]`](https://eel.is/c++draft/except), [`[temp]`](https://eel.is/c++draft/temp)와 [Arm ABI repository](https://github.com/ARM-software/abi-aa)를 읽습니다. ABI 문서는 사용한 release tag와 파일명을 적습니다.

## 비교 대상

Clock, Transport, Launcher 세 interface를 아래 방식으로 각각 작은 예제로 만듭니다.

1. virtual interface
2. template/static polymorphism
3. function pointer 또는 수동 type erasure

동일한 정상·timeout·cleanup test를 세 구현에 적용합니다.

## 안내 실습

host와 선택한 ARM target에서 symbol, vtable, relocation, text size를 확인합니다. boundary를 넘는 API는 `extern "C"` facade와 명시적 ownership 규칙으로 감쌉니다.

## 독립 실습

P01의 process launcher 또는 P02의 transport 하나를 골라 세 대안 중 하나를 선택합니다. 빌드 시간, binary size, test seam, lifetime, 오류 전달을 근거로 ADR을 씁니다.

## 전이 과제

다른 compiler와 build profile에서 exception·RTTI on/off 조합을 확인합니다. 지원하지 않는 flag는 억지로 쓰지 않고 compiler help와 build log를 근거로 제외합니다.

## 판정 기준

- 같은 target·optimization에서 map과 size를 비교
- public ABI의 layout, allocation, ownership, exception 전파 규칙이 명시됨
- 선택하지 않은 두 대안의 장점과 실제 비용을 수치 또는 test로 기록
- 처음 보는 interface에 같은 판단 기준을 적용하는 45분 구두 검토 통과

## 힌트

1. source 줄 수보다 호출 경계와 생성된 symbol을 먼저 봅니다.
2. template 중복은 linker folding과 LTO 설정의 영향을 받습니다.
3. exception을 끄면 오류 모델을 API에서 직접 설계해야 합니다.

## 비교를 다시 해야 하는 경우

서로 다른 대상을 빌드한 크기로 성능 순위를 냈거나 C ABI에 C++ object layout과 예외가 노출됐다면 인터페이스 하나만 남깁니다. 동일한 도구 설정으로 세 구현을 다시 빌드해 link map부터 비교합니다.
