#!/bin/bash
# =============================================================================
# skill-watch.sh — Validate, test, commit, and push when skill sources change
#
# Usage:
#   bash /root/.copilot/skills/skill-watch.sh          # foreground
#   nohup bash /root/.copilot/skills/skill-watch.sh &  # background
#
# Requires: inotifywait (apt install inotify-tools)
# =============================================================================

SKILLS_DIR="/root/.copilot/skills"
DEBOUNCE_SECONDS=3
WATCH_EXCLUDE='(\.git/|/__pycache__/|/\.gitignore$|/_index\.md$)'

# --- Check inotifywait is available ---
if ! command -v inotifywait &>/dev/null; then
  echo "[skill-watch] inotify-tools not found. Installing..."
  apt-get install -y inotify-tools -qq
fi

echo "[skill-watch] Watching $SKILLS_DIR for changes..."
echo "[skill-watch] Validation + publish will fire $DEBOUNCE_SECONDS seconds after last save."
echo ""

while true; do
  CHANGED=$(inotifywait -r -e close_write,moved_to,create \
    --format '%w%f' \
    --exclude "$WATCH_EXCLUDE" \
    --quiet \
    "$SKILLS_DIR" 2>/dev/null)

  if [[ -z "$CHANGED" ]]; then
    continue
  fi

  sleep "$DEBOUNCE_SECONDS"

  cd "$SKILLS_DIR"
  if git diff --quiet && git diff --cached --quiet; then
    if [[ -z "$(git status --short)" ]]; then
      continue
    fi
  fi

  if bash "$SKILLS_DIR/skill-publish.sh"; then
    echo "[skill-watch] Published changes triggered by: $CHANGED"
  else
    echo "[skill-watch] Validation failed. No commit created for: $CHANGED"
  fi

  echo ""
done
