# Sprint 8.7 — P01 Linux 릴리스

## 시간과 기준 자료

24–30시간. [P01 완료 증거](../../projects/01-process-supervisor/README.md), [숙련도 검토 양식](../../docs/templates/mastery-review.md), 이전 Sprint의 Buildroot·systemd·cgroup 정책을 기준으로 사용합니다. 이 Sprint가 시작되면 합격 기준과 고장 seed를 동결합니다.

## 릴리스 입력

P01 source, 시험 프로그램, systemd unit, Buildroot external tree, SBOM, 릴리스 manifest를 하나의 version tag 후보로 묶습니다. QEMU AArch64 결과와 실제 board 결과는 다른 디렉터리와 보고서에 둡니다.

## 안내 실습

다음 campaign runner를 만듭니다.

1. 정상 시작·정지 100회
2. non-zero crash와 restart limit
3. SIGTERM 무시와 강제 종료
4. grandchild 생성 후 parent exit
5. memory, CPU, PID pressure
6. supervisor 자체 재시작

각 시나리오는 시작 전 프로세스·cgroup 상태와 종료 후 상태를 비교합니다.

## 독립 실습

새 VM에서 source archive 또는 Git tag만으로 image를 만들고 대상에 부팅합니다. 장애 실험의 원본 로그에서 복구 시간, 재시작 횟수, orphan·zombie 수, 최대 자원 사용량을 계산합니다. 실패한 항목에는 재현 명령과 처리 계획을 붙입니다.

## 전이 과제

외부 검토자가 policy 값 하나와 fixture 순서 하나를 바꿉니다. 구현 수정 없이 설정으로 수용할 수 있는 범위와 code 변경이 필요한 경계를 설명합니다. 검토자는 README만 보고 build와 세 고장를 실행합니다.

## 판정 기준

- 전용 cgroup의 descendant 전체가 shutdown 상한 안에 정리되고 zombie/orphan 0건
- restart와 backoff가 virtual clock oracle 및 대상 log에서 일치
- hardening과 resource policy의 positive/negative 테스트 통과
- 새 환경에서 image build, boot, P01 실행, 고장 세 개 재현
- 릴리스에 source revision, toolchain, image hash, SBOM, 알려진 한계 포함
- 검토자가 lifecycle 결정, policy, Linux mechanism의 소유자를 바꿔 물어도 관련 시험과 문서를 찾음

## 힌트

1. campaign runner가 host의 다른 프로세스를 건드리지 않도록 전용 VM과 고정된 cgroup을 씁니다.
2. recovery time의 시작·끝 이벤트를 문서에서 먼저 정의합니다.
3. 릴리스 note에는 실험하지 않은 architecture와 kernel을 지원 대상으로 적지 않습니다.

## 치명적 실패와 보충

외부 재현이 안 되거나, 고장 뒤 child가 남거나, raw log 없이 요약 수치만 제출하면 Gate를 통과하지 못합니다. 실패 영역 Sprint로 돌아가 12–20시간 보강한 뒤 새 tag와 새 고장 seed로 다시 심사합니다.
