# Sprint 10.4 — Platform·Function Group State

## 시간과 기준 자료

24–30시간. R25-11 `State Management`와 `Execution Management`에서 Function Group State 요청, transition, 책임 경계 절을 읽습니다. P03 local state `Startup`, `Driving`, `Diagnostic`, `Update`, `Shutdown`의 의미는 `state-contract.md`에 고정합니다.

## 시작 조건과 모델

State Controller가 요청을 선택하고 Process Controller가 실행 계획을 수행하는 두 component를 둡니다. 요청 원인, 현재 state, target state, transition ID, deadline, 결과가 event contract에 포함됩니다. local state와 R25-11 개념의 mapping status를 각 state에 표시합니다.

## 안내 실습

허용 transition 표와 상태별 application set을 작성합니다. `Startup → Driving → Shutdown`, `Driving → Diagnostic → Driving`을 실행하고 dependency plan과 process event를 transition ID로 연결합니다. 같은 target 재요청은 idempotent하게 처리합니다.

## 독립 실습

illegal transition, transition 중 새 요청, partial start failure, deadline expiry, shutdown 우선 요청의 arbitration rule을 구현합니다. decision log에는 입력 근거와 선택 이유가 남고 action log에는 실제 start/stop 결과가 남게 합니다.

## 전이 과제

검토자가 `Update` 중 긴급 `Shutdown` 또는 `Driving` 진입 중 diagnostic 요청을 줍니다. rule table로 결과를 먼저 예측하고 model-based test로 구현과 대조합니다. 새 state 하나를 추가할 때 바뀌는 manifest, transition, process set도 찾습니다.

## 판정 기준

- state decision과 process action interface가 분리되어 독립 test 가능
- illegal·중복·경합 요청의 결과가 transition table과 일치
- partial failure 뒤 실제 process set과 reported state가 모순되지 않음
- 모든 event가 transition ID와 monotonic timestamp를 가짐
- generated sequence 1,000개가 reference state model과 일치
- local state와 R25-11 Function Group/Platform 관련 개념 차이를 설명

## 힌트

1. 요청을 받았다는 event와 state가 바뀌었다는 event를 분리합니다.
2. transition 중 재요청 규칙은 queue, replace, reject 중 하나를 명시합니다.
3. failed state를 하나로 뭉치기 전에 running process set을 확인합니다.

## 치명적 실패와 보충

State Controller가 직접 process signal을 보내거나, 완료되지 않은 transition을 current state로 보고하거나, 경합 결과가 실행마다 달라지면 실패입니다. 보충 과제는 세 state와 단일 process set으로 model test를 다시 만드는 것입니다.
