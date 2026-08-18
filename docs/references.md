# Official and Primary References

학습 노트는 가능하면 공식 사양, 공식 프로젝트 문서, 소스 코드와 테스트를 우선 근거로 사용합니다. 블로그와 영상은 탐색용으로만 사용하고 핵심 주장의 최종 근거로 삼지 않습니다.

## Adaptive Platform

- [AUTOSAR Adaptive Platform](https://www.autosar.org/standards/adaptive-platform/)
- [R25-11: Explanation of Adaptive Platform Software Architecture](https://www.autosar.org/fileadmin/standards/R25-11/AP/AUTOSAR_AP_EXP_SWArchitecture.pdf)
- [R25-11: Update and Configuration Management](https://www.autosar.org/fileadmin/standards/R25-11/AP/AUTOSAR_AP_SWS_UpdateAndConfigurationManagement.pdf)

AUTOSAR 문서는 링크로 참조하고 저장소 안에 복제하지 않습니다. 읽은 절, 핵심 주장, 내 실험과의 관계를 학습 노트에 기록합니다.

## Communication and Logging

- [COVESA vsomeip](https://github.com/COVESA/vsomeip)
- [vsomeip User Guide](https://github.com/COVESA/vsomeip/blob/master/documentation/vsomeipUserGuide.md)
- [CommonAPI C++ SOME/IP](https://covesa.github.io/capicxx-someip-tools/)
- [COVESA DLT daemon](https://github.com/COVESA/dlt-daemon)

CommonAPI/vsomeip은 공개 학습 도구이며 `ara::com` 구현과 동일시하지 않습니다. DLT daemon도 `ara::log` 구현이라고 부르지 않습니다.

## SDV Platform Engineering

- [Eclipse S-CORE documentation](https://eclipse-score.github.io/score/main/)

S-CORE는 요구사항 추적성, 빌드·CI, work product와 공개 SDV 구성요소를 참고하는 용도로 사용합니다. 이 저장소의 초반 목표를 S-CORE 전체 빌드로 바꾸지 않습니다.

## 노트 인용 규칙

```markdown
- Claim: 내가 확인한 기술적 주장
- Source: 공식 문서명, release, section 또는 source file/commit
- Checked: YYYY-MM-DD
- Evidence: 내 실험·테스트·캡처 링크
- Confidence: Confirmed / Partially confirmed / Unverified
```

