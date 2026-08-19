# Sprint 8.7 — P01 Linux 릴리스

## 시간과 기준 자료

24–30시간. [P01 완료 증거](../../projects/01-process-supervisor/README.md), [mastery review 양식](../../docs/templates/mastery-review.md), 이전 Sprint의 Buildroot·systemd·cgroup 정책을 기준으로 사용합니다. 이 Sprint가 시작되면 합격 기준과 fault seed를 동결합니다.

## 릴리스 입력

P01 source, test fixture, systemd unit, Buildroot external tree, SBOM, release manifest를 하나의 version tag 후보로 묶습니다. QEMU AArch64는 필수이며 실제 board 결과는 별도 evidence lane으로 표시합니다.

## 안내 실습

다음 campaign runner를 만듭니다.

1. 정상 시작·정지 100회
2. non-zero crash와 restart limit
3. SIGTERM 무시와 강제 종료
4. grandchild 생성 후 parent exit
5. memory, CPU, PID pressure
6. supervisor 자체 재시작

각 case는 시작 전 process/cgroup snapshot과 종료 후 snapshot을 비교합니다.

## 독립 실습

새 VM에서 source archive 또는 Git tag만으로 image를 만들고 target에 부팅합니다. 장애 campaign의 raw log를 parsing해 recovery time, restart count, orphan/zombie count, peak resource를 표로 만듭니다. 실패 case를 숨기지 않고 재현 명령과 disposition을 붙입니다.

## 전이 과제

외부 검토자가 policy 값 하나와 fixture 순서 하나를 바꿉니다. 구현 수정 없이 설정으로 수용할 수 있는 범위와 code 변경이 필요한 경계를 설명합니다. 검토자는 README만 보고 build와 세 fault를 실행합니다.

## 판정 기준

- process tree 전체가 shutdown 상한 안에 정리되고 zombie/orphan 0건
- restart와 backoff가 virtual clock oracle 및 target log에서 일치
- hardening과 resource policy의 positive/negative test 통과
- 새 환경에서 image build, boot, P01 실행, fault 세 개 재현
- release에 source revision, toolchain, image hash, SBOM, 알려진 한계 포함
- 검토자가 lifecycle, policy, mechanism 경계를 구두로 바꿔 물어도 답하고 필요한 test 위치를 찾음

## 힌트

1. campaign runner가 host의 다른 process를 건드리지 않도록 전용 VM과 고정된 cgroup을 씁니다.
2. recovery time의 시작·끝 event를 문서에서 먼저 정의합니다.
3. release note에는 실험하지 않은 architecture와 kernel을 지원 대상으로 적지 않습니다.

## 치명적 실패와 보충

외부 재현이 안 되거나, fault 뒤 child가 남거나, raw log 없이 요약 수치만 제출하면 Gate를 통과하지 못합니다. 실패 영역 Sprint로 돌아가 12–20시간 보강한 뒤 새 tag와 새 fault seed로 다시 심사합니다.
