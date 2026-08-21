# 임베디드 C++로 안전한 런타임 만들기

> 관리 코드: G2 · 권장 학습 순서: 3번째 · 현재 준비 상태: `Runnable`

이 장에서는 C++20으로 작은 실행 기반을 직접 만듭니다. 중요한 것은 문법을 많이 외우는 일이 아닙니다. 자원을 누가 소유하는지, 기다리던 스레드는 언제 깨어나는지, 오류가 나도 어떤 값은 지켜야 하는지를 코드와 검사 결과로 설명할 수 있어야 합니다.

## 이 장에서 완성하는 것

네 실습을 마치면 `임베디드 C++ 런타임 v1`이 완성됩니다.

```text
받아 온 바이트의 수명을 보장하는 데이터 뷰
  └─ 필요한 메모리를 미리 확보한 이벤트 처리기
      └─ 종료 요청이 와도 남은 작업을 마치는 큐
          └─ C/C++ 경계와 세 가지 다형성 비교 자료
```

자동 검사는 Zig 0.15.2로 개발 PC의 x86_64 C++20 프로그램을 빌드해 실행합니다. Cortex-M과 AArch64에서는 프로그램을 실행하지 않습니다. 운영체제 없이 동작하는 환경을 가정한 ELF 오브젝트 파일만 만들고, 섹션·심벌·재배치 정보를 확인합니다. 이 결과를 실제 보드에서 실행한 근거로 사용하면 안 됩니다.

## 시작 전 확인

Git과 `uv` 0.12.3이 필요합니다. 처음 한 번만 Python 3.12.13, Zig 0.15.2, ELF 판독기 0.32를 내려받아 사용자 캐시에 저장합니다.

```bash
uv run --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -c "import ziglang, elftools; print(ziglang.__file__)"
```

준비가 끝나면 저장소 최상위 폴더에서 환경 검사를 실행합니다.

```bash
G02_LAB_ID=G2.ENTRY \
uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g02_embedded_cpp.run_harness
```

PowerShell에서는 먼저 `$env:G02_LAB_ID = "G2.ENTRY"`를 실행한 다음 `uv run ...` 명령을 실행합니다. 출력에 나온 Python과 Zig 버전, 빌드 대상이 [G2 공통 계약](contract.md)과 다르면 코드를 고치기 전에 실행 환경부터 맞춰 주세요.

## 내 구현 폴더 만들기

저장소에 들어 있는 완성 구현은 검사기가 결함을 제대로 찾아내는지 확인할 때만 씁니다. 학습할 때는 시작 파일 네 개를 자신의 작업 폴더로 복사합니다.

```bash
mkdir -p study/g02/src
cp labs/g02_embedded_cpp/starter/*.cpp study/g02/src/

G02_TRUSTED_LOCAL_EXECUTION=1 G02_SUBMISSION_ROOT=study/g02/src G02_LAB_ID=G2.1 \
uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g02_embedded_cpp.run_harness
```

시작 파일은 빌드되지만 공개 검사를 통과하지 못합니다. 검사기는 학습자가 지정한 폴더의 코드와 별도로 작성된 검사 코드·입력만 연결합니다. 완성 구현이 학습자 프로그램에 섞이지 않도록 분리해 두었습니다. `G02_TRUSTED_LOCAL_EXECUTION=1`은 자신이 작성하거나 직접 검토한 코드에만 사용하세요. 이 로컬 검사기는 파일 시스템과 네트워크를 가두는 보안 샌드박스가 아닙니다.

PowerShell에서는 `$env:G02_TRUSTED_LOCAL_EXECUTION = "1"`, `$env:G02_SUBMISSION_ROOT = "study/g02/src"`, `$env:G02_LAB_ID = "G2.1"`을 차례로 지정한 뒤 같은 `uv run ...` 명령을 실행합니다.

## 실습 순서

