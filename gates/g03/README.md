# Arm 프로그램의 함수 호출부터 기계어까지 추적하기

> 관리 코드: G3 · 권장 학습 순서: 4번째 · 현재 준비 상태: `Runnable`

이 장에서는 C 함수 하나를 호출 지점에서 시작해 ARM 레지스터, ELF 재배치, LLVM IR, 대상 기계어까지 거꾸로 추적합니다. 서로 다른 대상이나 ABI의 숫자를 섞어 순위를 만들지 않고, 자동 검사가 확인한 사실과 실제 보드에서 아직 확인하지 못한 사실을 구분하는 것이 핵심입니다.

## 이 장에서 완성하는 것

| 실습 | 결과 | 상태 |
| --- | --- | --- |
| [3-1 ARM32 함수 호출 경로 추적하기](sprint-3.1.md) | Cortex-M4 AAPCS32 호출 경로 표 | Runnable |
| [3-2 AArch64 ELF에서 오류 주소 복원하기](sprint-3.2.md) | load bias·build ID·DWARF·PLT/GOT 복원 기록 | Runnable |
| [3-3 C에서 LLVM IR과 기계어까지 연결하기](sprint-3.3.md) | 정의된 입력 차등 판정과 IR·Thumb 산출물 | Runnable |
| [3-4 같은 ARM 대상에서 GCC와 Clang 공정하게 비교하기](sprint-3.4.md) | 동일 Cortex-M4 계약의 재배치 ELF 비교 | Runnable |
| [3-5 컴파일러 문제로 의심되는 사례를 최소 예제로 줄이고 신고 여부 판단하기](sprint-3.5.md) | 양·음성 대조군과 동료 검토 결정 | Runnable |

## 고정 도구와 비교 경계

Python 3.12.13, `pyelftools` 0.32, Zig 0.15.2의 Clang 20.1.2를 사용합니다. G3.1·G3.3·G3.4의 ARM 계약은 Cortex-M4, `thumb-freestanding-eabi`, AAPCS32, soft-float, 재배치 ELF입니다. GCC 비교에만 공식 Arm GNU Toolchain 14.3.Rel1을 사용합니다. 운영체제·보드 실행, cycle·latency, cross-LTO 결과는 이 장에서 검증하지 않습니다.

G3.4는 저장소의 플랫폼 명세에 고정된 공식 아카이브를 SHA-256으로 확인하고 해시별 캐시에 안전하게 푼 뒤, 그 안의 GCC만 실행합니다. 아카이브가 없거나 해시·대상·버전이 다르면 시스템 `PATH`의 GCC로 대신하지 않고 실패합니다.

시작하기 전에 [G3 입구 진단과 B-TOOL 보강](../../docs/gate-entry-diagnostics.md)을 먼저 확인합니다. 작은 ELF에서 함수 주소와 섹션·세그먼트 관계를 설명하지 못하면 B-TOOL 자체 점검을 마친 뒤 이 장으로 돌아옵니다.

## 시작하기

```bash
mkdir -p study/g03/src
cp labs/g03_compiler_analysis/starter/* study/g03/src/

G03_TRUSTED_LOCAL_EXECUTION=1 \
G03_SUBMISSION_ROOT=study/g03/src \
G03_LAB_ID=G3.1 \
uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g03_compiler_analysis.run_harness
```

PowerShell에서는 네 환경 변수를 `$env:G03_LAB_ID = "G3.1"` 같은 형식으로 먼저 지정합니다. 시작 코드는 의도적으로 판정을 통과하지 않습니다. 제3자가 보낸 C 코드를 이 검사기로 바로 실행하지 말고 자격 증명과 네트워크가 없는 일회용 환경에서 확인합니다.

## 공개 입력 A·B와 전체 검사

```bash
G03_LAB_ID=G3.ALL uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g03_compiler_analysis.run_harness

G03_LAB_ID=G3.RETEST uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g03_compiler_analysis.run_harness
```

입력 A·B는 [공개 입력 설명](../../fixtures/g03/README.md)에 있습니다. `defined=false` 행은 UB 관찰이며 최적화 동등성이나 컴파일러 결함 판정에서 제외합니다. 기준 구현과 결함 주입본은 검사기 자체를 검증할 때만 사용합니다.

## GNU 비교를 여는 방법

플랫폼 명세에 고정된 공식 아카이브를 다음 명령으로 준비합니다. 검사기는 내려받은 파일의 SHA-256을 확인한 뒤 경로 탈출을 거부하며 해시별 캐시에 직접 풉니다.

```bash
uv run --project toolchain --locked \
  python -m labs.g03_compiler_analysis.toolchain --download
```

Windows x86_64 ZIP과 Linux x86_64 tar.xz의 URL·파일명·해시는 [플랫폼 명세](../../toolchain/g03-arm-gnu.json)에 있습니다. 임의로 압축을 푼 폴더나 시스템 `PATH`의 GCC는 사용하지 않습니다.

## GitHub 포트폴리오 흐름

다섯 실습 기록을 [G3 포트폴리오 양식](../../portfolio/g03-compiler-analysis-v1/README.md)에 모읍니다. `study/g03-call-to-machine` 브랜치에서 작업하고, PR에는 입력 A·B 출력, 도구 버전, ARM 계약, 생성 명령, 주소 복원 계산, defined/UB 분리표, GNU 비교 상태, 아직 실행하지 않은 보드 범위를 함께 올립니다. 실제로 제출하지 않은 upstream issue URL이나 받은 적 없는 reviewer 의견을 적지 않습니다.

## 완료로 쓰지 않는 것

- 재배치 ELF 생성 결과를 Cortex-M4 보드 실행 결과로 표현
- 서로 다른 CPU·ABI·float ABI·최적화의 크기나 속도를 직접 순위 비교
- IR 모양이나 오브젝트 크기로 runtime·cycle·캐시 영향을 확정
- GNU 아카이브가 검증되지 않은 상태에서 G3.4를 완료로 표시
- UB 차이를 컴파일러 결함이나 최적화 동등성 실패로 분류
- peer review 전 실제 upstream 제출을 했다고 기록
