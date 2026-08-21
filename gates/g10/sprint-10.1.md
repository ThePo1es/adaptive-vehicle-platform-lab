# Sprint 10.1 — AUTOSAR Adaptive R25-11 책임 지도

> - 준비 상태: `Runnable`
> - 시작 커밋: `8b7ec2e55071c792be18d3e5afd877460baa2583`
> - 공개 입력 SHA-256: `35858c0b4ed341c462291955a37027d6ef0ce2c617ec5693a5be7f3b8f948ca5`
> - 실행 기록: [G10.1 실행 명세 v12](../../evidence/runnable/g10.1/run-manifest-v12.json)

현재 확인된 범위는 시작 커밋과 검사 경로 재현까지입니다. 다음 실행에서 원문 검토, 독립 실습, 학습 시간을 기록합니다.

## 시간과 기준 자료

28–36시간. [AUTOSAR Adaptive Platform](https://www.autosar.org/standards/adaptive-platform/)에서 R25-11을 고정하고 architecture, Communication, Execution, State, PHM, Persistency, Diagnostics, IAM, Cryptography, Manifest 문서를 받습니다. 각 PDF의 document ID, 릴리스, revision, 읽은 section title 또는 requirement ID를 `standards-ledger.md`에 기록합니다.

## 시작 조건과 질문

G9에서 구현한 P02와 P03 구성요소를 펼쳐 놓고 다음 순서로 자료를 읽습니다.

`Service Interface → generated Proxy/Skeleton 역할 → Service Instance/Deployment → SOME/IP binding → Executable/Process → Function Group State → Health Supervision`

이 순서는 학습 경로입니다. 결과물은 설계 산출물, 생성 코드, 배치 설정, 런타임 객체, 생명주기 시나리오를 구분한 관계 그래프입니다. 공식 SDK나 생성기를 쓰지 않은 부분은 시작부터 `local prototype`으로 표시합니다.

## 안내 실습

functional cluster마다 맡는 결정, 실행, 관찰, 데이터 경계를 한 문장으로 씁니다. `ara::com` proxy/skeleton 호출과 P02 vsomeip 호출을 sequence diagram 두 장으로 만들고 서비스 contract, generated code, binding configuration, runtime discovery가 만나는 지점을 표시합니다.

[G10.1 책임 지도 검사기](../../labs/g10_1_release_map/README.md)를 먼저 실행합니다. 공개 입력에는 통과 graph 하나와 node type·phase, role coverage, edge 방향·연결, scenario owner, 허용되지 않은 주장 값, 근거 재사용, 위조 review 등을 다루는 음성 사례 26개가 있습니다. 구조 검사가 끝나면 인용 절과 로컬 파일을 검토자가 직접 맞춰 봅니다.

## 독립 실습

R25-11에서 확인한 Application Design, Execution, Service Instance, Machine 관련 manifest와 Service Interface artifact를 서로 다른 node로 정리합니다. 생성된 Proxy/Skeleton 코드와 런타임 Proxy/Skeleton 객체도 나눕니다. P03의 YAML field는 대응 없음, 의미 축소, 여러 요소 합침 중 하나로 판정하고 로컬 파일 hash를 근거에 붙입니다.

## 전이 과제

처음 보는 manifest element 또는 functional cluster 하나를 받습니다. 90분 안에 node type, phase, typed edge, configuration source, 실패 관찰 위치를 찾아 지도에 넣습니다. 별도의 고장 scenario에서는 trigger report, policy decision, transition execution, recovery report 책임을 새로 정합니다.

## 판정 기준

- 모든 node에 역할별 R25-11 document ID, section citation, 공식 SHA-512, 로컬 PDF와 구현 파일의 실제 hash가 존재
- Service Interface, generated code, runtime Proxy/Skeleton, binding, discovery 책임을 별도 node로 분리함
- lifecycle scenario마다 reporter, policy decision owner, transition executor, recovery reporter가 citation과 함께 설명됨
- 로컬 구현의 `Mapped`, `Partial`, `Missing`, `Out of scope` 수를 집계
- 공식 API·ARXML을 사용하지 않은 지점을 AUTOSAR 구현으로 표기하지 않음
- `REVIEWED_PASS`가 release-authority 정책 서명, 검토자 SSHSIG, subject commit·path, node·citation·committed evidence hash를 검증함

## 문서를 대조할 때

1. 비교 순서는 책임, 생명주기, 클래스 이름입니다.
2. 설계 단계 산출물과 런타임 API는 표의 서로 다른 열에 둡니다.
3. 이전 릴리스 blog나 예제는 R25-11 원문과 다른 지점을 표시합니다.

## 매핑을 다시 작성할 조건

문서 절 없이 개념을 연결했거나 vsomeip wrapper를 `ara::com` 구현으로 적었거나 한 scenario의 policy 결정과 transition 실행을 같은 책임에 넣었다면 P02 메서드 하나와 P03 process 하나로 범위를 줄입니다. 생성 산출물과 런타임 객체부터 다시 나누고 새 입력으로 재시험합니다.
