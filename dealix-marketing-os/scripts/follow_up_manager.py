"""Follow-up manager: tracks and schedules follow-up sequence for approved sends."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

MEMORY_DIR = BASE_DIR / "memory"
APPROVED_SENDS_PATH = MEMORY_DIR / "approved_sends.jsonl"
DRAFT_QUEUE_PATH = MEMORY_DIR / "draft_queue.jsonl"
OPPORTUNITIES_PATH = MEMORY_DIR / "opportunities.jsonl"

FOLLOWUP_SCHEDULE = {
    "followup_1": 5,
    "followup_2": 12,
    "referral_request": 21,
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def compute_followup_dates(sent_date: str) -> dict[str, str]:
    try:
        base = date.fromisoformat(sent_date[:10])
    except (ValueError, TypeError):
        base = date.today()
    return {
        ft: (base + timedelta(days=offset)).isoformat()
        for ft, offset in FOLLOWUP_SCHEDULE.items()
    }


def list_due_followups() -> list[dict]:
    today = date.today().isoformat()
    approved_sends = read_jsonl(APPROVED_SENDS_PATH)
    drafts = read_jsonl(DRAFT_QUEUE_PATH)
    draft_map: dict[tuple[str, str], dict] = {
        (d["company_id"], d["draft_type"]): d for d in drafts
    }

    due: list[dict] = []
    for send in approved_sends:
        if send.get("status") != "sent":
            continue
        sent_date = send.get("sent_date", send.get("approved_at", today))
        schedule = compute_followup_dates(sent_date)
        for followup_type, due_date in schedule.items():
            if due_date <= today:
                key = (send["company_id"], followup_type)
                draft = draft_map.get(key)
                already_sent = send.get(f"{followup_type}_sent", False)
                if draft and not already_sent:
                    due.append({
                        "company_id": send["company_id"],
                        "company_name": send.get("company_name", ""),
                        "followup_type": followup_type,
                        "due_date": due_date,
                        "draft_id": draft["id"],
                        "subject": draft.get("subject", ""),
                        "quality_score": draft.get("quality_score"),
                    })
    return due


def run(action: str) -> None:
    if action == "list-due":
        due = list_due_followups()
        if not due:
            print("No follow-ups due today")
            return
        print(f"Follow-ups due today ({date.today().isoformat()}):")
        for item in due:
            print(
                f"  {item['company_name']} — {item['followup_type']} (due: {item['due_date']}, score: {item.get('quality_score')})"
            )
        print(f"\nTotal due: {len(due)}")
    elif action == "summary":
        approved_sends = read_jsonl(APPROVED_SENDS_PATH)
        sent = [s for s in approved_sends if s.get("status") == "sent"]
        print(f"Total approved sends: {len(approved_sends)}")
        print(f"Sent: {len(sent)}")
        due = list_due_followups()
        print(f"Follow-ups due today: {len(due)}")
    else:
        log.error("Unknown action: %s. Use 'list-due' or 'summary'", action)


def main() -> None:
    parser = argparse.ArgumentParser(description="Follow-up sequence manager")
    parser.add_argument("--action", choices=["list-due", "summary"], default="list-due")
    args = parser.parse_args()
    run(args.action)


if __name__ == "__main__":
    main()
