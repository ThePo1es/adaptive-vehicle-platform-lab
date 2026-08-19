# Embedded and Platform Foundations

이 표는 개념 목록 대신 Gate별 결과를 확인합니다. 각 Outcome에는 구현, negative test, 원본 evidence, reviewer 결과를 연결합니다.

| ID | Gate | Outcome | Evidence link | Status |
| --- | --- | --- | --- | --- |
| OUT-C-01 | G1 | 정수·정렬·endianness 경계를 지키는 serialization | — | Not started |
| OUT-C-02 | G1 | bounds·lifetime·aliasing 계약이 있는 parser | — | Not started |
| OUT-C-03 | G1 | 명시적 overflow 정책을 가진 bounded storage | — | Not started |
| OUT-C-04 | G1 | MMIO·ISR·thread 경계를 구분한 API | — | Not started |
| OUT-XCUT-G1 | G1 | parser misuse case와 입력 경계 기록 | — | Not started |
| OUT-CPP-01 | G2 | owner와 non-owning view의 수명이 검증된 message path | — | Not started |
| OUT-CPP-02 | G2 | heap·exception·RTTI 정책과 binary 영향 보고서 | — | Not started |
| OUT-CPP-03 | G2 | race와 backpressure를 자동 시험하는 runtime | — | Not started |
| OUT-XCUT-G2 | G2 | 소유권 침해와 race의 failure path 기록 | — | Not started |
| OUT-ABI-01 | G3 | AAPCS32/64와 ELF symbol을 source까지 추적 | — | Not started |
| OUT-ABI-02 | G3 | source→LLVM IR→machine code→measurement 보고서 | — | Not started |
| OUT-XCUT-G3 | G3 | compiler·ABI 가정과 깨지는 조건 기록 | — | Not started |
| OUT-MCU-01 | G4 | reset·startup·linker·main 경로가 동작하는 image | — | Not started |
| OUT-MCU-02 | G4 | interrupt·fault·watchdog 원인과 상태 기록 | — | Not started |
| OUT-MCU-03 | G4 | clock·timer·peripheral 측정과 errata 검토 | — | Not started |
| OUT-XCUT-G4 | G4 | debug·boot·key 신뢰 경계 기록 | — | Not started |
| OUT-RT-01 | G5 | 요구에서 도출한 task model과 response-time analysis | — | Not started |
| OUT-RT-02 | G5 | timing·stack·queue 원본 자료와 overload 정책 | — | Not started |
| OUT-RT-03 | G5 | priority inversion·blocking hidden fault 진단 | — | Not started |
| OUT-XCUT-G5 | G5 | deadline miss와 fallback 선택 근거 | — | Not started |
| OUT-CAN-01 | G6 | physical CAN timing·load·bus-off evidence | — | Not started |
| OUT-DIAG-01 | G6 | ISO-TP timer matrix와 UDS read interoperability | — | Not started |
| OUT-XCUT-G6 | G6 | 진단 권한과 flood misuse case 시험 | — | Not started |
| OUT-CP-01 | G7 | communication vertical slice | — | Not started |
| OUT-CP-02 | G7 | diagnostic vertical slice | — | Not started |
| OUT-CP-03 | G7 | DTC·persistent restore vertical slice | — | Not started |
| OUT-XCUT-G7 | G7 | E2E·SecOC 적용 지점과 남은 보장 기록 | — | Not started |
| OUT-LNX-01 | G8 | pidfd·cgroup 기반 process containment와 bounded recovery | — | Not started |
| OUT-LNX-02 | G8 | image·kernel·DT·service clean build | — | Not started |
| OUT-LNX-03 | G8 | core/syscall/performance 도구를 사용한 incident 진단 | — | Not started |
| OUT-LNX-04 | G8 | scheduling policy·priority inversion·PREEMPT_RT 비교 근거 | — | Not started |
| OUT-XCUT-G8 | G8 | privilege·resource 제한과 우회 시험 | — | Not started |
| OUT-NET-01 | G9 | Service Interface와 generated Proxy/Skeleton contract | — | Not started |
| OUT-NET-04 | G9 | SOME/IP/SD availability·version·reconnect packet evidence | — | Not started |
| OUT-NET-02 | G9 | DoIP read path와 CAN–SOME/IP vertical slice | — | Not started |
| OUT-NET-03 | G9 | clock offset·drift·uncertainty가 있는 time contract | — | Not started |
| OUT-XCUT-G9 | G9 | network service와 diagnostic gateway 위협 시나리오 | — | Not started |
| OUT-AP-01 | G10 | manifest dependency와 lifecycle manager | — | Not started |
| OUT-AP-02 | G10 | state decision·process action·health observation 분리 | — | Not started |
| OUT-AP-03 | G10 | Diagnostics transport·router·provider 책임 분리 | — | Not started |
| OUT-AP-04 | G10 | official release와 local behavior mapping | — | Not started |
| OUT-XCUT-G10 | G10 | authenticated principal·policy·audit 구현과 책임 매핑 | — | Not started |
| OUT-ASSURE-01 | G11B | 교육용 HARA·FMEA와 safety evidence | — | Not started |
| OUT-ASSURE-02 | G11A | TARA·trust boundary와 update negative corpus | — | Not started |
| OUT-ASSURE-03 | G11A | transfer·staging·activation·rollback evidence | — | Not started |
| OUT-SYS-01 | G12 | cross-node data·time·state·version contract | — | Not started |
| OUT-SYS-02 | G12 | budget과 10개 이상 fault campaign | — | Not started |
| OUT-SYS-03 | G12 | 제3자 clean reproduction과 design defense | — | Not started |

## 상태

`Not started`, `Learning`, `Evidence ready`, `Provisional`, `Validated`, `Needs refresh`만 사용합니다. `Validated`에는 reviewer와 commit을 함께 적습니다.

## 세부 범위

Outcome의 세부 학습 항목과 Sprint 순서는 [Gate Playbook](gate-playbook.md)에서 관리합니다.
