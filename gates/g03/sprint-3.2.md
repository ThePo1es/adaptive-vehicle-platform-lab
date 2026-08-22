# Sprint 3.2 — AAPCS64와 ELF

## 시간과 기준 자료

24–30시간. [Arm ABI repository](https://github.com/ARM-software/abi-aa)의 `aapcs64`, `aaelf64`와 사용 중인 binutils의 `readelf`, `objdump`, `nm` 도움말을 읽습니다. 문서와 tool version을 source manifest에 고정합니다.

## 시작 fixture

`libvehicle.so`는 signal decode와 상태 조회 함수를 export하고, `vehicle-cli`가 두 함수를 호출합니다. Debug·stripped binary, separate debug file, linker map을 준비합니다.

## 안내 실습

ELF header, section, segment, dynamic symbol, relocation, PLT/GOT를 순서대로 찾습니다. source call 하나가 relocation과 runtime address로 이어지는 경로를 기록합니다.

## 독립 실습

주어진 crash address와 build ID에서 함수와 source line을 찾습니다. 잘못된 debug file, stripped symbol, PIE/ASLR 조건을 각각 시험합니다.

## 전이 과제

처음 보는 shared object 하나에서 unresolved symbol 또는 ABI mismatch를 90분 안에 진단합니다. 증상, 필요한 관찰, 결론을 시간 순서대로 남깁니다.

## 판정 기준

- section과 load segment를 구분하고 주소 변환을 계산
- dynamic symbol과 local/debug symbol의 차이를 실제 binary에서 확인
- build ID와 정확한 debug artifact를 사용해 crash를 symbolization
- AAPCS64 argument/return 규칙을 call site와 callee 양쪽에서 확인

## 힌트

1. 파일 offset, virtual address, runtime address를 한 표에 넣습니다.
2. `readelf -l`, `-S`, `-r`, `-Ws` 결과를 서로 연결합니다.
3. crash 주소만 있으면 load bias가 필요한지 먼저 확인합니다.

## 주소 계산 재시험

다른 빌드의 debug file로 소스 줄을 확정했거나 section과 segment를 한 개념으로 설명했다면 PIE를 끈 작은 실행 파일로 돌아갑니다. 파일 offset, virtual address, load bias를 손으로 맞춘 뒤 원래 core를 다시 봅니다.
