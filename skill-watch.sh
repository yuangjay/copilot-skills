#!/bin/bash
# =============================================================================
# skill-watch.sh — Auto-commit and push when any SKILL.md file changes
#
# Usage:
#   bash /root/.copilot/skills/skill-watch.sh          # foreground
#   nohup bash /root/.copilot/skills/skill-watch.sh &  # background
#
# Requires: inotifywait (apt install inotify-tools)
# =============================================================================

SKILLS_DIR="/root/.copilot/skills"
DEBOUNCE_SECONDS=3

# --- Check inotifywait is available ---
if ! command -v inotifywait &>/dev/null; then
  echo "[skill-watch] inotify-tools not found. Installing..."
  apt-get install -y inotify-tools -qq
fi

echo "[skill-watch] Watching $SKILLS_DIR for changes..."
echo "[skill-watch] Auto-commit + push will fire $DEBOUNCE_SECONDS seconds after last save."
echo ""

# Track the last changed file for the commit message
LAST_FILE=""

while true; do
  # Wait for any file change (create, modify, move) in skills dir
  CHANGED=$(inotifywait -r -e close_write,moved_to,create \
    --format '%w%f' \
    --quiet \
    "$SKILLS_DIR" 2>/dev/null)

  # Skip .git internals
  if [[ "$CHANGED" == *".git"* ]]; then
    continue
  fi

  LAST_FILE="$CHANGED"

  # Debounce — wait for rapid saves to settle 
  sleep "$DEBOUNCE_SECONDS"

  # Check if there's actually anything to commit
  cd "$SKILLS_DIR"
  if git diff --quiet && git diff --cached --quiet; then
    # Check for untracked files too
    if [[ -z "$(git status --short)" ]]; then
      continue
    fi
  fi

  # Determine changed skill name from path
  SKILL_NAME=$(basename "$(dirname "$LAST_FILE")")
  FILENAME=$(basename "$LAST_FILE")
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

  # Stage all changes
  git add -A

  # Commit with detailed message
  git commit -m "skill($SKILL_NAME): auto-update $FILENAME [$TIMESTAMP]

Changed file: $LAST_FILE

Verification steps:
  1. cat \"$LAST_FILE\" — review the updated skill content
  2. Rollback: git revert HEAD — rolls back this change
  3. History: git log --oneline -- $FILENAME"

  echo "[skill-watch] Committed: skill($SKILL_NAME): $FILENAME"

  # Push if remote is configured
  if git remote get-url origin &>/dev/null; then
    git push origin "$(git branch --show-current)" && \
      echo "[skill-watch] Pushed to GitHub." || \
      echo "[skill-watch] WARNING: Push failed. Will retry on next change."
  else
    echo "[skill-watch] No remote configured. Commit saved locally only."
    echo "[skill-watch] Run: bash $SKILLS_DIR/setup-github-remote.sh"
  fi

  echo ""
done
