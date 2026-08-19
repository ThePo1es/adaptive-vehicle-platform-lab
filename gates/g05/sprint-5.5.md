# Sprint 5.5 — 계측기를 먼저 계측하기

추적 대상: `OUT-XCUT-G5`, `REQ-RTOS-001`, `REQ-RTOS-006`, `REQ-TIME-001`. `FATAL-G5.5-MEASURE`는 clock rate·wrap·observer loss를 모르는 trace로 timing 합격을 내린 경우입니다.

## 시간과 기준 자료

22–28시간. Cortex-M DWT cycle counter, 선택 timer, Zephyr timing API, 추적 backend 문서를 읽습니다. target에서 구현되지 않거나 debug 권한에 의존하는 counter는 capability table에 표시합니다.

100,000-event 입력과 유효 run 판정은 [G5 실행 계약](contract.md) 5.5에 고정합니다.

## calibration 질문

timestamp 한 번, 추적 event 한 번, buffer flush 한 번의 비용을 각각 어떻게 잴지 정합니다. clock source가 달라지는 low-power 구간과 32-bit wrap도 계획에 포함합니다.

## 안내 실습

빈 function, 고정 cycle loop, GPIO pulse를 이용해 cycle counter와 hardware timer를 교차 확인합니다. instrumentation on/off 두 image를 같은 workload로 반복해 평균, p95, measured worst와 sample count를 기록합니다. UART 출력 시간은 측정 구간 밖으로 옮깁니다.

binary 추적 기록에는 event ID, task/ISR identity, timestamp, sequence와 overflow counter만 둡니다. concurrent writer가 있다면 commit marker 또는 single-writer queue로 torn record를 막습니다.

## 독립 실습

Sprint 5.4 task의 release jitter, execution time, response time, stack high-water mark를 수집합니다. counter wrap을 강제로 짧게 만든 test와 추적 buffer 포화 test를 추가합니다. host 분석 script가 원시 기록과 summary를 함께 보존하게 합니다.

## 전이 과제

counter frequency 변경, 추적 buffer 절반, debug detach를 각각 새 run에 적용합니다. 잘못된 단위와 조용한 기록 손실은 자동 self-check가 잡아야 합니다.

## 판정 기준

- clock 입력·frequency·wrap·정지 조건이 target별로 기록됨
- instrumentation overhead와 flush overhead가 분리되어 있음
- 추적 기록의 `produced = decoded + buffered + dropped + corrupt` 보존식이 성립
- wrap과 concurrent write corpus를 decoder가 처리
- stack high-water 결과에 fill pattern 방법과 blind spot을 명시
- raw binary, decoder version, 요약 hash로 결과 재생 가능

## 계측 유효성 판정

runtime에서 확인한 counter frequency와 overflow 횟수를 원시 기록 첫머리에 둡니다. 둘 중 하나가 없으면 그 실행은 성능 표에서 `Invalid`로 표시합니다.

복구 시험은 GPIO pulse와 event 한 종류로 시작합니다. 외부 측정기와 timestamp 차이의 상한을 다시 구한 뒤에만 나머지 event를 활성화합니다.
