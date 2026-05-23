#!/usr/bin/env python3
"""Verify the Dealix Ultimate Level blueprint exists and is non-trivial.

This is the CI gate for the Ultimate Level. It checks:
1. Every required Ultimate document exists.
2. Each document is non-trivially sized.
3. Each document contains its required section headers.
4. The cross-document links (the document map in DEALIX_AUTONOMOUS_ENTERPRISE_OS.md)
   point to documents that exist.

Run locally:  python scripts/verify_ultimate_level.py
Run via Make: make ultimate-level
Run in CI:    .github/workflows/dealix-ultimate-level.yml

Exit codes:
  0 — all good.
  1 — one or more checks failed; details on stdout.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

REPO_ROOT = Path(__file__).resolve().parent.parent

# Minimum bytes for an Ultimate doc.  The spec demanded > 80; we hold the line
# at 2,000 because every doc in this blueprint is materially longer than that.
MIN_BYTES = 2_000


@dataclass(frozen=True)
class Required:
    path: str
    sections: tuple[str, ...]


REQUIRED: tuple[Required, ...] = (
    Required(
        "docs/company/DEALIX_AUTONOMOUS_ENTERPRISE_OS.md",
        ("Purpose", "Ultimate Principle", "Core Operating Layers", "North Star", "Rule"),
    ),
    Required(
        "docs/company/DEALIX_MATURITY_MODEL.md",
        ("L0", "L5", "L10", "Scale rule"),
    ),
    Required(
        "docs/architecture/ULTIMATE_ARCHITECTURE_MAP.md",
        ("Request Flow", "Data Flow", "AI Flow", "Production Flow"),
    ),
    Required(
        "docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md",
        ("/ceo", "/sales-cockpit", "/approvals", "/workers", "/trust", "/finance"),
    ),
    Required(
        "docs/api/ULTIMATE_INTERNAL_API.md",
        (
            "/api/v1/internal/ceo/summary",
            "/api/v1/internal/approvals",
            "/api/v1/internal/workers/health",
            "/api/v1/internal/trust/evaluate",
            "/api/v1/internal/finance/summary",
            "/api/v1/internal/audit/approvals",
        ),
    ),
    Required(
        "docs/data/ULTIMATE_DATA_PLATFORM.md",
        (
            "Private Ops CSV",
            "Postgres Primary",
            "Event Log",
            "accounts",
            "audit_events",
            "ai_eval_results",
        ),
    ),
    Required(
        "docs/trust/ULTIMATE_TRUST_PLANE.md",
        ("Policy Checks", "Approval Classes", "A0", "A1", "A2", "A3", "Required Artifacts"),
    ),
    Required(
        "docs/runtime/ULTIMATE_WORKER_MESH.md",
        ("W1", "W2", "W3", "W4", "Required Worker Metadata", "disable_switch"),
    ),
    Required(
        "docs/revenue/ULTIMATE_REVENUE_FACTORY.md",
        ("Flow", "Minimum Weekly Output", "Scale Rule"),
    ),
    Required(
        "docs/delivery/ULTIMATE_DELIVERY_OS.md",
        ("Delivery Flow", "Required Artifacts", "client_os.md", "qa_checklist.md"),
    ),
    Required(
        "docs/finance/ULTIMATE_FINANCE_OS.md",
        ("Core Metrics", "cash collected", "MRR", "runway", "Decisions"),
    ),
    Required(
        "docs/product/ULTIMATE_PRODUCT_PLATFORM.md",
        ("Productization Path", "Candidate Modules", "Gate"),
    ),
    Required(
        "docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md",
        (
            "Runtime Metrics",
            "Revenue Metrics",
            "Trust Metrics",
            "change lead time",
            "deployment frequency",
            "failed deployment recovery time",
            "change fail rate",
            "deployment rework rate",
        ),
    ),
    Required(
        "docs/security/ULTIMATE_SECURITY_GOVERNANCE.md",
        (
            "branch protection",
            "required status checks",
            "secret scanning",
            "dependency review",
            "Production",
        ),
    ),
)

# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #


def check_presence_and_size(req: Required) -> list[str]:
    """Return a list of failure strings for this doc.  Empty list ⇒ pass."""
    failures: list[str] = []
    path = REPO_ROOT / req.path
    if not path.exists():
        failures.append(f"Missing: {req.path}")
        return failures
    size = path.stat().st_size
    if size < MIN_BYTES:
        failures.append(
            f"Too small ({size} bytes < {MIN_BYTES}): {req.path}"
        )
    return failures


def check_sections(req: Required) -> list[str]:
    """Return a list of missing-section failures for this doc."""
    failures: list[str] = []
    path = REPO_ROOT / req.path
    if not path.exists():
        return failures  # already reported by check_presence_and_size
    body = path.read_text(encoding="utf-8").lower()
    for section in req.sections:
        if section.lower() not in body:
            failures.append(
                f"Missing section / keyword in {req.path}: '{section}'"
            )
    return failures


def check_constitution_links() -> list[str]:
    """Confirm the document map in the constitution points to real files."""
    failures: list[str] = []
    constitution = REPO_ROOT / "docs/company/DEALIX_AUTONOMOUS_ENTERPRISE_OS.md"
    if not constitution.exists():
        return failures  # already reported above
    body = constitution.read_text(encoding="utf-8")
    for req in REQUIRED:
        if req.path == "docs/company/DEALIX_AUTONOMOUS_ENTERPRISE_OS.md":
            continue
        if req.path not in body:
            failures.append(
                f"Constitution does not reference {req.path}"
            )
    return failures


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> int:
    all_failures: list[str] = []
    for req in REQUIRED:
        all_failures.extend(check_presence_and_size(req))
        all_failures.extend(check_sections(req))
    all_failures.extend(check_constitution_links())

    if all_failures:
        print("Ultimate level verification FAILED:")
        for f in all_failures:
            print(f"  - {f}")
        print()
        print(
            f"{len(all_failures)} failure(s). "
            "Fix the documents above and rerun:  make ultimate-level"
        )
        return 1

    print("PASS: Dealix Ultimate Level blueprint exists.")
    print(f"  - {len(REQUIRED)} documents verified")
    total_bytes = sum(
        (REPO_ROOT / r.path).stat().st_size for r in REQUIRED
    )
    print(f"  - {total_bytes:,} bytes of blueprint")
    print("  - constitution → chapter links verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
