# Sprint 10.2 — 매니페스트 스키마와 불변 실행 모델

## 시간과 기준 자료

26–34시간. R25-11 `Manifest Specification`과 `Execution Management`의 execution configuration 관련 절, [P03 Manifest 초안](../../projects/03-execution-manager/README.md)을 읽습니다. 로컬 YAML schema version은 `p03/v1`로 고정합니다.

## 시작 조건과 corpus

application name, executable, arguments, environment allowlist, dependencies, start states, restart policy, resource limits, health policy를 schema에 넣습니다. valid example 5개와 invalid example 20개를 준비합니다. unknown key, duplicate name, relative path escape, overflow duration, 빈 상태, 서로 모순된 limit을 포함합니다.

## 안내 실습

처리는 파싱, 문법·schema 검사, 의미 검사, 불변 실행 모델 생성으로 나눕니다. 오류에는 파일명, 경로, 잘못된 값, rule ID를 남깁니다. 실행 모델이 만들어진 뒤 원본 YAML을 바꿔도 실행 결과가 달라지지 않아야 합니다.

## 독립 실습

실행 파일과 환경 변수의 trust boundary를 정합니다. immutable read-only rootfs를 신뢰 가정으로 고정하거나, `openat2()`의 `RESOLVE_*`와 descriptor identity를 확인한 뒤 `execveat()` 등 fd 기반 실행을 사용합니다. duration과 count는 단위를 type에 포함하고 overflow를 막습니다. schema version upgrade fixture를 만들어 v1 unknown field 처리와 migration policy를 확인합니다.

YAML duplicate key, merge key, alias expansion, deep nesting, oversized document, symlink·rename·file-swap을 corpus에 넣습니다. duplicate key는 strict rejection으로 처리하고 parser별 resource limit을 고정합니다.

로컬 field를 R25-11 Execution Manifest, Service Instance Manifest, Machine Manifest 관련 요소에 매핑합니다. ARXML parser와 공식 schema를 구현하지 않은 상태는 표의 `Partial` 또는 `Missing` 열에 남깁니다.

## 전이 과제

검토자가 유효해 보이지만 의미가 충돌하는 manifest 세 개를 줍니다. runtime을 시작하기 전에 모두 거부하고 rule을 추가합니다. 하나의 새 optional field도 backward compatibility 절차에 맞춰 도입합니다.

## 판정 기준

- syntax, schema, semantic error가 서로 다른 code와 위치를 가짐
- invalid corpus 전체가 프로세스 spawn 전에 거부됨
- parse 뒤 runtime model이 불변이며 shared ownership/lifetime 테스트 통과
- path swap·symlink와 parser resource-limit corpus에서 crash·경계 우회 0건
- YAML field마다 requirement, 테스트, R25-11 mapping 상태가 연결됨
- `p03/v1` compatibility와 migration 규칙이 문서화됨

## 검증기 설계 메모

1. JSON Schema만으로 표현하기 어려운 graph·cross-field rule은 semantic validator에 둡니다.
2. 환경 변수를 통째로 상속하면 manifest에 없는 입력이 생깁니다.
3. 단위 없는 정수 duration은 config review에서 자주 놓칩니다.

## 검증기를 줄여야 할 때

검증 도중 프로세스를 실행했거나 알 수 없는 key를 조용히 넘겼거나 로컬 YAML을 AUTOSAR ARXML 호환으로 표시했다면 application 하나의 스키마로 돌아갑니다. 오류 입력 10개를 명확한 규칙 ID로 거부한 뒤 범위를 늘립니다.
