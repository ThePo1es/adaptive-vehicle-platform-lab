# Sprint 8.3 — Bounded IPC와 backpressure

## 시간과 기준 자료

24–30시간. Linux man-pages의 [`epoll(7)`](https://man7.org/linux/man-pages/man7/epoll.7.html), [`unix(7)`](https://man7.org/linux/man-pages/man7/unix.7.html), [`shm_overview(7)`](https://man7.org/linux/man-pages/man7/shm_overview.7.html), [`eventfd(2)`](https://man7.org/linux/man-pages/man2/eventfd.2.html)를 읽습니다. edge-triggered와 level-triggered 중 고른 방식을 ADR에 남깁니다.

## 시작 조건과 workload

고정 길이 32-byte 상태 record와 64KiB variable payload 두 workload를 씁니다. producer rate는 10, 100, 1,000Hz, consumer pause는 0, 50, 500ms입니다. queue capacity와 최대 message 크기는 시작 전에 고정합니다.

## 안내 실습

Unix domain socket에 길이 prefix framing과 non-blocking I/O를 구현합니다. partial read/write, peer close, `EAGAIN`, malformed length를 test합니다. `epoll` loop가 한 peer의 flood 때문에 다른 peer를 굶기지 않도록 한 cycle의 처리량을 제한합니다.

## 독립 실습

같은 record 경로를 shared memory ring buffer와 `eventfd` 알림으로 구현합니다. single-producer/single-consumer 조건, memory ordering, overwrite 정책을 문서화합니다. socket과 shared memory의 throughput, p99 전달 지연, CPU, RSS를 같은 workload로 비교합니다.

## 전이 과제

검토자가 consumer를 멈추거나 payload length를 깨거나 peer를 재시작합니다. system이 선택한 `block`, `drop-newest`, `drop-oldest`, `disconnect` 정책대로 움직이며 drop·disconnect counter가 정확히 맞아야 합니다.

## 판정 기준

- queue와 buffer가 선언한 상한을 넘지 않음
- 10분 overload 뒤 RSS 증가가 warm-up 기준 5% 이내
- partial I/O와 peer restart 뒤 framing이 다시 맞음
- accepted, processed, dropped, rejected 수의 보존식이 성립
- shared memory record에서 torn read가 0건
- raw CSV와 실행 명령으로 성능 표를 다시 생성

## 힌트

1. stream socket은 message 경계를 보존하지 않습니다.
2. shared memory의 layout version과 endian을 header에 둡니다.
3. 평균값과 함께 p50/p95/p99, 최대값, sample count를 남깁니다.

## 치명적 실패와 보충

무제한 queue, busy loop, silent drop, shared memory 크기 밖 접근이 나오면 실패입니다. 보충 과제는 Unix socket 경로만 남겨 capacity 8에서 보존식을 1,000개 생성 입력으로 확인하는 것입니다.
