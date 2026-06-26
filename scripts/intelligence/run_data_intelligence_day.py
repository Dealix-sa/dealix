#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.connectors.exa import ExaConnector

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "reports" / "intelligence"
LEDGERS_DIR = ROOT / "ledgers"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
LEDGERS_DIR.mkdir(parents=True, exist_ok=True)

RIYADH_QUERIES = [
    {"sector": "clinics", "query": "Riyadh clinics appointment follow up operations"},
    {"sector": "real_estate", "query": "Riyadh real estate companies sales follow up"},
    {"sector": "logistics", "query": "Riyadh logistics companies B2B operations"},
    {"sector": "training", "query": "Riyadh training centers registration operations"},
    {"sector": "marketing_agencies", "query": "Riyadh marketing agencies AI operations"},
    {"sector": "b2b_services", "query": "Riyadh B2B service companies proposal operations"},
]

FIELDS = [
    "company_name",
    "sector",
    "city",
    "website",
    "source_url",
    "verification_status",
    "confidence",
    "pain_hypothesis",
    "dealix_angle",
    "recommended_product",
    "message_stage",
    "next_action",
    "owner_decision",
]


def _company_name(title: str, sector: str) -> str:
    title = (title or "").strip()
    return title[:120] if title else f"Riyadh {sector.replace('_', ' ').title()} Research Item"


def _pain(sector: str) -> str:
    values = {
        "clinics": "Appointment and inquiry follow-up need daily visibility.",
        "real_estate": "Lead follow-up can fragment across portals, calls, and messages.",
        "logistics": "B2B quote and operations follow-up need a command room.",
        "training": "Registration inquiries need structured qualification and reminders.",
        "marketing_agencies": "Teams need reusable AI operating systems for delivery and reporting.",
        "b2b_services": "Proposals and follow-up need one owner decision workflow.",
    }
    return values.get(sector, "Operating visibility can improve with a review-first workflow.")


def _angle(sector: str) -> str:
    if sector in {"clinics", "real_estate", "training"}:
        return "Revenue Command Room OS + Follow-up OS"
    if sector == "marketing_agencies":
        return "Client Delivery OS + AI Trust OS"
    return "Data Intelligence OS + Company Brain OS"


def build_rows(exa: ExaConnector) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    for item in RIYADH_QUERIES:
        sector = item["sector"]
        query = item["query"]
        if exa.can_search_live():
            results = [asdict(result) for result in exa.search(query)]
            mode = "live_search"
        else:
            results = []
            mode = "dry_run"
        evidence.append({"sector": sector, "city": "Riyadh", "query": query, "mode": mode, "results_count": len(results), "results": results[:10]})
        if results:
            for result in results[:5]:
                source_url = result.get("url", "")
                rows.append({
                    "company_name": _company_name(result.get("title", ""), sector),
                    "sector": sector,
                    "city": "Riyadh",
                    "website": source_url,
                    "source_url": source_url,
                    "verification_status": "needs_human_review",
                    "confidence": "0.55",
                    "pain_hypothesis": _pain(sector),
                    "dealix_angle": _angle(sector),
                    "recommended_product": "Data Intelligence OS",
                    "message_stage": "research_only",
                    "next_action": "Founder reviews source and chooses the next step.",
                    "owner_decision": "pending_review",
                })
        else:
            rows.append({
                "company_name": f"Riyadh {sector.replace('_', ' ').title()} Research Queue",
                "sector": sector,
                "city": "Riyadh",
                "website": "",
                "source_url": "manual_research_required",
                "verification_status": "dry_run_query_ready",
                "confidence": "0.00",
                "pain_hypothesis": _pain(sector),
                "dealix_angle": _angle(sector),
                "recommended_product": "Data Intelligence OS",
                "message_stage": "research_only",
                "next_action": "Configure EXA_API_KEY to populate real Riyadh company sources.",
                "owner_decision": "pending_review",
            })
    return rows, evidence


def main() -> int:
    exa = ExaConnector()
    rows, evidence = build_rows(exa)
    generated_at = datetime.now(timezone.utc).isoformat()
    prospects_path = LEDGERS_DIR / "riyadh_exa_prospects.csv"
    with prospects_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    payload = {
        "generated_at": generated_at,
        "system": "Dealix Data Intelligence OS",
        "city": "Riyadh",
        "mode": "live_search" if exa.can_search_live() else "dry_run",
        "delivery_enabled": False,
        "human_review_required": True,
        "source_url_required": True,
        "prospects_path": str(prospects_path.relative_to(ROOT)),
        "prospects_count": len(rows),
        "evidence": evidence,
    }
    (REPORT_DIR / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [
        "# Dealix Data Intelligence Day — Riyadh",
        "",
        f"Generated at: {generated_at}",
        f"Mode: {payload['mode']}",
        f"Prospects file: `{payload['prospects_path']}`",
        "",
        "## Safety",
        "- Delivery is disabled.",
        "- Founder review is required before action.",
        "- Source evidence is required for every reviewed row.",
        "",
        "## Riyadh sectors covered",
    ]
    for item in RIYADH_QUERIES:
        md.append(f"- {item['sector']}: `{item['query']}`")
    md.extend(["", "## Next actions", "- Review `ledgers/riyadh_exa_prospects.csv`.", "- Move approved rows into `ledgers/prospects.csv`.", "- Run `make revenue-daily` after founder approval."])
    (REPORT_DIR / "latest.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("DATA_INTELLIGENCE_DAY_READY")
    print(f"mode={payload['mode']}")
    print(f"prospects={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
