# Primary References

Gate 시작 이슈에서 실제로 읽을 문서와 절을 고정합니다. Version, edition, commit, 접근 상태와 확인 날짜를 함께 적습니다.

## Source Manifest

```markdown
| Field | Value |
| --- | --- |
| Gate / question | |
| Document / repository | |
| Edition / release / commit | |
| Exact section / source / test | |
| Access | Available / Limited / Unavailable |
| Purpose | 어떤 설계·시험 결정을 확인할지 |
| Checked | YYYY-MM-DD |
| Local evidence | experiment/report link |
| Confidence | Confirmed / Partial / Unverified |
```

유료 규격에 접근할 수 없으면 공개 공식 설명, Linux kernel 문서, 공개 구현체의 source와 interoperability test를 사용합니다. Normative text를 직접 확인한 범위는 manifest에 표시합니다.

## G0–G3 Starter Source Pack

처음 네 Gate는 아래 절부터 읽습니다. Installed tool version과 문서 version이 다르면 차이를 이슈에 적습니다.

| Gate | Source | 읽을 절 | 연결할 실습 |
| --- | --- | --- | --- |
| G0 | [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html) | Step 0–2, Testing 관련 단계 | library + CTest skeleton |
| G0 | [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) | Introduction, Usage, Limitations | out-of-bounds/use-after-free 재현 |
| G0 | [Clang UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) | Available checks, Usage | overflow, shift, alignment 재현 |
| G1 | [WG14 N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) | 3.4, 6.2.6, 6.3.1, 6.5, 6.7.2.1, 6.7.3, 7.20.1, 7.24.2 | decoder, aliasing/alignment, `memcpy` 실험 |
| G1 | ISO/IEC 9899:2018 | 위 주제의 대응 절과 C17 변경 | C17 compiler mode 차이 기록 |
| G2 | [C++ working draft](https://eel.is/c%2B%2Bdraft/) | `[basic.life]`, `[basic.stc]`, `[class.copy.ctor]`, `[class.dtor]`, `[unique.ptr]`, `[atomics.order]`, `[intro.races]` | owner/view, RAII, race 실험 |
| G2 | ISO/IEC 14882:2020 | 위 stable name의 C++20 절 | compiler/library 지원 범위 기록 |
| G3 | [Arm ABI repository](https://github.com/ARM-software/abi-aa) | release를 고정한 `aapcs32`, `aapcs64`, `aaelf32`, `aaelf64` parameter passing·data type·stack·ELF 절 | ABI reverse walk |
| G3 | [LLVM LangRef](https://llvm.org/docs/LangRef.html) | Data Layout, Global Variables, Functions, Poison Values, Undefined Values, Memory Model | source→IR contract 분석 |
| G3 | [`opt` command guide](https://llvm.org/docs/CommandGuide/opt.html)와 [Optimization Remarks](https://llvm.org/docs/Remarks.html) | installed pass list, remark generation | pass·remark·기계어 비교 |

N1570은 공개 C11 working paper입니다. C17 실습의 최종 기준은 접근 가능한 ISO/IEC 9899:2018과 compiler documentation으로 보완합니다. C++ working draft도 사용 중인 C++20 edition과 stable section name을 대조합니다.

## C, C++, ARM and compiler

- [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)
- [Arm ABI specifications](https://github.com/ARM-software/abi-aa)
- [LLVM Language Reference](https://llvm.org/docs/LangRef.html)
- [LLVM Command Guide](https://llvm.org/docs/CommandGuide/)
- [Clang sanitizers](https://clang.llvm.org/docs/index.html)
- 선택한 MCU의 Arm core manual, vendor reference manual, schematic, errata

실험에는 language standard, target triple, CPU, ABI, compiler, flags, linker를 기록합니다. Sanitizer 결과는 사용한 instrumentation의 관찰 범위로 해석합니다.

## Real-time systems

- Jane W. S. Liu, *Real-Time Systems*
- Alan Burns and Andy Wellings, *Real-Time Systems and Programming Languages*
- [Response-time analysis literature survey and bounds](https://www-users.york.ac.uk/~rd17/papers/ResponseTimeUpperBound3.0.pdf)
- 선택 RTOS의 scheduling, interrupt, synchronization, timing 문서와 kernel tests
- [Zephyr Project documentation](https://docs.zephyrproject.org/)
- [Zephyr Twister](https://docs.zephyrproject.org/latest/develop/twister/index.html)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)

RTA equation은 task model, blocking, release jitter, interrupt interference와 함께 기록합니다. 실측 trace는 분석 가정과 bound를 점검하는 자료로 사용합니다.

## MCU and debug

- [Arm Cortex-M processors](https://developer.arm.com/Processors/Cortex-M)
- [QEMU Arm system emulator](https://www.qemu.org/docs/master/system/target-arm.html)
- [OpenOCD documentation](https://openocd.org/pages/documentation.html)
- board vendor HAL·example과 해당 silicon revision 문서

## Vehicle network and diagnostics

- [Linux SocketCAN documentation](https://docs.kernel.org/networking/can.html)
- [Linux ISO-TP documentation](https://docs.kernel.org/networking/iso15765-2.html)
- ISO 11898, ISO 15765-2, ISO 14229, ISO 13400의 합법적으로 접근 가능한 edition
- 선택한 CAN controller와 transceiver datasheet
- 사용한 UDS/DoIP tester의 versioned documentation

Gate G6/G9에서 timer, addressing, routing, session, NRC를 표로 옮기고 packet test와 연결합니다.

## AUTOSAR

- [AUTOSAR Classic Platform](https://www.autosar.org/standards/classic-platform/)
- [AUTOSAR Adaptive Platform](https://www.autosar.org/standards/adaptive-platform/)
- [AUTOSAR standards releases](https://www.autosar.org/standards/)
- [R25-11 Adaptive Platform Software Architecture](https://www.autosar.org/fileadmin/standards/R25-11/AP/AUTOSAR_AP_EXP_SWArchitecture.pdf)
- [R25-11 Update and Configuration Management](https://www.autosar.org/fileadmin/standards/R25-11/AP/AUTOSAR_AP_SWS_UpdateAndConfigurationManagement.pdf)

각 Gate는 release 하나를 고정합니다. 관련 module·functional cluster의 책임, interface, state, error handling을 local mapping에 연결합니다. AUTOSAR PDF는 링크로 참조하고 저장소에는 복제하지 않습니다.

## Linux, SOME/IP and platform tooling

- [Linux man-pages](https://www.kernel.org/doc/man-pages/)
- [Linux kernel documentation](https://docs.kernel.org/)
- [systemd documentation](https://systemd.io/)
- [Buildroot manual](https://buildroot.org/docs.html)
- [Yocto Project documentation](https://docs.yoctoproject.org/)
- [COVESA vsomeip](https://github.com/COVESA/vsomeip)
- [vsomeip User Guide](https://github.com/COVESA/vsomeip/blob/master/documentation/vsomeipUserGuide.md)
- [CommonAPI C++ SOME/IP](https://covesa.github.io/capicxx-someip-tools/)
- [COVESA DLT daemon](https://github.com/COVESA/dlt-daemon)

vsomeip, CommonAPI, DLT의 실제 역할과 local Adaptive mapping을 별도 표에 기록합니다.

## QNX portability

- 정식 접근 권한이 있는 QNX SDP release documentation
- [QNX Neutrino message passing overview](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.getting_started/topic/s1_msg.html)
- [QNX Neutrino programming overview](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.prog/topic/overview.html)
- [QNX resource managers](https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.resmgr/topic/overview.html)

QNX evidence에는 SDP version, target, channel/connection/pulse/resource-manager 사용과 tracing 결과를 넣습니다.

## Safety, cybersecurity and update

- [ISO 26262-1:2018](https://www.iso.org/standard/68383.html)
- [ISO/SAE 21434:2021](https://www.iso.org/standard/70918.html)
- ISO 24089의 합법적으로 접근 가능한 edition
- UNECE R155/R156의 공개 규정 원문
- 사용하는 crypto library의 official API, test vector, security policy
- target boot ROM/bootloader, secure storage, monotonic counter documentation

표준별 학습 목적과 교육용 work product는 [safety-security-engineering.md](safety-security-engineering.md)에 있습니다.

## Mixed-criticality 선택 Gate

- Steve Vestal, *Preemptive Scheduling of Multi-criticality Systems with Varying Degrees of Execution Time Assurance*
- Alan Burns and Robert Davis, *Mixed Criticality Systems — A Review*

M1에서는 criticality level, shared-resource interference, mode change, partitioning과 schedulability evidence를 다룹니다.

## SDV engineering

- [Eclipse S-CORE documentation](https://eclipse-score.github.io/score/main/)

요구사항 추적, build/CI, work product와 공개 SDV component를 참고합니다. 현재 Gate와 직접 연결되는 subsystem만 좁혀 읽습니다.
