# G10.1 R25-11 책임 지도 실습 도구

이 디렉터리는 Sprint 10.1의 제출물을 점검하는 작은 도구입니다. Service Interface, 생성 코드, 배치 산출물, 런타임 객체, Function Group State, Health Supervision을 typed graph의 서로 다른 node로 기록합니다. 선택한 통신 binding과 생명주기 시나리오별 책임도 따로 검사합니다.

## 도구 확인

저장소 루트에서 실행합니다. 네트워크와 추가 패키지는 필요 없습니다.

```bash
python3 labs/g10_1_release_map/run_harness.py
```

표준 출력은 아래와 같아야 합니다.

```text
STRUCTURE_PASS G10.1-MAP profile=harness nodes=11 edges=11 citations=1 statuses=Mapped:0,Partial:11,Missing:0,Out of scope:0 review=Pending
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
PASS negative=production-grade-series-deployment expected=E_SCOPE_CLAIM observed=E_SCOPE_CLAIM
PASS negative=korean-conformance-overclaim expected=E_SCOPE_CLAIM observed=E_SCOPE_CLAIM
PASS negative=claim-status-conflict expected=E_SCOPE_CLAIM observed=E_SCOPE_CLAIM
PASS negative=forged-review expected=E_REVIEW,E_REVIEW_TRUST observed=E_REVIEW,E_REVIEW_TRUST
G10.1 harness: PASS (1 valid, 20 negative cases)
```

별도 단위 시험도 실행합니다.

```bash
python3 -m unittest discover -s labs/g10_1_release_map/tests -p 'test_*.py' -v
```

`Ran 10 tests`와 마지막 `OK`를 확인합니다.

## 내 책임 지도 만들기

원본을 작업 디렉터리에 복사한 뒤 편집합니다.

```bash
mkdir -p study/g10.1
cp labs/g10_1_release_map/starter/release-map.json study/g10.1/release-map.json
python3 labs/g10_1_release_map/validator.py study/g10.1/release-map.json
```

첫 실행에는 `E_SUBMITTER`, `E_SOURCE_ACCESS`, `E_SOURCE_PATH`, `E_SOURCE_TRUST`, `E_CITATION_LOCATOR`, `E_MAPPING_INCOMPLETE`가 나옵니다. 제출자 ID, 공식 digest, 원문 절, 로컬 근거를 채우면서 항목별로 해소합니다.

1. AUTOSAR Adaptive Platform 공식 페이지에서 R25-11 문서를 내려받아 `sources/autosar-r25-11/`에 둔다. 이 PDF는 `.gitignore`에 들어 있다.
2. AUTOSAR의 `Adaptive Platform Specification Hashes`에서 각 PDF의 SHA-512를 확인한다. [R25-11 문서 lock](r25-11-document-lock.json)의 `official_sha512` 갱신은 제출물과 분리한 검토 커밋으로 진행한다.
3. `source_ledger`에 revision, 로컬 PDF 경로, 절 제목, 절 번호 또는 requirement ID, 실제 파일 SHA-256, 확인 날짜를 적는다.
4. 안정적으로 식별할 `submitter_id`를 넣고 P02/P03 파일의 SHA-256을 관련 node의 `local_evidence`에 연결한다.
5. 각 node의 `claim_type`, `mapped_behavior`, `excluded_behavior`를 채워 로컬 관찰과 제외 범위를 구조화한다.
6. generated Proxy/Skeleton 코드와 런타임 Proxy/Skeleton 객체를 별도 node로 유지한다. `edges`는 role·relation·방향이 동결된 11개 필수 관계를 모두 담는다.
7. 생명주기 시나리오마다 trigger reporter, policy decision owner, transition executor, recovery reporter를 원문 citation과 함께 정한다.
8. `Mapped / Partial / Missing / Out of scope`를 고르고 `summary`를 다시 계산한다.

공식 SHA-512 pin과 내부 일관성이 맞으면 `STRUCTURE_PASS profile=submission`이 출력됩니다. `REVIEWED_PASS`는 제출자와 다른 검토자의 서명까지 확인합니다. review manifest에는 전체 commit SHA, 검토자 SSH key fingerprint, node·citation·local evidence hash, source ledger와 source lock hash, limitation 확인, 승인 결정을 담습니다. manifest 원문은 `adaptive-vehicle-platform-lab-g10.1` namespace의 OpenSSH SSHSIG로 서명합니다. [검토자 registry](trusted-reviewers.json)에 등록된 공개키만 승인에 쓰며 registry 변경은 별도 검토 커밋으로 남깁니다.

[합성 review fixture](../../fixtures/g10/review-manifest-v1.json)는 hash 결속만 시험하고 출력도 `HARNESS_REVIEW_BINDING_PASS`로 구분합니다. 현재 registry에는 독립 검토자가 등록되지 않았습니다. 첫 검토자를 등록할 때 공개키 fingerprint, 이해관계, 검토 범위를 함께 기록합니다.

## 검사 범위

- graph coverage: 필수 semantic role 11개, node type, phase, role별 필수 edge 11개
- self-loop, 역방향 edge, 끊긴 필수 경로, 의미가 다른 relation 거부
- 생성 산출물과 런타임 객체, Executable과 Process의 분리
- 선택한 SOME/IP·DDS·local-loopback binding과 배치 node 연결
- 시나리오별 report·policy decision·transition execution·recovery report 책임
- 로컬 구현 표기: `concept-aligned local prototype`, `conformance_claim: false`, `educational-prototype`, node별 claim type·포함·제외 동작
- 동결한 R25-11 URL·파일명·revision, 역할별 필수 document, 직접 읽은 절, 공식 SHA-512, PDF와 로컬 파일 hash
- 여러 역할에 같은 README 하나를 재사용하는 근거 축소 감지
- 매핑 상태 집계의 재계산
- 제출자·검토자 분리, 전체 commit 결속, trusted key fingerprint, detached SSHSIG

검토자는 인용 절의 해석, 빠진 functional cluster, 원문 사이의 충돌, 실제 SDK·ARXML 범위를 확인합니다. 검사기는 검토 파일의 내용과 hash를 다시 읽어 claim·citation·근거 범위가 모두 덮였는지 확인합니다.
