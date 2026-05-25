import argparse
import csv
from pathlib import Path
from datetime import date

HEADERS = [
    "company",
    "sector",
    "website",
    "public_contact",
    "buyer_title",
    "fit_score",
    "priority",
    "why_fit",
    "source",
    "suggested_message",
    "approval_status",
    "next_action",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--batch-name", default=None)
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    batch_name = args.batch_name or f"{date.today().isoformat()}-{args.sector.replace(' ', '-').lower()}"
    out = root / "acquisition/lead_batches" / f"{batch_name}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    if not out.exists():
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()

    print(f"PASS: lead batch template created: {out}")
    print("Next: fill 25 public leads, then run lead scoring.")


if __name__ == "__main__":
    main()
