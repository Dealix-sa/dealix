import argparse
import csv
from pathlib import Path


def build_message(row: dict) -> str:
    company = row.get("company", "your company")
    sector = row.get("sector", "B2B")
    why_fit = row.get("why_fit", "your B2B market looks relevant")
    return (
        f"Hi — I'm Sami, building Dealix for Saudi B2B revenue operations. "
        f"I noticed {company} in {sector}. {why_fit}. "
        f"I'm preparing small Revenue Sprint samples: a short list of qualified opportunity targets, "
        f"why they fit, and suggested outreach angles. "
        f"Would it be useful if I send a small sample for {company}?"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    path = Path(args.file)
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            if not row.get("suggested_message"):
                row["suggested_message"] = build_message(row)
            rows.append(row)

    if "suggested_message" not in fieldnames:
        fieldnames.append("suggested_message")

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"PASS: generated suggested messages for {len(rows)} leads.")


if __name__ == "__main__":
    main()
