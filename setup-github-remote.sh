#!/bin/bash
# =============================================================================
# setup-github-remote.sh
# Run this ONCE to connect your local skills repo to GitHub.
# Usage: bash /root/.copilot/skills/setup-github-remote.sh
# =============================================================================

set -e

SKILLS_DIR="/root/.copilot/skills"
REPO_NAME="${1:-copilot-skills}"

echo "=== GitHub Remote Setup for Copilot Skills ==="
echo ""

# --- Check git is configured globally ---
if ! git config --global user.email > /dev/null 2>&1; then
  echo "Enter your GitHub email:"
  read GIT_EMAIL
  git config --global user.email "$GIT_EMAIL"
fi

if ! git config --global user.name > /dev/null 2>&1; then
  echo "Enter your name:"
  read GIT_NAME
  git config --global user.name "$GIT_NAME"
fi

# --- Check if gh CLI is available ---
if command -v gh &>/dev/null; then
  echo "[gh CLI found] Creating GitHub repo: $REPO_NAME ..."
  gh repo create "$REPO_NAME" --public --description "My personal Copilot skills library" --source="$SKILLS_DIR" --push
  echo ""
  echo "Done! Skills pushed to GitHub."
  echo "Repo URL: https://github.com/$(gh api user --jq .login)/$REPO_NAME"

else
  echo "[gh CLI not found] Follow these manual steps:"
  echo ""
  echo "  1. Create a new repo on GitHub:"
  echo "     https://github.com/new"
  echo "     Name: $REPO_NAME"
  echo "     Visibility: Public or Private"
  echo "     DO NOT initialize with README"
  echo ""
  echo "  2. Copy the SSH or HTTPS remote URL from GitHub, then run:"
  echo ""
  echo "     cd $SKILLS_DIR"
  echo "     git remote add origin <YOUR_REPO_URL>"
  echo "     git branch -m master main"
  echo "     git push -u origin main"
  echo ""
  echo "  3. Install gh CLI for future automation:"
  echo "     https://cli.github.com/"
fi
