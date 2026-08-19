# Sprint 8.8 — Linux 스케줄링과 우선순위 역전

## 시간과 기준 자료

26–38시간입니다. Linux의 [`sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html), [`sched_setaffinity(2)`](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html), [`mlockall(2)`](https://man7.org/linux/man-pages/man2/mlockall.2.html), rt-tests의 [cyclictest documentation](https://wiki.linuxfoundation.org/realtime/documentation/howto/tools/cyclictest/start)을 읽습니다. kernel, CPU governor, IRQ affinity, cgroup, build profile을 실행마다 기록합니다.

## 시작할 때 고정할 것

같은 workload를 `SCHED_OTHER`, `SCHED_FIFO`, `SCHED_RR`에서 실행합니다. CPU affinity, priority, period, runtime, memory-lock 여부, background load를 표로 정합니다. VM 결과는 scheduler 기능 확인용으로만 쓰고 지연 성능 주장은 실제 대상에서 냅니다.

## 안내 실습

periodic worker의 예정 릴리스, 실제 wake-up, start, finish를 monotonic clock으로 기록합니다. CPU 부하와 memory pressure를 각각 넣어 wake-up 지연 분포를 비교합니다. 권한이 부족한 설정은 조용히 넘어가지 않고 실패 원인과 현재 policy를 남깁니다.

## 독립 실습

낮은 priority task가 mutex를 쥔 상태에서 높은 priority task가 막히고 중간 priority task가 실행되는 역전 상황을 재현합니다. 기본 mutex와 priority inheritance mutex 결과를 scheduler trace로 비교합니다. `mlockall`, page prefault, affinity 변경이 무엇을 줄이고 무엇을 보장하지 못하는지도 적습니다.

## 전이 과제

검토자가 affinity, IRQ load, mutex protocol, cgroup CPU limit 중 하나를 바꿉니다. 평균이 비슷해도 tail latency가 달라진 원인을 trace에서 찾고, 요구를 만족시키는 최소 설정 변경을 제시합니다.

## 판정 기준

- policy·priority·affinity 적용 성공 여부를 runtime에서 확인
- 지연 보고서에 p50/p95/p99, 측정 최댓값, 표본 수, workload, clock 포함
- priority inversion을 trace에서 재현하고 inheritance 전후 blocking을 비교
- `SCHED_FIFO` runaway를 막는 watchdog·CPU budget·recovery 절차가 있음
- page 고장, CPU contention, IRQ interference를 다른 실험으로 분리
- VM과 실제 대상 결과의 주장 범위를 구분
- 설정 변경 전 raw data와 trace를 보존

## 힌트

1. 높은 priority는 짧은 지연을 자동으로 보장하지 않으며 낮은 priority 작업을 굶길 수 있습니다.
2. `mlockall` 성공 뒤에도 미리 접근하지 않은 stack page가 남을 수 있습니다.
3. 평균보다 최악 구간의 scheduler trace를 먼저 확인합니다.

## 재시험 조건

policy 적용 실패를 성공으로 기록하거나, `SCHED_FIFO` task가 무한 실행될 수 있거나, VM 수치를 대상의 실시간 성능으로 제시하면 다시 측정합니다. 보강 범위는 worker 두 개와 mutex 하나로 줄입니다.
