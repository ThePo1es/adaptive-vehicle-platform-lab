# Sprint 10.6 — Persistency와 구조화 로그

## 시간과 기준 자료

24–30시간. R25-11 `Persistency`와 `Log and Trace` 문서에서 데이터 식별, update/recovery, log context·severity 관련 절을 읽습니다. POSIX의 [`fsync`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fsync.html)와 [`rename`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html) 의미도 함께 확인합니다.

## 시작 조건과 데이터 계약

P03는 last accepted config version, last stable state, restart budget, monotonic generation을 저장합니다. file format에 magic, schema version, payload length, generation, checksum을 둡니다. secret와 개인 정보는 저장 대상에서 제외합니다.

## 안내 실습

temporary file write, data sync, atomic rename, parent directory sync 순서의 store를 구현합니다. 각 system call 경계에서 process를 kill하고 재부팅 후 old 또는 new complete record 중 하나만 읽히는지 확인합니다. 실제 보장 범위는 사용한 filesystem과 mount option까지 적습니다.

## 독립 실습

truncated record, bit flip, unknown version, rollback generation, disk full, permission error corpus를 처리합니다. 안전한 default로 복구하되 손상 원인과 선택한 record를 audit event에 남깁니다. log에는 run, process instance, transition, supervision, config generation correlation ID를 넣습니다.

## 전이 과제

검토자가 write sequence의 임의 지점에서 100회 kill하는 campaign과 corrupt record 하나를 줍니다. reference state model과 reboot 결과를 비교합니다. log만 받아 state transition과 recovery action을 재구성하는 과제도 수행합니다.

## 판정 기준

- 모든 kill point에서 old/new complete state 또는 문서화된 safe default
- checksum·version·length 오류가 구분되고 손상 payload를 사용하지 않음
- disk full과 permission 오류가 runtime state를 거짓 성공으로 보고하지 않음
- audit event만으로 요청→결정→action→결과 chain을 재구성
- log flood에서 bounded queue와 drop counter가 동작
- host filesystem 실험의 보장과 R25-11 Persistency mapping 범위를 따로 기록

## 힌트

1. file `fsync`와 directory entry durability는 구분해서 시험합니다.
2. checksum은 우발적 손상 감지용입니다. authenticity 요구는 G11에서 다룹니다.
3. wall-clock timestamp와 event ordering sequence를 함께 남깁니다.

## 치명적 실패와 보충

부분 record를 정상으로 읽거나, persist 실패 뒤 success를 기록하거나, log에 credential·key를 남기면 실패입니다. 보충 과제는 단일 record와 kill point 다섯 개만 다시 검증하는 것입니다.
