"""Growth Operating System.

Campaign orchestration, growth experiments, content briefs, and social proof —
all approval-first and never auto-published.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from intelligence.bilingual import BilingualRenderer, BilingualText, LanguageCode
from intelligence.ops_adapters import GTMAdapter, LeadMachineAdapter, PLGAdapter
from intelligence.send_gate import SendGate


class ExperimentStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    COMPLETED = "completed"
    INCONCLUSIVE = "inconclusive"


class ContentType(str, Enum):
    CASE_STUDY = "case_study"
    THOUGHT_LEADERSHIP = "thought_leadership"
    SOCIAL_PROOF = "social_proof"
    HOW_TO = "how_to"


@dataclass
class GrowthExperiment:
    experiment_id: str
    hypothesis: BilingualText
    channel: str
    metric: str
    baseline: float | None
    target: float
    status: ExperimentStatus
    result: float | None

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "hypothesis": BilingualRenderer.filter_text(self.hypothesis, lang),
            "channel": self.channel,
            "metric": self.metric,
            "baseline": self.baseline,
            "target": self.target,
            "status": self.status.value,
            "result": self.result,
        }


@dataclass
class ContentBrief:
    brief_id: str
    topic: BilingualText
    target_sector: str
    content_type: ContentType
    key_messages: list[BilingualText]
    distribution_channels: list[str]
    status: Literal["draft"] = "draft"

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "brief_id": self.brief_id,
            "topic": BilingualRenderer.filter_text(self.topic, lang),
            "target_sector": self.target_sector,
            "content_type": self.content_type.value,
            "key_messages": [BilingualRenderer.filter_text(m, lang) for m in self.key_messages],
            "distribution_channels": self.distribution_channels,
            "status": self.status,
        }


@dataclass
class SocialProofAsset:
    asset_id: str
    asset_type: Literal["testimonial", "metric", "case_study", "logo"]
    content: BilingualText
    company_name: str
    sector: str
    verified: bool

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "content": BilingualRenderer.filter_text(self.content, lang),
            "company_name": self.company_name,
            "sector": self.sector,
            "verified": self.verified,
        }


class GrowthOperatingSystem:
    """Approval-first growth operating system."""

    def __init__(self) -> None:
        self.gtm = GTMAdapter()
        self.plg = PLGAdapter()
        self.lead_machine = LeadMachineAdapter()
        self._experiments: list[GrowthExperiment] = []
        self._social_proof: list[SocialProofAsset] = []

    def plan_campaign(
        self,
        name: str,
        sector: str,
        city: str,
        objective: str,
        template: str | None = None,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        SendGate.assert_blocked("campaign_plan_auto_dispatch")
        campaign = self.gtm.create_campaign(name, sector, city, objective, template or "diagnostic_outreach")
        timeline = self.gtm.get_timeline(campaign)
        return BilingualRenderer.wrap(
            {
                "campaign": {
                    "campaign_id": campaign.campaign_id,
                    "name": campaign.name,
                    "sector": campaign.sector,
                    "city": campaign.city,
                    "objective": campaign.objective,
                    "status": campaign.status.value,
                    "steps": [
                        {
                            "channel": s.channel,
                            "delay_days": s.delay_days,
                            "action": s.action,
                            "approved": s.approved,
                        }
                        for s in campaign.steps
                    ],
                    "timeline": timeline,
                }
            },
            lang,
        )

    def approve_campaign(self, campaign_id: str) -> dict[str, Any]:
        # Simple approval by id lookup not stored in v1; return structured acknowledgment
        SendGate.assert_blocked("campaign_approval_auto_dispatch")
        return BilingualRenderer.wrap(
            {"campaign_id": campaign_id, "approval_status": "approved", "note": "External dispatch still requires manual action"},
            "both",
        )

    def create_experiment(
        self,
        hypothesis_en: str,
        hypothesis_ar: str,
        channel: str,
        metric: str,
        target: float,
        baseline: float | None = None,
    ) -> dict[str, Any]:
        experiment = GrowthExperiment(
            experiment_id=f"exp-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            hypothesis=BilingualRenderer.bt(hypothesis_en, hypothesis_ar),
            channel=channel,
            metric=metric,
            baseline=baseline,
            target=target,
            status=ExperimentStatus.DRAFT,
            result=None,
        )
        self._experiments.append(experiment)
        return BilingualRenderer.wrap({"experiment": experiment.to_dict()}, "both")

    def list_experiments(self) -> dict[str, Any]:
        return BilingualRenderer.wrap(
            {"experiments": [e.to_dict() for e in self._experiments]},
            "both",
        )

    def generate_content_brief(
        self,
        topic_en: str,
        topic_ar: str,
        target_sector: str,
        content_type: ContentType | str,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        if isinstance(content_type, str):
            content_type = ContentType(content_type)
        brief = ContentBrief(
            brief_id=f"brief-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            topic=BilingualRenderer.bt(topic_en, topic_ar),
            target_sector=target_sector,
            content_type=content_type,
            key_messages=[
                BilingualRenderer.bt("Saudi-first AI revenue operations", "عمليات إيرادات AI سعودية أولاً"),
                BilingualRenderer.bt("Approval-first governance", "حوكمة الترخيص أولاً"),
                BilingualRenderer.bt("Proof before scale", "الإثبات قبل التوسع"),
            ],
            distribution_channels=["LinkedIn", "Company blog", "WhatsApp status", "Email newsletter"],
        )
        return BilingualRenderer.wrap({"content_brief": brief.to_dict(lang)}, lang)

    def collect_social_proof(
        self,
        asset_type: Literal["testimonial", "metric", "case_study", "logo"],
        content_en: str,
        content_ar: str,
        company_name: str,
        sector: str,
        verified: bool,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        asset = SocialProofAsset(
            asset_id=f"sp-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            asset_type=asset_type,
            content=BilingualRenderer.bt(content_en, content_ar),
            company_name=company_name,
            sector=sector,
            verified=verified,
        )
        self._social_proof.append(asset)
        return BilingualRenderer.wrap({"social_proof_asset": asset.to_dict(lang)}, lang)

    def growth_dashboard(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return BilingualRenderer.wrap(
            {
                "active_experiments": len([e for e in self._experiments if e.status == ExperimentStatus.RUNNING]),
                "draft_experiments": len([e for e in self._experiments if e.status == ExperimentStatus.DRAFT]),
                "social_proof_assets": len(self._social_proof),
                "verified_social_proof": len([a for a in self._social_proof if a.verified]),
                "recent_social_proof": [a.to_dict(lang) for a in self._social_proof[-5:]],
            },
            lang,
        )

    def run_plg_diagnostic(
        self,
        company_name: str,
        sector: str,
        city: str,
        employees: int,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        rec = self.plg.run(company_name, sector, city, employees)
        return BilingualRenderer.wrap({"plg_recommendation": rec.to_dict()}, lang)
