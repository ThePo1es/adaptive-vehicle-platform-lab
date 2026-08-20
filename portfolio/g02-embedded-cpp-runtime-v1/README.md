# 임베디드 C++ 실행 기반 v1 포트폴리오

이 폴더에서는 G2의 네 실습 결과를 하나의 정적 라이브러리로 빌드하고 검사한 뒤 설치까지 해 볼 수 있습니다. GitHub에 공개할 포트폴리오를 만들 때 사용하는 작업 공간입니다. 아무 옵션도 주지 않으면 검사기 검증용 기준 구현을 사용합니다. 자신의 구현을 확인하려면 `G02_SOURCE_ROOT`에 `study/g02/src` 경로를 지정하세요.

## 새 빌드 폴더에서 확인하기

```bash
cmake -S portfolio/g02-embedded-cpp-runtime-v1 -B build/g02-release \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build/g02-release
ctest --test-dir build/g02-release --output-on-failure
cmake --install build/g02-release --prefix build/g02-install
```

자신의 구현을 빌드하려면 첫 번째 명령에 다음 옵션을 추가합니다.

```bash
-DG02_SOURCE_ROOT="$PWD/study/g02/src"
```

예제 프로그램은 C++ 사용자와 C 사용자를 각각 확인합니다.

- `g02_cpp_demo`: 데이터 수명 보장, 이벤트 처리, 작업 큐, 함수 테이블 호출
- `g02_c_demo`: C17 헤더, 음수인 정상 데이터, 불투명 핸들의 생성·실행·해제

## PR에 함께 올릴 자료

- 공개 입력 A·B의 전체 검사 출력
- 결함 주입본 10개가 모두 검출된 출력
- CMake 설정·빌드·검사·설치 명령의 원본 출력
- 객체 소유 관계도와 큐 종료 상태표
- 두 대상의 ELF 수치와 다형성 선택 ADR
- 개발 PC에서 실행한 항목, 오브젝트 파일만 만든 항목, 아직 실행하지 않은 보드를 나눈 범위표
- [G2 종합 평가](../../assessments/g02-embedded-cpp.md)와 독립 검토 결과

자신의 구현이 아니라 기준 구현으로 만든 예제는 검사기 자체를 확인한 결과일 뿐입니다. 이를 학습 포트폴리오 완성으로 기록하면 안 됩니다.
