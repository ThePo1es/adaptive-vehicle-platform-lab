# Performance Report: Scenario

## Question and acceptance criterion

- Question:
- Requirement:
- Threshold or comparison target:

## Environment

| Item | Value |
| --- | --- |
| Commit SHA |  |
| Hardware |  |
| OS / kernel |  |
| Compiler / flags |  |
| Build type |  |
| Network |  |
| Background load |  |
| Target clock / frequency |  |
| RTOS / configuration |  |
| Measurement clock / probe |  |

## Workload

- Warm-up:
- Duration:
- Sample count:
- Event/request rate:
- Payload size:
- Repetitions:

## Results

| Metric | p50 | p95 | p99 | Max | Unit |
| --- | ---: | ---: | ---: | ---: | --- |
| End-to-end latency |  |  |  |  | ms |
| Discovery time |  |  |  |  | ms |
| Recovery time |  |  |  |  | ms |

### MCU / RTOS timing

| Task / ISR | Period | Deadline | Releases | p50 exec | p95 exec | p99 exec | Worst exec | Max jitter | Misses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|  |  |  |  |  |  |  |  |  |  |

| Bounded resource | Configured capacity | Peak / high-water | Drops / overflow | Margin | Policy |
| --- | ---: | ---: | ---: | ---: | --- |
| Task stack |  |  |  |  |  |
| ISR-to-task queue |  |  |  |  |  |
| CAN RX/TX queue |  |  |  |  |  |
| Static/heap memory |  |  |  |  |  |

| Resource | Idle | Under load | Peak | Unit |
| --- | ---: | ---: | ---: | --- |
| CPU |  |  |  | % |
| RSS |  |  |  | MiB |
| Drops |  |  |  | count |

## Method and raw data

```bash
# 빌드, 실행, 측정, 요약을 재현하는 명령
```

- Raw data:
- Analysis script:
- Visualization:
- Timestamp overhead / resolution check:

## Interpretation

- Budget decision:
- Supported claim:
- Measurement limit:
- Next experiment:

## Threats to validity

- simulator와 target hardware 결과가 구분되어 있는가?
- timer resolution, probe overhead, cache/warm-up과 clock drift를 확인했는가?
- measured worst와 analytical/WCET bound를 별도 필드에 기록했는가?
- cross-node timestamp의 clock domain, offset, drift와 uncertainty를 기록했는가?
- interrupt/background load와 release policy가 실제 workload를 대표하는가?
