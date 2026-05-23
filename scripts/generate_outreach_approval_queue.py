import argparse
import csv
from pathlib import Path
from datetime import date


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    parser.add_argument("--batch-file", required=True)
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    batch = Path(args.batch_file)

    with batch.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    top = [
        r for r in rows
        if r.get("priority") in {"A", "B"} and r.get("approval_status", "Pending") == "Pending"
    ]

    lines = [
        "# Outreach Approval Queue",
        "",
        "## Date",
        date.today().isoformat(),
        "",
        "## Batch File",
        str(batch),
        "",
        "## Leads Ready For Review",
        str(len(top)),
        "",
        "## Approval Decision",
        "Approved / Needs Edit / Rejected",
        "",
        "## Leads",
        "",
    ]

    for i, row in enumerate(top[:25], start=1):
        lines.extend([
            f"### {i}. {row.get('company','')}",
            f"- Sector: {row.get('sector','')}",
            f"- Website: {row.get('website','')}",
            f"- Priority: {row.get('priority','')}",
            f"- Score: {row.get('fit_score','')}",
            f"- Why fit: {row.get('why_fit','')}",
            f"- Message: {row.get('suggested_message','')}",
            "",
        ])

    out = root / "founder/outreach_approval_queue.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"PASS: approval queue generated: {out}")


if __name__ == "__main__":
    main()
