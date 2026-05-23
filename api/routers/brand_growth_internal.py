"""
Internal read-only endpoints for the Brand & Growth Operating Layer.

These endpoints power the Founder Console (apps/web) and never trigger
external action. They read from the seeded CSVs in data/seeds/ and from
the canonical brand tokens in docs/brand/brand-tokens.json.

All endpoints return source provenance so the founder can tell signal
from fallback at a glance.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/internal", tags=["internal-brand-growth"])

REPO_ROOT = Path(__file__).resolve().parents[2]
BRAND_TOKENS_PATH = REPO_ROOT / "docs" / "brand" / "brand-tokens.json"
SEEDS = REPO_ROOT / "data" / "seeds"


def _load_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _load_brand_tokens() -> dict[str, Any]:
    if not BRAND_TOKENS_PATH.exists():
        raise HTTPException(status_code=503, detail="brand tokens not provisioned")
    with BRAND_TOKENS_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


@router.get("/brand/summary")
async def brand_summary() -> dict[str, Any]:
    """
    Read-only brand summary. Returns the brand pillars, tagline, palette
    snapshot and a registry of brand assets.
    """
    try:
        tokens = _load_brand_tokens()
        token_source = "signal"
    except HTTPException:
        tokens = {}
        token_source = "fallback"

    assets = _load_csv(SEEDS / "brand" / "brand_assets_registry.csv")
    return {
        "brand": {
            "name": "DEALIX",
            "tagline": "INTELLIGENT DEALS. REAL GROWTH.",
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
        },
        "palette": {
            "bg_primary": "#0B1220",
            "bg_surface": "#0F1726",
            "accent_primary": "#00D1A1",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B2BBC6",
        },
        "tokens_source": token_source,
        "tokens_meta": tokens.get("meta", {}),
        "assets": assets,
        "assets_source": "signal" if assets else "fallback",
    }


@router.get("/growth/targeting")
async def growth_targeting() -> dict[str, Any]:
    """
    Read-only growth targeting payload. Sectors, ICP segments, account scores
    and active distribution machines.
    """
    sectors = _load_csv(SEEDS / "growth" / "sector_targets.csv")
    segments = _load_csv(SEEDS / "growth" / "target_segments.csv")
    accounts = _load_csv(SEEDS / "growth" / "account_scores.csv")
    machines = _load_csv(SEEDS / "growth" / "distribution_machines.csv")
    return {
        "sectors": sectors,
        "sectors_source": "signal" if sectors else "fallback",
        "segments": segments,
        "segments_source": "signal" if segments else "fallback",
        "accounts": accounts,
        "accounts_source": "signal" if accounts else "fallback",
        "machines": machines,
        "machines_source": "signal" if machines else "fallback",
        "trust_note": (
            "All scores and recommendations are decision support only. "
            "Engagement decisions are made via /approvals."
        ),
    }


@router.get("/marketing/summary")
async def marketing_summary() -> dict[str, Any]:
    """
    Read-only marketing summary: calendar, campaigns, and the content idea
    backlog.
    """
    calendar = _load_csv(SEEDS / "marketing" / "content_calendar.csv")
    campaigns = _load_csv(SEEDS / "marketing" / "campaigns.csv")
    ideas = _load_csv(SEEDS / "marketing" / "content_ideas.csv")
    return {
        "calendar": calendar,
        "calendar_source": "signal" if calendar else "fallback",
        "campaigns": campaigns,
        "campaigns_source": "signal" if campaigns else "fallback",
        "ideas": ideas,
        "ideas_source": "signal" if ideas else "fallback",
        "trust_note": (
            "No campaign launches without brand check and trust check. "
            "All copy passes through the Brand Guardian and Trust Guardian."
        ),
    }


@router.get("/product/distribution")
async def product_distribution() -> dict[str, Any]:
    """
    Read-only offer ladder and per-rung distribution allocation.
    """
    ladder = _load_csv(SEEDS / "product" / "offer_ladder.csv")
    distribution = _load_csv(SEEDS / "product" / "product_distribution.csv")
    return {
        "offer_ladder": ladder,
        "offer_ladder_source": "signal" if ladder else "fallback",
        "product_distribution": distribution,
        "product_distribution_source": "signal" if distribution else "fallback",
        "pricing_guardrails_doc": "docs/product/PRICING_GUARDRAILS.md",
        "trust_note": (
            "No rung promises guaranteed revenue. No pricing variance happens "
            "without founder approval."
        ),
    }
