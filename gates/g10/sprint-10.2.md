# Sprint 10.2 — Manifest schema와 불변 모델

## 시간과 기준 자료

24–30시간. R25-11 `Manifest Specification`과 `Execution Management`의 execution configuration 관련 절, [P03 Manifest 초안](../../projects/03-execution-manager/README.md)을 읽습니다. 로컬 YAML schema version은 `p03/v1`로 고정합니다.

## 시작 조건과 corpus

application name, executable, arguments, environment allowlist, dependencies, start states, restart policy, resource limits, health policy를 schema에 넣습니다. valid example 5개와 invalid example 20개를 준비합니다. unknown key, duplicate name, relative path escape, overflow duration, 빈 state, 서로 모순된 limit을 포함합니다.

## 안내 실습

parse, syntax/schema validation, semantic validation, immutable domain model 변환 단계를 분리합니다. 오류에는 file, path, value, rule ID를 담습니다. validated model이 만들어진 뒤 원본 YAML 변경이 runtime behavior에 영향을 주지 않게 합니다.

## 독립 실습

실행 파일과 환경 변수의 trust boundary를 정하고 canonical path와 허용 directory를 검증합니다. duration과 count는 단위를 type에 포함하고 overflow를 막습니다. schema version upgrade fixture를 만들어 v1 unknown field 처리와 migration policy를 확인합니다.

로컬 field를 R25-11 Execution Manifest, Service Instance Manifest, Machine Manifest 관련 요소에 매핑합니다. ARXML parser와 공식 schema를 구현하지 않은 상태는 표의 `Partial` 또는 `Missing` 열에 남깁니다.

## 전이 과제

검토자가 유효해 보이지만 의미가 충돌하는 manifest 세 개를 줍니다. runtime을 시작하기 전에 모두 거부하고 rule을 추가합니다. 하나의 새 optional field도 backward compatibility 절차에 맞춰 도입합니다.

## 판정 기준

- syntax, schema, semantic error가 서로 다른 code와 위치를 가짐
- invalid corpus 전체가 process spawn 전에 거부됨
- parse 뒤 runtime model이 불변이며 shared ownership/lifetime test 통과
- path·duration·count 경계값 fuzz에서 crash와 우회 0건
- YAML field마다 requirement, test, R25-11 mapping 상태가 연결됨
- `p03/v1` compatibility와 migration 규칙이 문서화됨

## 힌트

1. JSON Schema만으로 표현하기 어려운 graph·cross-field rule은 semantic validator에 둡니다.
2. 환경 변수를 통째로 상속하면 manifest에 없는 입력이 생깁니다.
3. 단위 없는 정수 duration은 config review에서 자주 놓칩니다.

## 치명적 실패와 보충

validation 도중 process를 실행하거나, unknown key를 조용히 무시하거나, 로컬 YAML을 AUTOSAR ARXML 호환으로 표기하면 실패입니다. 보충 과제는 application 하나의 schema와 invalid corpus 10개만 다시 완성하는 것입니다.
