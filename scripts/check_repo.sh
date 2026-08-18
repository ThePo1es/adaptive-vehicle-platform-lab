#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd -- "$script_dir/.." && pwd)
cd "$repo_root"

required_files=(
    README.md
    ROADMAP.md
    PROGRESS.md
    SECURITY.md
    docs/requirements.md
    docs/traceability.md
    docs/autosar-mapping.md
)

for file in "${required_files[@]}"; do
    if [[ ! -f $file ]]; then
        echo "error: required file is missing: $file" >&2
        exit 1
    fi
done

bash -n scripts/new-study-log.sh scripts/check_repo.sh
python3 -c 'import ast, pathlib; ast.parse(pathlib.Path("scripts/check_internal_links.py").read_text(encoding="utf-8"))'
python3 scripts/check_internal_links.py

if find . -path './.git' -prune -o -type f \
    \( -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '*.pcap' -o -name '*.pcapng' \) \
    -print -quit | grep -q .; then
    echo "error: potentially sensitive key or capture file found" >&2
    exit 1
fi

echo "Repository checks: OK"
