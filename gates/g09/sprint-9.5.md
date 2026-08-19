# Sprint 9.5 — 부하, backpressure, 재연결

## 시간과 기준 자료

24–30시간. [performance report 양식](../../docs/templates/performance-report.md), P02의 time/availability contract, Linux의 [`ss(8)`](https://man7.org/linux/man-pages/man8/ss.8.html)와 [`tc-netem(8)`](https://man7.org/linux/man-pages/man8/tc-netem.8.html)을 읽습니다. 측정 전 CPU governor, affinity, build profile, logging level을 고정합니다.

## 시작 조건과 실험 행렬

10Hz/100Hz, UDP/TCP, payload 32/512/1,400 byte, normal/slow consumer 조합을 최소 행렬로 사용합니다. 추가 fault는 loss 0/1/5%, delay 0/10/50ms, reorder 0/1%, provider restart입니다. run마다 warm-up, 측정 시간, seed, sample count를 적습니다.

## 안내 실습

같은 host의 monotonic clock으로 source enqueue부터 consumer callback까지 구간 지연을 측정합니다. p50/p95/p99/max, throughput, drop, duplicate, gap, CPU, RSS, socket queue를 raw CSV와 함께 저장합니다. instrumentation overhead를 빈 payload run으로 추정합니다.

## 독립 실습

`tc netem`과 consumer pause로 손실·지연·backpressure를 만듭니다. UDP와 TCP에서 나타나는 drop, head-of-line blocking, reconnect 차이를 측정합니다. freshness limit을 넘긴 event는 폐기하고 sequence gap과 transport drop을 가능한 범위에서 구분합니다.

## 전이 과제

검토자가 workload와 queue capacity를 바꿉니다. 시작 전에 기대하는 병목과 합격 상한을 써 두고 실행 뒤 차이를 설명합니다. tuning은 원본 run을 보존한 다음 별도 commit에서 합니다.

## 판정 기준

- 모든 요약 수치가 추적 가능한 raw row와 script에서 생성됨
- sample count, clock, 구간 시작·끝, warm-up이 보고서에 명시됨
- 10분 overload 뒤 RSS와 queue가 설정 상한 안에 머묾
- accepted/processed/dropped/rejected/expired count의 보존식 성립
- provider restart 뒤 recovery time과 중복·누락 수를 보고
- UDP/TCP 선택을 실제 workload 결과와 service 요구사항으로 설명

## 힌트

1. 같은 machine 구간 측정과 두 node end-to-end 측정을 분리합니다.
2. log I/O가 병목이면 logging level별 결과를 따로 냅니다.
3. p99 sample이 충분한지 총 sample count를 확인합니다.

## 치명적 실패와 보충

서로 다른 clock을 보정 없이 빼거나, raw data를 버리거나, overload 중 memory가 계속 자라면 실패입니다. 보충 과제는 같은 host 10/100Hz와 slow consumer 세 run만 다시 측정하는 것입니다.
