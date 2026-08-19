# G5 실행 계약

G5는 [합성 task set](../../fixtures/g05/task-set-v1.yml)을 공통 입력으로 씁니다. 우선순위 숫자는 클수록 높고, 모든 시간값의 단위는 µs입니다. 실제 project 수치는 별도 설정으로 옮기며 v1 결과를 덮어쓰지 않습니다.

## 시간표

| Sprint | Core | Gate 근거 | Stretch | Active 합계 | 별도 wall time |
| --- | ---: | ---: | ---: | ---: | --- |
| 5.1 | 15–18h | 7–8h | 0–2h | 22–28h | 요구 검토 대기 제외 |
| 5.2 | 18–21h | 8–9h | 0–2h | 26–32h | calculator replay 3회 |
| 5.3 | 15–18h | 7–8h | 0–2h | 22–28h | 추적 capture 1h 이하 |
| 5.4 | 18–22h | 8–10h | 0–2h | 26–34h | build·flash 별도 |
| 5.5 | 15–18h | 7–8h | 0–2h | 22–28h | 100,000-event capture |
| 5.6 | 18–21h | 8–9h | 0–2h | 26–32h | soak 8–24h |
| 5.7 | 16–18h | 8h | 0–2h | 24–28h | 시험 210분·검토 대기 별도 |

## Sprint별 동결값

| Sprint | 시작 파일·시험 입력 | 기계 판정과 허용 범위 | 산출물 진화 |
| --- | --- | --- | --- |
| 5.1 | `fixtures/g05/task-set-v1.yml`, G4 `board-runtime-v1` | schema 필수 field 누락 0; 단위 없는 시간 0; 네 task의 utilization·deadline 표 생성 | G4 timer/ISR → versioned task model |
| 5.2 | task-set-v1, 두 논문의 recurrence, 독립 hand worksheet | response bound가 sensor 100, control 480, communication 1120, diagnostics 1850 µs; integer overflow와 non-convergence를 명시적 오류로 반환 | task model에 analytical bound 추가 |
| 5.3 | 세-task inversion seed, Zephyr v4.4.0 mutex capability 표 | PI 설정에서 high task blocking이 measured critical section + 10% 계측 오차 안; lock-order cycle 100% 탐지 | RTA의 `B_i`와 runtime lock policy 연결 |
| 5.4 | `p00-a/prj.conf`, static thread/큐 skeleton, virtual-clock overload 입력 모음 | 큐 capacity 32, heap allocation 0, `released = completed + active + missed`; deadline miss 후 fallback 1 period 이내 | G4 main loop → P00-A task set; G4 fault/watchdog 유지 |
| 5.5 | cycle-counter/timer calibration vector, wrap 시험 입력, 100,000 event seed | timestamp 역행 0; `produced = decoded + buffered + dropped + corrupt`; 추적 on/off overhead와 counter frequency 보고 | analytical field에 raw distribution 연결 |
| 5.6 | phase×interrupt-rate×seed matrix, 정상/overrun image | 분석 bound 초과 run 0개가 합격으로 분류됨; unknown reset 0; 같은 seed의 first failure 재현 | P00-A acceptance workload와 raw 근거 완성 |
| 5.7 | 초기화한 board manifest, 바뀐 task set, 봉인 scheduling fault | 빈 환경 build·flash, RTA·추적 기록 동시 갱신, 봉인 fault 원인과 regression 확인 | `P00-A` tag → G6의 CAN/diagnostic task가 같은 모델을 확장 |

## 결과 파일

task model, RTA iteration log, RTOS 설정, 원시 binary 추적 기록, decoder, stack·큐 report, soak matrix, image/설정 SHA-256을 한 release ID로 묶습니다. 5.2 계산값 또는 5.5 계측 clock이 달라지면 뒤 Sprint 결과는 보존하고 새 contract version으로 재시험합니다.
