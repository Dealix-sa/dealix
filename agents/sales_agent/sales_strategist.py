"""
Sales Strategist Agent

An autonomous agent that analyzes a Saudi prospect and produces:
- ICP fit score
- Outreach strategy
- Personalized pitch angles
- Objection handling
- Next-step recommendation

Built on the Dealix BaseAgent and Intelligence Layer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from core.agents.base import BaseAgent
from core.config.models import Task
from core.errors import AgentError
from core.utils import generate_id
from intelligence import SaudiCompanyProfile, SaudiMarketIntelligence


@dataclass
class SalesStrategy:
    prospect_name: str
    icp_score: float
    fit_summary: str
    pitch_angles: list[str] = field(default_factory=list)
    outreach_channel: str = "email"
    objections_handling: dict[str, str] = field(default_factory=dict)
    recommended_next_step: str = ""
    confidence: float = 0.0


class SalesStrategistAgent(BaseAgent):
    """Agent that crafts data-informed sales strategies for Saudi B2B prospects."""

    name = "sales_strategist"

    def __init__(self, agent_id: str | None = None, tenant_id: str | None = None):
        super().__init__(agent_id=agent_id or generate_id(self.name), tenant_id=tenant_id)
        self.market_intel = SaudiMarketIntelligence()

    async def run(self, prospect: SaudiCompanyProfile) -> SalesStrategy:
        """Generate a complete sales strategy for one prospect."""
        icp = self.market_intel.score_icp(prospect)
        entry = self.market_intel.recommend_entry(prospect.sector, prospect.city)

        # Build prompt for the LLM
        system_prompt = self._system_prompt()
        user_prompt = self._user_prompt(prospect, icp, entry)

        response = await self.router.run(
            Task.PROPOSAL,
            messages=[{"role": "user", "content": user_prompt}],
            system=system_prompt,
            max_tokens=2048,
            temperature=0.4,
            force_json=True,
        )

        try:
            parsed = json.loads(response.content)
        except json.JSONDecodeError as exc:
            raise AgentError(f"Sales strategist returned invalid JSON: {response.content}") from exc

        return SalesStrategy(
            prospect_name=prospect.company_name,
            icp_score=icp.score,
            fit_summary=parsed.get("fit_summary", ""),
            pitch_angles=parsed.get("pitch_angles", []),
            outreach_channel=parsed.get("outreach_channel", "email"),
            objections_handling=parsed.get("objections_handling", {}),
            recommended_next_step=parsed.get("recommended_next_step", ""),
            confidence=parsed.get("confidence", 0.5),
        )

    def _system_prompt(self) -> str:
        return (
            "You are the Dealix Sales Strategist, an expert in Saudi B2B sales. "
            "You analyze a prospect profile and output a JSON strategy with these keys: "
            "fit_summary (string), pitch_angles (list of 3 strings), outreach_channel "
            "(email/linkedin/whatsapp), objections_handling (dict string→string), "
            "recommended_next_step (string), confidence (0.0-1.0). "
            "Be concise, culturally appropriate for Saudi business, and never overclaim."
        )

    def _user_prompt(
        self,
        prospect: SaudiCompanyProfile,
        icp: Any,
        entry: dict[str, Any],
    ) -> str:
        return (
            f"Prospect: {prospect.company_name}\n"
            f"Sector: {prospect.sector}\n"
            f"City: {prospect.city}\n"
            f"Employees: {prospect.employees_estimate or 'unknown'}\n"
            f"Website: {prospect.website or 'unknown'}\n"
            f"ICP Score: {icp.score}/100\n"
            f"Reasons: {', '.join(icp.reasons)}\n"
            f"Risk flags: {', '.join(icp.risk_flags)}\n"
            f"Market momentum: {entry.get('momentum')}\n"
            f"Recommended package: {entry.get('recommended_package')}\n\n"
            "Generate a Saudi-appropriate sales strategy in JSON."
        )
