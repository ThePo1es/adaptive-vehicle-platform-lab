# Sprint 10.9 — 통합 Linux 차량 노드

## 시간과 기준 자료

24–28시간. [P01](../../projects/01-process-supervisor/README.md), [P02](../../projects/02-vehicle-state-service/README.md), [P03](../../projects/03-execution-manager/README.md)의 릴리스 산출물과 G10.1 책임 지도를 사용합니다. 세 프로젝트 버전과 인터페이스 호환표를 시작 전에 동결합니다.

## 시작 조건과 deployment

Buildroot AArch64 image에 Execution Manager, Process Supervisor, Vehicle State Service, Diagnostic Manager, Policy Engine, simulator, consumer를 넣습니다. manifest는 dependency, 상태별 프로세스 set, restart, health, resource policy를 담습니다. [lifecycle owner 표](../../docs/lifecycle-ownership.md)와 서비스·manifest 호환 규칙을 배포 문서에 넣습니다.

## 안내 실습

boot에서 manifest validation, dependency plan, 프로세스 start, health status, 서비스 offer, consumer subscription까지 하나의 timeline을 만듭니다. `Startup → Driving → Diagnostic → Shutdown` transition마다 기대 프로세스 set과 서비스 availability를 oracle JSON에 둡니다.

## 독립 실습

서비스 crash, heartbeat stop, dependency start failure, corrupted persisted 상태, incompatible 서비스 major를 차례로 넣습니다. scenario마다 detection deadline, recovery budget, 대상 상태, 프로세스 set, client-visible availability를 확인합니다.

## 전이 과제

전이 시험은 두 고장을 겹칩니다. 예시는 서비스 restart 중 상태 change, persistency corruption과 dependency failure, policy reload 중 diagnostic request입니다. 두 고장의 발생 원인과 복구 과정을 로그에서 따로 추적할 수 있어야 합니다.

## 판정 기준

- 정상 부팅과 네 상태 전이에서 프로세스·서비스 집합이 기준값과 일치
- 단일 고장 5종과 복합 고장 1종이 정해 둔 시간 안에 안정 상태로 수렴
- EM/SM/PHM/Diagnostics/IAM 역할에 해당하는 로컬 component 경계가 trace에서 보임
- health recovery 뒤 서비스 availability·subscription 상태가 일관됨
- incompatible deployment가 시작 전에 거부되거나 격리된 degraded 상태에서 해당 서비스를 offer하지 않음
- 새 AArch64 VM에서 image build와 scenario suite를 재현

## 힌트

1. component log의 timestamp만 맞추지 말고 공통 transition·run ID를 전달합니다.
2. 부분 실패 뒤 보고한 상태와 실제 프로세스·서비스 목록을 비교합니다.
3. integration에서 발견한 고장은 가장 낮은 소유 component에 regression 테스트를 둡니다.

## 통합 상태 불일치

reported 상태와 실제 프로세스 set이 다르거나, health recovery가 restart storm으로 번지거나, 새 환경 배포가 안 되면 실패입니다. 해당 component Sprint로 돌아가 수정한 뒤 integration 고장 전체를 다시 실행합니다.
