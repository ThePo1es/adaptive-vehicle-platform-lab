# G3 실행 계약

## 도구와 대상

| 항목 | 고정 값 |
| --- | --- |
| Python | 3.12.13 |
| ELF 판독 | pyelftools 0.32 |
| 기본 C 도구 | Zig 0.15.2, Clang 20.1.2 |
| ARM32 공통 대상 | Cortex-M4, Thumb, AAPCS32, soft-float, freestanding relocatable ELF |
| GNU 비교 도구 | Arm GNU Toolchain 14.3.Rel1 (`arm-none-eabi-gcc` 14.3.1) |
| AArch64 분석 | freestanding relocatable ELF, 외부 호출 재배치와 DWARF |

G3.4에서 Clang과 GCC는 같은 C 입력, Cortex-M4, Thumb, AAPCS32, soft-float, `-ffreestanding -fno-builtin -O2 -c` 계약으로만 비교합니다. 드라이버마다 CPU 이름 표기가 달라도 뜻은 같아야 합니다. 실행 파일, 런타임, cycle, cross-LTO 순위는 보드 근거가 없으므로 비교하지 않습니다.

## 공식 GNU 아카이브 고정

파일명과 배포 해시는 [Arm GNU Toolchain 14.3.Rel1 공식 다운로드](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)의 SHA-256 sidecar에서 확인했습니다.

| 호스트 | 파일 | SHA-256 |
| --- | --- | --- |
| Linux x86_64 | `arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi.tar.xz` | `8f6903f8ceb084d9227b9ef991490413014d991874a1e34074443c2a72b14dbd` |
| Windows x86_64 | `arm-gnu-toolchain-14.3.rel1-mingw-w64-x86_64-arm-none-eabi.zip` | `864c0c8815857d68a1bbba2e5e2782255bb922845c71c97636004a3d74f60986` |

파일명, 해시, 설치 루트, 버전 중 하나라도 맞지 않으면 resolver는 실패로 닫힙니다. 자동 설치나 `PATH` 대체 탐색을 하지 않습니다. 이때 G3.4는 `Provisional`이며 GCC 수치를 만들지 않습니다.

## 실습별 독립 판정

| 실습 | 자동 판정 | 사람이 설명할 것 |
| --- | --- | --- |
| G3.1 | EM_ARM, DWARF, `mix4`·caller 심벌, 실제 branch-and-link | r0–r3와 stack의 다섯 번째 인자, caller/callee-save |
| G3.2 | EM_AARCH64, 외부 호출 재배치, build ID 일치, runtime-load bias 계산 | section/segment 차이, PLT가 GOT를 거치는 이유, DWARF의 역할 |
| G3.3 | Clang LLVM IR, Thumb 어셈블리, 컴파일 시간 경계 oracle, A·B defined case 일치 | `poison`·wrap flag와 UB 관찰의 분리 |
| G3.4 | 두 EM_ARM 재배치 ELF와 `.text` 크기, 동일 대상 계약 | 중간 표현 이름을 섞지 않고 차이가 없는 결과도 기록 |
| G3.5 | 양성 1개와 누락 조건별 음성 대조군, `upstream_submitted=false` | 보고하지 않기로 한 판단도 근거와 함께 기록 |

## 입력과 결함 주입

공개 A·B는 `fixtures/g03/input-a.tsv`, `input-b.tsv`입니다. 봉인 C는 평가자가 별도 보관합니다. 기준 구현에는 다음 결함을 하나씩 넣어 판정기가 잡는지 확인합니다.

| ID | 결함 | 잡아야 하는 판정 |
| --- | --- | --- |
| 101 | caller에서 실제 `mix4` 호출 제거 | 호출 심벌·branch-and-link 없음 |
| 201 | AArch64 export와 외부 호출 제거 | 심벌·재배치 없음 |
| 301 | 경계 갱신을 덧셈으로 바꿈 | 컴파일 시간 defined-input oracle 실패 |
| 401 | `crc_step` 심벌 제거 | 공통 ELF 비교 계약 실패 |
| 501 | 제출하지 않은 upstream 보고를 `true`로 기록 | no-fake-upstream 대조군 실패 |

## G3.2 주소 복원 계약

오류 주소는 `link_address = runtime_address - load_bias`로 복원하되, 바이너리와 separate debug file의 build ID가 먼저 같아야 합니다. section의 파일 offset과 load segment의 가상 주소를 같은 값으로 취급하지 않습니다. 외부 함수 호출은 호출 재배치가 PLT 엔트리를 고르고 PLT가 GOT 슬롯을 통해 해석된 주소로 이동하는 흐름으로 설명합니다. DWARF는 복원한 링크 주소를 소스 줄에 연결할 때 사용합니다.

## G3.3 정의된 입력 계약

동등성 판정에는 C 언어 계약에서 정의된 입력만 넣습니다. signed overflow, 범위 밖 shift, 잘못된 정렬·수명·별칭을 포함한 입력은 별도의 UB 관찰로 남기며 두 결과가 같거나 다르다는 사실로 컴파일러 결함을 판정하지 않습니다. GCC 산출물을 LLVM IR이라고 부르지 않습니다.

## 즉시 보류

- 대상 삼중항, CPU, Thumb, AAPCS, float ABI 중 하나가 빠진 비교
- 다른 build ID의 debug file로 소스 줄 확정
- section과 load segment 또는 runtime 주소와 link 주소 혼동
- 보드 없이 runtime·cycle·cross-LTO 우열 주장
- source UB를 optimizer/backend 결함으로 보고
- 재현·축소·문서 근거·중복 검색·peer review 없이 upstream 제출 주장
