# Official and Primary References

학습 노트는 가능하면 공식 사양, 공식 프로젝트 문서, 소스 코드와 테스트를 우선 근거로 사용합니다. 블로그와 영상은 탐색용으로만 사용하고 핵심 주장의 최종 근거로 삼지 않습니다.

## C, C++, ARM and compiler

- [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)
- [Arm ABI specifications](https://github.com/ARM-software/abi-aa)
- [LLVM Language Reference](https://llvm.org/docs/LangRef.html)
- [LLVM Command Guide](https://llvm.org/docs/CommandGuide/)
- [Clang UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)

언어·ABI·compiler 실험은 standard/version, target triple, compiler version과 flags를 기록합니다. sanitizer가 통과했다는 사실을 undefined behavior 부재의 증명으로 과장하지 않습니다.

## MCU and RTOS

- [Arm Cortex-M processors](https://developer.arm.com/Processors/Cortex-M)
- [Zephyr Project documentation](https://docs.zephyrproject.org/)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
- [FreeRTOS kernel book](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
- [QEMU Arm system emulator](https://www.qemu.org/docs/master/system/target-arm.html)
- [OpenOCD documentation](https://openocd.org/pages/documentation.html)

board vendor HAL/example은 해당 silicon revision의 reference manual, errata와 함께 확인합니다. RTOS 비교는 API 수가 아니라 scheduling, interrupt boundary, timing, memory, isolation과 testability 기준으로 수행합니다.

## Classic Platform

- [AUTOSAR Classic Platform](https://www.autosar.org/standards/classic-platform/)
- [AUTOSAR standards releases](https://www.autosar.org/standards/)

Classic 문서도 저장소에 복제하지 않습니다. OS/RTE/COM/PduR/CanIf/CanTp/DCM/DEM/NvM/WdgM/EcuM/BswM 중 현재 구현 경로에 필요한 책임과 interface만 좁혀 읽고, release와 document section을 노트에 기록합니다.

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
- [Linux kernel SocketCAN documentation](https://docs.kernel.org/networking/can.html)
- [Linux kernel ISO-TP documentation](https://docs.kernel.org/networking/iso15765-2.html)
- [Linux networking documentation](https://docs.kernel.org/networking/index.html)

CommonAPI/vsomeip은 공개 학습 도구이며 `ara::com` 구현과 동일시하지 않습니다. DLT daemon도 `ara::log` 구현이라고 부르지 않습니다.

## Linux platform and tooling

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [CMake documentation](https://cmake.org/documentation/)
- [Git documentation](https://git-scm.com/doc)
- [GoogleTest documentation](https://google.github.io/googletest/)

QNX 자료는 정식 접근 권한이 있는 경우 해당 release의 vendor documentation을 사용하고, Linux에서 관찰한 동작을 그대로 QNX의 보장으로 일반화하지 않습니다.

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
