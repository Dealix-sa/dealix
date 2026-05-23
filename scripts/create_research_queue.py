import argparse
import csv
from pathlib import Path


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
    sources = read_csv(root / "acquisition/source_targets.csv")
    out = root / "acquisition/lead_research_queue.csv"
    headers = [
        "company",
        "sector",
        "website",
        "source",
        "status",
        "research_notes",
        "next_action",
    ]
    exists = out.exists() and out.stat().st_size > 0
    with out.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not exists:
            writer.writeheader()
        for source in sources:
            if source.get("status") == "Planned":
                writer.writerow({
                    "company": "",
                    "sector": source.get("sector", ""),
                    "website": source.get("source_url", ""),
                    "source": source.get("source_name", ""),
                    "status": "Research",
                    "research_notes": source.get("next_action", ""),
                    "next_action": "collect public company leads",
                })
    print(f"PASS: research queue updated: {out}")


if __name__ == "__main__":
    main()
