# G11B 교차 도메인 보증 계약

G11B는 G7의 MCU/Classic 결과와 G11A의 Adaptive 보안·업데이트 결과를 한 주장 체계로 묶습니다. 대상 기능은 격리된 벤치의 VehicleState gateway와 actuator simulation입니다. 실제 차량 제어, 형식 승인, ISO 인증은 범위에 넣지 않습니다.

## 시간과 산출물

Sprint 11.5–11.7의 집중시간 합계는 62–80시간입니다. 검토자가 답을 기다리는 시간과 hardware 예약 대기는 별도로 기록합니다.

| Sprint | 집중시간 | 주 결과 |
| --- | ---: | --- |
| 11.5 | 22–28h | item, HARA, FMEA/FTA, TARA, 요구사항과 근거 연결 |
| 11.6 | 24–32h | T1/T2/T3 trust claim과 physical power-cut·storage evidence |
| 11.7 | 16–20h | safety/security 독립 검토, 반대 의견 처리, P04 보증 릴리스 |

## 고정 주장 경로

`source sample → MCU task → CAN → Linux gateway → VehicleState service → actuator simulation`

기준 top event는 `stale vehicle state가 유효한 값으로 전달됨`입니다. freshness, clock uncertainty, source session, quality, fallback transition을 함께 봅니다. 업데이트 경로에서는 새 버전이 이 네 계약을 바꾸는 경우를 별도 change case로 다룹니다.

## 주장 상태

| 상태 | 필요한 내용 |
| --- | --- |
| Supported | 범위·가정이 적힌 주장, 연결된 요구사항, 실행한 시험, 전체 commit SHA, 두 검토자의 관련 의견 |
| Provisional | 논리는 있으나 원문 접근·실장·검토자·power-cut 중 하나가 비어 있음 |
| Rejected | 시험이 주장을 반박했거나 trust assumption이 성립하지 않음 |

T3 표기는 immutable trust root, 보호된 monotonic state, 실제 boot/recovery chain을 같은 target에서 확인한 경우에만 씁니다. 프로세스 kill 시험과 전원 차단 시험은 결과 표의 열을 나눕니다.

## 변경 입력

[assurance-change-v1.json](../../fixtures/g11/assurance-change-v1.json)의 세 사례를 사용합니다.

- 운행 속도와 controllability 가정 변경
- MCU와 Linux가 함께 의존하는 시계의 역행
- boot trust root와 보호된 monotonic state 제거

변경 사례마다 영향 목록과 `unchanged_areas`를 모두 검토합니다. 무조건 전체 문서를 고치는 방식과 한 문서만 고치는 방식은 모두 오답입니다.

## 검토 책임

- safety 검토자: hazard–goal–requirement–시험 연결, fallback, 잔여 위험
- security 검토자: attacker capability, key·identity·rollback 가정, negative corpus
- 공동 검토: common cause, update 중 상태, diagnostic access가 safety 주장에 미치는 영향

두 역할은 서로 다른 사람이 맡습니다. 사람을 구하지 못한 실행은 `Provisional`로 남기고, 누락된 검토 역할과 재검토 조건을 명세에 적습니다.

## 자료 기준선

- [ISO 26262-3:2018](https://www.iso.org/standard/68385.html)과 합법적으로 접근한 관련 part
- [ISO/SAE 21434:2021](https://www.iso.org/standard/70918.html)
- [UN Regulation No. 155](https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security)
- [UN Regulation No. 156](https://unece.org/transport/documents/2021/03/standards/un-regulation-no-156-software-update-and-software-update)
- AUTOSAR R25-11 UCM, Cryptography, IAM, Execution, State, PHM 문서

접근한 판과 절, 확인 날짜는 자료 장부에 남깁니다. 공개 초록만 읽은 항목은 원문을 읽은 것처럼 표시하지 않습니다.
