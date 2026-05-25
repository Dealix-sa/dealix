"""Execution assurance calculation against a private ops ledger."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def path_has_evidence(root: Path, relative_path: str) -> bool:
    path = root / relative_path
    if path.is_file():
        return path.stat().st_size > 0
    if path.is_dir():
        return any(path.iterdir())
    return False


def calculate_execution_assurance(private_ops_root: str) -> dict[str, Any]:
    root = Path(private_ops_root)
    ledger = read_csv(root / "evidence/execution_evidence_ledger.csv")
    pipeline = read_csv(root / "pipeline/pipeline_tracker.csv")
    revenue_actions = read_csv(root / "revenue/revenue_action_log.csv")

    evidence_count = len(ledger)
    lead_count = len(pipeline)

    outbound_actions = [
        row for row in revenue_actions
        if (row.get("type") or "").strip().lower() == "outbound"
    ]
    proposal_actions = [
        row for row in revenue_actions
        if (row.get("type") or "").strip().lower() == "proposal"
    ]
    payment_actions = [
        row for row in revenue_actions
        if "payment" in (row.get("type") or "").strip().lower()
        or "po" in (row.get("type") or "").strip().lower()
    ]

    checks = {
        "25_leads": lead_count >= 25,
        "25_outbound": len(outbound_actions) >= 25,
        "3_samples": path_has_evidence(root, "delivery/samples"),
        "1_proposal": len(proposal_actions) >= 1,
        "payment_or_po_followup": len(payment_actions) >= 1,
        "weekly_learning": path_has_evidence(root, "learning/weekly_intelligence_review.md"),
        "business_score": path_has_evidence(root, "business_audit/ceo_business_score.md"),
        "control_tower": path_has_evidence(root, "founder/control_tower_brief.md"),
    }

    passed = sum(1 for value in checks.values() if value)
    total = len(checks)
    score = round((passed / total) * 100) if total else 0

    if score >= 90:
        status = "OPERATING"
    elif score >= 70:
        status = "EXECUTING"
    elif score >= 40:
        status = "PARTIAL"
    else:
        status = "SETUP"

    missing = [key for key, value in checks.items() if not value]

    return {
        "score": score,
        "status": status,
        "evidence_count": evidence_count,
        "checks": checks,
        "missing": missing,
    }
