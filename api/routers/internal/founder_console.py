"""
api.routers.internal.founder_console — Founder Console reader endpoints.

Mounted under /api/v1/internal/founder-console/*. Every endpoint is:
  - read-only
  - gated by Authorization: Bearer <DEALIX_ADMIN_API_KEY>
  - returns {data, source, freshness, is_estimate}

These endpoints do not modify state, do not send external messages, and
do not charge payments. They surface the private-ops runtime CSVs (and
the in-repo policy/registry view) for the Founder Console.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.internal import policy_adapter, runtime_reader
from api.internal.auth import require_admin_bearer

router = APIRouter(
    prefix="/api/v1/internal/founder-console",
    tags=["Admin"],
    dependencies=[Depends(require_admin_bearer)],
)


@router.get("/ceo/daily-brief", summary="CEO daily brief (read-only)")
def get_ceo_daily_brief() -> dict[str, Any]:
    return runtime_reader.ceo_daily_brief()


@router.get("/capital-allocation", summary="Capital allocation view (read-only)")
def get_capital_allocation() -> dict[str, Any]:
    return runtime_reader.capital_allocation()


@router.get("/market-attack", summary="Market-attack beachhead view (read-only)")
def get_market_attack() -> dict[str, Any]:
    return runtime_reader.market_attack()


@router.get("/ai-governance", summary="AI-governance inventory (read-only)")
def get_ai_governance() -> dict[str, Any]:
    return runtime_reader.ai_governance()


@router.get("/trust/flags", summary="Trust flags (read-only)")
def get_trust_flags() -> dict[str, Any]:
    return runtime_reader.trust_flags()


@router.get("/audit/recent", summary="Recent approval decisions (read-only)")
def get_audit_recent() -> dict[str, Any]:
    return runtime_reader.audit_recent()


@router.get("/policy", summary="Merged policy view (read-only)")
def get_policy() -> dict[str, Any]:
    return policy_adapter.merged_policy_view()
