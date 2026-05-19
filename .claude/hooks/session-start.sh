#!/bin/bash
# SessionStart hook — installs Python dependencies so tests, verifier
# scripts, and linters work in Claude Code on the web sessions.
#
# The container state is cached after this completes, so a fresh
# `pip install` here makes every later session start test-ready.
set -euo pipefail

# Only run in the remote (Claude Code on the web) environment. Local
# developers manage their own virtualenvs.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "[session-start] installing Dealix Python dependencies..."

# 1. Refresh build tooling. The Debian-shipped setuptools lacks the
#    attributes some sdist-only deps (e.g. ummalqura) need to build a
#    wheel; --ignore-installed replaces it cleanly in this environment.
pip install --quiet --upgrade --ignore-installed setuptools wheel

# 2. Install runtime + dev requirements. --ignore-installed PyYAML
#    avoids the "RECORD file not found" uninstall error from the
#    Debian-managed system PyYAML.
pip install --quiet --ignore-installed PyYAML \
  -r requirements.txt -r requirements-dev.txt

echo "[session-start] dependencies installed."
