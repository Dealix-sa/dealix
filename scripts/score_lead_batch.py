import argparse
import csv
from pathlib import Path


def score_row(row: dict) -> tuple[int, str]:
    score = 0
    text = " ".join(str(v or "").lower() for v in row.values())

    if row.get("website"):
        score += 10
    if any(term in text for term in ["saudi", "riyadh", "jeddah", "dammam", "ksa", "السعودية", "الرياض", "جدة"]):
        score += 20
    if any(term in text for term in ["b2b", "enterprise", "erp", "crm", "cybersecurity", "logistics", "consulting", "saas", "agency"]):
        score += 25
    if row.get("buyer_title"):
        score += 15
    if row.get("public_contact"):
        score += 10
    if row.get("why_fit"):
        score += 20

    if score >= 80:
        priority = "A"
    elif score >= 60:
        priority = "B"
    elif score >= 40:
        priority = "C"
    else:
        priority = "Reject"

    return score, priority


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
            score, priority = score_row(row)
            row["fit_score"] = str(score)
            row["priority"] = priority
            if not row.get("approval_status"):
                row["approval_status"] = "Pending"
            rows.append(row)

    if "fit_score" not in fieldnames:
        fieldnames.append("fit_score")
    if "priority" not in fieldnames:
        fieldnames.append("priority")
    if "approval_status" not in fieldnames:
        fieldnames.append("approval_status")

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"PASS: scored {len(rows)} leads in {path}")


if __name__ == "__main__":
    main()
