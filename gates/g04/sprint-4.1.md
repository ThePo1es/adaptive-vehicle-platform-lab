# Sprint 4.1 — Reset에서 `main`까지

추적 대상: `OUT-XCUT-G4`, `REQ-MCU-START-001`. `FATAL-G4.1-START`는 잘못된 stack/vector나 초기화되지 않은 C runtime으로 application을 실행한 경우입니다.

## 시간과 기준 자료

22–28시간. G0에서 고른 MCU와 보드의 데이터시트, reference manual, startup file, linker 문서, errata를 고정합니다. 기본 대상은 NUCLEO-G474RE의 STM32G474RE입니다. Arm Cortex-M4 Devices Generic User Guide의 programmer's model·exception model·vector table 절도 함께 읽습니다.

시작 파일, 수치 판정, 시간 배분, 산출물 계보는 [G4 실행 계약](contract.md)의 4.1 행을 사용합니다.

## 먼저 확인할 것

초기 stack pointer와 reset vector를 16진수로 읽고, 두 값이 어느 메모리 구간을 가리켜야 하는지 설명합니다. 답을 못 하면 ELF section, VMA/LMA, reset sequence를 작은 host 예제로 다시 확인합니다.

## 안내 실습

vendor startup file을 한 줄씩 지우며 최소 image를 만듭니다. 직접 작성한 vector table, reset handler, linker script로 `.data`를 flash에서 RAM으로 옮기고 `.bss`를 0으로 만든 뒤 `main`에 진입합니다. UART가 준비되기 전에는 GPIO와 debugger watchpoint를 부팅 표식으로 씁니다.

map file에서 vector table, code, constants, initialized data, zero-initialized data, stack, heap 영역을 찾아 메모리 그림과 대조합니다. reset 직후와 `main` 직전의 SP·PC·VTOR·주요 section 경계를 캡처합니다.

## 독립 실습

vendor startup object를 link에서 제외한 깨끗한 target을 하나 더 만듭니다. C runtime 초기화 값은 서로 다른 pattern을 사용해 copy와 zero를 눈으로 구분할 수 있게 합니다. orphan section, stack/heap 충돌, RAM 범위 초과를 link 단계에서 막습니다.

## 전이 과제

전이용 linker 설정에는 flash origin, RAM 크기, vector alignment 가운데 하나가 바뀌어 있습니다. link-time assertion 또는 이른 boot 진단으로 문제를 잡고, 수정 전후 map과 첫 20개 명령의 disassembly를 제출합니다.

## 판정 기준

- vector[0]과 vector[1]이 선택한 target의 유효한 SP·Thumb reset 주소를 가리킴
- `.data` 초기값과 `.bss` zeroing을 debugger와 firmware self-test가 함께 확인
- vendor startup object 없이 빈 환경 build·flash·reset 재현
- map에 설명하지 못한 allocatable section과 겹치는 memory region이 없음
- linker assertion이 RAM 초과와 stack reserve 침범을 build에서 차단
- 코드 revision, toolchain, linker flags, image SHA-256, board ID가 기록됨

## 부팅이 멈췄을 때 확인 순서

1. reset handler에 breakpoint가 걸리는지 본다.
2. SP, PC, fault status, memory map을 차례로 대조한다.
3. `main` 진입과 section 초기화를 각각 확인한다.

이 네 가지가 정리된 뒤 UART와 주변 장치를 다시 붙입니다. 먼저 UART를 손대면 초기화 실패와 출력 실패를 구분하기 어렵습니다.
