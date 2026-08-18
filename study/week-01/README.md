# Week 01 — Adaptive Architecture and Project Boundary

## 이번 주 결론 목표

Adaptive Application, Functional Cluster, POSIX OS의 관계와 EM·SM·PHM·COM·PER·UCM의 책임 경계를 설명하고, 첫 프로젝트인 Process Supervisor의 범위를 확정합니다.

## 핵심 질문

1. Adaptive Application을 프로세스 단위로 배포·실행하는 이유는 무엇인가?
2. State Management가 상태를 결정하는 것과 Execution Management가 프로세스를 실행하는 것은 어떻게 다른가?
3. Platform Health Management가 일반 process restart loop와 다른 점은 무엇인가?
4. Service interface와 service instance는 어떻게 다른가?
5. 공개 오픈소스로 구현할 수 있는 부분과 AUTOSAR 적합성을 검증할 수 없는 부분은 어디인가?

## 읽을 자료

- [AUTOSAR Adaptive Platform](https://www.autosar.org/standards/adaptive-platform/)
- [R25-11 Software Architecture explanation](https://www.autosar.org/fileadmin/standards/R25-11/AP/AUTOSAR_AP_EXP_SWArchitecture.pdf)
- 저장소의 [AUTOSAR concept mapping](../../docs/autosar-mapping.md)

## 해야 할 일

- [ ] Adaptive Application → Functional Cluster → POSIX OS 관계를 직접 그린다.
- [ ] EM, SM, PHM, COM, PER, UCM을 각각 3문장 이내로 설명한다.
- [ ] Classic signal/RTE 방식과 Adaptive service-oriented 방식의 차이를 표로 정리한다.
- [ ] Machine/Application/Execution Manifest가 결정하는 범위를 구분한다.
- [ ] `projects/01-process-supervisor/README.md`의 요구사항과 제외 범위를 검토한다.
- [ ] 학습 중 불확실한 항목을 `Unverified`로 분리한다.

## 최소 실험

아직 AUTOSAR API를 구현하지 않습니다. Linux 프로세스의 observable lifecycle을 먼저 확인합니다.

```bash
python3 -c 'import os,signal,time; print(os.getpid(), flush=True); signal.signal(signal.SIGTERM, lambda *_: exit(0)); time.sleep(30)'
```

다른 터미널에서 PID에 SIGTERM을 보내고, 정상 종료 status와 로그에 필요한 정보를 정리합니다.

## 주차 통과 기준

- [ ] 노트를 보지 않고 EM·SM·PHM의 입력, 결정, 출력을 구분해 설명할 수 있다.
- [ ] SOME/IP 실습과 Adaptive Platform 구현을 같은 것으로 부르지 않는다.
- [ ] Process Supervisor v1에서 구현할 것과 구현하지 않을 것이 명확하다.
- [ ] 다음 주 이슈에 POSIX lifecycle 실험 3개와 예상 결과가 작성되어 있다.

## 결과 및 회고

작업 후 아래를 채웁니다.

- 확인한 내용:
- 틀렸던 가정:
- 아직 불확실한 내용:
- 다음 주에 검증할 내용:

