#!/usr/bin/env bash
# Verify Dealix CEO business systems — docs presence, size, and required terms.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3 2>/dev/null || command -v py 2>/dev/null || true)}"
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python3/py not found" >&2
  exit 1
fi
if [[ "${PYTHON_BIN}" == *py ]]; then
  PYTHON_BIN="py -3"
fi

exec $PYTHON_BIN "${ROOT}/scripts/verify_ceo_business_systems.py" "$@"
