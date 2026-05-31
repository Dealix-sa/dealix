"""Custom Systems OS router — governed per-client custom design + structure + spec.

Thin wrapper over ``auto_client_acquisition.custom_systems_os``. Mirrors the
``data_os`` router conventions: inline Source Passport, a top-level
``governance_decision`` field, and ``safe_to_send`` always False (no surface
here ever sends externally). The capability is gated by the doctrine entry
rule (>= 3 paid pilots) inside ``entry_gate.check_entry``.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.custom_systems_os.engagement_runner import (
    run_custom_system_engagement,
)
from auto_client_acquisition.custom_systems_os.entry_gate import (
    DELIVERY_MODE,
    MIN_PAID_PILOTS,
    check_entry,
)
from auto_client_acquisition.custom_systems_os.ledger import list_engagements
from auto_client_acquisition.data_os.source_passport import SourcePassport

router = APIRouter(prefix="/api/v1/custom-systems", tags=["custom-systems"])

# Where governed spec artifacts are written (out of docs/ at runtime).
_EXPORT_DIR = "var/custom-systems-exports"


class PassportBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = ""
    source_type: str = "client_upload"
    owner: str = "client"
    allowed_use: list[str] = Field(default_factory=lambda: ["internal_analysis"])
    contains_pii: bool = False
    sensitivity: str = "medium"
    retention_policy: str = "project_duration"
    ai_access_allowed: bool = True
    external_use_allowed: bool = False


class EntryCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paid_pilots_completed: int = Field(ge=0)
    workflow_owner_present: bool = False


class RunEngagementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    engagement_id: str = Field(min_length=1)
    paid_pilots_completed: int = Field(ge=0)
    declared_modules: list[str] = Field(default_factory=list)
    declared_workflows: list[str] = Field(default_factory=list)
    direction_name: str = "saudi_executive_trust"
    sector: str | None = None
    workflow_owner_present: bool = False
    adoption_score: float = 0.0
    passport: PassportBody | None = None


def _build_passport(body: PassportBody | None) -> SourcePassport:
    """Build a SourcePassport; a missing passport yields an invalid one so the
    engagement is governed-blocked (never silently allowed)."""
    if body is None:
        return SourcePassport(
            source_id="",
            source_type="missing",
            owner="",
            allowed_use=frozenset(),
            contains_pii=False,
            sensitivity="unknown",
            retention_policy="",
            ai_access_allowed=False,
            external_use_allowed=False,
        )
    return SourcePassport(
        source_id=body.source_id,
        source_type=body.source_type,
        owner=body.owner,
        allowed_use=frozenset(body.allowed_use),
        contains_pii=body.contains_pii,
        sensitivity=body.sensitivity,
        retention_policy=body.retention_policy,
        ai_access_allowed=body.ai_access_allowed,
        external_use_allowed=body.external_use_allowed,
    )


@router.get("/health")
async def health() -> dict[str, Any]:
    return {
        "system": "custom_systems_os",
        "status": "ok",
        "hard_gates": {
            "min_paid_pilots": MIN_PAID_PILOTS,
            "delivery_mode": DELIVERY_MODE,
            "source_passport_required": True,
            "proof_pack_required": True,
            "capital_asset_required": True,
            "no_automated_external_send": True,
        },
    }


@router.post("/entry-check")
async def entry_check(body: EntryCheckRequest) -> dict[str, Any]:
    decision = check_entry(
        paid_pilots_completed=body.paid_pilots_completed,
        workflow_owner_present=body.workflow_owner_present,
    )
    out = decision.to_dict()
    out["safe_to_send"] = False
    return out


@router.post("/run")
async def run(body: RunEngagementRequest) -> dict[str, Any]:
    result = run_custom_system_engagement(
        customer_id=body.customer_id,
        customer_name=body.customer_name,
        engagement_id=body.engagement_id,
        passport=_build_passport(body.passport),
        paid_pilots_completed=body.paid_pilots_completed,
        declared_modules=body.declared_modules,
        declared_workflows=body.declared_workflows,
        direction_name=body.direction_name,
        sector=body.sector,
        workflow_owner_present=body.workflow_owner_present,
        adoption_score=body.adoption_score,
        out_dir=_EXPORT_DIR,
        write_ledger=True,
    )
    out = result.to_dict()
    out["safe_to_send"] = False
    out["approval_required"] = True
    return out


@router.get("/engagements/{customer_id}")
async def engagements(customer_id: str, limit: int = 200) -> dict[str, Any]:
    records = list_engagements(customer_id=customer_id, limit=limit)
    return {
        "customer_id": customer_id,
        "count": len(records),
        "engagements": [r.to_dict() for r in records],
    }
