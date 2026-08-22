# Linux Lifecycle Ownership Contract

프로세스 하나에 재시작 actuator를 둘 이상 두지 않습니다. systemd, P01, P03, PHM, UCM의 역할은 아래 표로 고정합니다.

| 대상 | 부팅 책임 | lifecycle 결정 | action 실행 | 건강 관찰 |
| --- | --- | --- | --- | --- |
| Execution Manager 자체 | systemd | systemd unit policy | systemd | 외부 watchdog 또는 systemd watchdog |
| P03가 관리하는 application | P03 Process Controller | P03 Process Controller | P01 launcher·stopper | PHM-style monitor |
| update 중인 application set | systemd가 P03만 유지 | UCM 요청을 받은 P03 State/Process Controller | P01; slot 전환은 P04 | health check provider |

관리 대상 application의 systemd unit에는 `Restart=no`를 둡니다. systemd는 P03를 시작하고 resource·security envelope를 제공할 수 있지만 application 재시작을 직접 결정하지 않습니다. PHM-style monitor는 고장을 관찰하고 recovery request를 보냅니다. restart, degraded state, shutdown 중 무엇을 실행할지는 P03의 versioned policy가 정합니다.

## 프로세스 instance 식별

PID만으로 instance를 식별하지 않습니다. 기본 handle은 다음 값을 묶습니다.

- P03가 발급한 128-bit `process_instance_id`
- `pidfd`
- executable·manifest generation
- 전용 cgroup 경로와 inode 또는 동등한 identity
- spawn 시각의 monotonic sequence

timer와 signal action은 `pidfd`와 instance generation을 다시 확인한 뒤 실행합니다. PID가 재사용됐거나 cgroup identity가 바뀌면 stale action으로 거부합니다.

## descendant containment

process group은 협조적인 child의 signal 전달에 사용합니다. 완전한 containment는 전용 cgroup v2를 기준으로 합니다.

1. spawn 전에 빈 cgroup을 준비합니다.
2. child를 전용 process group과 cgroup에 넣습니다.
3. P01은 subreaper로 고아 descendant를 회수합니다.
4. 정상 종료는 application protocol 또는 SIGTERM으로 시작합니다.
5. timeout 뒤 `cgroup.kill` 또는 동등한 cgroup-wide action을 실행합니다.
6. cgroup이 비고 모든 wait status가 회수된 뒤 instance를 종료 처리합니다.

`setsid()`, double-fork, 새 process group, signal 무시, fork bomb, supervisor crash를 시험 corpus에 넣습니다. cgroup·pidfd를 쓰지 않는 port는 주장 범위를 `동일 process group 안의 협조적인 descendant`로 줄입니다.

## 시작 완료 신호

다음 사건을 각각 기록합니다.

| 사건 | 의미 |
| --- | --- |
| Spawned | process image 실행이 시작됨 |
| ExecutionReady | process instance가 P03 readiness channel로 준비를 보고함 |
| ServiceOffered | service binding이 offer를 시작함 |
| Healthy | 정해진 supervision window를 통과함 |

`ExecutionReady`는 Unix domain socket 또는 상속한 descriptor를 사용합니다. `SO_PEERCRED`, process instance ID, one-time nonce를 확인해 다른 process가 대신 Ready를 보낼 수 없게 합니다. P03는 `ServiceOffered`나 첫 heartbeat를 spawn 성공과 같은 사건으로 처리하지 않습니다.

## 부팅과 저장된 상태

Persistency에는 마지막으로 승인된 요청, config generation, restart budget, 마지막 완전한 transition 결과를 저장할 수 있습니다. 저장된 `Driving`, `Diagnostic`, `Update` 값을 현재 commanded state로 바로 적용하지 않습니다.

부팅 순서는 고정합니다.

1. `Startup`으로 시작합니다.
2. 저장 record의 schema, generation, checksum 또는 authenticity를 확인합니다.
3. 현재 vehicle condition, software compatibility, process inventory를 다시 읽습니다.
4. 이전 요청을 재적용할 수 있는지 State Controller가 새 transition으로 판단합니다.
5. 조건이 맞지 않으면 안전한 startup policy에 머물고 이유를 기록합니다.

## 자동으로 넣을 고장

- PID 재사용 뒤 늦게 도착한 restart timer
- child의 `setsid()`와 double-fork
- systemd와 P03의 동시 restart 시도
- PHM recovery request와 shutdown request 경합
- 이전 instance가 보낸 Ready·heartbeat
- 저장된 `Driving` 상태와 현재 update-only boot condition 충돌
- UCM activation 중 service crash와 Function Group State 변경

모든 scenario는 최종 process inventory, active restart owner, policy version, transition ID, 소요 시간을 oracle과 비교합니다.
