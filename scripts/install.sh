#!/usr/bin/env bash
# Install Omnideck skills from this repo into the state skills directory.
# Usage: install.sh <skill-name> ... | --all
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${OMNIDECK_SKILLS_DIR:-/var/lib/omnideck/skills}"

if [[ "${1:-}" == "--all" ]]; then
    targets=("$REPO_DIR"/skills/*/skill.json)
elif [[ $# -ge 1 ]]; then
    targets=()
    for name in "$@"; do
        targets+=("$REPO_DIR/skills/$name/skill.json")
    done
else
    echo "Usage: install.sh <skill-name> ... | --all" >&2
    exit 2
fi

mkdir -p "$SKILLS_DIR"
installed=0
for rec in "${targets[@]}"; do
    [[ -f "$rec" ]] || { echo "SKIP: $rec not found" >&2; continue; }
    python3 "$REPO_DIR/scripts/validate.py" "$rec"
    name="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['id'])" "$rec")"
    cp "$rec" "$SKILLS_DIR/$name.json"
    echo "Installed: $name -> $SKILLS_DIR/$name.json"
    installed=$((installed + 1))
done
echo "Done: $installed skill(s) installed. Available to agents immediately."
