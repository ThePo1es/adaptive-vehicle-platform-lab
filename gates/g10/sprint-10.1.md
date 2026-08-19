# Sprint 10.1 — AUTOSAR Adaptive release와 책임 지도

## 시간과 기준 자료

24–30시간. [AUTOSAR Adaptive Platform](https://www.autosar.org/standards/adaptive-platform/)에서 R25-11을 고정하고 `Explanation of Adaptive Platform Software Architecture`, `Communication Management`, `Execution Management`, `State Management`, `Platform Health Management`, `Manifest Specification` 문서를 받습니다. 각 PDF의 document ID, release, revision, 읽은 절을 `standards-ledger.md`에 기록합니다.

## 시작 조건과 질문

P02와 P03 구성요소를 펼쳐 놓고 다음 흐름을 먼저 그립니다.

`Service Interface → generated Proxy/Skeleton 역할 → Service Instance/Deployment → SOME/IP binding → Executable/Process → Function Group State → Health Supervision`

공식 SDK나 generator를 쓰지 않은 부분은 시작부터 `local prototype`으로 표시합니다.

## 안내 실습

functional cluster마다 맡는 결정, 실행, 관찰, 데이터 경계를 한 문장으로 씁니다. `ara::com` proxy/skeleton 호출과 P02 vsomeip 호출을 sequence diagram 두 장으로 만들고 service contract, generated code, binding configuration, runtime discovery가 만나는 지점을 표시합니다.

## 독립 실습

R25-11 manifest 종류와 산출 시점을 표로 정리합니다. P03의 YAML field가 어느 공식 artifact·요소에 가까운지, 대응 없음, 의미 축소, 여러 요소 합침 중 하나로 판정합니다. 문서 이름만 적지 않고 근거 절과 짧은 해석을 붙입니다.

## 전이 과제

검토자가 생소한 manifest element 또는 functional cluster 하나를 고릅니다. 90분 안에 upstream/downstream 책임, runtime actor, configuration source, 실패 관찰 위치를 찾아 기존 지도에 넣습니다.

## 판정 기준

- 모든 표에 R25-11 document ID와 section citation 존재
- Service Interface, Proxy/Skeleton, binding, discovery 책임이 분리됨
- EM, SM, PHM 사이의 decision/action/observation 경계가 설명됨
- local 구현의 `Mapped`, `Partial`, `Missing`, `Out of scope` 수를 집계
- 공식 API·ARXML을 사용하지 않은 지점을 AUTOSAR 구현으로 표기하지 않음
- 생소한 요소 전이 과제를 외부 검토자가 section과 함께 확인

## 힌트

1. 이름이 비슷한 class보다 책임과 lifecycle을 먼저 비교합니다.
2. design-time artifact와 runtime API를 같은 열에 넣지 않습니다.
3. 이전 release blog나 예제는 R25-11 원문과 다른 지점을 표시합니다.

## 치명적 실패와 보충

문서 절 없이 개념을 연결하거나, vsomeip wrapper를 `ara::com` 구현으로 부르거나, SM과 EM이 같은 결정을 내리게 그리면 실패입니다. 보충 과제는 P02 한 method와 P03 한 process의 end-to-end 책임 지도만 다시 작성하는 것입니다.
