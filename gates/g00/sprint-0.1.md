# Sprint 0.1 — 환경과 진단

## 시간

24–30시간. 구현 16–20h, 누적·검토·기록 8–10h.

## 기준 자료

- [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html): Step 0–2와 testing 관련 단계
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html): Introduction, Usage, Limitations
- [Clang UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html): Available checks, Usage
- [GoogleTest Quickstart with CMake](https://google.github.io/googletest/quickstart-cmake.html)

## 시작 상태

빈 디렉터리에서 시작합니다. 아래 파일을 직접 만듭니다.

```text
baseline/
├── CMakeLists.txt
├── include/checked_add.h
├── src/checked_add.c
└── tests/checked_add_test.cpp
```

## 안내 실습

1. C library와 C++ test executable을 분리합니다.
2. `Debug`, `Release`, `ASan+UBSan` preset을 만듭니다.
3. 정상 덧셈, overflow 거부, null output 거부 test를 작성합니다.
4. 의도적인 out-of-bounds와 signed overflow 예제를 sanitizer로 실행합니다.

## 독립 실습

60분 동안 새 디렉터리에서 같은 구조를 다시 만듭니다. 기존 파일 복사는 허용하지 않습니다. README에는 configure, build, test 명령을 한 블록으로 적습니다.

## 전이 과제

`checked_mul_i32`를 추가하고 overflow 판정을 구현합니다. Compiler builtin을 썼다면 fallback 구현과 지원 조건을 문서화합니다.

## 판정 기준

- GCC와 Clang build가 모두 경고 없이 끝난다.
- `ctest --test-dir build --output-on-failure`가 같은 test를 실행한다.
- ASan은 out-of-bounds, UBSan은 signed overflow 예제를 잡는다.
- Release test는 정상 결과를 낸다.
- README만 읽은 새 VM 사용자가 15분 안에 test를 실행한다.

## 힌트

1. CMake target 단위로 include path와 compile option을 설정합니다.
2. Sanitizer flag는 compile과 link 단계에 모두 필요합니다.
3. Overflow 판정식 자체가 overflow를 일으키지 않는지 확인합니다.

## 치명적 실패

- test가 개인 절대 경로 또는 설치되지 않은 local library에 의존함
- sanitizer 경고를 suppression으로 숨김
- overflow가 발생한 뒤 결과를 검사함

## 보충 과제

CMake target과 directory scope를 다시 읽고, 4파일짜리 project를 45분 안에 재작성합니다.

