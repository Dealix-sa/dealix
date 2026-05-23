import argparse
import csv
from pathlib import Path
from datetime import date

PIPELINE_HEADERS = [
    "company",
    "sector",
    "contact",
    "stage",
    "priority",
    "next_action",
    "last_touch",
    "notes",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    parser.add_argument("--batch-file", required=True)
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    batch = Path(args.batch_file)
    pipeline_path = root / "pipeline/pipeline_tracker.csv"
    pipeline_path.parent.mkdir(parents=True, exist_ok=True)

    with batch.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    approved = [
        r for r in rows
        if r.get("approval_status") == "Approved" and r.get("priority") in {"A", "B"}
    ]

    exists = pipeline_path.exists() and pipeline_path.stat().st_size > 0
    with pipeline_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PIPELINE_HEADERS)
        if not exists:
            writer.writeheader()
        for row in approved:
            writer.writerow({
                "company": row.get("company", ""),
                "sector": row.get("sector", ""),
                "contact": row.get("public_contact", ""),
                "stage": "Qualified",
                "priority": row.get("priority", ""),
                "next_action": "Send approved founder-led outreach",
                "last_touch": date.today().isoformat(),
                "notes": f"source={row.get('source','')}; website={row.get('website','')}; why={row.get('why_fit','')}",
            })

    print(f"PASS: exported {len(approved)} approved leads to pipeline.")


if __name__ == "__main__":
    main()
