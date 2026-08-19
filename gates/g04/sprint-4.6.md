# Sprint 4.6 — Watchdog, reset reason, flash layout

추적 대상: `OUT-XCUT-G4`, `REQ-MCU-WDG-001`, `REQ-FALLBACK-001`. `FATAL-G4.6-WDG`는 거짓 health feed, 원인 없는 reset loop, 복구 확인 전 protected flash 변경입니다.

## 시간과 기준 자료

26–32시간. IWDG/WWDG, option bytes, reset and clock control, flash programming·erase, brownout 관련 절과 board power schematic을 읽습니다. 범위는 reset 후 진단 가능성과 image layout 경계까지이며 bootloader·secure boot 적합성은 G11B에서 다룹니다.

watchdog window, reset 허용 시간, G4 산출물 인계는 [G4 실행 계약](contract.md) 4.6을 사용합니다.

## 안전한 시험 범위

Core에서는 option byte를 읽고 기록할 뿐 값을 바꾸지 않습니다. 변경·power interruption은 Stretch이며 ROM boot/SWD 복구 drill과 별도 probe를 통과한 bench에서만 수행합니다. 실제 차량 network나 공동 장비에는 연결하지 않습니다. flash endurance를 소모하는 반복은 RAM mock으로 먼저 검증합니다.

## 안내 실습

main loop가 살아 있다는 이유만으로 watchdog을 feed하지 않게 합니다. 주기 task의 health vote, 큐 진행, fatal fault 여부를 모아 window 안에서 한 번 feed하는 정책을 만듭니다. 일부 vote가 멈춘 경우 의도한 watchdog reset이 발생하고 다음 boot에서 reset reason과 마지막 health snapshot을 읽습니다.

애플리케이션, immutable metadata, crash 기록, 설정 journal, 향후 update slot을 포함한 flash layout ADR을 작성합니다. erase unit, write granularity, alignment, protection, endurance와 linker region을 연결합니다.

## 독립 실습

startup, 정상 운전, flash operation, degraded mode 각각의 watchdog window와 허용 동작을 표로 만듭니다. watchdog이 시작된 뒤 멈출 수 없는 target 특성도 정책에 반영합니다. stale vote와 counter wrap을 negative test에 넣습니다.

## 전이 과제

전이 세션에서는 initialization hang, interrupt storm, flash write 중 reset, 잘못된 reset flag clear 가운데 하나를 무작위로 뽑습니다. power cut은 전원 제어가 가능한 bench에서만 수행하고 나머지는 reset injection으로 분리합니다.

## 판정 기준

- health 조건을 만족하지 않은 경로는 watchdog feed에 도달하지 않음
- 정상·고장 reset reason이 board log와 reset register에서 구별됨
- watchdog reset 뒤 crash/health record가 CRC와 sequence 검사를 통과
- linker map과 flash layout ADR의 주소·크기·erase unit이 일치
- flash write 중 reset 결과가 사전에 정한 old/new/default 상태 중 하나임
- debug halt가 watchdog에 주는 영향을 설정과 시험 기록에 명시
- G4 새 환경 build·flash·fault replay를 다른 host에서 1회 완료

## G4 인수인계 메모

다음 세 항목 가운데 하나라도 비어 있으면 G4는 열린 상태로 둡니다.

- debugger가 watchdog을 멈춘 실행과 실제 watchdog 실행을 구분한 기록
- reset register에서 읽은 reboot 원인
- option-byte 변경 뒤 원래 image로 돌아오는 복구 절차

빠진 항목은 최소 image와 health vote 하나로 다시 확인합니다. 통과한 reset log를 G5의 watchdog 기준 입력으로 넘깁니다.
