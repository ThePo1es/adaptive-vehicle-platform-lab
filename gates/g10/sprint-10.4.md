# Sprint 10.4 — Platform·Function Group State

## 시간과 기준 자료

24–30시간. R25-11 `State Management`와 `Execution Management`에서 Function Group State 요청, transition, 책임 경계 절을 읽습니다. P03 로컬 상태 `Startup`, `Driving`, `Diagnostic`, `Update`, `Shutdown`의 의미는 `state-contract.md`에 고정합니다.

## 시작 조건과 모델

State Controller가 요청을 선택하고 Process Controller가 실행 계획을 수행하는 두 component를 둡니다. 요청 원인, 현재 상태, 대상 상태, transition ID, deadline, 결과가 이벤트 contract에 포함됩니다. 로컬 상태와 R25-11 개념의 mapping status를 각 상태에 표시합니다.

## 안내 실습

허용 transition 표와 상태별 application set을 작성합니다. `Startup → Driving → Shutdown`, `Driving → Diagnostic → Driving`을 실행하고 dependency plan과 프로세스 이벤트를 transition ID로 연결합니다. 같은 대상 재요청은 idempotent하게 처리합니다.

## 독립 실습

illegal transition, transition 중 새 요청, partial start failure, deadline expiry, shutdown 우선 요청의 arbitration rule을 구현합니다. decision log에는 입력 근거와 선택 이유가 남고 action log에는 실제 start/stop 결과가 남게 합니다.

## 전이 과제

검토자가 `Update` 중 긴급 `Shutdown` 또는 `Driving` 진입 중 diagnostic 요청을 줍니다. rule table로 결과를 먼저 예측하고 model-based 테스트로 구현과 대조합니다. 새 상태 하나를 추가할 때 바뀌는 manifest, transition, 프로세스 set도 찾습니다.

## 판정 기준

- 상태 decision과 프로세스 action interface가 분리되어 독립 테스트 가능
- illegal·중복·경합 요청의 결과가 transition table과 일치
- partial failure 뒤 실제 프로세스 set과 reported 상태가 모순되지 않음
- 모든 이벤트가 transition ID와 monotonic timestamp를 가짐
- generated sequence 1,000개가 reference 상태 model과 일치
- 로컬 상태와 R25-11 Function Group/Platform 관련 개념 차이를 설명

## 전이 규칙 확인

1. 요청을 받았다는 이벤트와 상태가 바뀌었다는 이벤트를 분리합니다.
2. transition 중 재요청 규칙은 queue, replace, reject 중 하나를 명시합니다.
3. failed 상태를 하나로 뭉치기 전에 running 프로세스 set을 확인합니다.

## 상태 모델을 다시 만들 때

State Controller가 직접 프로세스 signal을 보냈거나 끝나지 않은 전이를 현재 상태로 보고했거나 경합 결과가 매번 달라진다면 상태 세 개와 프로세스 집합 하나로 줄입니다. 모델 테스트가 모든 순서를 판정한 뒤 원래 상태를 복원합니다.
