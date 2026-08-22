# Safety and Cybersecurity Engineering

이 작업은 G1부터 누적합니다. Adaptive 보안과 UCM은 G11A에서 구현하고, MCU/Classic까지 포함한 보증 검토는 G11B에서 마칩니다. 결과물은 교육과 설계 연습용이며 확인 범위는 README에 맞춥니다.

## Gate별 누적 작업

| Gate | Safety 작업 | Cybersecurity 작업 |
| --- | --- | --- |
| G1–G2 | bounds, invariant, failure response | parser attack surface, misuse case |
| G3–G4 | compiler·ABI 가정, fault record | debug interface, image·key boundary |
| G5 | deadline miss와 fallback 요구 | task isolation, diagnostic surface |
| G6–G7 | communication fault, DTC, E2E 개념 | diagnostic authorization, flood, SecOC 개념 |
| G8–G10 | process containment, resource budget | principal, privilege, service policy, audit |
| G11A | update state·health·rollback consistency | TARA, package trust, key policy, secure update |
| G11B | HARA·FMEA/FTA·assurance case | cross-domain trust chain과 common-cause review |
| G12 | cross-node safety argument | end-to-end attack·recovery campaign |

## Safety work products

### 1. Item definition

- 기능과 사용 환경
- 외부 actor와 물리적 경계
- 정상 상태와 degraded/fallback 상태
- driver·vehicle·bench 가정
- 다루는 기능과 제외 범위

### 2. 교육용 HARA

| Field | Example question |
| --- | --- |
| Hazard | 어떤 오동작이 위험한가? |
| Operational situation | 언제, 어떤 환경에서 발생하는가? |
| Severity | 잠재 피해의 크기는 어느 정도인가? |
| Exposure | 그 상황에 노출될 가능성은 어느 정도인가? |
| Controllability | 사람이 상황을 통제할 가능성은 어느 정도인가? |
| Safety goal | 어떤 위험 동작을 막아야 하는가? |
| Assumptions | 이 판단에 필요한 외부 조건은 무엇인가? |

ASIL 분류는 개념 학습용으로만 사용합니다. 실제 분류에는 조직의 item 정의, 차량 맥락, 전문가 판단과 독립 검토가 필요합니다.

### 3. Safety requirement

요구사항에는 stimulus, precondition, response, time bound, tolerance, 검증 방법을 넣습니다. `safe state`라는 이름은 hazard 분석과 안전 목표가 있을 때 사용합니다. 그 전에는 `fallback state` 또는 `defined output state`로 기록합니다.

### 4. FMEA와 FTA

FMEA에는 component failure, local effect, system effect, detection, control, residual effect를 적습니다. FTA는 중요한 top event 하나를 고르고 공통 원인과 조합 fault를 확인합니다.

### 5. Freedom from interference

다음 간섭 경로를 검토합니다.

- CPU와 scheduling
- memory와 DMA
- network bandwidth와 queue
- persistent storage
- logging과 diagnostic traffic
- update·startup 중 resource contention

격리 효과를 기록할 때는 정책 문서, 설정, 고장 주입 시험, 측정 결과를 함께 연결합니다.

### 6. Assurance case

작은 주장–논리–근거 구조를 사용합니다. Safety case 문헌의 `claim–argument–evidence`에 대응합니다.

```text
주장: 특정 운행 조건에서 stale data가 actuator simulation에 사용되지 않는다.
논리: timestamp·sequence·quality 계약과 fallback transition이 stale data를 차단한다.
근거: requirement, state model, unit test, end-to-end 고장 주입 시험, timing trace.
가정: clock uncertainty가 정해진 상한 안에 있고 input source가 정상 timestamp를 제공한다.
남은 결손: 실제 actuator와 차량 환경은 시험 범위 밖이다.
```

## Cybersecurity work products

### 1. Asset와 boundary

- 실행 image와 configuration
- signing key와 trust anchor
- firmware minimum version
- diagnostic 권한과 caller identity
- vehicle data의 authenticity·integrity·availability
- audit log와 update journal

각 asset의 owner, 저장 위치, 변경 주체, 신뢰 경계를 적습니다.

### 2. 교육용 TARA

| Field | Content |
| --- | --- |
| Threat scenario | 공격자가 원하는 결과 |
| Entry point | packet, package, debug port, local process 등 |
| Preconditions | 필요한 접근과 권한 |
| Attack path | boundary를 넘는 단계 |
| Impact | safety, operation, finance, privacy 영향 |
| Control | prevention, detection, response, recovery |
| Verification | negative test, policy test, review |
| Residual risk | 남은 공격 가능성과 가정 |

### 3. Update assurance tiers

| Tier | 보장 범위 | 필수 증거 |
| --- | --- | --- |
| T0 File installer | 파일 배치와 기본 오류 처리 | install/uninstall test |
| T1 Crash-consistent updater | 중단 뒤 defined state 복구 | kill-at-each-state, journal model |
| T2 Authenticated updater | package authenticity와 integrity | canonical encoding, signature/hash corpus |
| T3 Rollback-protected chain | boot authenticity와 monotonic version | verified root, protected counter, key policy |
| T4 Production lifecycle study | provisioning, rotation, revocation, recovery | 조직·장비·PKI 절차 검토 |

P04 core는 T1을 완성한 뒤 T2를 구현합니다. T3는 선택한 board가 제공하는 immutable root와 보호 저장소를 실제로 사용할 수 있을 때 통과 처리합니다.

### 4. 필수 negative corpus

- malformed, duplicate, unknown, oversized manifest field
- non-canonical encoding과 integer boundary
- payload truncation, hash mismatch, signature mismatch
- path traversal, absolute path, symlink, hard link, TOCTOU
- unknown·revoked key와 잘못된 target
- lower version, replay, interrupted monotonic-state update
- disk/flash full, short write, corrupted journal
- crash와 전원 중단을 각 상태 전이 전후에 주입

## Review 절차

G11을 `Validated`로 닫으려면 safety reviewer와 security reviewer가 서로 다른 사람이어야 합니다. 한 사람만 검토했다면 두 관점을 모두 기록해도 상태는 `Provisional`로 남깁니다.

Safety 검토자는 hazard–goal–requirement–근거 연결과 fallback의 타당성을 봅니다. Security 검토자는 attacker capability, trust root, key·identity·rollback 가정과 negative corpus를 봅니다. 두 사람이 공통 원인, update 중 상태, diagnostic access가 safety argument에 주는 영향을 함께 검토합니다.

## 표준 읽기

- [ISO 26262 road vehicles — functional safety](https://www.iso.org/standard/68383.html)
- [ISO/SAE 21434 road vehicles — cybersecurity engineering](https://www.iso.org/standard/70918.html)
- AUTOSAR release 자료와 관련 functional cluster 문서
- UNECE software update·cybersecurity regulation의 공개 원문

읽은 edition, 절, 접근 권한, 확인 날짜를 [references.md](references.md)의 Source Manifest에 기록합니다. 접근하지 못한 normative text의 세부 요구사항은 `Unverified`로 남깁니다.
