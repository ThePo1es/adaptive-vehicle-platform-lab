# Sprint 9.7 — Clock contract와 PTP 기초

## 시간과 기준 자료

24–30시간. POSIX의 [clock 요구사항](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html), linuxptp의 [`ptp4l`](https://www.linuxptp.org/documentation/ptp4l/)과 [`phc2sys`](https://www.linuxptp.org/documentation/phc2sys/) 문서를 읽습니다. hardware timestamp와 TSN scheduling은 이번 Sprint 범위에서 제외합니다.

## 시작 조건과 clock inventory

source capture, service enqueue, wire send/receive, consumer callback에 쓰는 clock을 표로 만듭니다. 각 clock의 domain, monotonic 여부, 조정 가능성, resolution, timestamp 위치, conversion 책임을 기록합니다. PTP offset 실험에는 clock이 독립된 Linux VM 두 대 또는 물리 node 두 대를 씁니다. network namespace는 host clock을 공유하므로 packet·state 연습에만 사용합니다.

## 안내 실습

한 machine에서 `CLOCK_MONOTONIC`과 `CLOCK_REALTIME`의 차이를 관찰하고 realtime 조정이 duration 계산에 들어가지 않도록 test합니다. 독립된 두 node에서 software timestamp mode의 `ptp4l` 상태와 offset log를 수집합니다. PHC가 있는 두 번째 evidence lane에서는 hardware timestamp mode와 `phc2sys`로 PHC–system clock 관계까지 확인합니다.

## 독립 실습

30분 동안 offset, frequency adjustment, path delay를 기록합니다. sync 시작 전, 안정 구간, network delay fault, sync 상실 구간을 나눠 max offset과 drift 추정치를 냅니다. P02 message에 `clock_id`, `timestamp`, `sequence`, `quality`를 넣고 unsynchronized 상태 처리 규칙을 구현합니다.

## 전이 과제

검토자가 sync daemon을 멈추거나 delay asymmetry를 넣습니다. consumer가 latency를 계속 표시할지, quality를 낮출지, sample을 제외할지 contract대로 판정합니다. clock uncertainty 상한을 만족하지 못하면 end-to-end one-way latency 대신 RTT 또는 같은 clock 구간 지연을 보고합니다.

## 판정 기준

- 모든 timestamp field에 clock domain과 capture point가 있음
- duration과 deadline은 monotonic clock으로 계산
- offset/drift 결과가 raw linuxptp log와 분석 script에서 재생됨
- software timestamp와 PHC evidence가 환경별로 분리됨
- sync loss가 data quality와 latency report에 전파됨
- one-way latency를 보고한 경우 uncertainty budget과 bound를 제시
- clock step·slew·restart 상황의 contract test 통과

## 힌트

1. clock resolution과 실제 timestamp 정확도는 같은 값이 아닙니다.
2. software timestamp 결과를 hardware timestamp 성능으로 적지 않습니다.
3. 음수 latency가 나오면 packet보다 clock path를 먼저 조사합니다.

## 치명적 실패와 보충

clock domain을 적지 않은 timestamp, realtime 기반 timeout, uncertainty 없는 두 node one-way latency는 실패입니다. 보충 과제는 같은 machine의 monotonic 구간 측정과 sync-loss state test만 다시 수행하는 것입니다.
