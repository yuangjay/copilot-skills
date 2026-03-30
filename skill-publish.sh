#!/bin/bash

set -euo pipefail

SKILLS_DIR="/root/.copilot/skills"
PYTHON_BIN="${PYTHON_BIN:-/ephemeral/workspace/study/integration/tests/.venv/bin/python}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

cd "$SKILLS_DIR"

"$PYTHON_BIN" scripts/skill_repo.py ci

git add -A

if git diff --cached --quiet; then
  echo "[skill-publish] No changes to commit."
  exit 0
fi

git commit -m "skill: validate and publish [$TIMESTAMP]

Verification steps:
  1. $PYTHON_BIN scripts/skill_repo.py ci
  2. $PYTHON_BIN -m unittest discover -s tests -q
  3. $PYTHON_BIN scripts/skill_repo.py classify \"<query>\""

if git remote get-url origin &>/dev/null; then
  git push origin "$(git branch --show-current)"
  echo "[skill-publish] Pushed to origin."
else
  echo "[skill-publish] No remote configured. Commit saved locally only."
  echo "[skill-publish] Run: bash $SKILLS_DIR/setup-github-remote.sh"
fi