# GitHub 저장소 운영

연결된 GitHub 계정 `ThePo1es`를 기준으로 작성한 절차입니다.

## 1. 처음 내려받기

```bash
git clone https://github.com/ThePo1es/adaptive-vehicle-platform-lab.git
cd adaptive-vehicle-platform-lab

git config user.name "ThePo1es"
git config user.email "190378110+ThePo1es@users.noreply.github.com"

bash scripts/check_repo.sh
```

SSH를 사용한다면 clone URL을 다음처럼 바꿉니다.

```bash
git clone git@github.com:ThePo1es/adaptive-vehicle-platform-lab.git
```

라이선스는 실제 공개할 코드와 외부 의존성의 라이선스를 확인한 뒤 별도 커밋으로 선택합니다.

## 2. GitHub 설정

저장소의 `Settings`에서 다음을 적용합니다.

1. `General > Features > Issues` 활성화
2. `Pull Requests > Allow squash merging` 활성화
3. `Pull Requests > Automatically delete head branches` 활성화
4. `Branches > Add branch protection rule`에서 `main` 보호
5. `Require a pull request before merging` 활성화
6. `Require status checks to pass`에서 `docs-integrity` 선택

혼자 쓰는 저장소이므로 승인자 수 강제는 필요 없습니다. 대신 모든 의미 있는 변경을 PR로 올려 self-review 기록을 남깁니다.

현재 `docs-integrity`는 문서 구조, 내부 링크, 요구사항 추적 형식과 민감 확장자를 검사합니다. C/C++ source나 `CMakeLists.txt`가 생기면 `LICENSE` 또는 `LICENSE.md`, `THIRD_PARTY_NOTICES.md`, 별도 `code-build` workflow가 모두 있어야 검사를 통과합니다.

| 구현 단계 | Required check |
| --- | --- |
| Host C/C++ | GCC/Clang build, unit test, ASan/UBSan |
| Parser/state machine | fuzz smoke, coverage, mutation/model test |
| Cortex-M | cross compile, size/map artifact, simulator smoke |
| Linux service | integration test, package/image smoke |
| Hardware | CI 밖의 HIL record와 reviewer link |

`docs-integrity`의 녹색 상태는 문서 무결성만 표시합니다.

## 3. 이슈·마일스톤·Project 보드

다음 labels를 GitHub UI에서 한 번 생성합니다.

| Label | Use |
| --- | --- |
| `study` | Gate 내부의 주차별 학습 질문과 노트 |
| `experiment` | 가설·실험·측정 |
| `project` | 구현 작업 |
| `mastery-gate` | Gate 승급 시험과 재시험 |
| `long-term` | G12 이후 유지보수·이식·연구·교육 근거 |
| `documentation` | 아키텍처·요구사항·보고서 |
| `blocked` | 외부 조건 때문에 진행 불가 |
| `safety-review` | 실차·벤치·민감 데이터 검토 필요 |

Milestone은 `G0 — Engineering Baseline`부터 `G12 — Architecture and Integration`까지 만듭니다. 각 Study/Experiment/Project 이슈에 현재 Gate milestone을 지정하고, exit artifact가 준비되면 닫습니다.

G12 통과 뒤에는 `E1 — Maintainer`부터 `E4 — Architecture/Teaching` milestone을 추가합니다. 시작 전에 맡을 하위 시스템과 검토자를 정합니다.

GitHub Project를 추가한다면 Board view 하나로 충분합니다.

```text
Backlog → This week → In progress → Evidence review → Gate review → Done
```

`Done`에는 PR, 학습 노트, 테스트/측정 증거가 모두 연결된 이슈만 이동합니다. Gate milestone은 `Mastery gate review`까지 통과해야 닫습니다.

## 4. 매주 반복할 명령

```bash
git switch main
git pull --ff-only

./scripts/new-study-log.sh 2 "C integer conversions and bit extraction"
git switch -c study/g01-w02-integer-conversions

# 학습·실험·코드 작성 후
./scripts/check_repo.sh
git add .
git commit -m "study(g01-w02): test C integer conversions"
git push -u origin HEAD
```

GitHub에서 PR을 열고 템플릿의 확인 항목을 채운 뒤 squash merge합니다.

## 5. 커밋 규칙

```text
study(gNN-wNN): 학습 내용
feat(pNN): 프로젝트 기능
test(pNN): 테스트 또는 장애 주입
docs: 문서·아키텍처·측정 결과
fix(pNN): 버그 수정
chore: 빌드·CI·저장소 관리
```

예시:

```text
study(g01-w05): compare defined and undefined bit extraction
feat(p02): publish vehicle speed events through SOME/IP
test(p04): reject rollback package after interrupted update
docs: add p99 event latency report
```

Gate를 통과할 때는 새 `Mastery gate review` 이슈를 만들고 [평가 기준](ASSESSMENTS.md)과 [review template](docs/templates/mastery-review.md)의 증거를 연결합니다. 분기 누적 시험은 별도 `mastery-gate` 이슈로 기록합니다.

## 6. 올리면 안 되는 것

- AUTOSAR PDF 원본과 라이선스가 불명확한 사양 파일
- 차량 VIN, 인증서, 개인 데이터, 위치, 실제 키·토큰
- OEM 비공개 펌웨어·DBC·진단 데이터
- 100MB 이상 캡처나 빌드 산출물
- 재현 절차 없이 결과 화면만 있는 기록

민감 정보가 이미 커밋됐다면 단순 삭제 커밋으로 끝내지 말고, 키를 폐기·교체한 후 Git history 정리 여부를 판단합니다.
