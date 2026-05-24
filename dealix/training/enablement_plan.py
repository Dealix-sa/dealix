"""خادم التدريب — EnablementPlanner."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EnablementPlan(BaseModel):
    """A role-specific enablement plan."""

    model_config = ConfigDict(extra="forbid")

    role: str = Field(..., min_length=1, max_length=120)
    gaps: list[str] = Field(default_factory=list, max_length=12)
    actions: list[dict[str, str]] = Field(..., min_length=1, max_length=12)
    duration_weeks: int = Field(..., ge=1, le=26)
    success_metric: str = Field(..., min_length=1, max_length=400)


# Action menu — gap keyword → enablement action
_ACTION_MENU: dict[str, dict[str, str]] = {
    "trust": {
        "action": "Walk through Sovereignty + Evidence Pack module",
        "owner": "GuardrailAgent",
        "duration_days": "3",
    },
    "sales": {
        "action": "Run two pilot calls with shadowing by HeadOfRevenue",
        "owner": "ProposalFactoryAgent",
        "duration_days": "5",
    },
    "partner": {
        "action": "Score 3 candidates + run PartnerPitch dry-run",
        "owner": "PartnerPitchAgent",
        "duration_days": "4",
    },
    "data": {
        "action": "Complete PDPL data-handling micro-course",
        "owner": "RiskOpsAgent",
        "duration_days": "2",
    },
    "product": {
        "action": "Pair-build one Offer via OfferBuilder",
        "owner": "OfferBuilderAgent",
        "duration_days": "3",
    },
    "customer": {
        "action": "Lead one health-score review with HealthAgent",
        "owner": "CustomerHealthAgent",
        "duration_days": "3",
    },
}


class EnablementPlanner:
    """Build a role-specific enablement plan from a gap list."""

    def plan(self, role: str, gaps: list[str]) -> EnablementPlan:
        if not gaps:
            return EnablementPlan(
                role=role,
                gaps=[],
                actions=[
                    {
                        "action": "Refresh onboarding playbook (no gaps surfaced)",
                        "owner": "KnowledgeCuratorAgent",
                        "duration_days": "1",
                    }
                ],
                duration_weeks=1,
                success_metric=(
                    f"{role} confirms readiness in a 30-minute review."
                ),
            )
        seen: set[str] = set()
        actions: list[dict[str, str]] = []
        for gap in gaps:
            key = gap.lower().strip()
            for needle, action in _ACTION_MENU.items():
                if needle in key and needle not in seen:
                    actions.append({"gap": gap, **action})
                    seen.add(needle)
                    break
            else:
                actions.append(
                    {
                        "gap": gap,
                        "action": f"Curate a learning bundle for: {gap}",
                        "owner": "KnowledgeCuratorAgent",
                        "duration_days": "2",
                    }
                )
        if not actions:
            actions.append(
                {
                    "action": "Generic enablement spike — capture follow-up gaps",
                    "owner": "KnowledgeCuratorAgent",
                    "duration_days": "1",
                }
            )
        total_days = sum(int(a.get("duration_days", "1")) for a in actions)
        duration_weeks = max(1, (total_days + 4) // 5)
        return EnablementPlan(
            role=role,
            gaps=list(gaps),
            actions=actions,
            duration_weeks=duration_weeks,
            success_metric=(
                f"All gaps closed; {role} signs off after a 30-minute review."
            ),
        )


__all__ = ["EnablementPlan", "EnablementPlanner"]
