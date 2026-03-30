#!/bin/bash

set -euo pipefail

SKILLS_DIR="/root/.copilot/skills"
PYTHON_BIN="${PYTHON_BIN:-/ephemeral/workspace/study/integration/tests/.venv/bin/python}"
LOCAL_OVERRIDE_PATH="/root/.copilot/copilot-instructions.local.md"
LOCAL_OVERRIDE_EXAMPLE="$SKILLS_DIR/templates/copilot-instructions.local.example.md"

cd "$SKILLS_DIR"

if [[ ! -f "$LOCAL_OVERRIDE_PATH" ]]; then
  cp "$LOCAL_OVERRIDE_EXAMPLE" "$LOCAL_OVERRIDE_PATH"
  echo "[install] Created local override file at $LOCAL_OVERRIDE_PATH"
fi

"$PYTHON_BIN" scripts/skill_repo.py sync
"$PYTHON_BIN" scripts/skill_repo.py build-index
"$PYTHON_BIN" scripts/skill_repo.py benchmark
"$PYTHON_BIN" scripts/skill_repo.py validate

echo "[install] Skill system synced."
echo "[install] Global instructions: /root/.copilot/copilot-instructions.md"
echo "[install] Local overrides: $LOCAL_OVERRIDE_PATH"