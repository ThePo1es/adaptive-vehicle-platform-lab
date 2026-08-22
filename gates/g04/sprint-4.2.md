# Sprint 4.2 — Clock tree와 단조 시간

추적 대상: `OUT-XCUT-G4`, `REQ-MCU-TIME-001`. `FATAL-G4.2-TIME`은 역행하거나 출처·rate를 모르는 timestamp를 timing 근거로 사용한 경우입니다.

## 시간과 기준 자료

24–30시간. 선택한 silicon의 RCC, flash latency, power control, SysTick, general-purpose timer 절과 clock errata를 읽습니다. 설정 도구의 그림은 출발점으로만 쓰고 register 값과 실제 입력 clock을 근거로 남깁니다.

동결할 입력과 10,000-edge 판정은 [G4 실행 계약](contract.md)의 4.2 행에 있습니다.

## 측정 준비

보드에서 확인 가능한 oscillator, debugger clock 영향, timer output pin을 정합니다. logic analyzer의 sample rate와 자체 오차를 기록하고, firmware timestamp와 외부 측정의 관찰 지점을 맞춥니다.

## 안내 실습

reset clock에서 시작해 목표 system clock으로 전환합니다. oscillator ready, PLL lock, flash wait-state, bus prescaler 순서를 상태기로 만들고 각 단계에 timeout과 안전한 fallback을 둡니다. timer output compare로 1 kHz 신호를 내보내 계산값과 logic analyzer 결과를 비교합니다.

32-bit counter의 wrap을 건너는 단조 clock을 구현합니다. read 중 overflow, ISR 지연, clock 전환이 timestamp에 미치는 영향을 시험하고 tick rate·단위·wrap period를 interface 문서에 적습니다.

## 독립 실습

SysTick과 한 개의 hardware timer로 같은 주기 event를 만들고 10,000개 interval의 분포를 비교합니다. debugger 정지 중 clock이 멈추는지, 저전력 또는 clock 입력 변경이 counter에 어떤 흔적을 남기는지도 확인합니다.

## 전이 과제

PLL multiplier나 bus prescaler 하나가 잘못된 image를 진단합니다. 검토자는 기대 주파수를 알려 주지 않고 UART baud 오차, timer period, clock status register만 제공합니다. 원인을 좁힌 계산표와 측정 trace를 남깁니다.

## 판정 기준

- clock tree의 모든 입력·분주·곱셈 값이 register dump와 일치
- 1 kHz 출력의 허용오차를 측정기 오차와 oscillator 사양에서 도출
- clock 준비 실패가 timeout 뒤 기록된 fallback으로 끝남
- 단조 clock이 wrap 경계와 concurrent read 시험을 통과
- timestamp schema에 clock 입력, rate, unit, wrap, uncertainty가 있음
- debugger 연결 여부에 따른 결과를 분리해 기록

## 측정값을 보류하는 경우

외부 파형과 계산값의 차이가 선언한 오차를 넘은 실행은 결과표에서 뺍니다. reset clock 하나로 계측 경로를 점검한 뒤 prescaler를 한 단계씩 되붙입니다. 차이가 처음 나타난 설정과 원시 파형을 짝지어 재시험 기록에 남깁니다.
