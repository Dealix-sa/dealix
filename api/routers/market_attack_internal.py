"""Internal Market Attack & Scaling endpoints.

Reads the same CSVs that the markdown generators read, but exposes
them as JSON for the apps/web internal dashboard. Read-only.
Admin-key gated to match the rest of the internal command surface.

Endpoints:
  GET /api/v1/internal/market-attack/summary
  GET /api/v1/internal/campaigns/summary
  GET /api/v1/internal/partners/pipeline
  GET /api/v1/internal/sales-assets/summary
  GET /api/v1/internal/authority/queue
"""
from __future__ import annotations

import csv
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends

try:
    from api.security.api_key import require_admin_key  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - safety net so import never crashes app
    def require_admin_key() -> None:  # type: ignore[no-redef]
        return None

router = APIRouter(prefix="/api/v1/internal", tags=["market-attack"])

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BOOTSTRAP_ROOT = REPO_ROOT / "scripts" / "market_attack_bootstrap"


def _private_ops_root() -> Path:
    raw = os.environ.get("PRIVATE_OPS", "").strip()
    if raw:
        return Path(raw)
    return REPO_ROOT / ".private_ops_sandbox"


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [dict(row) for row in reader if row]


def _load(rel_runtime: Path, rel_bootstrap: Path) -> tuple[list[dict[str, str]], str]:
    if rel_runtime.exists():
        return _read_csv(rel_runtime), "api"
    return _read_csv(rel_bootstrap), "fallback"


def _safe_int(value: str | None) -> int:
    try:
        return int((value or "0").strip())
    except (TypeError, ValueError):
        return 0


def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _combine_sources(*sources: str) -> str:
    """Aggregate per-CSV source labels into a single `api` or `fallback`.

    Returns `fallback` only when *every* input came from the bootstrap;
    otherwise the runtime is partially live and we call it `api`.
    """
    return "fallback" if all(s == "fallback" for s in sources) else "api"


def _priority_for(score: int) -> str:
    if score >= 36:
        return "P0"
    if score >= 30:
        return "P1"
    if score >= 24:
        return "P2"
    if score >= 18:
        return "hold"
    return "kill"


@router.get("/market-attack/summary", dependencies=[Depends(require_admin_key)])
def market_attack_summary() -> dict[str, Any]:
    priv = _private_ops_root()
    sectors, src1 = _load(
        priv / "market_attack" / "beachhead_sector_scorecard.csv",
        BOOTSTRAP_ROOT / "market_attack" / "beachhead_sector_scorecard.csv",
    )
    objections, src2 = _load(
        priv / "market_attack" / "objection_library.csv",
        BOOTSTRAP_ROOT / "market_attack" / "objection_library.csv",
    )
    accounts, src3 = _load(
        priv / "market_attack" / "strategic_accounts.csv",
        BOOTSTRAP_ROOT / "market_attack" / "strategic_accounts.csv",
    )

    scored: list[dict[str, Any]] = []
    for r in sectors:
        total = sum(
            _safe_int(r.get(k))
            for k in (
                "saudi_relevance",
                "buyer_clarity",
                "pain_urgency",
                "high_ticket_potential",
                "proof_fit",
                "delivery_fit",
                "competition_gap",
                "channel_access",
                "trust_risk",
            )
        )
        scored.append(
            {
                "sector": r.get("sector", ""),
                "totalScore": total,
                "priority": _priority_for(total),
            }
        )

    scored.sort(key=lambda x: x["totalScore"], reverse=True)
    beachhead = scored[0] if scored and scored[0]["priority"] == "P0" else None

    p0 = sum(1 for s in scored if s["priority"] == "P0")
    p1 = sum(1 for s in scored if s["priority"] == "P1")

    high_freq = sum(1 for o in objections if _safe_int(o.get("frequency")) >= 3)

    active_strategic = sum(
        1 for a in accounts if (a.get("priority") or "").strip() in ("T0", "T1")
    )

    source = _combine_sources(src1, src2, src3)

    return {
        "source": source,
        "generatedAt": _now(),
        "beachhead": beachhead,
        "p0Count": p0,
        "p1Count": p1,
        "openObjections": len(objections),
        "highFrequencyObjections": high_freq,
        "activeT0AndT1Accounts": active_strategic,
    }


