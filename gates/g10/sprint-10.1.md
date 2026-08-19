# Sprint 10.1 — AUTOSAR Adaptive R25-11 책임 지도

## 시간과 기준 자료

28–36시간. [AUTOSAR Adaptive Platform](https://www.autosar.org/standards/adaptive-platform/)에서 R25-11을 고정하고 architecture, Communication, Execution, State, PHM, Persistency, Diagnostics, IAM, Cryptography, Manifest 문서를 받습니다. 각 PDF의 document ID, 릴리스, revision, 읽은 section title 또는 requirement ID를 `standards-ledger.md`에 기록합니다.

## 시작 조건과 질문

G9에서 구현한 P02와 P03 구성요소를 펼쳐 놓고 다음 흐름을 다시 그립니다.

`Service Interface → generated Proxy/Skeleton 역할 → Service Instance/Deployment → SOME/IP binding → Executable/Process → Function Group State → Health Supervision`

공식 SDK나 generator를 쓰지 않은 부분은 시작부터 `local prototype`으로 표시합니다.

## 안내 실습

functional cluster마다 맡는 결정, 실행, 관찰, 데이터 경계를 한 문장으로 씁니다. `ara::com` proxy/skeleton 호출과 P02 vsomeip 호출을 sequence diagram 두 장으로 만들고 서비스 contract, generated code, binding configuration, runtime discovery가 만나는 지점을 표시합니다.

[G10.1 책임 지도 검사기](../../labs/g10_1_release_map/README.md)를 먼저 실행합니다. 공개 입력에는 통과 지도 하나와 단계 순서, 산출 시점, 생명주기 책임자, 적합성 과장, 집계 오류를 각각 하나씩 넣은 음성 사례가 있습니다. 검사기는 표의 구조와 내부 일관성을 보고, 인용 절의 의미는 원문 검토에 남깁니다.

## 독립 실습

R25-11에서 확인한 Application Design, Execution, Service Instance, Machine 관련 manifest와 Service Interface artifact를 서로 다른 행에 정리합니다. 정확한 taxonomy와 산출 시점은 원문 section으로 확인합니다. P03의 YAML field가 어느 요소에 가까운지, 대응 없음, 의미 축소, 여러 요소 합침 중 하나로 판정합니다.

## 전이 과제

처음 보는 manifest element 또는 functional cluster 하나를 받습니다. 90분 안에 upstream/downstream 책임, runtime actor, configuration source, 실패 관찰 위치를 찾아 기존 지도에 넣습니다.

## 판정 기준

- 모든 표에 R25-11 document ID와 section citation 존재
- Service Interface artifact와 manifest taxonomy를 섞지 않고 Proxy/Skeleton, binding, discovery 책임을 분리함
- EM, SM, PHM 사이의 decision/action/observation 경계가 설명됨
- 로컬 구현의 `Mapped`, `Partial`, `Missing`, `Out of scope` 수를 집계
- 공식 API·ARXML을 사용하지 않은 지점을 AUTOSAR 구현으로 표기하지 않음
- 생소한 요소 전이 과제를 외부 검토자가 section과 함께 확인

## 문서를 대조할 때

1. 이름이 비슷한 class보다 책임과 lifecycle을 먼저 비교합니다.
2. design-time artifact와 runtime API를 같은 열에 넣지 않습니다.
3. 이전 릴리스 blog나 예제는 R25-11 원문과 다른 지점을 표시합니다.

## 매핑을 다시 작성할 조건

문서 절 없이 개념을 연결했거나 vsomeip wrapper를 `ara::com` 구현으로 적었거나 SM과 EM에 같은 결정을 배치했다면 매핑을 보류합니다. P02 메서드 하나와 P03 프로세스 하나의 종단 책임 지도부터 다시 만듭니다.
