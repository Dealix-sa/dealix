#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = dt.date.today().isoformat()
OUT = ROOT / "company" / "runtime" / "intake" / TODAY
CRM = ROOT / "company" / "crm" / "pipeline.csv"

OUT.mkdir(parents=True, exist_ok=True)
CRM.parent.mkdir(parents=True, exist_ok=True)

FIELDS = [
    "company_name",
    "sector",
    "city",
    "branches",
    "contact_name",
    "whatsapp",
    "email",
    "website",
    "weekly_leads",
    "main_channel",
    "has_crm",
    "has_reports",
    "main_problem",
    "goal_30_days",
    "budget_range",
    "fit_score",
    "recommended_offer",
    "next_action",
]

def score(row: dict[str, str]) -> int:
    value = 40

    try:
        weekly = int(row.get("weekly_leads") or 0)
        if weekly >= 100:
            value += 25
        elif weekly >= 30:
            value += 15
        elif weekly >= 10:
            value += 8
    except (ValueError, TypeError):
        pass

    if row.get("main_problem"):
        value += 15
    if row.get("whatsapp"):
        value += 10
    if row.get("budget_range") in ["25k - 75k", "75k+"]:
        value += 10

    return min(value, 100)

def recommend(row: dict[str, str]) -> str:
    problem = (row.get("main_problem") or "").lower()
    sector = (row.get("sector") or "").lower()

    if "واتساب" in problem or "whatsapp" in problem:
        return "WhatsApp Revenue OS"
    if "تقييم" in problem or "review" in problem:
        return "Review Intelligence OS"
    if "هوية" in problem or "brand" in problem:
        return "Brand Intelligence OS"
    if "تقرير" in problem or "إدارة" in problem:
        return "AI Business Command Center"
    if "training" in sector or "تدريب" in sector:
        return "Growth Engine OS"
    return "Transformation Diagnostic Sprint"

def write_empty_template() -> None:
    path = OUT / "CLIENT_INTAKE_TEMPLATE.csv"
    if not path.exists():
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow({
                "company_name": "Example Company",
                "sector": "Clinics",
                "city": "Riyadh",
                "branches": "1",
                "contact_name": "Name",
                "whatsapp": "+9665xxxxxxx",
                "email": "email@example.com",
                "website": "https://example.com",
                "weekly_leads": "30",
                "main_channel": "WhatsApp",
                "has_crm": "No",
                "has_reports": "No",
                "main_problem": "واتساب والمتابعة",
                "goal_30_days": "تنظيم المتابعة وزيادة الحجوزات",
                "budget_range": "10k - 25k",
                "fit_score": "",
                "recommended_offer": "",
                "next_action": "",
            })

def process_intake_file(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            row["fit_score"] = str(score(row))
            row["recommended_offer"] = recommend(row)
            row["next_action"] = "book_20_min_fit_call" if int(row["fit_score"]) >= 65 else "send_diagnostic_summary"
            rows.append(row)

    return rows

def write_outputs(rows: list[dict[str, str]]) -> None:
    summary = OUT / "INTAKE_SUMMARY.md"

    lines = [
        "# Dealix Intake Summary",
        "",
        f"Date: {TODAY}",
        "",
    ]

    if not rows:
        lines += [
            "No intake rows processed yet.",
            "",
            "Use:",
            f"`company/runtime/intake/{TODAY}/CLIENT_INTAKE_TEMPLATE.csv`",
        ]
    else:
        lines += [
            "| Company | Sector | Score | Recommended Offer | Next Action |",
            "|---|---|---:|---|---|",
        ]
        for row in rows:
            lines.append(
                f"| {row.get('company_name','')} | {row.get('sector','')} | {row.get('fit_score','')} | {row.get('recommended_offer','')} | {row.get('next_action','')} |"
            )

    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if rows:
        with (OUT / "PROPOSAL_READY_INTAKES.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

def main() -> None:
    write_empty_template()

    manual_path = OUT / "CLIENT_INTAKE_TEMPLATE.csv"
    rows = process_intake_file(manual_path)
    write_outputs(rows)

    print(f"Intake template: {manual_path}")
    print(f"Intake summary: {OUT / 'INTAKE_SUMMARY.md'}")

if __name__ == "__main__":
    main()
