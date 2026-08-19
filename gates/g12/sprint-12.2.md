# Sprint 12.2 — 측정 가능한 시스템 요구사항

[P06 통합 계약](contract.md)의 종단 불변 조건과 Sprint 12.1의 성공 장면을 요구사항 집합으로 바꿉니다.

## 시간 배분

22–28시간. 요구사항 작성 8시간, 모호성·충돌 검사 5–7시간, 추적 연결 5–7시간, 전이 과제와 리뷰 4–6시간입니다. 기존 `docs/requirements.md`의 식별자·상태 규칙을 그대로 사용합니다.

## 입력과 문장 규칙

각 항목에 stimulus, precondition, response, tolerance, observer, evidence grade를 둡니다. `빠르게`, `적절히`, `가능하면` 같은 표현은 측정값이나 상태로 바꿉니다. 안전·보안 요구사항에는 실패 시 상태와 audit event를 함께 적습니다.

## 안내 실습

“MCU가 재부팅되면 gateway가 알아야 한다”를 세 요구사항으로 나눕니다. 새 source session 관찰, 이전 값 폐기, VehicleState 재공개 조건을 각각 기술하고 session tracker·lifecycle coordinator·service client가 보는 결과를 정합니다.

요구사항 lint는 필수 field, 단위, owner, verification method, 상·하위 링크, 중복 ID를 검사하게 작성합니다. 문장만 다른 중복 항목과 서로 다른 timeout을 가진 충돌 사례를 음성 입력에 넣습니다.

## 독립 실습

data, diagnostic, lifecycle, update 네 묶음에서 최소 6개씩 작성합니다. 모든 항목을 architecture component와 시험 ID에 연결하고, 아직 구현되지 않은 항목에는 `Draft`와 준비 조건을 남깁니다. 두 사람이 같은 요구사항을 읽고 예상 결과를 따로 쓴 뒤 차이가 난 문장을 고칩니다.

## 전이 과제

다음 문장을 45분 안에 고칩니다. “통신이 불안정하면 시스템은 안전하게 복구해야 한다.” 어떤 통신, 관찰 window, 전이 상태, 복구 제한 시간, 최초 관찰자, 남길 audit event를 채우고 회귀 시험 하나를 설계합니다.

## 판정 기준

- 네 영역에 최소 24개 요구사항과 고유 ID가 있음
- 모든 항목에 조건·응답·허용치·관찰자·검증 방법이 있음
- 단위 없는 시간 표현과 의미가 겹치는 중복 항목을 lint가 잡음
- source session, freshness, version, diagnostic 결과 경계가 요구사항에 나타남
- safety·security 항목이 failure state와 audit event를 가짐
- requirement–component–test 링크가 양방향으로 조회됨
- 두 독자의 예상 결과가 일치하도록 모호한 문장이 수정됨

## 보강 기준

lint 통과 뒤에도 두 독자가 다른 상태를 예상하면 그 요구사항을 봉인 입력으로 보지 않습니다. stimulus와 observer만 남겨 문장을 다시 쓰고 양성 1개·경계 2개·실패 2개 시험으로 재확인합니다.
