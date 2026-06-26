#!/usr/bin/env python3
"""Generate a review-first Authorized Sales Agent pack.

This script creates strategy and draft assets only. It never sends external messages.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.sales_intelligence.authorized_agent import (
    AuthorizationLevel,
    CompanyVoiceProfile,
    SalesAgentRequest,
    build_sales_angle,
    evaluate_authorized_sales_action,
)
from app.sales_intelligence.pain_radar import PainSignal, analyze_company_pain

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "commercial" / "authorized_sales_agent"

DEMO_SIGNALS = [
    PainSignal(
        source="demo public website",
        signal_type="follow-up signal",
        description="Multiple service inquiry paths but no visible operating promise for response ownership.",
        confidence=7,
    ),
    PainSignal(
        source="demo sales notes",
        signal_type="proposal signal",
        description="Customer asks about price and scope before the first diagnostic call.",
        confidence=6,
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    radar = analyze_company_pain(DEMO_SIGNALS)
    voice = CompanyVoiceProfile(
        company_name="Dealix",
        allowed_signatory_names=("Sami",),
        allowed_titles=("Founder", "Sales Lead"),
    )
    request = SalesAgentRequest(
        target_company="Demo B2B Company",
        source_url="https://example.com",
        pain_hypothesis=radar.primary_pain,
        recommended_offer=radar.recommended_offer,
        authorization_level=AuthorizationLevel.DRAFT_ONLY,
        claims=("review-first operating system",),
    )
    decision = evaluate_authorized_sales_action(request, voice)
    angle = build_sales_angle(
        target_company=request.target_company,
        sector="Saudi B2B Services",
        pain_signal=radar.primary_pain,
        offer=radar.recommended_offer,
    )

    payload = {
        "mode": "draft_only",
        "external_send": False,
        "target_company": request.target_company,
        "pain_radar": radar.__dict__,
        "policy_decision": decision.__dict__,
        "sales_angle": angle,
        "next_actions": [
            "Founder reviews pain hypothesis.",
            "Founder confirms approved company voice.",
            "Founder decides hold/review/send manually.",
        ],
    }

    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "latest.md").write_text(
        "# Authorized Sales Agent Pack\n\n"
        f"## Mode\n\n{payload['mode']}\n\n"
        f"## Target\n\n{request.target_company}\n\n"
        f"## Pain hypothesis\n\n{radar.primary_pain}\n\n"
        f"## Recommended offer\n\n{radar.recommended_offer}\n\n"
        f"## Policy decision\n\n{decision.status}: {decision.reason}\n\n"
        f"## Sales angle\n\n{angle}\n\n"
        "## Safety\n\nNo external action was performed. This is a review-first pack.\n",
        encoding="utf-8",
    )
    print("AUTHORIZED_SALES_AGENT_PACK_READY")
    print(OUT / "latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