@router.get("/campaigns/summary", dependencies=[Depends(require_admin_key)])
def campaigns_summary() -> dict[str, Any]:
    priv = _private_ops_root()
    registry, s1 = _load(
        priv / "campaigns" / "campaign_registry.csv",
        BOOTSTRAP_ROOT / "campaigns" / "campaign_registry.csv",
    )
    queue, s2 = _load(
        priv / "campaigns" / "campaign_queue.csv",
        BOOTSTRAP_ROOT / "campaigns" / "campaign_queue.csv",
    )
    assets, s3 = _load(
        priv / "campaigns" / "campaign_assets.csv",
        BOOTSTRAP_ROOT / "campaigns" / "campaign_assets.csv",
    )
    results, s4 = _load(
        priv / "campaigns" / "campaign_results.csv",
        BOOTSTRAP_ROOT / "campaigns" / "campaign_results.csv",
    )

    cs: dict[str, int] = defaultdict(int)
    for r in registry:
        cs[(r.get("status") or "draft").strip() or "draft"] += 1
    qs: dict[str, int] = defaultdict(int)
    for q in queue:
        qs[(q.get("send_status") or "queued").strip() or "queued"] += 1

    pending = sum(
        1 for a in assets if (a.get("approval_status") or "pending").strip() == "pending"
    )

    totals: dict[str, int] = defaultdict(int)
    for row in results:
        for col in (
            "impressions",
            "clicks",
            "replies",
            "positive_replies",
            "samples",
            "proposals",
            "payments",
        ):
            totals[col] += _safe_int(row.get(col))

    source = _combine_sources(s1, s2, s3, s4)

    return {
        "source": source,
        "generatedAt": _now(),
        "campaignsByStatus": dict(cs),
        "queueByStatus": dict(qs),
        "assetsPendingApproval": pending,
        "results": {
            "impressions": totals["impressions"],
            "clicks": totals["clicks"],
            "replies": totals["replies"],
            "positiveReplies": totals["positive_replies"],
            "samples": totals["samples"],
            "proposals": totals["proposals"],
            "payments": totals["payments"],
        },
    }


@router.get("/partners/pipeline", dependencies=[Depends(require_admin_key)])
def partners_pipeline() -> dict[str, Any]:
    priv = _private_ops_root()
    rows, src = _load(
        priv / "partners" / "partner_pipeline.csv",
        BOOTSTRAP_ROOT / "partners" / "partner_pipeline.csv",
    )
    by_type: dict[str, int] = defaultdict(int)
    by_status: dict[str, int] = defaultdict(int)
    high_referral = 0
    white_label = 0
    for r in rows:
        by_type[r.get("type", "other")] += 1
        by_status[(r.get("status") or "prospect").strip() or "prospect"] += 1
        if (r.get("referral_potential") or "").strip() == "high":
            high_referral += 1
        if (r.get("white_label_potential") or "").strip() == "yes":
            white_label += 1

    return {
        "source": _combine_sources(src),
        "generatedAt": _now(),
        "byType": dict(by_type),
        "byStatus": dict(by_status),
        "highReferralPartners": high_referral,
        "whiteLabelCandidates": white_label,
    }


@router.get("/sales-assets/summary", dependencies=[Depends(require_admin_key)])
def sales_assets_summary() -> dict[str, Any]:
    priv = _private_ops_root()
    rows, src = _load(
        priv / "sales_assets" / "sales_asset_registry.csv",
        BOOTSTRAP_ROOT / "sales_assets" / "sales_asset_registry.csv",
    )
    by_type: dict[str, int] = defaultdict(int)
    by_approval: dict[str, int] = defaultdict(int)
    champion = 0
    for r in rows:
        by_type[r.get("type", "other")] += 1
        by_approval[(r.get("approval_status") or "pending").strip() or "pending"] += 1
        if (r.get("status") or "").strip() == "champion":
            champion += 1

    return {
        "source": _combine_sources(src),
        "generatedAt": _now(),
        "total": len(rows),
        "byType": dict(by_type),
        "byApprovalStatus": dict(by_approval),
        "championAssets": champion,
    }


@router.get("/authority/queue", dependencies=[Depends(require_admin_key)])
def authority_queue() -> dict[str, Any]:
    priv = _private_ops_root()
    posts, s1 = _load(
        priv / "authority" / "founder_posts.csv",
        BOOTSTRAP_ROOT / "authority" / "founder_posts.csv",
    )
    insights, s2 = _load(
        priv / "authority" / "sector_insights.csv",
        BOOTSTRAP_ROOT / "authority" / "sector_insights.csv",
    )
    reports, s3 = _load(
        priv / "authority" / "report_ideas.csv",
        BOOTSTRAP_ROOT / "authority" / "report_ideas.csv",
    )

    posts_pending = sum(
        1 for p in posts if (p.get("approval_status") or "pending").strip() == "pending"
    )
    posts_approved = sum(
        1 for p in posts if (p.get("approval_status") or "").strip() == "approved"
    )
    validated = sum(
        1 for i in insights if (i.get("status") or "").strip() == "validated"
    )

    source = _combine_sources(s1, s2, s3)

    return {
        "source": source,
        "generatedAt": _now(),
        "postsPending": posts_pending,
        "postsApproved": posts_approved,
        "insightsValidated": validated,
        "reportIdeas": len(reports),
    }
