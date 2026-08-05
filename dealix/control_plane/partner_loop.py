"""
Section 72 — Partner Value Loop.

For each partner:
    Scout → Fit Score → Pitch → Agreement → Onboard → First client →
    Revenue share → Performance review → Scale or remove.

Every white-label partner output passes through Trust Check before
leaving the workspace.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class PartnerStage(StrEnum):
    SCOUTING = "scouting"
    FIT_SCORED = "fit_scored"
    PITCHED = "pitched"
    AGREEMENT = "agreement"
    ONBOARDED = "onboarded"
    FIRST_CLIENT = "first_client"
    SCALED = "scaled"
    REMOVED = "removed"


class PartnerRiskKind(StrEnum):
    BRAND = "brand_risk"
    DELIVERY = "delivery_risk"
    DATA = "data_risk"
    CLAIM = "claim_risk"
    COMMERCIAL = "commercial_risk"


@dataclass
class PartnerRiskCheck:
    risk_kind: PartnerRiskKind
    severity: str
    note: str
    cleared: bool = False
    at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Partner:
    partner_id: str
    name: str
    workspace_id: str
    stage: PartnerStage = PartnerStage.SCOUTING
    fit_score: float = 0.0
    revenue_share_pct: float = 0.0
    risks: list[PartnerRiskCheck] = field(default_factory=list)
    notes: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "partner_id": self.partner_id,
            "name": self.name,
            "workspace_id": self.workspace_id,
            "stage": self.stage.value,
            "fit_score": self.fit_score,
            "revenue_share_pct": self.revenue_share_pct,
            "risks": [
                {
                    "risk_kind": r.risk_kind.value,
                    "severity": r.severity,
                    "note": r.note,
                    "cleared": r.cleared,
                    "at": r.at.isoformat(),
                }
                for r in self.risks
            ],
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }


class PartnerValueLoop:
    def __init__(self) -> None:
        self._partners: dict[str, Partner] = {}

    def scout(self, *, name: str, workspace_id: str) -> Partner:
        partner = Partner(
            partner_id=f"prt_{uuid.uuid4().hex[:12]}",
            name=name,
            workspace_id=workspace_id,
        )
        self._partners[partner.partner_id] = partner
        return partner

    def score_fit(self, partner_id: str, *, fit_score: float) -> Partner:
        if not 0.0 <= fit_score <= 1.0:
            raise ValueError("fit_score must be in [0.0, 1.0]")
        partner = self.get(partner_id)
        partner.fit_score = fit_score
        partner.stage = PartnerStage.FIT_SCORED
        return partner

    def advance(self, partner_id: str, *, stage: PartnerStage) -> Partner:
        partner = self.get(partner_id)
        partner.stage = stage
        return partner

    def set_revenue_share(self, partner_id: str, *, pct: float) -> Partner:
        if not 0.0 <= pct <= 100.0:
            raise ValueError("revenue_share_pct must be in [0.0, 100.0]")
        partner = self.get(partner_id)
        partner.revenue_share_pct = pct
        return partner

    def add_risk_check(
        self,
        partner_id: str,
        *,
        risk_kind: PartnerRiskKind,
        severity: str,
        note: str,
        cleared: bool = False,
    ) -> PartnerRiskCheck:
        partner = self.get(partner_id)
        check = PartnerRiskCheck(
            risk_kind=risk_kind, severity=severity, note=note, cleared=cleared
        )
        partner.risks.append(check)
        return check

    def trust_check_clear(self, partner_id: str) -> bool:
        partner = self.get(partner_id)
        if not partner.risks:
            return False
        return all(r.cleared for r in partner.risks)

    def remove(self, partner_id: str, *, reason: str) -> Partner:
        partner = self.get(partner_id)
        partner.stage = PartnerStage.REMOVED
        partner.notes = (partner.notes + f" | removed: {reason}").strip(" |")
        return partner

    def get(self, partner_id: str) -> Partner:
        try:
            return self._partners[partner_id]
        except KeyError as exc:
            raise KeyError(f"unknown partner: {partner_id}") from exc

    def all(self) -> list[Partner]:
        return list(self._partners.values())

    def without_revenue(self) -> list[Partner]:
        return [
            p
            for p in self._partners.values()
            if p.revenue_share_pct == 0.0 and p.stage != PartnerStage.REMOVED
        ]
