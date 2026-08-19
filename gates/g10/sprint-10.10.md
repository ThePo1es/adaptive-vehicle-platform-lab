# Sprint 10.10 — Adaptive 설계 심사와 P03 릴리스

## 시간과 기준 자료

18–20시간. R25-11 standards ledger, [AUTOSAR mapping](../../docs/autosar-mapping.md), [mastery review](../../docs/templates/mastery-review.md), P01–P03 근거를 사용합니다. 시험 시작 전에 공개 scenario와 비공개 고장 manifest의 hash를 기록합니다.

## 릴리스 입력

릴리스 후보는 네 묶음으로 정리합니다.

- 실행물: source tag, AArch64 image, SBOM
- 설정과 검증: manifest schema, 오류 입력 모음, 상태·health·policy model 테스트
- 통합 근거: SOME/IP capture, diagnostic audit, persistency kill campaign
- 문서: architecture, AUTOSAR mapping, 알려진 한계

## 안내 실습

30분 demo에서 다음 흐름을 재현합니다.

1. manifest validation과 dependency startup
2. Function Group에 대응시킨 로컬 상태 transition
3. VehicleStateService discovery와 이벤트
4. missed heartbeat 감지와 bounded recovery
5. 프로세스 restart 뒤 persisted 상태 복구
6. clean shutdown과 프로세스 inventory 확인

## 독립 실습·심사

구술 검토에서는 Service Interface/Proxy·Skeleton, SOME/IP binding, Execution Manifest, lifecycle, State Management, PHM, Persistency, Diagnostics, IAM 중 세 영역을 받습니다. 답변마다 근거가 된 R25-11 section, 대응 코드와 시험, 구현에서 생략한 기능을 함께 제시합니다.

## 전이 과제 — 비공개 고장

책임 배치가 잘못된 결함 하나를 120분 안에 분석합니다. 예시는 State Controller가 프로세스를 직접 재시작함, health monitor가 상태를 결정함, logical address를 principal로 신뢰함, old 프로세스 heartbeat가 새 instance에 들어옴입니다. 수정 전에는 책임을 어느 component로 옮길지와 이를 고정할 regression 테스트를 먼저 제시합니다.

## 판정 기준

- public scenario 전체가 릴리스 artifact에서 재현
- 책임이 처음 잘못 배치된 지점을 찾고 회귀 테스트를 먼저 작성해 수정
- P01–P03 requirement와 근거 link가 끊기지 않음
- R25-11 mapping의 각 `Mapped` 항목을 자격 있는 검토자가 section으로 확인
- 검토 자격이 부족한 영역은 로컬 동작 `Validated`, AUTOSAR mapping `Provisional`로 기록
- 제3자가 새 환경에서 build, boot, 고장 하나를 실행하고 서명된 review를 남김
- 릴리스 note에 측정 환경, SBOM, 제한, 다음 보강 항목 포함

## 힌트

1. 설계 답변은 class 이름보다 책임, 입력, 출력, 실패 mode 순서로 말합니다.
2. mapping 표의 빈칸은 구현 결함일 수도 있고 범위 제외일 수도 있습니다. 근거를 붙입니다.
3. demo 전날 새 고장을 고치며 기준을 낮추지 않습니다. 실패는 보강 계획으로 남깁니다.

## G10 재심사 조건

공식 문서 인용 없이 AUTOSAR 적합을 주장하거나, 비공개 고장을 다른 component 탓으로 넘기거나, 제3자 재현이 실패하면 G10을 통과하지 못합니다. 16–30시간 보강 후 새 릴리스 candidate와 새 비공개 고장으로 재심사합니다.
