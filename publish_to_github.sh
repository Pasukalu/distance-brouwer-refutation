#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# One-Click Local Verification & GitHub Publishing Script
# Target repository: https://github.com/Pasukalu/distance-brouwer-refutation
# ==============================================================================

GITHUB_USER="${GITHUB_USER:-Pasukalu}"
REPO_NAME="${REPO_NAME:-distance-brouwer-refutation}"
REPO_DESC="Formally verified refutation (Lean 4) and structural correction of the Distance Laplacian and Distance Signless Laplacian Brouwer-type conjectures."
VISIBILITY="${VISIBILITY:-public}" # public or private

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Working directory: $SCRIPT_DIR"

# Optional local verification if tools are available
if [[ "${1:-}" == "--verify" ]]; then
  echo "==> [1/2] Running Lean 4 formal verification..."
  if command -v lake >/dev/null 2>&1; then
    (cd lean && lake clean && lake build)
  else
    echo "    [skip] 'lake' not found; install Lean 4 via elan to verify locally."
  fi
  echo "==> [2/2] Running Python verification suite..."
  if command -v python3 >/dev/null 2>&1; then
    python3 python/verify_all.py
  else
    echo "    [skip] 'python3' not found."
  fi
fi

# Initialize Git repository cleanly if needed
if [[ ! -d .git ]]; then
  echo "==> Initializing Git repository on branch 'main'..."
  git init -b main
fi

git add .
if ! git diff --cached --quiet; then
  git commit -m "Initial release: Lean 4 formal refutation, n<=7 census, and corrected bounds"
else
  echo "==> Working tree already committed."
fi

# Option A: Use GitHub CLI (gh) if installed and authenticated
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  echo "==> GitHub CLI detected and authenticated. Creating/pushing ${GITHUB_USER}/${REPO_NAME}..."
  if gh repo view "${GITHUB_USER}/${REPO_NAME}" >/dev/null 2>&1; then
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
    git push -u origin main
  else
    gh repo create "${GITHUB_USER}/${REPO_NAME}" \
      --"${VISIBILITY}" \
      --description "${REPO_DESC}" \
      --source=. \
      --remote=origin \
      --push
  fi
  echo "==> DONE! Published at: https://github.com/${GITHUB_USER}/${REPO_NAME}"
  exit 0
fi

# Option B: Plain git push (works with HTTPS PAT or SSH key)
REMOTE_URL="${REMOTE_URL:-https://github.com/${GITHUB_USER}/${REPO_NAME}.git}"
echo "==> GitHub CLI ('gh') not logged in; configuring remote: ${REMOTE_URL}"
echo "    Make sure the empty repository '${GITHUB_USER}/${REPO_NAME}' exists on GitHub first:"
echo "    https://github.com/new"
git remote remove origin 2>/dev/null || true
git remote add origin "${REMOTE_URL}"
git branch -M main
echo "==> Pushing to origin/main..."
git push -u origin main
echo "==> DONE! Published at: https://github.com/${GITHUB_USER}/${REPO_NAME}"
