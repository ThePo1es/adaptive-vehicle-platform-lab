# P05 — CAN–SOME/IP Vertical Slice

Status: Planned

P05는 G9에서 처음 완성하는 MCU–Linux 통신 경로입니다. P06의 작은 walking skeleton으로 사용합니다.

## 기능 범위

```mermaid
flowchart LR
    Source["MCU signal source"] --> CAN["CAN frame"]
    CAN --> Adapter["Linux CAN adapter"]
    Adapter --> Model["Vehicle data model"]
    Model --> Service["SOME/IP event"]
    Service --> Client["Client"]
```

- vehicle signal 1–3개
- CAN receive와 bounds validation
- unit·range·sequence·timestamp·quality 변환
- versioned SOME/IP event 하나
- bounded queue와 stale/unavailable policy
- cross-node correlation log

이번 release의 scope boundary는 DoIP, process manager, update, 전체 차량 signal catalog 앞에서 끝납니다.

## Interface contract

| Field | Decision |
| --- | --- |
| Signal | ID, bit layout, scaling, unit, valid range |
| Rate | expected period와 burst 조건 |
| Freshness | source sequence와 stale threshold |
| Clock | timestamp domain, offset/drift/uncertainty |
| Queue | capacity와 drop/overwrite policy |
| Version | CAN schema와 SOME/IP major/minor mapping |
| Quality | valid, stale, lost, unavailable 표현 |

## Requirements

- `REQ-CAN-001`–`REQ-CAN-004`
- `REQ-COM-001`–`REQ-COM-005`
- `REQ-TIME-001`–`REQ-TIME-003`
- `REQ-ARCH-006`

## Fault scenarios

| Fault | Expected behavior |
| --- | --- |
| truncated/invalid CAN frame | published state를 갱신하지 않고 counter 증가 |
| sequence gap | quality와 loss counter 갱신 |
| source stops | stale 뒤 unavailable 전환 |
| CAN flood | bounded queue, explicit drop, service 생존 |
| SOME/IP client restart | 재발견·재구독 뒤 최신 상태 전달 |
| clock offset change | uncertainty가 허용 범위를 넘으면 one-way latency claim 중단 |

## Completion

- two-node clean run script
- CAN과 SOME/IP packet capture
- data·time·version contract test
- latency·drop·recovery 원본 자료
- restart와 bus fault 자동 시험
- G12에서 재사용할 versioned release
