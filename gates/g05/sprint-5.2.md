# Sprint 5.2 — 고정 우선순위 응답시간 분석

추적 대상: `OUT-XCUT-G5`, `REQ-RTOS-003`. `FATAL-G5.2-RTA`는 jitter·blocking·interrupt interference 누락이나 ISR 중복 합산으로 schedulable을 잘못 판정한 경우입니다.

## 시간과 기준 자료

26–32시간. Joseph·Pandya와 Tindell·Burns·Wellings 논문의 고정 우선순위 response-time analysis, blocking, release jitter, arbitrary deadline 절을 읽습니다. [G5 실행 계약](contract.md) 5.2의 네 기대값을 hand worksheet와 calculator가 각각 구해야 합니다.

## 계산 계약

각 task `i`에 대해 `C_i`, `B_i`, `J_i`, `T_i`, `D_i`와 higher-priority 집합을 versioned input으로 둡니다. recurrence의 초기값, ceil 경계, 수렴 조건, deadline 초과 중단 조건을 명시합니다. interrupt interference를 task interference에 중복 합산하지 않게 모델을 한 번만 배정합니다.

## 안내 실습

작은 task set을 손으로 두 번 반복 계산한 뒤 같은 입력을 읽는 독립 calculator를 만듭니다. 결과에는 iteration별 값, 최종 bound, slack, schedulable 판정이 나옵니다. exact multiple, zero jitter, large blocking, non-convergence vector를 unit test로 고정합니다.

## 독립 실습

Sprint 5.1 task set을 분석합니다. priority assignment의 근거와 shared resource에서 나온 blocking bound를 연결하고, end-to-end path에는 task response와 communication delay를 중복 없이 합칩니다. 분석 가정과 실제 RTOS 설정의 차이를 표로 남깁니다.

## 전이 과제

처음 보는 task set을 90분 안에 계산합니다. 검토자는 period보다 긴 deadline, 같은 priority, bursty ISR 중 하나를 포함합니다. 사용한 분석이 해당 조건을 지원하지 않으면 판정을 유보하고 맞는 모델을 선택합니다.

## 판정 기준

- 손 계산, calculator, 검토자 oracle이 기준 벡터에서 같은 결과를 냄
- integer arithmetic과 ceil division이 overflow·경계 test를 통과
- blocking과 interrupt interference의 출처가 task model에 연결됨
- recurrence가 수렴하지 않거나 deadline을 넘을 때 명시적으로 종료
- 분석 가정과 RTOS priority/interrupt 설정의 차이가 0건이거나 gap으로 기록
- 변경된 task set의 영향받는 task를 자동으로 다시 계산
- raw input, tool commit, output hash가 보고서에 있음

## 계산이 어긋났을 때 남길 것

- 가장 작은 반례와 각 반복 단계의 손 계산
- 모델을 잘못 고른 것인지, 계산기 구현이 틀린 것인지에 대한 판정
- 수정 전후 출력 hash

이 세 가지가 모이면 전체 task set을 다시 계산합니다. 기대값에 맞추려고 recurrence 자체를 바꾼 결과는 채점에서 제외합니다.
