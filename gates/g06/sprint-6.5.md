# Sprint 6.5 — ISO-TP sender, flow control, timer

추적 대상: `OUT-XCUT-G6`, `REQ-ECU-DIAG-002`. `FATAL-G6.5-ISOTP-TX`는 timer 의미 오류나 late frame이 재사용 channel을 훼손한 경우입니다.

## 시간과 기준 자료

24–30시간. Sprint 6.4와 같은 ISO edition을 사용합니다. BS, STmin, wait-frame 처리, sender/receiver timer 이름과 시작·중지 지점을 원문 접근 범위 안에서 표로 옮깁니다.

BS·STmin·timer 경계값과 산출물 계보는 [G6 실행 계약](contract.md) 6.5에 고정했습니다.

## timer matrix

각 state에 expected event, timeout, late-event 처리, counter, 다음 state를 적습니다. STmin `0x00–0x7F`와 `0xF1–0xF9`, reserved 값, BS=0을 edition에 맞춰 해석합니다. 구현 또는 Linux stack이 지원하지 않는 wait-frame 송신 기능은 gap으로 남깁니다.

## 안내 실습

virtual clock 기반 sender가 FF 뒤 FC를 기다리고 BS마다 멈추며 STmin보다 빠르지 않게 CF를 보냅니다. timeout, Overflow FC, invalid STmin, excessive wait를 corpus로 주입합니다. wall-clock sleep은 상태기 unit test에서 사용하지 않습니다.

## 독립 실습

sender와 receiver를 크기가 정해진 channel table로 통합합니다. late FC/CF가 재사용된 channel의 새 transfer를 건드리지 않게 generation identity를 둡니다. backpressure가 애플리케이션 큐와 transport buffer에 어떻게 전파되는지 counter로 확인합니다.

## 전이 과제

BS, STmin, timer, concurrent peer 가운데 두 값이 달라진 fixture를 받습니다. packet timeline과 내부 상태 timeline을 대조해 첫 위반을 찾고 같은 seed로 수정 전후를 재생합니다.

## 판정 기준

- timer start/stop과 timeout transition이 versioned matrix와 일치
- STmin code와 실제 send interval을 virtual clock으로 경계 검사
- BS=0, Overflow, reserved STmin, wait limit의 정책이 명시됨
- late frame이 generation이 다른 transfer를 훼손하지 않음
- channel·큐·payload memory 상한과 full response가 있음
- sender/receiver pair와 Linux differential test 결과가 재현됨

## 시간 판정의 경계

host scheduler 지연은 protocol timer의 의미를 증명하지 못합니다. late frame 때문에 실행마다 결과가 달라진 자료도 합격 근거에서 뺍니다.

timer matrix는 virtual clock과 channel 하나에서 다시 확인합니다. board에서는 같은 경계값의 실제 지연만 따로 재고 두 결과를 한 표에 섞지 않습니다.
