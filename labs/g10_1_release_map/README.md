# G10.1 R25-11 책임 지도 실습 도구

이 디렉터리는 Sprint 10.1의 제출물을 점검하는 작은 도구입니다. 일곱 단계의 순서, 설계 시점과 런타임 구분, SM·EM·PHM 생명주기 책임, 매핑 집계, 근거 없는 적합성 표현을 검사합니다. 인용한 AUTOSAR 원문이 주장을 뒷받침하는지는 검토자가 직접 확인합니다.

## 도구 확인

저장소 루트에서 실행합니다. 네트워크와 추가 패키지는 필요 없습니다.

```bash
python3 labs/g10_1_release_map/run_harness.py
```

stdout은 아래 일곱 줄과 같아야 합니다.

```text
PASS G10.1-MAP rows=7 citations=1 statuses=Mapped:0,Partial:7,Missing:0,Out of scope:0
PASS negative=stage-order expected=E_STAGE_ORDER observed=E_STAGE_ORDER
PASS negative=artifact-phase expected=E_PHASE observed=E_PHASE
PASS negative=owner-conflict expected=E_OWNER_BOUNDARY observed=E_OWNER_BOUNDARY
PASS negative=scope-overclaim expected=E_SCOPE_CLAIM observed=E_SCOPE_CLAIM
PASS negative=summary-drift expected=E_SUMMARY observed=E_SUMMARY
G10.1 harness: PASS (1 valid, 5 negative cases)
```

별도 단위 시험도 실행합니다.

```bash
python3 -m unittest discover -s labs/g10_1_release_map/tests -p 'test_*.py' -v
```

`Ran 4 tests`와 마지막 `OK`를 확인합니다.

## 내 책임 지도 만들기

원본을 작업 디렉터리에 복사한 뒤 편집합니다.

```bash
mkdir -p study/g10.1
cp labs/g10_1_release_map/starter/release-map.json study/g10.1/release-map.json
python3 labs/g10_1_release_map/validator.py --profile submission study/g10.1/release-map.json
```

첫 실행은 실패가 정상입니다. `E_CITATION_ID`, `E_SOURCE_ACCESS`, `E_CITATION_LOCATOR`는 R25-11 원문을 직접 읽은 기록이 비어 있다는 뜻입니다. 다음 순서로 채웁니다.

1. AUTOSAR Adaptive Platform 공식 페이지에서 R25-11 문서를 내려받는다.
2. `source_ledger`에 실제 문서 식별자, 화면에 보이는 절 제목과 절 번호 또는 requirement ID, 확인 날짜를 적는다.
3. P02/P03의 로컬 파일과 실행 주체를 각 행에 연결하고 `Mapped / Partial / Missing / Out of scope` 중 하나를 고른다.
4. `limitations`에 공식 API, ARXML, 생성기, 배포 도구와 다른 점을 구체적으로 남긴다.
5. 상태 개수를 다시 세어 `summary`를 고친다.

완성된 제출물은 한 줄의 `PASS G10.1-MAP ...`을 출력합니다. 이 결과는 형식과 내부 일관성 통과를 뜻합니다. Sprint 검토자는 연결된 원문 절과 로컬 파일을 함께 확인합니다.

## 검사 범위

- 고정 순서: Service Interface → Proxy/Skeleton → Service Instance/Deployment → SOME/IP binding → Executable/Process → Function Group State → Health Supervision
- 산출물 단계: design-time, generation-time, deployment-time, runtime
- 한 고장 시나리오의 역할: State Management가 목표를 정하고, Execution Management가 실행 계획을 적용하며, Platform Health Management가 supervision 결과를 관찰
- 로컬 구현 표기: `concept-aligned local prototype`
- 행별 citation ID와 R25-11 자료 장부 연결
- 매핑 상태 집계의 재계산

검사기가 알아내지 못하는 부분도 있습니다. 인용 절의 해석, 빠진 functional cluster, 원문 사이의 충돌, 실제 SDK·ARXML 적합성은 사람의 검토 범위입니다.
