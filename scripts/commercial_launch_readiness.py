#!/usr/bin/env python3
"""Commercial launch readiness check.

Confirms the launch spine is in place: configs, seed data, key docs, and (if
already generated) the day's draft + safety artifacts. Writes
outputs/commercial_launch/<date>/launch_readiness.json and returns non-zero if
any critical item is missing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    COMMERCIAL_OUTPUTS,
    DATA_DIR,
    ROOT,
    today_str,
    write_json,
)

REQUIRED_CONFIGS = [
    "commercial_launch.json",
    "commercial_verticals.json",
    "commercial_offers.json",
    "commercial_channels.json",
    "commercial_quality_gates.json",
    "commercial_compliance_gates.json",
    "commercial_draft_distribution.json",
    "commercial_risk_terms.json",
    "commercial_founder_review_rules.json",
    "commercial_metrics.json",
    "crm_pipeline_schema.json",
]

REQUIRED_DOCS = [
    "docs/company-os/00_DEALIX_COMPANY_OS.md",
    "docs/commercial-launch/00_COMMERCIAL_LAUNCH_OS.md",
    "docs/commercial-launch/verticals/01_facilities_management.md",
    "docs/delivery-os/00_DELIVERY_OS.md",
    "docs/media-social-os/00_MEDIA_SOCIAL_OS.md",
    "docs/analytics-os/00_ANALYTICS_OS.md",
    "docs/go-live/00_EXTERNAL_GO_LIVE_REQUIREMENTS.md",
    "docs/launch-control/00_FINAL_LAUNCH_CONTROL_TOWER.md",
    "docs/site-launch/00_SITE_LAUNCH_OS.md",
]


def run(day: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, critical: bool = True, detail: str = "") -> None:
        checks.append({"check": name, "passed": bool(ok), "critical": critical, "detail": detail})

    for cfg in REQUIRED_CONFIGS:
        add(f"config:{cfg}", (ROOT / "config" / cfg).exists())
    add("data:seed_leads", (DATA_DIR / "commercial_seed_leads.example.jsonl").exists())
    for doc in REQUIRED_DOCS:
        add(f"doc:{doc}", (ROOT / doc).exists())

    # Optional artifacts (present after the generator runs).
    metrics_path = COMMERCIAL_OUTPUTS / day / "daily_metrics.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        add(
            "drafts:>=400",
            metrics.get("drafts_generated", 0) >= 400,
            detail=str(metrics.get("drafts_generated")),
        )
    else:
        add("drafts:>=400", False, critical=False, detail="run commercial_generate_400_drafts.py")

    safety_path = COMMERCIAL_OUTPUTS / day / "safety_audit.json"
    if safety_path.exists():
        safety = json.loads(safety_path.read_text(encoding="utf-8"))
        add("safety:pass", bool(safety.get("passed")))
    else:
        add("safety:pass", False, critical=False, detail="run commercial_safety_audit.py")

    critical_failed = [c for c in checks if c["critical"] and not c["passed"]]
    return {
        "date": day,
        "passed": not critical_failed,
        "go_no_go": "GO" if not critical_failed else "NO-GO",
        "total_checks": len(checks),
        "failed_critical": len(critical_failed),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Commercial launch readiness.")
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    report = run(args.date)
    out = COMMERCIAL_OUTPUTS / args.date / "launch_readiness.json"
    write_json(out, report)

    print(
        f"LAUNCH READINESS: {report['go_no_go']} — "
        f"{report['total_checks'] - report['failed_critical']}/{report['total_checks']} checks ok."
    )
    if not report["passed"]:
        for c in report["checks"]:
            if c["critical"] and not c["passed"]:
                print(f"  - MISSING: {c['check']} {c['detail']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
