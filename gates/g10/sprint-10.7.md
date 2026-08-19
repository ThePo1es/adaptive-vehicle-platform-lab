# Sprint 10.7 — Managed Linux vehicle node

## 시간과 기준 자료

24–30시간. [P01](../../projects/01-process-supervisor/README.md), [P02](../../projects/02-vehicle-state-service/README.md), [P03](../../projects/03-execution-manager/README.md)의 release artifact와 G10.1 책임 지도를 사용합니다. 세 project version과 interface compatibility matrix를 시작 전에 동결합니다.

## 시작 조건과 deployment

Buildroot AArch64 image에 Execution Manager, Process Supervisor, Vehicle State Service, simulator, consumer를 넣습니다. manifest는 dependency, state별 process set, restart, health, resource policy를 담습니다. service version과 manifest version의 호환 규칙을 배포 표에 적습니다.

## 안내 실습

boot에서 manifest validation, dependency plan, process start, health status, service offer, consumer subscription까지 하나의 timeline을 만듭니다. `Startup → Driving → Diagnostic → Shutdown` transition마다 기대 process set과 service availability를 oracle JSON에 둡니다.

## 독립 실습

service crash, heartbeat stop, dependency start failure, corrupted persisted state, incompatible service major를 차례로 넣습니다. scenario마다 detection deadline, recovery budget, target state, process set, client-visible availability를 확인합니다.

## 전이 과제

검토자가 두 fault를 겹칩니다. 예시는 service restart 중 state change, persistency corruption과 dependency failure, subscription 중 provider kill입니다. 첫 fault가 두 번째 fault의 evidence를 지우지 않게 correlation chain을 보존합니다.

## 판정 기준

- clean boot와 네 state transition이 oracle process/service set과 일치
- 다섯 단일 fault와 한 복합 fault가 bounded result로 끝남
- EM/SM/PHM 역할에 해당하는 local component 경계가 trace에서 보임
- health recovery 뒤 service availability·subscription 상태가 일관됨
- incompatible deployment가 시작 전에 거부되거나 격리된 degraded state에서 해당 service를 offer하지 않음
- 새 AArch64 VM에서 image build와 scenario suite를 재현

## 힌트

1. component log의 timestamp만 맞추지 말고 공통 transition·run ID를 전달합니다.
2. partial failure 뒤 reported state와 실제 process/service inventory를 비교합니다.
3. integration에서 발견한 fault는 가장 낮은 소유 component에 regression test를 둡니다.

## 치명적 실패와 보충

reported state와 실제 process set이 다르거나, health recovery가 restart storm으로 번지거나, 새 환경 배포가 안 되면 실패입니다. 해당 component Sprint로 돌아가 수정한 뒤 integration fault 전체를 다시 실행합니다.
