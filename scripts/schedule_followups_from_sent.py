import argparse
import csv
from pathlib import Path
from datetime import datetime, timedelta

HEADERS = [
    "lead",
    "company",
    "channel",
    "last_touch",
    "next_followup_date",
    "followup_type",
    "status",
    "next_action",
]


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    send_queue = read_csv(root / "outreach/outreach_send_queue.csv")
    out = root / "outreach/followup_queue.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    sent = [
        r for r in send_queue
        if (r.get("status") or "").lower() == "sent"
        and r.get("sent_date")
    ]
    exists = out.exists() and out.stat().st_size > 0
    with out.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        for row in sent:
            sent_date = datetime.fromisoformat(row["sent_date"]).date()
            writer.writerow({
                "lead": row.get("lead", ""),
                "company": row.get("company", ""),
                "channel": row.get("channel", ""),
                "last_touch": row.get("sent_date", ""),
                "next_followup_date": (sent_date + timedelta(days=2)).isoformat(),
                "followup_type": "Follow-Up 1",
                "status": "Planned",
                "next_action": "send follow-up if no reply",
            })
    print(f"PASS: scheduled followups for {len(sent)} sent leads.")


if __name__ == "__main__":
    main()
