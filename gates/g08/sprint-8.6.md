# Sprint 8.6 — Buildroot 이미지와 BSP 경계

## 시간과 기준 자료

24–30시간. [Buildroot 2026.05 manual](https://buildroot.org/downloads/manual/manual.html)의 configuration, out-of-tree build, project-specific customization, package, legal notice 절과 Linux kernel의 [Device Tree usage model](https://docs.kernel.org/devicetree/usage-model.html)을 읽습니다. 시작할 때 Buildroot release tarball과 source hash를 고정합니다.

## 시작 조건과 target

AArch64 QEMU `virt`를 필수 target으로 사용합니다. 보유한 AArch64 board는 두 번째 target으로 추가할 수 있습니다. `BR2_EXTERNAL`, defconfig, rootfs overlay, P01 package, kernel fragment, post-build script를 저장소에서 추적합니다.

## 안내 실습

out-of-tree directory에서 최소 이미지를 만들고 kernel, Device Tree, root filesystem, init 순서의 boot log를 주석 처리합니다. P01 package를 cross-compile해 systemd service로 부팅하고 read-only rootfs 또는 명시된 writable partition에서 동작시킵니다.

## 독립 실습

Device Tree에서 serial 또는 virtio 장치 하나의 node, compatible, interrupt, address가 driver와 연결되는 경로를 설명합니다. board가 있으면 LED/UART 등 안전한 peripheral 하나를 overlay 또는 board DTS로 변경합니다. kernel module 작성은 이번 범위에 넣지 않습니다.

Buildroot가 만든 package manifest, license 자료, CycloneDX SBOM을 보관합니다. image, kernel, DTB, defconfig, toolchain의 SHA-256과 build duration을 release manifest에 적습니다.

## 전이 과제

빈 build directory와 새 container/VM에서 release tag만 받아 이미지를 다시 만듭니다. 검토자가 RAM 크기, console, network interface 중 하나를 바꾼 target을 줍니다. 필요한 config와 DT 차이를 찾아 부팅 근거를 제출합니다.

## 판정 기준

- clone부터 QEMU login과 P01 active 상태까지 문서 명령으로 재현
- defconfig와 external tree 외의 수동 output 변경이 0건
- boot log에서 bootloader/kernel/DT/init/P01 경계를 설명
- package manifest, SBOM, legal-info, artifact hash가 release에 포함
- 동일 입력 두 build의 차이를 diffoscope 또는 hash 비교로 설명
- 실제 board 결과와 QEMU 결과를 섞지 않고 target별로 표시

## 힌트

1. `output/` 수정은 다음 clean build에서 사라집니다.
2. 완전한 bit-for-bit 재현이 깨지면 timestamp, host tool, archive ordering부터 좁힙니다.
3. Device Tree는 hardware description과 driver binding을 함께 읽습니다.

## 치명적 실패와 보충

binary toolchain이나 download cache를 출처 없이 배포하거나, output directory를 손으로 고쳐 성공시키거나, SBOM에 없는 binary를 image에 넣으면 실패입니다. 보충 과제는 QEMU target 하나만 남겨 clean image와 artifact manifest를 다시 만드는 것입니다.
