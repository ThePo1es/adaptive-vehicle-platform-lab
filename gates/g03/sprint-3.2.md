# 실습 3-2 — AArch64 ELF에서 오류 주소 복원하기

> 상태: `Runnable` · [장 안내](README.md) · [실행 계약](contract.md)

## 시간과 기준 자료

능동 작업 17시간, 도구 실행 4시간, 검토 대기 3시간으로 모두 24시간을 잡습니다. [Arm ABI 저장소](https://github.com/ARM-software/abi-aa)의 `aapcs64`, `aaelf64`와 `readelf`, `objdump`, `nm` 도움말을 읽습니다. 문서와 도구 버전을 원본 명세에 고정합니다.

## 시작 자료

`libvehicle.so`는 신호 해석 함수와 상태 조회 함수를 내보내며, `vehicle-cli`가 두 함수를 호출합니다. 디버그 정보가 있는 파일과 제거된 파일, 별도 디버그 파일, 링커 맵을 준비합니다.

## 안내 실습

ELF 헤더, 섹션, 세그먼트, 동적 심벌, 재배치, PLT/GOT를 순서대로 찾습니다. 원본 호출 하나가 재배치와 실행 중 주소로 이어지는 경로를 기록합니다.

## 독립 실습

주어진 오류 주소와 build ID에서 함수와 원본 코드 줄을 찾습니다. 잘못된 디버그 파일, 심벌 제거 파일, PIE/ASLR 조건을 각각 시험합니다.

## 전이 과제

처음 보는 공유 객체 하나에서 미해결 심벌 또는 ABI 불일치를 90분 안에 진단합니다. 증상, 필요한 관찰, 결론을 시간 순서대로 남깁니다.

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