| 실습 | 만드는 것 | 예상 활동 시간 | 준비 상태 |
| --- | --- | ---: | --- |
| [2-1 원본이 파괴되어도 안전한 데이터 뷰 만들기](sprint-2.1.md) | 원본 객체가 파괴된 뒤에도 안전하게 읽을 수 있는 데이터 뷰 | 24–32시간 | Runnable |
| [2-2 힙 없이 동작하는 이벤트 처리기 만들기](sprint-2.2.md) | 이벤트 32개와 콜백 8개를 담는 고정 용량 처리기 | 28–36시간 | Runnable |
| [2-3 멈추지 않고 종료되는 작업 큐 만들기](sprint-2.3.md) | 생산자 2개와 소비자 1개가 함께 쓰는 용량 8의 큐 | 30–40시간 | Runnable |
| [2-4 가상 함수·템플릿·C 경계를 비교해 선택하기](sprint-2.4.md) | 세 가지 구현 비교, C17 공개 API, 두 대상의 ELF 보고서 | 26–34시간 | Runnable |

총 108–142시간은 자료를 읽고 안내 실습과 독립 구현을 수행하며, 실패 원인을 분석하고 응용 과제와 학습 기록을 마치는 데 필요한 예상 시간입니다. 아직 실제 학습 시간을 바탕으로 계산한 값이 아니므로 `Provisional`로 표시합니다. 자동 빌드에 걸린 시간은 학습 시간과 따로 기록합니다.

## 공개 검사와 재시험

전체 공개 입력 A를 실행합니다.

```bash
G02_TRUSTED_LOCAL_EXECUTION=1 G02_SUBMISSION_ROOT=study/g02/src G02_LAB_ID=G2.ALL \
uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g02_embedded_cpp.run_harness
```

통과 뒤 값과 경계를 바꾼 입력 B로 다시 시험합니다.

```bash
G02_TRUSTED_LOCAL_EXECUTION=1 G02_SUBMISSION_ROOT=study/g02/src G02_LAB_ID=G2.RETEST \
uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g02_embedded_cpp.run_harness
```

A와 B는 누구나 볼 수 있는 반복 검사입니다. 입력값이 달라져도 구현이 제대로 동작하는지 확인할 수 있지만, [G2 종합 평가](../../assessments/g02-embedded-cpp.md)에서 처음 공개하는 입력이나 제3자의 검토를 대신하지는 못합니다.

## 실습마다 남길 기록

1. 작업을 시작한 커밋과 입력 A·B 파일의 SHA-256
2. 소유 관계도, 대기 상태 전이표, 콜백 실행 규칙
3. 처음 실패한 검사와 소유권 또는 동기화가 처음 어긋난 지점
4. O0·O2 빌드와 결함 주입 검사의 원본 출력
5. 동적 메모리 할당을 허용하는 구간과 금지하는 구간, 예외·RTTI 사용 방침
6. 두 독립 실행 대상에서 확인한 섹션·심벌·재배치 수치
7. 자동 검사로 확인하지 못한 위험과 응용 과제에 쓴 시간

[학습 기록 양식](../../docs/templates/learning-note.md)을 복사해 실습별 판단과 실패 원인을 남깁니다.

```bash
mkdir -p study/g02
cp docs/templates/learning-note.md study/g02/learning-note.md
```

## GitHub 포트폴리오로 마무리하기

네 실습을 모두 통과하면 [CMake 공개 작업 공간](../../portfolio/g02-embedded-cpp-runtime-v1/README.md)에서 새 빌드 폴더로 빌드·검사·설치·예제 실행을 확인합니다. `release/g02-embedded-cpp-v1` 브랜치의 PR에는 다음 자료를 넣습니다.

- 새로 내려받은 저장소에서 재현하는 명령
- 입력 A·B와 결함 주입본 11개를 검사한 원본 출력
- 객체 수명에 관한 소유 관계도와 큐 종료 상태표
- 초기화가 끝난 뒤 동적 메모리를 할당하지 않았음을 확인한 구간
- 같은 Zig·최적화·대상으로 만든 ELF 비교표와 선택 ADR
- 개발 PC에서 실행한 항목, 오브젝트 파일만 만든 항목, 아직 실행하지 않은 보드를 구분한 범위표
- 봉인 종합 평가와 독립 검토 결과가 있다면 그 링크

자동 검사를 통과했어도 사람이 직접 구현하지 않았거나 실물 대상에서 실행하지 않은 내용은 완료로 표시하지 않습니다.
