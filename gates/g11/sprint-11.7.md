# Sprint 11.7 — 보증 사례 반박과 P04 릴리스

이 Sprint는 [G11B 보증 계약](assurance-contract.md)의 두 검토 역할을 실제 기록으로 닫습니다. G11A 릴리스와 Sprint 11.5–11.6의 claim graph가 시작 자료입니다.

## 시간과 참여자

16–20시간. 제출 묶음 정리 5–6시간, safety review 3–4시간, security review 3–4시간, 반박 처리와 재릴리스 5–6시간을 잡습니다. safety와 security 검토는 서로 다른 사람이 맡고 각자의 관련 경험 또는 검토한 공식 문서 절을 남깁니다.

## 제출 묶음

`assurance-index.yml`에 claim ID, 상태, 범위, 가정, 요구사항, 시험, result hash, 전체 commit SHA를 기록합니다. HARA·FMEA/FTA·TARA, trust chain, power-cut 표, 알려진 공백, 5–10분 demo 순서를 README 하나에서 찾을 수 있게 만듭니다.

## 안내 실습

서로 충돌하는 두 질문을 먼저 만듭니다. 예를 들어 safety 검토자는 빠른 fallback을 요구하고 security 검토자는 인증되지 않은 상태 전이를 막으라고 요구할 수 있습니다. 해당 충돌을 decision owner, 제한 시간, degraded state, audit event가 있는 요구사항으로 바꾸고 두 고장을 함께 실행합니다.

검토자는 `Accepted`, `Change requested`, `Question`으로 의견을 남깁니다. 답변에는 설명 문장만 붙이지 않고 변경된 claim·시험·result hash를 연결합니다.

## 독립 실습

검토 순서를 공개하지 않은 채 두 사람에게 같은 릴리스 후보를 전달합니다. 각자 가장 약한 Supported claim 세 개와 누락된 common cause 하나를 고르게 합니다. 작성자는 반박을 재현하고 claim 유지·축소·철회 결정을 ADR에 기록합니다.

## 전이 과제

세 변경 사례 중 검토자가 고른 하나를 릴리스 후보에 적용합니다. 120분 안에 영향 분석, 필요한 회귀 시험, 새 claim 상태를 제시하고 그중 한 시험을 실제로 실행합니다.

## 판정 기준

- safety와 security 검토 기록에 서로 다른 reviewer ID와 시간이 있음
- 모든 Supported claim이 전체 commit과 원본 result hash까지 추적됨
- 두 검토자가 각각 약한 주장과 common cause를 실제로 지적함
- Change requested 의견마다 변경 또는 수용하지 않은 근거가 남음
- 변경 사례의 기대 영향과 유지 영역이 함께 검토됨
- demo가 정상 경로, 고장 경로, 남은 공백을 같은 릴리스에서 보여 줌
- P04 tag가 assurance index와 SBOM·image hash를 고정함

## 방어가 막혔을 때

두 역할 중 한 검토가 비어 있으면 릴리스 후보와 실행 자료를 그대로 보존하고 claim 상태를 `Provisional`로 정리합니다. 지적이 여러 경계를 한꺼번에 건드리면 가장 약한 claim 하나로 범위를 축소해 시험과 답변을 다시 준비합니다.
