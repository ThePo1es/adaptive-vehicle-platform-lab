# Sprint 10.8 — Adaptive 설계 심사와 P03 릴리스

## 시간과 기준 자료

24–30시간. R25-11 standards ledger, [AUTOSAR mapping](../../docs/autosar-mapping.md), [mastery review](../../docs/templates/mastery-review.md), P01–P03 evidence를 사용합니다. 시험 시작 전에 public scenario와 비공개 fault manifest의 hash를 기록합니다.

## 릴리스 입력

source tag, AArch64 image, manifest schema/corpus, state·health model tests, SOME/IP captures, persistency kill campaign, SBOM, architecture와 mapping 문서를 release candidate로 묶습니다. 미완료 항목은 숨기지 않고 `Known limits`와 mapping status에 남깁니다.

## 안내 실습

30분 demo에서 다음 흐름을 재현합니다.

1. manifest validation과 dependency startup
2. Function Group에 대응시킨 local state transition
3. VehicleStateService discovery와 event
4. missed heartbeat 감지와 bounded recovery
5. process restart 뒤 persisted state 복구
6. clean shutdown과 process inventory 확인

## 독립 실습·심사

검토자가 Service Interface/Proxy·Skeleton, SOME/IP binding, Execution Manifest, lifecycle, State Management, PHM, Persistency 중 세 영역을 골라 설계 질의를 합니다. 답은 R25-11 section, local code/test, 빠진 기능 세 지점을 연결해야 합니다.

## 전이 과제 — 비공개 fault

경계가 틀린 fault 하나를 120분 안에 분석합니다. 예시는 State Controller가 process를 직접 재시작함, health monitor가 state를 결정함, incompatible service가 offer됨, old process heartbeat가 새 instance에 들어옴입니다. 수정 전에 책임을 옮길 위치와 regression test를 제시합니다.

## 판정 기준

- public scenario 전체가 release artifact에서 재현
- 비공개 fault의 첫 잘못된 책임 경계를 찾고 test-first로 수정
- P01–P03 requirement와 evidence link가 끊기지 않음
- R25-11 mapping의 각 `Mapped` 항목을 자격 있는 검토자가 section으로 확인
- 검토 자격이 부족한 영역은 local 동작 `Validated`, AUTOSAR mapping `Provisional`로 기록
- 제3자가 새 환경에서 build, boot, fault 하나를 실행하고 서명된 review를 남김
- release note에 측정 환경, SBOM, 제한, 다음 보강 항목 포함

## 힌트

1. 설계 답변은 class 이름보다 책임, 입력, 출력, 실패 mode 순서로 말합니다.
2. mapping 표의 빈칸은 구현 결함일 수도 있고 범위 제외일 수도 있습니다. 근거를 붙입니다.
3. demo 전날 새 fault를 고치며 기준을 낮추지 않습니다. 실패는 보강 계획으로 남깁니다.

## 치명적 실패와 보충

공식 문서 인용 없이 AUTOSAR 적합을 주장하거나, 비공개 fault를 다른 component 탓으로 넘기거나, 제3자 재현이 실패하면 G10을 통과하지 못합니다. 16–30시간 보강 후 새 release candidate와 새 비공개 fault로 재심사합니다.
