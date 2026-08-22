# Sprint 8.9 — PREEMPT_RT 비교 실험

## 시간과 기준 자료

32–42시간을 잡습니다. Linux kernel의 [Real-time preemption documentation](https://docs.kernel.org/next/core-api/real-time/index.html), rt-tests, `trace-cmd`, timerlat 문서를 사용합니다. 같은 kernel 릴리스와 toolchain에서 일반 preemption 구성과 PREEMPT_RT 구성을 만들고, 의도한 config 차이를 manifest로 남깁니다.

## 비교 설계

두 image의 kernel version, compiler, rootfs, CPU governor, firmware, thermal 조건, IRQ affinity, workload를 맞춥니다. PREEMPT_RT 외의 config 차이는 diff와 이유를 기록합니다. QEMU에서는 boot와 기능 시험만 하고, 지연 비교는 같은 실제 AArch64 대상에서 번갈아 실행합니다.

## 안내 실습

idle, CPU load, memory pressure, network·storage I/O 조건에서 cyclictest와 timerlat을 실행합니다. warm-up, run duration, priority, interval, histogram 범위를 먼저 고정합니다. worst sample 주변의 scheduler·IRQ trace를 따로 보관합니다.

## 독립 실습

각 image에서 세 번 이상 반복해 run 간 분산과 thermal 상태를 확인합니다. 측정 최댓값을 WCET로 부르지 않습니다. PREEMPT_RT가 tail을 줄인 구간, 변화가 없거나 악화된 구간, 측정으로 설명할 수 없는 구간을 나눠 씁니다. P01/P03의 실제 workload도 한 번 포함합니다.

## 전이 과제

전이 실행에서는 background workload나 IRQ affinity가 바뀝니다. 기존 결론이 유지되는지 다시 계산하고, 달라졌다면 어느 조건에만 유효한 결론인지 보고서를 고칩니다. kernel config와 trace만 받아 재현하는 사람도 같은 요약값을 만들 수 있어야 합니다.

## 판정 기준

- 두 image가 같은 source 릴리스와 명시된 config delta에서 재현됨
- 실제 대상에서 동일한 측정 절차를 번갈아 세 번 이상 수행
- 원본 histogram·trace에서 보고서 수치를 다시 생성
- thermal throttling, governor, IRQ affinity, logging overhead를 기록
- measured worst, 통계적 tail, 분석 상한을 서로 다른 용어로 사용
- P01/P03 workload에서 scheduler 선택이 lifecycle deadline에 미치는 영향 설명
- 제3자가 image hash, config, command로 결과 하나를 재생

## 참고할 함정

- PREEMPT_RT build가 성공했다는 사실만으로 deadline 충족을 증명할 수 없습니다.
- 서로 다른 board나 kernel version 결과는 정면 비교 자료로 쓰지 않습니다.
- 가장 나쁜 sample을 지운 경우에는 제거 규칙과 원본을 함께 남겨야 합니다.
- hardware·firmware의 System Management 동작은 kernel trace 밖에 있을 수 있습니다.

## PREEMPT_RT 비교 보류

QEMU 수치로 대상 latency를 주장하거나, kernel·workload가 다른 결과를 PREEMPT_RT 효과로 해석하거나, 원본 trace를 버리면 이 Sprint를 닫지 않습니다. 보강 시 idle과 단일 CPU-load 조건만 남겨 비교 설계를 다시 검증합니다.
