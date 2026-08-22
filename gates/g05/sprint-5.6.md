# Sprint 5.6 — Stress, phase sweep, soak

추적 대상: `OUT-XCUT-G5`, `REQ-RTOS-004`, `REQ-RTOS-006`, `REQ-ARCH-002`. `FATAL-G5.6-STRESS`는 분석 bound 초과나 설명되지 않은 reset을 합격 자료에서 제외하지 않은 경우입니다.

## 시간과 기준 자료

26–32시간. 이전 Sprint의 task model, RTA 결과, instrumentation calibration을 시험 기준선으로 씁니다. soak 시간은 wall time으로, 설정·분석·수정 시간은 active time으로 따로 기록합니다.

phase matrix, 합격 run 분류, 8–24시간 soak는 [G5 실행 계약](contract.md) 5.6에서 관리합니다.

## workload matrix

정상, 최대 periodic load, diagnostic burst, interrupt storm, 큐 포화, clock drift, 한 task overrun을 행으로 둡니다. 각 행에 seed, phase, duration, expected deadline/drop/fallback을 적습니다.

## 안내 실습

periodic task의 initial phase를 systematic하게 움직이고 ISR rate를 단계별로 올립니다. 각 run에서 deadline miss, response-time measured worst, 큐 high-water, drop, stack margin, watchdog outcome을 수집합니다. first failure 직전과 직후 설정을 보존합니다.

짧은 exhaustive phase sweep와 긴 soak를 구분합니다. soak는 memory/stack/sequence leak를 찾고, worst-case를 증명하는 자료로 과장하지 않습니다. 모든 random run은 seed와 generator commit으로 다시 실행됩니다.

## 독립 실습

최소 8시간 wall-time campaign을 설계하고 unattended failure 뒤에도 마지막 유효 trace와 reset reason이 남도록 합니다. 보드 전원·debugger 재연결 실패는 product fault와 다른 결과로 분류합니다.

## 전이 과제

봉인 workload는 task phase, burst length, priority 중 두 값을 바꿉니다. RTA 상한과 측정 결과의 차이를 분석하고 모델 누락, 계측 오차, 구현 결함 가운데 어디에 해당하는지 근거와 함께 적습니다.

## 판정 기준

- workload마다 입력, seed, duration, 기대 결과가 versioned file에 있음
- 같은 seed와 image로 first failure 재현
- measured response가 분석 bound를 넘으면 release가 자동 차단됨
- 추적 기록 유실 때문에 sample이 사라진 run을 성능 합격 자료에서 제외
- stack margin·큐 high-water·watchdog 결과가 모든 run에 있음
- active time과 soak wall time을 분리해 기록
- unattended reset 뒤 image와 reset reason을 식별 가능

## 장시간 시험 운용 규칙

전원·probe 문제와 firmware fault를 구분할 수 없거나 추적 기록 유실이 처음 잡힌 시점에서 시험을 중단합니다. 그 뒤의 수치는 보고서에 합치지 않습니다.

다음 실행은 짧은 duration과 같은 seed를 사용합니다. 관찰 경로가 안정되면 10분, 1시간, 목표 시간 순으로 늘리고 각 구간의 image·reset reason을 확인합니다.
