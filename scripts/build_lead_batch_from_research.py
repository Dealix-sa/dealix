import argparse
import csv
from pathlib import Path
from datetime import date

BATCH_HEADERS = [
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


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    rows = read_csv(root / "acquisition/lead_research_queue.csv")
    selected = [
        r for r in rows
        if args.sector.lower() in (r.get("sector") or "").lower()
        and (r.get("company") or "").strip()
    ][:args.limit]
    batch_name = f"{date.today().isoformat()}-{args.sector.replace(' ', '-').lower()}"
    out = root / "acquisition/lead_batches" / f"{batch_name}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=BATCH_HEADERS)
        writer.writeheader()
        for row in selected:
            writer.writerow({
                "company": row.get("company", ""),
                "sector": row.get("sector", ""),
                "website": row.get("website", ""),
                "public_contact": "",
                "buyer_title": "Founder / CEO / Sales Leader",
                "fit_score": "",
                "priority": "",
                "why_fit": row.get("research_notes", ""),
                "source": row.get("source", ""),
                "suggested_message": "",
                "approval_status": "Pending",
                "next_action": "score and draft outreach",
            })
    print(f"PASS: built lead batch with {len(selected)} leads: {out}")


if __name__ == "__main__":
    main()
