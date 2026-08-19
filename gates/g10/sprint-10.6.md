# Sprint 10.6 — Persistency와 구조화 로그

## 시간과 기준 자료

24–32시간. R25-11 `Persistency`와 `Log and Trace` 문서에서 데이터 식별, update/recovery, log context·severity 관련 절을 읽습니다. POSIX의 [`fsync`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fsync.html)와 [`rename`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html) 의미도 함께 확인합니다.

## 시작 조건과 데이터 계약

P03는 last accepted config version, last accepted 상태 request, completed transition result, restart budget, monotonic generation을 저장합니다. persisted observation/request와 current commanded 상태를 다른 type으로 둡니다. file format에는 magic, schema version, payload length, generation, checksum을 넣고 secret와 개인 정보는 저장하지 않습니다.

## 안내 실습

temporary file write, data sync, atomic rename, parent directory sync 순서의 store를 구현합니다. 각 system call 경계에서 프로세스를 kill하고 재부팅 후 old 또는 new complete record 중 하나만 읽히는지 확인합니다. 실제 보장 범위는 사용한 filesystem과 mount option까지 적습니다.

## 독립 실습

truncated record, bit flip, unknown version, rollback generation, disk full, permission error corpus를 처리합니다. boot는 항상 `Startup`에서 시작하고 현재 vehicle condition, software compatibility, 프로세스 inventory를 확인한 뒤 새 transition을 결정합니다. 손상 원인과 선택한 record는 audit 이벤트에 남깁니다.

## 전이 과제

봉인 campaign은 write sequence의 임의 지점에서 100회 kill하며 corrupt record 하나를 포함합니다. reference 상태 model과 reboot 결과를 비교합니다. log만 받아 상태 transition과 recovery action을 재구성하는 과제도 수행합니다.

## 판정 기준

- 모든 kill point에서 old/new complete 상태 또는 문서화된 safe default
- checksum·version·length 오류가 구분되고 손상 payload를 사용하지 않음
- disk full과 permission 오류가 runtime 상태를 거짓 성공으로 보고하지 않음
- audit 이벤트만으로 요청→결정→action→결과 chain을 재구성
- log flood에서 bounded queue와 drop counter가 동작
- host filesystem 실험의 보장과 R25-11 Persistency mapping 범위를 따로 기록
- stored `Driving/Diagnostic/Update` 요청이 boot에서 자동 commanded 상태가 되지 않음

## 저장 경로 점검

1. file `fsync`와 directory entry durability는 구분해서 시험합니다.
2. checksum은 우발적 손상 감지용입니다. authenticity 요구는 G11에서 다룹니다.
3. wall-clock timestamp와 이벤트 ordering sequence를 함께 남깁니다.

## 복구 시험을 다시 할 조건

부분 record를 정상으로 읽었거나 저장 실패 뒤 성공을 기록했거나 로그에 credential·key가 남았다면 단일 record와 종료 지점 다섯 개로 줄입니다. old/new complete record 또는 안전 기본값만 나오는지 다시 확인합니다.
