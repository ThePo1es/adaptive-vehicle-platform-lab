# Sprint 6.8 — P00-B CAN/진단 릴리스

추적 대상: `OUT-XCUT-G6`, `REQ-CAN-001`–`REQ-CAN-007`, `REQ-ECU-DIAG-001`–`REQ-ECU-DIAG-003`. `FATAL-G6.8-RELEASE`는 physical·simulation 근거 혼합 또는 malformed 입력의 last-valid 훼손입니다.

## 시간과 기준 자료

28–34시간. Sprint 6.1–6.7의 자료 명세, vcan 입력 모음, [G6 bench contract](bench-contract.md), timing model, packet oracle을 release candidate와 함께 동결합니다. ISO 적합성 표기는 실제 원문 접근과 검토 범위에 맞춰 `Provisional` 또는 더 좁은 로컬 주장으로 둡니다.

P00-B 입력·120분 시험·릴리스 근거는 [G6 실행 계약](contract.md) 6.8에 묶습니다.

## 릴리스 구성

P00-A task/큐/watchdog를 그대로 유지하고 CAN driver, CAN timing, ISO-TP, read-focused UDS를 추가합니다. build·flash·vcan replay·physical replay·report 명령과 코드/image/시험 입력 SHA-256을 release manifest에 넣습니다.

## 안내 실습

synthetic signal이 CAN/CAN FD frame에서 애플리케이션 값으로 들어오고, read DID와 DTC query로 조회되는 경로를 한 correlation ID로 추적합니다. normal, malformed, 큐 포화, timeout, bus-off scenario의 packet·controller·task·애플리케이션 상태를 맞춥니다.

## 독립 실습

새 host와 초기화한 board 두 대에서 릴리스를 재현합니다. vcan 실행과 실장비 실행은 별도 디렉터리에 저장하고, scope가 없는 analog 주장은 `Unverified`로 유지합니다. 검토자는 원시 packet과 counter에서 요약을 다시 계산합니다.

## 전이 과제

봉인된 fault는 DLC/len, ISO-TP timer, UDS session, bus-off recovery 중 하나입니다. 120분 안에 처음 깨진 불변 조건을 찾고 수정한 뒤 다른 seed로 regression을 실행합니다.

## 판정 기준

- P00-A timing·watchdog regression이 모두 통과
- packet→controller→transport→dispatcher→애플리케이션 추적 기록이 이어짐
- malformed frame와 transport error 뒤 last-valid state가 보존됨
- bus-off unavailable·recovery limit·delay가 physical bench에서 확인됨
- vcan/API, controller, analog 주장이 근거 묶음별로 표시됨
- 시험 입력의 출처·license·hash와 새 환경 재현 기록이 있음
- 검토자가 봉인 고장과 packet 요약을 독립 확인

## P00-B 판정 보류

P00-B 태그는 세 경우에 보류합니다: vcan으로 physical bus-off를 증명한 경우, ISO 원문 확인 없이 적합성을 적은 경우, P00-A deadline이 깨진 경우.

원인이 있는 근거 묶음만 떼어내 최소 시험으로 다시 확인합니다. 나머지 합격 자료는 그대로 보존하고 새 고장을 사용합니다.
