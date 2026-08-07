from __future__ import annotations

import csv
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

PIPELINE_PATH = Path("company/crm/pipeline.csv")
RUNTIME_DIR = Path("company/runtime")

FOLLOWUP_STATUSES = {"replied", "discovery_booked"}

DISCLAIMER = (
    "Estimated value is not Verified value / "
    "القيمة التقديرية ليست قيمة مُتحقَّقة"
)

DRAFT_STUB = (
    "يحتاج اعتماد المؤسس قبل الإرسال / "
    "Requires founder approval before sending"
)

OUTPUT_COLUMNS = [
    "company",
    "contact_name",
    "status",
    "suggested_next_action",
    "draft_message_stub",
    "governance_decision",
]


def _parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _load_pipeline() -> list[dict[str, str]]:
    if not PIPELINE_PATH.exists():
        return []
    with PIPELINE_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader]


def _suggest_next_action(status: str) -> str:
    mapping = {
        "replied": "send_proposal_draft_for_founder_approval",
        "discovery_booked": "prepare_discovery_call_brief_for_founder_review",
    }
    return mapping.get(status, "review_and_decide")


def compute_due_rows(rows: list[dict[str, str]], today: date) -> list[dict[str, Any]]:
    """Return rows that are due for follow-up based on status and date."""
    due: list[dict[str, Any]] = []
    for row in rows:
        status = row.get("status", "").strip().lower()
        if status not in FOLLOWUP_STATUSES:
            continue
        followup_date = _parse_date(row.get("next_followup_date", ""))
        if followup_date is None or followup_date > today:
            continue
        due.append({
            "company": row.get("company", "").strip(),
            "contact_name": row.get("contact", "").strip(),
            "status": status,
            "suggested_next_action": _suggest_next_action(status),
            "draft_message_stub": DRAFT_STUB,
            "governance_decision": "draft_queued_for_founder_approval",
        })
    return due


def write_drafts(due_rows: list[dict[str, Any]], today: date) -> Path:
    """Write due rows to a dated CSV in company/runtime/. Returns output path."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RUNTIME_DIR / f"{today.isoformat()}_followup_drafts.csv"

    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in due_rows:
            writer.writerow(row)
        # Bilingual disclaimer as a trailing comment row
        fh.write(f"# {DISCLAIMER}\n")

    return output_path


def run() -> None:
    today = date.today()
    rows = _load_pipeline()
    due = compute_due_rows(rows, today)

    print(f"Pipeline rows loaded: {len(rows)}")
    print(f"Due for follow-up today ({today.isoformat()}): {len(due)}")

    for entry in due:
        # Log company name only — never log personal email or phone
        print(
            f"  queued: {entry['company']} | status={entry['status']} "
            f"| governance_decision={entry['governance_decision']}"
        )

    output_path = write_drafts(due, today)
    print(f"Output: {output_path}")
    print(f"Disclaimer: {DISCLAIMER}")
    print("governance_decision: draft_queued_for_founder_approval")
    print("No messages sent. All drafts require founder approval before sending.")


if __name__ == "__main__":
    run()
