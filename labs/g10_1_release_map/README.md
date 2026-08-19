# G10.1 R25-11 책임 지도 실습 도구

이 디렉터리는 Sprint 10.1의 제출물을 점검하는 작은 도구입니다. Service Interface, 생성 코드, 배치 산출물, 런타임 객체, Function Group State, Health Supervision을 typed graph의 서로 다른 node로 기록합니다. 선택한 통신 binding과 생명주기 시나리오별 책임도 따로 검사합니다.

## 도구 확인

저장소 루트에서 실행합니다. 네트워크와 추가 패키지는 필요 없습니다.

```bash
python3 labs/g10_1_release_map/run_harness.py
```

표준 출력은 아래 열두 줄과 같아야 합니다.

```text
STRUCTURE_PASS G10.1-MAP nodes=11 edges=11 citations=1 statuses=Mapped:0,Partial:11,Missing:0,Out of scope:0 review=Pending
PASS negative=artifact-phase expected=E_PHASE observed=E_PHASE
PASS negative=role-coverage expected=E_GRAPH_COVERAGE,E_PHASE observed=E_GRAPH_COVERAGE,E_PHASE
PASS negative=edge-reference expected=E_EDGE_REF observed=E_EDGE_REF
PASS negative=owner-conflict expected=E_OWNER_BOUNDARY observed=E_OWNER_BOUNDARY
PASS negative=scope-overclaim expected=E_SCOPE_CLAIM observed=E_SCOPE_CLAIM
PASS negative=summary-drift expected=E_SUMMARY observed=E_SUMMARY
PASS negative=profile-downgrade expected=E_PROFILE_DOWNGRADE observed=E_PROFILE_DOWNGRADE
PASS negative=all-missing expected=E_MAPPING_INCOMPLETE observed=E_MAPPING_INCOMPLETE
PASS negative=gibberish-claim expected=E_NODE_FIELD observed=E_NODE_FIELD
PASS negative=binding-reference expected=E_BINDING observed=E_BINDING
G10.1 harness: PASS (1 valid, 10 negative cases)
```

별도 단위 시험도 실행합니다.

```bash
python3 -m unittest discover -s labs/g10_1_release_map/tests -p 'test_*.py' -v
```

`Ran 5 tests`와 마지막 `OK`를 확인합니다.

## 내 책임 지도 만들기

원본을 작업 디렉터리에 복사한 뒤 편집합니다.

```bash
mkdir -p study/g10.1
cp labs/g10_1_release_map/starter/release-map.json study/g10.1/release-map.json
python3 labs/g10_1_release_map/validator.py study/g10.1/release-map.json
```

첫 실행에는 `E_SOURCE_ACCESS`, `E_CITATION_LOCATOR`, `E_SOURCE_HASH`, `E_MAPPING_INCOMPLETE`가 나옵니다. 원문과 로컬 근거를 연결하면 이 항목들이 차례로 사라집니다.

1. AUTOSAR Adaptive Platform 공식 페이지에서 R25-11 문서를 내려받는다.
2. [R25-11 문서 lock](r25-11-document-lock.json)과 PDF 앞표지의 식별자를 대조한다. 다른 식별자가 보이면 lock을 고치는 PR부터 만든다.
3. `source_ledger`에 절 제목, 절 번호 또는 requirement ID, PDF SHA-256, 확인 날짜를 적는다.
4. P02/P03의 로컬 파일과 각 파일의 SHA-256을 관련 node의 `local_evidence`에 연결한다.
5. generated Proxy/Skeleton 코드와 런타임 Proxy/Skeleton 객체를 별도 node로 유지한다. `edges`에는 생성·배치·실행 관계만 적는다.
6. 생명주기 시나리오마다 trigger reporter, policy decision owner, transition executor, recovery reporter를 원문 citation과 함께 정한다.
7. `Mapped / Partial / Missing / Out of scope`를 고르고 `summary`를 다시 계산한다.

내부 일관성이 맞으면 `STRUCTURE_PASS`가 출력됩니다. 검토자가 citation과 claim을 원문에서 대조하고 review manifest hash를 채운 제출물은 `REVIEWED_PASS`로 바뀝니다. Gate 평가는 `REVIEWED_PASS`와 검토 기록을 함께 봅니다.

## 검사 범위

- graph coverage: 필수 semantic role 11개, node type, phase, typed edge
- 생성 산출물과 런타임 객체, Executable과 Process의 분리
- 선택한 SOME/IP·DDS·local-loopback binding과 배치 node 연결
- 시나리오별 report·policy decision·transition execution·recovery report 책임
- 로컬 구현 표기: `concept-aligned local prototype`
- 동결한 R25-11 document ID, 직접 읽은 절, PDF hash, 로컬 파일 hash
- 매핑 상태 집계의 재계산

검토자는 인용 절의 해석, 빠진 functional cluster, 원문 사이의 충돌, 실제 SDK·ARXML 범위를 확인합니다. 검사기는 그 검토 결과의 hash와 citation coverage를 보존합니다.
