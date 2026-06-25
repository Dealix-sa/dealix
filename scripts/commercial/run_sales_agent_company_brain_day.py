#!/usr/bin/env python3
"""Run a review-first Sales Agent + Company Brain commercial day.

Reads the commercial account pipeline, generates company-specific packs,
prioritizes accounts, and writes a daily command report. No external
communication is performed.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from app.commercial.prioritizer import queue as build_priority_queue
from app.commercial.sales_agent import build_sales_agent_pack

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / "data" / "commercial" / "lead_pipeline.csv"
FALLBACK_PIPELINE = ROOT / "data" / "commercial" / "lead_pipeline_template.csv"
OUT_DIR = ROOT / "reports" / "commercial" / "sales_agent_company_brain"


def load_rows() -> list[dict[str, str]]:
    path = PIPELINE if PIPELINE.exists() else FALLBACK_PIPELINE
    if not path.exists():
        raise FileNotFoundError(f"missing pipeline file: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_name(value: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
    return safe or "company"


def pack_markdown(pack: dict[str, object]) -> str:
    questions = "\n".join(f"- {item}" for item in pack["discovery_questions"])
    notes = "\n".join(f"- {item}" for item in pack["negotiation_notes"])
    return f"""# {pack['company_name']} — Sales Agent + Company Brain Pack

## Target

- Sector: {pack['sector']}
- City: {pack['city']}
- Source: {pack['source_url']}
- Buyer persona: {pack['buyer_persona']}

## Pain hypothesis

{pack['pain_hypothesis']}

## Recommended offer

{pack['recommended_offer']}

## Draft for review

{pack['draft_message_ar']}

## Discovery questions

{questions}

## Negotiation notes

{notes}

## Company Brain decision

{pack['company_brain_decision']}

## Safety

- Mode: {pack['communication_mode']}
- Owner decision required: {pack['owner_decision_required']}
"""


def summary_markdown(packs: list[dict[str, object]], priority_queue: list[dict[str, object]]) -> str:
    lines = [
        "# Sales Agent + Company Brain Day",
        "",
        "## Verdict",
        "",
        "Daily commercial packs generated for founder review. No external communication was performed.",
        "",
        "## Metrics",
        "",
        f"- targets loaded: {len(packs)}",
        f"- packs generated: {len(packs)}",
        f"- priority queue items: {len(priority_queue)}",
        "- communication mode: draft_only",
        "- owner review required: true",
        "",
        "## Priority queue",
        "",
        "| Priority | Score | Company | Sector | Offer | Reason |",
        "|---|---:|---|---|---|---|",
    ]
    for item in priority_queue[:20]:
        lines.append(
            f"| {item['priority']} | {item['priority_value']} | {item['company_name']} | {item['sector']} | {item['recommended_offer']} | {item['reason']} |"
        )
    lines += ["", "## Founder actions", ""]
    for item in priority_queue[:10]:
        lines.append(f"- Review {item['company_name']} — {item['recommended_offer']} — priority: {item['priority']}")
    lines += ["", "## Generated packs", "", "| Company | Sector | Offer | Buyer | Source |", "|---|---|---|---|---|"]
    for pack in packs:
        lines.append(
            f"| {pack['company_name']} | {pack['sector']} | {pack['recommended_offer']} | {pack['buyer_persona']} | {pack['source_url']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    rows = load_rows()
    priority_queue = build_priority_queue(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    packs: list[dict[str, object]] = []
    for row in rows:
        company_name = row.get("company_name", "").strip()
        if not company_name:
            continue
        pack = build_sales_agent_pack(
            company_name=company_name,
            sector=row.get("sector", "b2b_services"),
            city=row.get("city", "Riyadh"),
            source_url=row.get("source_url", "manual_review_required"),
        ).to_dict()
        packs.append(pack)
        name = safe_name(company_name)
        (OUT_DIR / f"{name}.md").write_text(pack_markdown(pack), encoding="utf-8")
        (OUT_DIR / f"{name}.json").write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "draft_only",
        "owner_review_required": True,
        "source_pipeline": str(PIPELINE.relative_to(ROOT) if PIPELINE.exists() else FALLBACK_PIPELINE.relative_to(ROOT)),
        "targets_loaded": len(rows),
        "packs_generated": len(packs),
        "priority_queue": priority_queue,
        "packs": packs,
    }
    (OUT_DIR / "latest.md").write_text(summary_markdown(packs, priority_queue), encoding="utf-8")
    (OUT_DIR / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("SALES_AGENT_COMPANY_BRAIN_DAY=reports/commercial/sales_agent_company_brain/latest.md")
    print(f"PACKS_GENERATED={len(packs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
