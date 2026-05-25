import argparse
import csv
from pathlib import Path


def route(reply_type: str) -> str:
    value = reply_type.lower().strip()
    if value in {"positive", "interested", "yes"}:
        return "prepare sample or book call"
    if value in {"pricing", "cost"}:
        return "send short offer explanation or proposal if qualified"
    if value in {"not now", "later"}:
        return "schedule nurture follow-up"
    if value in {"not interested", "no"}:
        return "mark as lost and log reason"
    if value in {"refer", "forwarded"}:
        return "ask for correct decision maker"
    return "review manually"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    path = root / "outreach/reply_log.csv"
    if not path.exists():
        print(f"Missing: {path}")
        raise SystemExit(1)
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    updated = []
    for row in rows:
        if not row.get("next_action"):
            row["next_action"] = route(row.get("reply_type", ""))
        updated.append(row)
    headers = ["date", "company", "channel", "reply_type", "summary", "next_action"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated)
    print(f"PASS: routed {len(updated)} replies.")


if __name__ == "__main__":
    main()
