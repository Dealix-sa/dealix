#!/usr/bin/env python3
"""Verify the Dealix Company OS is present and well-formed.

Checks:
- Required doctrine files exist at the repo root.
- Required `control_plane/` modules exist and are importable.
- Required `docs/control_plane/` documentation exists.
- Required founder, trust, learning, ops docs exist.

Exit code 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_ROOT_FILES = [
    "DEALIX_OPERATING_DOCTRINE.md",
    "DEALIX_COMPANY_OS_SCORECARD.md",
]

REQUIRED_CONTROL_PLANE_MODULES = [
    "control_plane",
    "control_plane.company_state",
    "control_plane.metrics_collector",
    "control_plane.ceo_brief",
    "control_plane.decision_engine",
    "control_plane.approval_router",
    "control_plane.risk_engine",
    "control_plane.system_scorecard",
    "control_plane.learning_router",
]

REQUIRED_DOC_FILES = [
    "docs/control_plane/CONTROL_PLANE_ARCHITECTURE.md",
    "docs/control_plane/COMPANY_STATE_SCHEMA.md",
    "docs/control_plane/DECISION_ENGINE.md",
    "docs/control_plane/APPROVAL_ROUTING.md",
    "docs/control_plane/RISK_ENGINE.md",
    "docs/control_plane/SYSTEM_SCORECARD.md",
    "docs/control_plane/CEO_BRIEF_SPEC.md",
    "docs/control_plane/LEARNING_ROUTER.md",
    "docs/founder/CEO_OPERATING_SYSTEM.md",
    "docs/founder/DAILY_COMMAND_BRIEF.md",
    "docs/founder/WEEKLY_CEO_REVIEW.md",
    "docs/founder/CEO_ALERTS.md",
    "docs/trust/AUTONOMY_POLICY.md",
    "docs/trust/EVIDENCE_SYSTEM.md",
    "docs/learning/LEARNING_ROUTER.md",
    "docs/ops/OPERATING_CADENCE.md",
]


def _check_file(rel: str) -> str | None:
    path = REPO_ROOT / rel
    if not path.exists():
        return f"missing: {rel}"
    if path.stat().st_size < 64:
        return f"too small: {rel}"
    return None


def _check_module(name: str) -> str | None:
    try:
        importlib.import_module(name)
    except Exception as exc:  # pragma: no cover - defensive
        return f"import failed: {name} ({exc})"
    return None


def main() -> int:
    errors: list[str] = []

    sys.path.insert(0, str(REPO_ROOT))

    for f in REQUIRED_ROOT_FILES:
        err = _check_file(f)
        if err:
            errors.append(err)

    for m in REQUIRED_CONTROL_PLANE_MODULES:
        err = _check_module(m)
        if err:
            errors.append(err)

    for f in REQUIRED_DOC_FILES:
        err = _check_file(f)
        if err:
            errors.append(err)

    if errors:
        print("[FAIL] Company OS verification failed:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("[PASS] Company OS verification passed.")
    print(f"  root files OK: {len(REQUIRED_ROOT_FILES)}")
    print(f"  control_plane modules OK: {len(REQUIRED_CONTROL_PLANE_MODULES)}")
    print(f"  doc files OK: {len(REQUIRED_DOC_FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
