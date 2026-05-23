"""
Market Domination internal endpoints — safe, read-only summaries that
back the brand-growth operating layer on the founder console.

Every endpoint:
- Is read-only.
- Returns ``source=fallback`` until real data is wired.
- Never reaches an external system.
- Never returns customer PII.

Mounted under ``/api/v1/internal/`` so external callers do not get
public access by default. Authentication is intentionally left to the
host application's standard internal-route security layer (e.g. the
existing admin-key dependency) — wire it in via main.py when needed.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/internal",
    tags=["market-domination-internal"],
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/brand/summary")
def brand_summary() -> dict:
    """Return the canonical brand summary the founder console reads."""
    return {
        "source": "fallback",
        "as_of": _now_iso(),
        "brand": {
            "name": "Dealix",
            "wordmark": "DEALIX",
            "tagline_en": "Intelligent Deals. Real Growth.",
            "tagline_ar": "صفقات ذكية. نمو حقيقي.",
            "positioning": (
                "Saudi B2B Revenue Operating System for intelligent deal flow, "
                "founder-approved growth, and trust-gated AI execution."
            ),
            "pillars": [
                "Built on Trust",
                "Driven by Growth",
                "Closing Deals",
                "Focused on Results",
                "Global Mindset, Local Impact",
            ],
            "colors": {
                "deep_navy": "#0B1220",
                "emerald_teal": "#00D1A1",
                "soft_silver": "#B2BBC6",
                "slate": "#0F1726",
                "white": "#FFFFFF",
            },
        },
        "assets": {
            "logo_full_svg": "/brand/dealix-logo-full.svg",
            "mark_svg": "/brand/dealix-mark.svg",
            "og_svg": "/brand/og.svg",
            "favicon_svg": "/brand/favicon.svg",
        },
    }


@router.get("/growth/targeting")
def growth_targeting() -> dict:
    """Return sector targeting + tier-shape summary (recommendation only)."""
    sectors = [
        "ERP / CRM implementers",
        "Cybersecurity",
        "B2B agencies",
        "Logistics / industrial services",
        "Consulting / digital transformation",
        "SaaS / software",
        "Enterprise services",
        "Saudi high-ticket B2B providers",
    ]
    return {
        "source": "fallback",
        "as_of": _now_iso(),
        "sectors": [
            {"sector_id": f"sec-{i+1:02d}", "name": s, "rank": i + 1}
            for i, s in enumerate(sectors)
        ],
        "tier_distribution": {"A": 0, "B": 0, "C": 0, "D": 0},
        "notes": [
            "All values are fallback until intelligence layer is wired.",
            "No external action is taken from this endpoint.",
        ],
    }


@router.get("/marketing/summary")
def marketing_summary() -> dict:
    """Return marketing calendar + drafts summary."""
    return {
        "source": "fallback",
        "as_of": _now_iso(),
        "calendar": {
            "slots_next_7d": 0,
            "drafts_queued": 0,
            "voice_blocks_last_7d": 0,
            "published_last_7d": 0,
        },
        "surfaces": [
            {"surface": "linkedin", "cadence": "2-4/week"},
            {"surface": "sector_pulse", "cadence": "1/sector/month"},
            {"surface": "case_study", "cadence": "per consented proof"},
            {"surface": "landing", "cadence": "quarterly review"},
        ],
    }


@router.get("/product/distribution")
def product_distribution() -> dict:
    """Return the Dealix product ladder + rung-to-channel map."""
    return {
        "source": "fallback",
        "as_of": _now_iso(),
        "ladder": [
            {"rung": 1, "name": "Free Sample / Diagnostic"},
            {"rung": 2, "name": "Revenue Sprint"},
            {"rung": 3, "name": "Managed Pilot"},
            {"rung": 4, "name": "Revenue Desk Retainer"},
            {"rung": 5, "name": "Founder Console / Command Center"},
            {"rung": 6, "name": "Enterprise Revenue Intelligence OS"},
            {"rung": 7, "name": "Partner / White-label Revenue OS"},
        ],
        "rung_channel_map": {
            "1": ["warm_intro", "contact_form", "linkedin_draft"],
            "2": ["sample_to_sprint", "partner_referral", "email_draft"],
            "3": ["proposal_factory", "abm"],
            "4": ["renewal_motion", "proof_to_demand"],
            "5": ["annual_plan", "partner_referral"],
            "6": ["abm", "executive_briefing"],
            "7": ["partner_program"],
        },
        "guardrails": {
            "no_guaranteed_claims": True,
            "no_pricing_in_marketing": True,
            "trust_gated_external_actions": True,
        },
    }
