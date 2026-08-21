# CI 도구 잠금

`pyproject.toml`에는 자동 검사에 필요한 Python 패키지와 C/C++ 도구 버전을 적습니다. `uv.lock`은 내려받을 파일의 주소와 SHA-256까지 고정합니다. GitHub Actions에서 uv 자체를 설치할 때도 운영체제별 SHA-256을 확인합니다. 그다음 `uv sync --locked`로 잠금 파일을 확인하고, 이후 단계에서는 `--locked --no-sync --offline`으로 네트워크와 자동 갱신을 막습니다.

도구 버전을 바꿀 때는 `pyproject.toml`을 먼저 수정한 뒤 아래 명령으로 잠금 파일을 다시 만듭니다.

```bash
uv lock --project toolchain --python 3.12.13
uv sync --project toolchain --locked --python 3.12.13
```

두 파일의 변경 내용과 잠금 파일에 기록된 배포 파일 해시를 PR에서 함께 검토합니다. uv 버전을 올릴 때는 [공식 릴리스](https://github.com/astral-sh/uv/releases)의 운영체제별 `.sha256` 파일도 확인해 두 워크플로의 `checksum`을 함께 바꿉니다.

G3의 기본 ARM 산출물은 잠긴 `ziglang==0.15.2`가 제공하는 Clang 20.1.2로 만듭니다. GCC 비교는 Python 잠금과 별개로 [G3 실행 계약](../gates/g03/contract.md)에 적힌 공식 Arm GNU Toolchain 14.3.Rel1 호스트 아카이브 SHA-256을 먼저 확인합니다. 검증된 아카이브와 설치 루트를 둘 다 지정하지 않으면 시스템 GCC로 대체하지 않고 `Provisional`로 남깁니다.
