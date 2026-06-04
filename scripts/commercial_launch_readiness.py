"""Commercial Launch readiness check.

Verifies the OS is present and internally consistent, runs the no-send safety
audit, and confirms the draft factory invariants. Artifact-only; sends nothing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import (
    ALLOWED_STATUSES,
    MANDATORY_FLAGS,
    REPO_ROOT,
    generate_drafts,
    load_all_configs,
    load_seed_leads,
)
from scripts.commercial_safety_audit import run_safety_audit

REQUIRED_PATHS = [
    "config/commercial_launch.json",
    "config/commercial_verticals.json",
    "config/commercial_offers.json",
    "config/commercial_channels.json",
    "config/commercial_quality_gates.json",
    "config/commercial_compliance_gates.json",
    "config/commercial_draft_distribution.json",
    "config/commercial_risk_terms.json",
    "scripts/commercial_generate_400_drafts.py",
    "scripts/commercial_safety_audit.py",
    "data/commercial_seed_leads.example.jsonl",
    ".github/workflows/commercial-draft-factory.yml",
    "docs/commercial-launch/verticals/01_facilities_management.md",
    "docs/commercial-launch/verticals/02_contracting_project_controls.md",
    "docs/commercial-launch/verticals/03_real_estate_property_ops.md",
    "docs/commercial-launch/verticals/04_legal_professional_services.md",
    "docs/commercial-launch/verticals/05_consulting_training_b2b.md",
    "docs/commercial-launch/06_CHANNEL_POLICY.md",
]


def run_readiness(target: int = 400) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    # 1. required files present
    for rel in REQUIRED_PATHS:
        add(f"exists:{rel}", (REPO_ROOT / rel).exists())

    # 2. configs load + 5 verticals
    cfg = load_all_configs()
    verticals = cfg["verticals"]["verticals"]
    add("five_verticals", len(verticals) >= 5, f"{len(verticals)} verticals")

    # 3. distribution sums to >= target floor
    dist_total = sum(cfg["distribution"]["distribution"].values())
    add("distribution_floor", dist_total >= 400, f"distribution sums to {dist_total}")

    # 4. draft factory invariants
    leads = load_seed_leads()
    result = generate_drafts(target=target, leads=leads, cfg=cfg)
    add("target_met", len(result.drafts) >= target, f"{len(result.drafts)} drafts")

    flags_ok = all(all(d.get(f) == v for f, v in MANDATORY_FLAGS.items()) for d in result.drafts)
    add("mandatory_flags", flags_ok, "every draft carries safe flags")

    status_ok = all(d.get("status") in ALLOWED_STATUSES for d in result.drafts)
    add("allowed_statuses", status_ok)

    # 5. safety audit
    audit = run_safety_audit()
    add("safety_audit", audit["pass"], f"{len(audit['violations'])} violations")

    passed = all(c["ok"] for c in checks)
    return {
        "schema_version": "1.0",
        "verdict": "GO" if passed else "NO-GO",
        "pass": passed,
        "checks": checks,
        "failed": [c for c in checks if not c["ok"]],
        "doctrine": "AI drafts only. Founder approves. No external sending.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Commercial launch readiness.")
    ap.add_argument("--target", type=int, default=400)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    report = run_readiness(args.target)
    if args.out:
        Path(args.out).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(
        json.dumps(
            {"verdict": report["verdict"], "pass": report["pass"], "failed": report["failed"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
