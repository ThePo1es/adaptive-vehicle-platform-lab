# Sprint 9.9 — 시계 계약과 PTP 기초

## 시간과 기준 자료

24–32시간. POSIX의 [clock 요구사항](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html), linuxptp의 [`ptp4l`](https://www.linuxptp.org/documentation/ptp4l/)과 [`phc2sys`](https://www.linuxptp.org/documentation/phc2sys/) 문서를 읽습니다. hardware timestamp와 TSN scheduling은 이번 Sprint 범위에서 제외합니다.

## 시작 조건과 clock inventory

입력 캡처, 서비스 큐 삽입, 전송·수신, consumer callback에 쓰는 시계를 표로 만듭니다. 각 시계의 영역, 단조 증가 여부, 조정 가능성, 해상도, timestamp 위치, 변환 책임을 기록합니다. 두 VM 실험은 프로토콜과 상태 머신 확인용이며 독립 시계 성능 근거로 사용하지 않습니다. offset·drift 성능은 서로 다른 물리 노드 또는 명시적인 합성 시계 모델에서만 주장합니다. network namespace는 호스트 시계를 공유합니다.

## 안내 실습

한 machine에서 `CLOCK_MONOTONIC`과 `CLOCK_REALTIME`의 차이를 관찰하고 realtime 조정이 duration 계산에 들어가지 않도록 테스트합니다. 두 node에서는 guest NTP·hypervisor time sync를 끄고 L2 multicast 경로, capability, linuxptp config를 고정합니다. PHC가 있는 환경에서는 hardware timestamp mode와 `phc2sys`로 PHC–system clock 관계를 확인합니다.

## 독립 실습

30분 동안 offset, frequency adjustment, path delay를 기록합니다. sync 시작 전, 안정 구간, network delay 고장, sync 상실 구간을 나눠 max offset과 drift 추정치를 냅니다. P02 message에 `clock_id`, `timestamp`, `sequence`, `quality`를 넣고 unsynchronized 상태 처리 규칙을 구현합니다.

## 전이 과제

검토자가 sync daemon을 멈추거나 delay asymmetry를 넣습니다. consumer가 latency를 계속 표시할지, quality를 낮출지, sample을 제외할지 contract대로 판정합니다. clock uncertainty 상한을 만족하지 못하면 end-to-end one-way latency 대신 RTT 또는 같은 clock 구간 지연을 보고합니다.

## 판정 기준

- 모든 timestamp field에 clock domain과 capture point가 있음
- duration과 deadline은 monotonic clock으로 계산
- offset/drift 결과가 raw linuxptp log와 분석 script에서 재생됨
- software timestamp와 PHC 결과가 환경별로 분리됨
- sync loss가 data quality와 latency report에 전파됨
- one-way latency를 보고한 경우 uncertainty budget과 bound를 제시
- clock step·slew·restart 상황의 contract 테스트 통과

## 시계 자료 확인

1. clock resolution만으로 실제 timestamp 정확도를 정하지 않습니다.
2. software timestamp 결과를 hardware timestamp 성능으로 적지 않습니다.
3. 음수 latency가 나오면 packet보다 clock path를 먼저 조사합니다.

## 주장 범위를 줄이는 경우

timestamp의 시계 영역이 없거나 timeout이 realtime 기준이거나 불확실성 없는 두 노드 단방향 지연을 제시했다면 성능 주장을 철회합니다. 같은 장비의 monotonic 구간 측정과 동기 상실 상태 테스트만 다시 수행합니다.
