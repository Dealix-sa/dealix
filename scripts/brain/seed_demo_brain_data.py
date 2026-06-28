"""Seed the Company Brain OS ledgers with demo data.

This is intended for testing and demonstrations. It populates all six ledgers
with a small set of realistic-looking rows. No external data is fetched.

Usage:
    python -m scripts.brain.seed_demo_brain_data
    python -m scripts.brain.seed_demo_brain_data --clean   # overwrite ledgers with headers + demo rows
"""
from __future__ import annotations

import csv
import os
from datetime import datetime, timedelta, timezone
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGERS_DIR = os.path.join(REPO_ROOT, "ledgers")

LEDGER_SPECS: dict[str, tuple[str, list[dict[str, Any]]]] = {
    "company_signals.csv": (
        "date,company_name,signal_type,signal_source,direction,strength,confidence,notes",
        [
            {"date": "2026-06-20", "company_name": "Demo Co", "signal_type": "revenue", "signal_source": "finance",
             "direction": "up", "strength": "medium", "confidence": "medium", "notes": "MRR growth observed in May."},
            {"date": "2026-06-21", "company_name": "Demo Co", "signal_type": "churn", "signal_source": "product",
             "direction": "down", "strength": "low", "confidence": "low", "notes": "One pilot account paused."},
        ],
    ),
    "decisions_log.csv": (
        "id,date,decision,why_now,assumption,confidence,owner,next_action,success_metric,review_date,risk_if_delayed",
        [
            {"id": "DEC-DEMO01", "date": "2026-06-20",
             "decision": "Launch weekly decision review.",
             "why_now": "Backlog growing; assumptions going stale.",
             "assumption": "Founders can commit 30 min weekly.",
             "confidence": "medium", "owner": "CEO",
             "next_action": "Schedule recurring slot.",
             "success_metric": ">=80% decisions reviewed on time.",
             "review_date": "2026-07-04",
             "risk_if_delayed": "Stale assumptions compound risk."},
        ],
    ),
    "assumptions_log.csv": (
        "id,date,assumption,category,confidence,evidence_for,evidence_against,review_date,owner",
        [
            {"id": "ASM-DEMO01", "date": "2026-06-20",
             "assumption": "Founders can attend a weekly 30-min review.",
             "category": "operational", "confidence": "medium",
             "evidence_for": "Team is co-located and aligned.",
             "evidence_against": "Travel schedules unknown.",
             "review_date": "2026-07-04", "owner": "CEO"},
        ],
    ),
    "experiments_log.csv": (
        "id,date,hypothesis,metric,status,result,confidence,owner,review_date",
        [
            {"id": "EXP-DEMO01", "date": "2026-06-15",
             "hypothesis": "Weekly review reduces time-to-decision.",
             "metric": "time_to_decision_days", "status": "running",
             "result": "", "confidence": "low", "owner": "CEO",
             "review_date": "2026-07-15"},
        ],
    ),
    "risk_register.csv": (
        "id,date,risk,likelihood,impact,confidence,mitigation,owner,review_date",
        [
            {"id": "RSK-DEMO01", "date": "2026-06-20",
             "risk": "Single-owner concentration on key decisions.",
             "likelihood": "medium", "impact": "high",
             "confidence": "medium", "mitigation": "Assign co-owners; weekly review.",
             "owner": "CEO", "review_date": "2026-07-04"},
        ],
    ),
    "opportunity_register.csv": (
        "id,date,opportunity,category,confidence,scenario_base,scenario_upside,scenario_downside,owner,next_action,review_date",
        [
            {"id": "OPP-DEMO01", "date": "2026-06-20",
             "opportunity": "Expand pilot to second sector.",
             "category": "growth", "confidence": "low",
             "scenario_base": "One new pilot signed in 30 days.",
             "scenario_upside": "Two pilots signed if outbound holds.",
             "scenario_downside": "No pilots if outbound stalls.",
             "owner": "Head of Sales", "next_action": "Draft sector shortlist.",
             "review_date": "2026-07-04"},
        ],
    ),
}


def seed_demo_brain_data(ledgers_dir: str | None = None, clean: bool = False) -> dict[str, int]:
    """Seed all brain ledgers with demo data. Returns a mapping of ledger -> row count."""
    base = ledgers_dir or LEDGERS_DIR
    os.makedirs(base, exist_ok=True)
    counts: dict[str, int] = {}

    for fname, (header, rows) in LEDGER_SPECS.items():
        path = os.path.join(base, fname)
        if clean or not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                fh.write(header + "\n")
        # Append demo rows (avoid duplicate seeding by checking for existing IDs).
        existing_ids: set[str] = set()
        if os.path.getsize(path) > 0:
            with open(path, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    if row.get("id"):
                        existing_ids.add(row["id"])
        new_rows = [r for r in rows if not r.get("id") or r["id"] not in existing_ids]
        with open(path, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=header.split(","))
            for r in new_rows:
                writer.writerow({k: r.get(k, "") for k in header.split(",")})
        counts[fname] = len(new_rows)

    return counts


if __name__ == "__main__":
    import sys

    clean = "--clean" in sys.argv
    print(seed_demo_brain_data(clean=clean))
