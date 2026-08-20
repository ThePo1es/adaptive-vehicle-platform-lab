# Safe C Components v1 릴리스 작업 공간

이 디렉터리는 1장 결과를 한 라이브러리로 빌드·시험·설치·시연하는 공개 릴리스 골격입니다. 기본값은 저장소의 기준 구현을 사용해 골격 자체를 검증합니다. 학습 결과를 공개할 때는 `G01_SOURCE_ROOT`를 본인의 `study/g01/src`로 바꿉니다.

## 깨끗한 빌드와 데모

```bash
cmake -S portfolio/g01-safe-c-components-v1 -B build/g01-release \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build/g01-release
ctest --test-dir build/g01-release --output-on-failure
./build/g01-release/g01_safe_c_demo
cmake --install build/g01-release --prefix build/g01-install
```

Windows의 여러 구성 생성기에서는 `cmake --build ... --config Release`, `ctest ... -C Release`, `build/g01-release/Release/g01_safe_c_demo.exe`를 사용합니다.

Windows SDK 없이 `zig.exe cc`를 CMake 드라이버로 직접 쓸 때는 `-DCMAKE_C_COMPILER=/path/to/zig.exe -DCMAKE_C_COMPILER_ARG1=cc -DG01_ZIG_DRIVER=ON`을 구성 명령에 더합니다.

## 내 구현으로 후보 만들기

```bash
cmake -S portfolio/g01-safe-c-components-v1 -B build/g01-my-release \
  -DG01_SOURCE_ROOT="$PWD/study/g01/src" \
  -DG01_INCLUDE_ROOT="$PWD/labs/g01_safe_c/include" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build/g01-my-release
ctest --test-dir build/g01-my-release --output-on-failure
```

릴리스 PR에는 1장의 입력 A·B 결과, 컴파일러 출력, 설치된 `include/g01_lab.h`와 라이브러리 목록, 데모 출력, 지원하지 않는 Cortex-M·DMA 범위를 함께 남깁니다.
