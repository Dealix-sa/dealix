#!/usr/bin/env bash
# Dealix — web/session bootstrap. Make a fresh (ephemeral) session reproducible-green.
#
# Intended to be wired as a Claude Code SessionStart hook by the repo owner, e.g.
# add to .claude/settings.json:
#   { "hooks": { "SessionStart": [ { "hooks": [
#       { "type": "command", "command": "$CLAUDE_PROJECT_DIR/scripts/dealix_web_session_bootstrap.sh" }
#   ] } ] } }
# (Writing into .claude/ is intentionally left to the owner — this script does not.)
#
# Best-effort and idempotent: it NEVER hard-fails the session (always exits 0).
set -u

# Web/remote only by default; pass --force to run locally.
if [ "${1:-}" != "--force" ] && [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

log() { printf '[dealix:bootstrap] %s\n' "$1"; }

# 1) Persist env so `import api.main` and the package resolve all session.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo 'export PYTHONPATH="."'
    echo 'export APP_ENV="test"'
  } >> "$CLAUDE_ENV_FILE"
fi
export PYTHONPATH="." APP_ENV="test"

# 2) Install deps (best-effort). Two known snags are worked around:
#    - the Debian-managed PyYAML cannot be uninstalled (--ignore-installed PyYAML),
#    - the ummalqura (Hijri calendar) wheel fails to build and is only used by
#      integrations/saudi_market.py; the app degrades gracefully without it.
if ! python -c "import fastapi, pydantic, pytest" >/dev/null 2>&1; then
  log "installing dependencies (can take a few minutes)..."
  REQ_TMP="$(mktemp)"
  grep -viE '^(ummalqura|pyyaml)' requirements.txt > "$REQ_TMP" 2>/dev/null || cp requirements.txt "$REQ_TMP"
  if python -m pip install --quiet --ignore-installed PyYAML -r "$REQ_TMP" \
      pytest pytest-asyncio pytest-cov pytest-mock aiosqlite ruff black httpx >/dev/null 2>&1; then
    log "dependencies ready"
  else
    log "WARN: dependency install incomplete (continuing)"
  fi
  rm -f "$REQ_TMP"
else
  log "dependencies already present"
fi

# 3) Import smoke — the app must boot with optional routers registered.
if APP_ENV=test DEALIX_STRICT_OPTIONAL_ROUTERS=1 python -c "import api.main" >/dev/null 2>&1; then
  log "api.main import OK"
else
  log "WARN: api.main import failed (debug: DEALIX_STRICT_OPTIONAL_ROUTERS=1 python -c 'import api.main')"
fi

# 4) Doctrine subset — every web session starts green (report-only).
if python -c "import pytest" >/dev/null 2>&1; then
  if APP_ENV=test python -m pytest -q --no-cov -p no:cacheprovider \
      tests/test_no_source_passport_no_ai.py \
      tests/test_no_guaranteed_claims.py \
      tests/test_proof_pack_required.py \
      tests/test_output_requires_governance_status.py \
      tests/test_custom_systems_entry_gate.py >/dev/null 2>&1; then
    log "doctrine subset green"
  else
    log "WARN: doctrine subset not green — run the subset to see details"
  fi
fi

exit 0
