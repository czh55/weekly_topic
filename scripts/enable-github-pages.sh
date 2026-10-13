#!/usr/bin/env bash
# Create GitHub repo (if needed), push main, enable Pages via Actions.
set -euo pipefail

REPO="${1:-czh55/weekly_topic}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v gh >/dev/null; then
  echo "需要已安装并登录的 gh CLI" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "请先运行: gh auth login" >&2
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  if gh repo view "$REPO" >/dev/null 2>&1; then
    git remote add origin "https://github.com/${REPO}.git"
  else
    gh repo create "$REPO" --public --source=. --remote=origin --description "每周主题学习总结墙"
  fi
fi

git push -u origin main

# Prefer GitHub Actions as Pages source (matches deploy-pages.yml)
gh api -X PUT "repos/${REPO}/pages" \
  -f build_type=workflow \
  -f source[branch]=main \
  -f source[path]=/docs \
  >/dev/null 2>&1 || \
gh api -X POST "repos/${REPO}/pages" \
  -f build_type=workflow \
  >/dev/null 2>&1 || true

echo "Done. Open: https://github.com/${REPO}/settings/pages"
echo "Site (after first Actions run): https://czh55.github.io/weekly_topic/"
