"""Pytest counterpart of `scripts/check_doctrine.py`.

Fails the build if any code in `api/`, `auto_client_acquisition/`, `dealix/`,
`scripts/`, or `frontend/src/` violates the 11 non-negotiables.

Why a paired pytest + standalone script:
  - `scripts/check_doctrine.py` can be wired to a pre-commit hook or a
    standalone Bash step (no Python test harness required).
  - This pytest gives the rest of the test suite a hard dependency on the
    doctrine — if doctrine fails, the whole `pytest -q` run goes red, which
    means PR CI catches violations before merge.

Both use the SAME `scan()` function, so they cannot drift.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.check_doctrine import scan  # noqa: E402


def test_no_doctrine_violations() -> None:
    violations = scan()
    if violations:
        # Build a readable failure message so the founder can see exactly
        # which file/line broke which rule.
        lines = [f"{rel}:{lineno}  {msg}" for rel, lineno, msg in violations]
        pytest.fail(
            "doctrine violations found:\n  - " + "\n  - ".join(lines)
        )


def test_scan_returns_list_of_tuples() -> None:
    """Smoke test: scan() must always return a list (possibly empty)."""
    result = scan()
    assert isinstance(result, list)
    for entry in result:
        assert isinstance(entry, tuple)
        assert len(entry) == 3
        rel, lineno, msg = entry
        assert isinstance(rel, str) and rel
        assert isinstance(lineno, int) and lineno > 0
        assert isinstance(msg, str) and msg
