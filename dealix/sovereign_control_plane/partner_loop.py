"""
Partner Value Loop — §103.

Partners are scored on fit and on five risk axes (brand, delivery,
data, claim, commercial). Any partner output must pass the trust
check. Critical risk in any axis flunks the check.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.types import RiskLevel


_RISK_AXES = ("brand", "delivery", "data", "claim", "commercial")


@dataclass
class Partner:
    partner_id: str
    name: str
    fit_score: float
    risks: dict[str, RiskLevel]
    revenue_share_pct: float
    status: str = "scouted"
    revenue_log: list[dict[str, Any]] = field(default_factory=list)
    onboarded_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "partner_id": self.partner_id,
            "name": self.name,
            "fit_score": self.fit_score,
            "risks": {k: v.value for k, v in self.risks.items()},
            "revenue_share_pct": self.revenue_share_pct,
            "status": self.status,
            "revenue_log": list(self.revenue_log),
            "onboarded_at": self.onboarded_at,
        }


class PartnerValueLoop:
    def __init__(self) -> None:
        self._items: dict[str, Partner] = {}
        self._lock = threading.Lock()

    def scout(self, name: str, metadata: dict[str, Any] | None = None) -> Partner:
        with self._lock:
            p = Partner(
                partner_id=f"par_{uuid.uuid4().hex[:12]}",
                name=name, fit_score=0.0,
                risks={k: RiskLevel.LOW for k in _RISK_AXES},
                revenue_share_pct=0.0, status="scouted",
            )
            self._items[p.partner_id] = p
            return p

    def get(self, partner_id: str) -> Partner | None:
        return self._items.get(partner_id)

    def score(
        self, partner_id: str, fit_score: float, risks: dict[str, RiskLevel]
    ) -> Partner:
        with self._lock:
            p = self._items[partner_id]
            p.fit_score = float(fit_score)
            for axis, level in risks.items():
                if axis in _RISK_AXES:
                    p.risks[axis] = level
            p.status = "scored"
            return p

    def agree(self, partner_id: str, revenue_share_pct: float) -> Partner:
        with self._lock:
            p = self._items[partner_id]
            p.revenue_share_pct = float(revenue_share_pct)
            p.status = "agreed"
            return p

    def onboard(self, partner_id: str) -> Partner:
        with self._lock:
            p = self._items[partner_id]
            p.status = "onboarded"
            p.onboarded_at = datetime.now(UTC).isoformat()
            return p

    def log_revenue(
        self, partner_id: str, amount_sar: float, deal_id: str | None = None
    ) -> dict[str, Any]:
        rec = {
            "amount_sar": amount_sar, "deal_id": deal_id,
            "at": datetime.now(UTC).isoformat(),
        }
        p = self._items[partner_id]
        p.revenue_log.append(rec)
        return rec

    def performance_review(self, partner_id: str) -> dict[str, Any]:
        p = self._items[partner_id]
        total = round(sum(r["amount_sar"] for r in p.revenue_log), 2)
        return {
            "partner_id": p.partner_id,
            "fit_score": p.fit_score,
            "total_revenue_sar": total,
            "risks": {k: v.value for k, v in p.risks.items()},
            "recommendation": self.recommend_action(partner_id),
        }

    def recommend_action(self, partner_id: str) -> str:
        p = self._items[partner_id]
        if any(level == RiskLevel.CRITICAL for level in p.risks.values()):
            return "remove"
        total = sum(r["amount_sar"] for r in p.revenue_log)
        if total == 0 and p.status == "onboarded":
            return "pause"
        if total > 100_000 and p.fit_score >= 0.7:
            return "scale"
        return "hold"

    def trust_check(self, output: dict[str, Any]) -> tuple[bool, list[str]]:
        findings: list[str] = []
        partner_id = output.get("partner_id")
        p = self._items.get(partner_id or "")
        if p is None:
            findings.append("unknown_partner")
            return False, findings
        for axis, level in p.risks.items():
            if level == RiskLevel.CRITICAL:
                findings.append(f"{axis}_risk_critical")
        text = str(output.get("text", "")).lower()
        if "guaranteed" in text or "بالتأكيد" in text:
            findings.append("forbidden_claim")
        return (len(findings) == 0), findings
