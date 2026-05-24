#!/usr/bin/env python3
"""Verify Makefile: every required target exists in Makefile."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, report  # noqa: E402

LAYER = "Makefile"
REQUIRED = [
    "everything", "company-os", "brand-system", "policy-check", "agent-registry",
    "machine-registry", "eval-gate", "ai-governance", "founder-console",
    "capital-allocation", "strategy-scorecard", "revenue-forecast",
    "launch-layer", "market-attack-system", "scale-moat-system",
    "founder-ceo-hypergrowth-layer", "ceo-daily-brief", "ceo-weekly-review",
    "smoke-internal-api", "worker-orchestrator", "customer-success",
    "enterprise-sales", "legal-trust-security", "company-memory",
    "bootstrap-runtime",
]


def main() -> None:
    p = REPO_ROOT / "Makefile"
    if not p.exists():
        report(LAYER, False, ["missing: Makefile"])
    text = p.read_text(encoding="utf-8")
    reasons = [f"missing target: {t}" for t in REQUIRED if f"\n{t}:" not in text]
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
