"""خادم المال — RevenueHunter (spec §43).

Pure scoring of an account pool against a buyer profile. Returns the
ranked TargetAccounts so the operator can decide where to spend the
week's outbound budget. No IO, no LLM calls.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import Money


class AccountProfile(BaseModel):
    """The buyer profile we are hunting against."""

    model_config = ConfigDict(extra="forbid")

    sector: str = Field(..., min_length=1, max_length=64)
    company_size: str = Field(default="sme", min_length=1, max_length=32)
    region: str = Field(default="saudi", min_length=1, max_length=64)
    target_budget: Money | None = None
    keywords: tuple[str, ...] = Field(default_factory=tuple)


class TargetAccount(BaseModel):
    """An account ranked by fit against the AccountProfile."""

    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(..., min_length=1, max_length=128)
    name: str = Field(..., min_length=1, max_length=200)
    fit_score: float = Field(..., ge=0.0, le=5.0)
    reasons: list[str] = Field(default_factory=list, max_length=10)
    expected_value: Money | None = None


class RevenueHunter:
    """Recommend target accounts from a candidate pool."""

    def recommend_targets(
        self,
        account_pool: list[dict[str, Any]],
        profile: AccountProfile,
        top_k: int = 10,
    ) -> list[TargetAccount]:
        if top_k <= 0:
            return []
        scored: list[TargetAccount] = []
        for entry in account_pool:
            target = self._score(entry, profile)
            if target.fit_score <= 0.0:
                continue
            scored.append(target)
        scored.sort(key=lambda t: (-t.fit_score, t.name))
        return scored[:top_k]

    @staticmethod
    def _score(entry: dict[str, Any], profile: AccountProfile) -> TargetAccount:
        name = str(entry.get("name") or entry.get("account_id") or "unknown")
        account_id = str(entry.get("account_id") or name)
        reasons: list[str] = []
        score = 0.0

        if str(entry.get("sector", "")).lower() == profile.sector.lower():
            score += 2.0
            reasons.append(f"sector match ({profile.sector})")
        if str(entry.get("region", "")).lower() == profile.region.lower():
            score += 1.0
            reasons.append(f"region match ({profile.region})")
        if str(entry.get("company_size", "")).lower() == profile.company_size.lower():
            score += 0.5
            reasons.append(f"size match ({profile.company_size})")

        # Keyword matches on entry.notes
        notes = str(entry.get("notes", "")).lower()
        for kw in profile.keywords:
            if kw.lower() in notes:
                score += 0.5
                reasons.append(f"signal keyword: {kw}")

        # Budget alignment
        budget = entry.get("budget_sar")
        expected_value: Money | None = None
        if isinstance(budget, (int, float)):
            expected_value = Money.sar(budget)
            if profile.target_budget is not None:
                target = profile.target_budget.amount
                if abs(float(target) - float(budget)) / max(1.0, float(target)) <= 0.3:
                    score += 1.0
                    reasons.append("budget within 30 % of target")

        score = round(min(5.0, score), 3)
        return TargetAccount(
            account_id=account_id,
            name=name,
            fit_score=score,
            reasons=reasons,
            expected_value=expected_value,
        )


__all__ = [
    "AccountProfile",
    "RevenueHunter",
    "TargetAccount",
]
