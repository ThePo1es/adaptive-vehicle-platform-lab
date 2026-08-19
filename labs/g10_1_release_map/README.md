# G10.1 R25-11 책임 지도 실습 도구

이 디렉터리는 Sprint 10.1의 제출물을 점검하는 작은 도구입니다. Service Interface, 생성 코드, 배치 산출물, 런타임 객체, Function Group State, Health Supervision을 typed graph의 서로 다른 node로 기록합니다. 선택한 통신 binding과 생명주기 시나리오별 책임도 따로 검사합니다.

## 도구 확인

저장소 루트에서 실행합니다. 네트워크와 추가 패키지는 필요 없습니다.

```bash
python3 labs/g10_1_release_map/run_harness.py
```

표준 출력은 아래와 같아야 합니다.

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
PASS negative=self-loop-only expected=E_EDGE_SEMANTICS,E_GRAPH_CONNECTIVITY observed=E_EDGE_SEMANTICS,E_GRAPH_CONNECTIVITY
PASS negative=reversed-edge expected=E_EDGE_SEMANTICS,E_GRAPH_CONNECTIVITY observed=E_EDGE_SEMANTICS,E_GRAPH_CONNECTIVITY
PASS negative=missing-required-edge expected=E_GRAPH_CONNECTIVITY observed=E_GRAPH_CONNECTIVITY
PASS negative=production-overclaim expected=E_SCOPE_CLAIM observed=E_SCOPE_CLAIM
PASS negative=structured-conformance expected=E_SCOPE_CLAIM observed=E_SCOPE_CLAIM
PASS negative=reused-local-evidence expected=E_LOCAL_EVIDENCE_DIVERSITY observed=E_LOCAL_EVIDENCE_DIVERSITY
PASS negative=forged-review expected=E_REVIEW observed=E_REVIEW
G10.1 harness: PASS (1 valid, 17 negative cases)
```

별도 단위 시험도 실행합니다.

```bash
python3 -m unittest discover -s labs/g10_1_release_map/tests -p 'test_*.py' -v
```

`Ran 8 tests`와 마지막 `OK`를 확인합니다.

## 내 책임 지도 만들기

원본을 작업 디렉터리에 복사한 뒤 편집합니다.

```bash
mkdir -p study/g10.1
cp labs/g10_1_release_map/starter/release-map.json study/g10.1/release-map.json
python3 labs/g10_1_release_map/validator.py study/g10.1/release-map.json
```

첫 실행에는 `E_SOURCE_ACCESS`, `E_SOURCE_PATH`, `E_CITATION_LOCATOR`, `E_MAPPING_INCOMPLETE`가 나옵니다. 원문과 로컬 근거를 연결하면 이 항목들이 차례로 사라집니다.

1. AUTOSAR Adaptive Platform 공식 페이지에서 R25-11 문서를 내려받아 `sources/autosar-r25-11/`에 둔다. 이 PDF는 `.gitignore`에 들어 있다.
2. [R25-11 문서 lock](r25-11-document-lock.json)의 URL·파일명·release와 PDF 앞표지를 대조한다. 배포 내용이 달라졌다면 lock 변경을 별도 PR로 검토한다.
3. `source_ledger`에 revision, 로컬 PDF 경로, 절 제목, 절 번호 또는 requirement ID, 실제 파일 SHA-256, 확인 날짜를 적는다.
4. P02/P03의 로컬 파일과 각 파일의 SHA-256을 관련 node의 `local_evidence`에 연결한다.
5. generated Proxy/Skeleton 코드와 런타임 Proxy/Skeleton 객체를 별도 node로 유지한다. `edges`는 role·relation·방향이 동결된 11개 필수 관계를 모두 담는다.
6. 생명주기 시나리오마다 trigger reporter, policy decision owner, transition executor, recovery reporter를 원문 citation과 함께 정한다.
7. `Mapped / Partial / Missing / Out of scope`를 고르고 `summary`를 다시 계산한다.

내부 일관성이 맞으면 `STRUCTURE_PASS`가 출력됩니다. `REVIEWED_PASS`에는 실제 review manifest 파일이 필요합니다. 그 파일은 reviewer ID, 모든 node·citation·local evidence hash, source ledger hash, limitation 확인, 승인 결정을 담고 제출물의 `review_manifest_path`와 SHA-256에 연결됩니다. [합성 review fixture](../../fixtures/g10/review-manifest-v1.json)는 이 결속 규칙을 자동 시험하는 예시입니다.

## 검사 범위

- graph coverage: 필수 semantic role 11개, node type, phase, role별 필수 edge 11개
- self-loop, 역방향 edge, 끊긴 필수 경로, 의미가 다른 relation 거부
- 생성 산출물과 런타임 객체, Executable과 Process의 분리
- 선택한 SOME/IP·DDS·local-loopback binding과 배치 node 연결
- 시나리오별 report·policy decision·transition execution·recovery report 책임
- 로컬 구현 표기: `concept-aligned local prototype`, `conformance_claim: false`, `educational-prototype`
- 동결한 R25-11 URL·파일명·revision, 역할별 필수 document, 직접 읽은 절, PDF와 로컬 파일 hash
- 여러 역할에 같은 README 하나를 재사용하는 근거 축소 감지
- 매핑 상태 집계의 재계산

검토자는 인용 절의 해석, 빠진 functional cluster, 원문 사이의 충돌, 실제 SDK·ARXML 범위를 확인합니다. 검사기는 검토 파일의 내용과 hash를 다시 읽어 claim·citation·근거 범위가 모두 덮였는지 확인합니다.
