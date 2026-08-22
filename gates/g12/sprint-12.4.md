# Sprint 12.4 — 20 ms 예산과 자원 장부

이 Sprint의 기준 경로와 20 ms 배분은 [P06 통합 계약](contract.md)에 있습니다. 숫자를 바꾸는 결정은 ADR로 남기고 fixture도 같은 변경에서 갱신합니다.

## 시간과 측정 준비

26–34시간. 예산 tree와 계산기 7–9시간, 계측점 삽입 7–9시간, 부하 matrix 8–10시간, 조정과 리뷰 4–6시간입니다. MCU cycle counter, CAN controller timestamp, Linux monotonic clock의 해상도와 오차를 먼저 측정합니다.

## 안내 실습

fixture의 여섯 allocation을 읽어 합계가 20,000 µs인지 재계산합니다. owner, 시작·종료 event, clock domain, percentile, sample count를 각 구간에 붙입니다. clock domain을 건너는 구간은 offset과 uncertainty를 결과에 함께 냅니다.

CPU, stack·heap, CAN load, socket queue, storage에도 별도 budget을 만듭니다. 한 자원을 아끼면서 다른 자원 사용량이 늘어난 경우 같은 run에서 함께 비교합니다.

## 독립 실습

10 Hz·100 Hz VehicleState와 idle·CPU load·CAN flood 조합을 최소 30회씩 실행합니다. raw sample을 보존하고 median, p95, p99, maximum, miss count를 계산합니다. 각 구간의 실측과 end-to-end 결과를 합계 계산과 대조합니다.

## 전이 과제

gateway decode가 4 ms에서 6 ms로 늘고 network 구간이 1 ms를 쓰는 workload를 받습니다. 최적화, 표본 주기 조정, 기한 변경 가운데 하나를 선택해 ADR과 새 예산을 제시합니다.

## 판정 기준

- 여섯 구간에 owner·두 event·clock domain·측정 오차가 있고 합계가 정확히 20,000 µs임
- SIM과 HW 결과가 다른 run manifest에 저장됨
- 부하 조합별 raw sample, 표본 수, percentile, 최대값, miss 수가 남음
- CPU·memory·network·storage 장부가 timing run과 같은 release를 가리킴
- 예산 초과가 ADR의 선택과 회귀 시험으로 이어짐
- end-to-end 값과 구간 합계의 차이가 uncertainty 안에서 설명됨

## 수치가 맞지 않을 때

서로 다른 시계를 뺀 결과와 원본 표본이 없는 백분위 값은 보고서에서 제외합니다. 복구 순서는 동일 시계의 두 구간 측정, 계측 오차 재산정, 전체 경로 재시험입니다.
