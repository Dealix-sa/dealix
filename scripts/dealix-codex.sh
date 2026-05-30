#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../dealix-v2"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI not found. Installing @openai/codex..."
  npm install -g @openai/codex
fi

codex "$@"
