# Embedded and Platform Foundations

이 문서는 Gate 학습 중 빠진 기반이 없는지 확인하는 범위표입니다. 항목을 읽었다고 체크하지 않고 code/test/measurement 링크를 붙입니다.

## Systems C

- [ ] integer promotion과 usual arithmetic conversion
- [ ] signed/unsigned overflow와 comparison
- [ ] object representation, padding, trap/indeterminate value
- [ ] effective type, strict aliasing, pointer provenance 개념
- [ ] alignment와 unaligned access
- [ ] endianness와 explicit serialization
- [ ] `volatile`/atomic/barrier의 역할 구분
- [ ] MMIO register abstraction
- [ ] stack/heap/static storage duration
- [ ] linker section과 startup initialization
- [ ] callback/state machine/ring buffer/fixed pool
- [ ] ISR-safe와 thread-safe contract 구분
- [ ] MISRA 제한의 failure rationale

## Embedded C++

- [ ] lifetime, RAII, copy/move, rule of zero/five
- [ ] `span`, `optional`, `variant`, fixed-capacity type
- [ ] smart pointer와 non-owning view 선택
- [ ] template instantiation/code bloat
- [ ] exception/RTTI/dynamic allocation policy
- [ ] custom/fixed allocator
- [ ] virtual dispatch와 static polymorphism
- [ ] thread/atomic memory ordering
- [ ] zero-copy ownership and backpressure
- [ ] ABI/name mangling/vtable/structure passing

## Cortex-M and bare metal

- [ ] vector table/reset handler/startup code
- [ ] MSP/PSP and exception frame
- [ ] NVIC priority and interrupt nesting
- [ ] fault status and crash record
- [ ] MPU region and privilege concept
- [ ] linker script and memory map
- [ ] `.text/.rodata/.data/.bss/stack/heap`
- [ ] memory-mapped peripheral and DMA
- [ ] watchdog and reset reason
- [ ] flash layout and boot selection

## AArch64 and Linux SoC

- [ ] exception level and privilege boundary
- [ ] virtual memory/page table/MMU
- [ ] cache/TLB/locality/false sharing
- [ ] DMA coherency and barrier concept
- [ ] SMP and atomics
- [ ] ELF, AAPCS, calling convention
- [ ] PLT/GOT, dynamic linker, shared library
- [ ] bootloader → kernel → userspace

## RTOS

- [ ] preemptive/cooperative scheduling
- [ ] task states and priority
- [ ] ISR/task boundary
- [ ] mutex/semaphore/queue/event/timer
- [ ] priority inversion/inheritance
- [ ] race/deadlock/starvation
- [ ] period/deadline/execution/jitter/overrun
- [ ] tick/tickless time behavior
- [ ] stack high-water mark and heap fragmentation
- [ ] watchdog and safe state
- [ ] WCET concept and measurement limits
- [ ] MPU-based task isolation

## Classic AUTOSAR concept flow

### General communication

```text
CAN Driver → CanIf → PduR → COM → RTE → SWC
```

### Diagnostics

```text
CAN Driver → CanIf → CanTp → PduR → DCM → Application
```

### Fault storage

```text
Application → DEM → NvM → Flash
```

### Module responsibility checklist

- [ ] AUTOSAR OS, RTE
- [ ] COM, PduR, CanIf, CanTp
- [ ] DCM, DEM, NvM
- [ ] EcuM, BswM, WdgM
- [ ] SecOC concept
- [ ] Flash Bootloader

## Linux/QNX systems

- [ ] process lifecycle, signal, process group
- [ ] thread scheduling, affinity, priority inversion
- [ ] `epoll`, Unix socket, shared memory, `mmap`
- [ ] TCP/UDP/multicast and backpressure
- [ ] systemd/service supervision
- [ ] resource limit and watchdog
- [ ] core dump, `gdb`, `strace`, `perf`
- [ ] cross compilation and sysroot
- [ ] Device Tree and driver model basics
- [ ] boot time, logging, tracing, observability

## Vehicle networks

### CAN

- [ ] arbitration and timing fundamentals
- [ ] error frame, error active/passive, bus-off
- [ ] CAN FD
- [ ] SocketCAN and queue behavior
- [ ] DBC signal encoding/decoding
- [ ] ISO-TP and UDS
- [ ] Network Management concept
- [ ] routing/rate/stale-data policy

### Ethernet

- [ ] VLAN/multicast
- [ ] TCP/UDP selection
- [ ] SOME/IP and SOME/IP-SD
- [ ] DoIP
- [ ] service availability and versioning
- [ ] serialization and compatibility
- [ ] E2E vs cryptographic protection
- [ ] time sync and TSN concepts

## Completion rule

체크 항목마다 가능한 경우 다음 링크를 붙입니다.

```text
Concept note → implementation → negative test → raw evidence → explanation/review
```

링크가 없으면 `Learned`가 아니라 `Unverified` 또는 `Needs practice`로 유지합니다.

