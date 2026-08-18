#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 WEEK_NUMBER TOPIC" >&2
    echo "Example: $0 2 \"POSIX process lifecycle\"" >&2
}

if [[ $# -lt 2 ]]; then
    usage
    exit 2
fi

week_input=$1
shift
topic=$*

if [[ ! $week_input =~ ^[0-9]{1,2}$ ]] || (( 10#$week_input < 1 || 10#$week_input > 99 )); then
    echo "error: WEEK_NUMBER must be an integer from 1 to 99" >&2
    exit 2
fi

if [[ -z ${topic//[[:space:]]/} ]]; then
    echo "error: TOPIC must not be empty" >&2
    exit 2
fi

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd -- "$script_dir/.." && pwd)
week=$(printf '%02d' "$((10#$week_input))")
target="$repo_root/study/week-$week"
template="$repo_root/docs/templates/learning-note.md"

if [[ -e $target ]]; then
    echo "error: $target already exists" >&2
    exit 1
fi

mkdir -p "$target/experiments" "$target/diagrams" "$target/evidence"
cp -- "$template" "$target/README.md"

TOPIC=$topic WEEK=$week TARGET_FILE="$target/README.md" python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["TARGET_FILE"])
text = path.read_text(encoding="utf-8")
lines = text.splitlines()
lines[0] = f"# Week {os.environ['WEEK']} — {os.environ['TOPIC']}"
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

touch "$target/experiments/.gitkeep" "$target/diagrams/.gitkeep"

cp -- "$repo_root/docs/templates/experiment-report.md" "$target/evidence/README.md"

echo "created: ${target#$repo_root/}/README.md"
echo "next: create a Study task issue, then fill Questions and Minimal experiment"

