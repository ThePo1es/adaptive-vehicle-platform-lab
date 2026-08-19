# Sprint 11.5 — 운행 시나리오에서 보증 주장까지

공통 범위와 판정 용어는 [G11B 보증 계약](assurance-contract.md), 변경 문제는 [보증 변경 입력](../../fixtures/g11/assurance-change-v1.json)을 사용합니다.

## 시간과 기준 자료

22–28시간. 처음 4시간은 item과 운행 시나리오, 8–10시간은 HARA·FMEA/FTA·TARA, 6–8시간은 요구사항과 시험 연결, 나머지는 변경 분석과 리뷰에 씁니다. ISO 26262-3:2018, ISO/SAE 21434:2021, AUTOSAR R25-11의 Communication·State·PHM 문서에서 실제로 읽은 절을 자료 장부에 남깁니다.

## 시작 입력

G7의 MCU task·watchdog·CAN 경로와 G11A의 인증 업데이트 결과를 준비합니다. 기준 경로는 `source sample → MCU task → CAN → Linux gateway → VehicleState service → actuator simulation`, top event는 `stale vehicle state가 유효한 값으로 전달됨`입니다. 합성 운행 조건과 교육용 severity·exposure·controllability 척도는 분석 시작 전에 고정합니다.

## 안내 실습

한 개의 stale source를 따라 item boundary, hazardous event, safety goal, attack path를 한 장에 배치합니다. FMEA에는 원인·local effect·end effect·탐지·대응을 적고, FTA에는 source session 재사용과 freshness 오판이 top event로 합쳐지는 최소 cut set을 만듭니다. TARA의 attacker capability와 자산은 보안 요구사항으로 이어지게 합니다.

`claim → assumption → requirement → implementation point → test → result` 식별자를 붙입니다. 같은 clock을 MCU와 Linux가 쓰는 경우에는 FMEA, FTA, TARA 세 분석에서 common cause가 어떻게 달라지는지 직접 설명합니다.

## 독립 실습

VehicleState의 speed·quality·source session·timestamp 네 field를 선택해 새 보증 묶음을 작성합니다. 정상, 늦은 frame, MCU reset 뒤 counter 재사용, clock 250 ms 역행을 실행하고 관찰자와 fallback 시점을 원본 log hash에 연결합니다. 실행 결과가 가정을 깨면 관련 claim 상태를 `Rejected`로 바꿉니다.

## 전이 과제

`SCENARIO-SPEED-001`을 열어 합성 속도와 controllability가 바뀐 뒤 영향을 받는 문서와 시험을 90분 안에 고릅니다. `unchanged_areas`에 든 signature vector까지 수정했다면 이유를 남기고, 그대로 둔 영역에는 영향이 전파되지 않는 경계를 적습니다.

## 판정 기준

- item, 운행 시나리오, top event, 합성 척도의 판과 commit이 고정됨
- hazardous event에서 safety goal, safety requirement, 실행 시험까지 끊기지 않음
- FMEA와 FTA가 freshness·session·clock의 서로 다른 실패 조합을 다룸
- TARA에 attacker capability, trust boundary, security requirement, negative test가 연결됨
- `SCENARIO-SPEED-001`의 기대 영향 6개와 유지 영역을 모두 검토함
- 모든 결과가 Supported·Provisional·Rejected 가운데 하나이고 근거 공백이 드러남
- 실제 차량 적용이나 ISO 적합성으로 넓힌 문구가 결과물에 없음

## 다시 좁혀 볼 때

hazard와 attack path가 같은 원인 목록으로 끝나거나 claim에서 raw log까지 추적되지 않으면 speed field 하나만 남깁니다. 정상·stale·MCU reset 세 입력으로 표를 다시 만들고, 누락된 연결을 새 식별자와 함께 재시험합니다.
