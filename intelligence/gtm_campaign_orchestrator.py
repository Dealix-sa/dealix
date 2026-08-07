"""
GTM Campaign Orchestrator

Plans, sequences, and tracks multi-channel GTM campaigns for Saudi B2B.
Approval-first: no external sends without human sign-off.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


@dataclass
class CampaignStep:
    channel: str
    delay_days: int
    action: str
    approved: bool = False


@dataclass
class GTMCampaign:
    campaign_id: str
    name: str
    sector: str
    city: str
    objective: str
    steps: list[CampaignStep]
    status: CampaignStatus
    created_at: datetime


class GTMCampaignOrchestrator:
    """Designs approval-first GTM campaigns for Saudi B2B."""

    TEMPLATES: dict[str, list[CampaignStep]] = {
        "diagnostic_outreach": [
            CampaignStep(channel="email", delay_days=0, action="Send personalized diagnostic invitation"),
            CampaignStep(channel="linkedin", delay_days=2, action="LinkedIn connection request with value note"),
            CampaignStep(channel="email", delay_days=5, action="Follow up with sector insight"),
            CampaignStep(channel="call", delay_days=7, action="Founder/consultant call"),
        ],
        "lead_sprint": [
            CampaignStep(channel="email", delay_days=0, action="Deliver prospect pack"),
            CampaignStep(channel="email", delay_days=1, action="Send outreach sequence drafts for approval"),
            CampaignStep(channel="email", delay_days=3, action="Send first external send after approval"),
            CampaignStep(channel="call", delay_days=6, action="Review responses and refine"),
        ],
        "pilot nurturing": [
            CampaignStep(channel="email", delay_days=0, action="Share pilot proof pack"),
            CampaignStep(channel="call", delay_days=2, action="Q&A call with decision makers"),
            CampaignStep(channel="email", delay_days=5, action="Send proposal and SOW"),
            CampaignStep(channel="call", delay_days=10, action="Contract review call"),
        ],
    }

    def create_campaign(
        self,
        name: str,
        sector: str,
        city: str,
        objective: str,
        template: str,
    ) -> GTMCampaign:
        """Create a new campaign from a template."""
        steps = self.TEMPLATES.get(template, self.TEMPLATES["diagnostic_outreach"])
        return GTMCampaign(
            campaign_id=f"gtm-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            name=name,
            sector=sector,
            city=city,
            objective=objective,
            steps=[CampaignStep(channel=s.channel, delay_days=s.delay_days, action=s.action) for s in steps],
            status=CampaignStatus.DRAFT,
            created_at=datetime.utcnow(),
        )

    def approve_campaign(self, campaign: GTMCampaign) -> GTMCampaign:
        campaign.status = CampaignStatus.APPROVED
        return campaign

    def get_timeline(self, campaign: GTMCampaign, start_date: datetime | None = None) -> list[dict[str, Any]]:
        start = start_date or campaign.created_at
        return [
            {
                "day": step.delay_days,
                "scheduled_at": (start + timedelta(days=step.delay_days)).isoformat(),
                "channel": step.channel,
                "action": step.action,
                "approved": step.approved,
            }
            for step in campaign.steps
        ]

    def mark_step_approved(self, campaign: GTMCampaign, step_index: int) -> GTMCampaign:
        if 0 <= step_index < len(campaign.steps):
            campaign.steps[step_index].approved = True
        return campaign
