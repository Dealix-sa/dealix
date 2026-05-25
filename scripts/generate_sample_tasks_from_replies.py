import argparse
import csv
from pathlib import Path
from datetime import date

HEADERS = [
    "date",
    "prospect",
    "sector",
    "sample_path",
    "quality_score",
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
    replies = read_csv(root / "outreach/reply_log.csv")
    out = root / "delivery/sample_quality_log.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    positive = [
        r for r in replies
        if (r.get("reply_type") or "").lower() in {"positive", "interested", "yes"}
    ]
    exists = out.exists() and out.stat().st_size > 0
    with out.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        for row in positive:
            company = row.get("company", "")
            sample_file = f"delivery/samples/{company.replace(' ', '_').lower()}_sample.md"
            writer.writerow({
                "date": date.today().isoformat(),
                "prospect": company,
                "sector": "",
                "sample_path": sample_file,
                "quality_score": "",
                "status": "Planned",
                "next_action": "prepare 5 opportunity sample",
            })
            sample_path = root / sample_file
            sample_path.parent.mkdir(parents=True, exist_ok=True)
            if not sample_path.exists():
                sample_path.write_text(f"# Sample Pack for {company}\n\n", encoding="utf-8")
    print(f"PASS: generated {len(positive)} sample tasks.")


if __name__ == "__main__":
    main()
