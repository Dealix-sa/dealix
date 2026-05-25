import argparse
import csv
from pathlib import Path

HEADERS = [
    "lead",
    "company",
    "channel",
    "recipient",
    "message",
    "status",
    "approval_status",
    "sent_date",
    "next_action",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    parser.add_argument("--batch-file", required=True)
    parser.add_argument("--channel", default="Manual")
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    batch = Path(args.batch_file)
    out = root / "outreach/outreach_send_queue.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with batch.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    approved = [
        r for r in rows
        if r.get("approval_status") == "Approved"
        and r.get("priority") in {"A", "B"}
    ]
    exists = out.exists() and out.stat().st_size > 0
    with out.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        for row in approved:
            writer.writerow({
                "lead": row.get("company", ""),
                "company": row.get("company", ""),
                "channel": args.channel,
                "recipient": row.get("public_contact", ""),
                "message": row.get("suggested_message", ""),
                "status": "Ready",
                "approval_status": "Approved",
                "sent_date": "",
                "next_action": "send approved outreach",
            })
    print(f"PASS: added {len(approved)} approved leads to outreach send queue: {out}")


if __name__ == "__main__":
    main()
