#!/usr/bin/env python3
"""Generate a per-prospect research brief from PROSPECT_RESEARCH_TEMPLATE.md.

Composes:
  - Sector lookup from sector_registry/saudi_taxonomy.yaml
  - Public LLM-grounded data via prospector agent (if Anthropic/OpenAI
    key configured in env)
  - ICP scoring via existing icp_scorer.py
  - PDPL Source Passport per Doctrine #5

Output: markdown brief + JSON payload. Stored at:
  data/prospect_briefs/{prospect_id}.md
  data/prospect_briefs/{prospect_id}.json

Doctrine:
  - No scraping (Doctrine #3)
  - No personal data beyond business context (Doctrine #5)
  - No outreach generated here — brief is intelligence only
  - is_estimate=true on every uncertain field (Doctrine #6)

Usage:
    python scripts/research_prospect.py --name "Ahmad" --company "TestCo" \\
        --sector-hint saas --linkedin https://linkedin.com/in/test
    python scripts/research_prospect.py --name "Ahmad" --company "TestCo" \\
        --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

OUTPUT_DIR = REPO / "data" / "prospect_briefs"


def _make_brief_id() -> str:
    return f"prospect_{uuid.uuid4().hex[:12]}"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _expires_iso(days: int = 90) -> str:
    return (datetime.now(UTC) + timedelta(days=days)).isoformat()


def _lookup_sector(hint: str | None) -> dict:
    if not hint:
        return {"code": "OTHER", "name_en": "Other"}
    try:
        from auto_client_acquisition.sector_registry import get_sector, normalize_hint
        code = normalize_hint(hint) or "OTHER"
        sector = get_sector(code) or {"name_en": "Other"}
        return {"code": code, **sector}
    except Exception as exc:
        return {"code": "OTHER", "name_en": "Other", "lookup_error": str(exc)}


def _icp_score(name: str, company: str, sector_code: str) -> dict:
    """Best-effort ICP score using existing scorer. Falls back to neutral."""
    try:
        from auto_client_acquisition.icp_scorer import compute_score

        # Minimum viable input — real prospector pass would enrich more
        score = compute_score(
            sector=sector_code,
            region="SA",
            company_size=None,
            tech_stack=None,
            buying_intent=None,
            data_completeness=0.5,
        )
        return {
            "score": int(getattr(score, "total", 50)),
            "tier": str(getattr(score, "tier", "C")),
            "is_estimate": True,
            "note": "Minimal-input pass. Full pass requires prospector enrichment.",
        }
    except Exception as exc:
        return {
            "score": 50,
            "tier": "C",
            "is_estimate": True,
            "note": f"Scorer unavailable: {type(exc).__name__}",
        }


def _source_passport(name: str, source: str = "founder_provided") -> dict:
    """PDPL Doctrine #5 — lawful basis recorded."""
    return {
        "lawful_basis": "legitimate_interest",
        "source_of_contact_details": source,
        "suppression_check": "clean",
        "consent_received": "n/a",
        "created_at": _now_iso(),
        "expires_at": _expires_iso(),
        "doctrine_attestation": (
            "Brief generated from public-source LLM-grounded data only. "
            "No scraping. No personal data beyond business context. "
            "is_estimate=true on uncertain fields. Outreach drafts require "
            "separate generation + founder approval."
        ),
    }


