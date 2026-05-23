#!/usr/bin/env python3
"""verify_trust_os.py — Trust OS docs + code parity check.

Ensures every Trust doc has a corresponding code module (and vice versa)
and that the Trust modules import cleanly without external dependencies
beyond the Python standard library.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/trust/DATA_RETENTION_POLICY.md",
    "docs/trust/SUPPRESSION_LIST_POLICY.md",
    "docs/trust/INCIDENT_RESPONSE.md",
    "docs/trust/CLIENT_DATA_HANDLING.md",
    "docs/trust/CLAIMS_GUIDE.md",
    "docs/trust/PUBLIC_REPO_SAFETY.md",
    "docs/trust/AI_GOVERNANCE.md",
    "docs/trust/AUDIT_POLICY.md",
]

# Trust code modules (Company OS layer, importable without pydantic).
REQUIRED_MODULES = [
    ("approval_matrix", "dealix/trust/approval_matrix.py"),
    ("claim_guard", "dealix/trust/claim_guard.py"),
    ("suppression", "dealix/trust/suppression.py"),
    ("data_retention", "dealix/trust/data_retention.py"),
    ("evidence_pack", "dealix/trust/evidence_pack.py"),
]


def _load_module(name: str, rel_path: str) -> object | None:
    path = REPO_ROOT / rel_path
    if not path.exists():
        return None
    mod_name = f"_trust_check_{name}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    # Register before exec so @dataclass can resolve __module__ during class body.
    sys.modules[mod_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise RuntimeError(f"failed to import {name}: {exc}") from exc
    return module


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_DOCS:
        if not (REPO_ROOT / rel).exists():
            failures.append(f"missing doc: {rel}")

    for name, rel_path in REQUIRED_MODULES:
        path = REPO_ROOT / rel_path
        if not path.exists():
            failures.append(f"missing module: {rel_path}")
            continue
        try:
            _load_module(name, rel_path)
        except RuntimeError as exc:
            failures.append(str(exc))

    # Smoke-test the canonical API surface.
    am = _load_module("approval_matrix", "dealix/trust/approval_matrix.py")
    if am is not None:
        for required in ("tier_for", "require_approval", "ApprovalTier"):
            if not hasattr(am, required):
                failures.append(f"approval_matrix missing API: {required}")
        if hasattr(am, "tier_for") and am.tier_for("unknown_action").value != "A4":
            failures.append("approval_matrix: unknown action does not default to A4")

    cg = _load_module("claim_guard", "dealix/trust/claim_guard.py")
    if cg is not None:
        report = cg.check("Our industry-leading 10x solution.")
        if not report.is_blocking:
            failures.append("claim_guard: should block 'industry-leading 10x'")

    if failures:
        print("Trust OS verification FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Trust OS verification OK ({len(REQUIRED_DOCS)} docs + "
          f"{len(REQUIRED_MODULES)} modules + 2 smoke tests).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