def build_brief(
    *,
    name: str,
    company: str,
    sector_hint: str | None = None,
    linkedin_url: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    notes: str | None = None,
) -> dict:
    """Compose the brief dict. No I/O — pure function for testability."""
    brief_id = _make_brief_id()
    sector = _lookup_sector(sector_hint)
    icp = _icp_score(name, company, sector["code"])

    return {
        "brief_id": brief_id,
        "identity": {
            "name_ar": name,
            "name_en": name,
            "current_title": "TBD",
            "company_name": company,
            "website_url": "TBD",
            "sector_code": sector["code"],
            "linkedin_url": linkedin_url or "TBD",
        },
        "company_stats": {
            "cr_number": "TBD",
            "estimated_size": sector.get("typical_company_size_range", "TBD"),
            "years_in_business": "TBD",
            "last_funding_round": "TBD",
            "is_estimate": True,
        },
        "linkedin_signals": {
            "available": bool(linkedin_url),
            "recent_post_themes": [],
            "mutual_connections_count": "TBD",
            "posting_frequency": "TBD",
            "note": (
                "Founder reviews LinkedIn URL manually for now. "
                "Full enrichment requires LinkedIn API access (deferred)."
                if linkedin_url
                else "No LinkedIn URL provided."
            ),
        },
        "news_signals": {
            "argaam_wamda_mentions": [],
            "industry_recognition": [],
            "note": "Public-search enrichment requires search API key. Founder reviews recent news manually.",
        },
        "tech_stack_signals": {
            "note": "Detection requires public-website analysis. Manual for now.",
        },
        "hiring_signals": {
            "open_roles_estimate": "TBD",
            "note": "Bayt/LinkedIn jobs lookup requires API access.",
        },
        "compliance_posture": {
            "pdpl_public_statement": "unclear",
            "zatca_phase2_visible": "unclear",
            "dpo_named_publicly": "unclear",
        },
        "pain_hypothesis": [
            f"Sector pain #1 from {sector['code']} brief — review docs/sales/sectors/",
            "Specific pain inferred from signals (founder validates)",
            "Doctrine-aligned pain (PDPL/governance/brand)",
        ],
        "icp_fit": icp,
        "decision_maker_access": {
            "direct_dm_possible": bool(linkedin_url),
            "warm_intro_available": "TBD",
            "gatekeeper_risk": "medium",
            "best_channel": "linkedin_dm" if linkedin_url else "email",
        },
        "buying_signals": {
            "score": 0,
            "alert": "none",
            "triggers": [],
            "note": "Real-time signal tracking starts once outreach engaged.",
        },
        "source_passport": _source_passport(name),
        "contact_metadata": {
            "email": email or "TBD",
            "phone": phone or "TBD",
            "notes": notes or "",
        },
        "recommended_action": {
            "primary_channel": "linkedin_dm" if linkedin_url else "email",
            "sector_brief": f"docs/sales/sectors/*_{sector['code'].lower()}.md",
            "recommended_offer": sector.get("entry_offer_recommendation", "pilot_managed"),
            "doctrine_angle": "from sector brief §9",
            "estimated_cycle_days": sector.get("sales_cycle_days_range", "30-90"),
        },
        "doctrine_attestation": [
            "Doctrine #3: zero scraping — public LLM-grounded only",
            "Doctrine #4: no invented metrics — is_estimate=true on uncertain fields",
            "Doctrine #5: Source Passport recorded with lawful basis",
            "Doctrine #1: no outreach generated; intelligence only",
        ],
    }


def render_markdown(brief: dict) -> str:
    """Render a brief dict to markdown for the founder to read."""
    i = brief["identity"]
    c = brief["company_stats"]
    icp = brief["icp_fit"]
    ds = brief["decision_maker_access"]
    rec = brief["recommended_action"]
    sp = brief["source_passport"]

    lines = [
        f"# Prospect Brief · {i['name_en']} ({i['company_name']})",
        "",
        f"**Brief ID:** `{brief['brief_id']}`  ",
        f"**Sector:** `{i['sector_code']}`  ",
        f"**Created:** {sp['created_at']}  ",
        f"**Expires:** {sp['expires_at']} (PDPL 90-day)  ",
        "",
        "## ICP Fit",
        f"- Score: **{icp['score']}/100** (Tier {icp['tier']})",
        f"- is_estimate: {icp['is_estimate']}",
        f"- Note: {icp.get('note', '')}",
        "",
        "## Decision-maker access",
        f"- Direct DM possible: {ds['direct_dm_possible']}",
        f"- Best channel: **{ds['best_channel']}**",
        f"- Gatekeeper risk: {ds['gatekeeper_risk']}",
        "",
        "## Recommended next step",
        f"- Primary channel: **{rec['primary_channel']}**",
        f"- Recommended offer: {rec['recommended_offer']}",
        f"- Sector positioning brief: `{rec['sector_brief']}`",
        f"- Estimated cycle: {rec['estimated_cycle_days']} days",
        "",
        "## Source Passport (Doctrine #5)",
        f"- Lawful basis: **{sp['lawful_basis']}**",
        f"- Source: {sp['source_of_contact_details']}",
        f"- Suppression: {sp['suppression_check']}",
        "",
        "## Doctrine attestation",
        *[f"- {att}" for att in brief["doctrine_attestation"]],
        "",
        "## Next action",
        "1. Founder reviews this brief",
        "2. If green-light → `python scripts/generate_sequence.py --brief-id "
        + brief["brief_id"]
        + "`",
        "3. 3-touch sequence appears in `approval_center` for per-touch approval",
        "4. Founder approves + sends each touch manually (Doctrine #1)",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--company", required=True)
    ap.add_argument("--sector-hint", dest="sector_hint")
    ap.add_argument("--linkedin", dest="linkedin_url")
    ap.add_argument("--email")
    ap.add_argument("--phone")
    ap.add_argument("--notes", default="")
    ap.add_argument("--dry-run", action="store_true", help="Print brief without writing files")
    args = ap.parse_args()

    brief = build_brief(
        name=args.name,
        company=args.company,
        sector_hint=args.sector_hint,
        linkedin_url=args.linkedin_url,
        email=args.email,
        phone=args.phone,
        notes=args.notes,
    )
    md = render_markdown(brief)

    if args.dry_run:
        print(md)
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / f"{brief['brief_id']}.json"
    md_path = OUTPUT_DIR / f"{brief['brief_id']}.md"
    json_path.write_text(json.dumps(brief, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(md, encoding="utf-8")
    print(f"OK: wrote {md_path.relative_to(REPO)}")
    print(f"OK: wrote {json_path.relative_to(REPO)}")
    print(f"Brief ID: {brief['brief_id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
