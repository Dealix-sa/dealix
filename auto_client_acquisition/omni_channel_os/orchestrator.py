"""Omni-Channel OS Orchestrator — runs the full pipeline for a batch of companies."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Company,
    DailyQuota,
    FounderReviewItem,
    Language,
    OmniChannelBrief,
    ReviewAction,
    RiskLevel,
)

log = logging.getLogger(__name__)
_NO_AUTO_SEND = True


@dataclass
class PipelineResult:
    total_companies: int = 0
    total_assets: int = 0
    founder_queue: list[FounderReviewItem] = field(default_factory=list)
    auto_queued: list[ChannelAsset] = field(default_factory=list)
    blocked: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    quota: DailyQuota | None = None
    report: Any | None = None


class OmniChannelOrchestrator:
    """
    Main pipeline:
    companies -> enrich -> classify -> buyer_map -> offer_route -> channel_route
              -> asset_generate -> quality_gate -> compliance_gate
              -> founder_queue (sensitive) / auto_queue (inbound only)
              -> report
    """

    _NO_AUTO_SEND = True

    def __init__(self) -> None:
        from auto_client_acquisition.omni_channel_os.asset_factory import AssetFactory
        from auto_client_acquisition.omni_channel_os.buyer_mapper import BuyerMapper
        from auto_client_acquisition.omni_channel_os.channel_report import ChannelReporter
        from auto_client_acquisition.omni_channel_os.channel_router import ChannelRouter
        from auto_client_acquisition.omni_channel_os.compliance_gate import ComplianceGate
        from auto_client_acquisition.omni_channel_os.founder_review_queue import FounderReviewQueue
        from auto_client_acquisition.omni_channel_os.offer_router import OfferRouter
        from auto_client_acquisition.omni_channel_os.quality_gate import QualityGate

        self.buyer_mapper = BuyerMapper()
        self.channel_router = ChannelRouter()
        self.offer_router = OfferRouter()
        self.asset_factory = AssetFactory()
        self.quality_gate = QualityGate()
        self.compliance_gate = ComplianceGate()
        self.review_queue = FounderReviewQueue()
        self.reporter = ChannelReporter()

    def run_batch(
        self,
        companies: list[Company],
        date: str | None = None,
    ) -> PipelineResult:
        """Process a batch of companies through the full pipeline."""
        result = PipelineResult()
        quota = DailyQuota(date=date or datetime.now(UTC).strftime("%Y-%m-%d"))

        for company in companies:
            try:
                brief = self._process_one(company)
                if brief:
                    result.total_companies += 1
                    result.total_assets += len(brief.assets)
                    quota.company_briefs_done += 1
                    self._route_brief(brief, result, quota)
            except Exception as exc:
                result.errors.append(f"{company.name}: {exc}")
                log.warning("pipeline_error company=%s error=%s", company.name, str(exc))

        result.quota = quota
        result.report = self.reporter.generate(result, quota)
        return result

    def _process_one(self, company: Company) -> OmniChannelBrief | None:
        """Run a single company through the full pipeline."""
        from auto_client_acquisition.omni_channel_os.asset_factory import OfferData

        persona = self.buyer_mapper.map(company)
        channel_decision = self.channel_router.route(company)
        offer_name, angle = self.offer_router.route(company, persona)

        offer_data = OfferData(
            offer_name=offer_name,
            angle_ar=angle if company.language == Language.arabic else "",
            angle_en=angle if company.language != Language.arabic else angle,
            lead_magnet_ar=self.offer_router.get_lead_magnet(
                company.sector.value, Language.arabic
            ),
            lead_magnet_en=self.offer_router.get_lead_magnet(
                company.sector.value, Language.english
            ),
            cta_ar=self.offer_router.get_cta(offer_name, Language.arabic),
            cta_en=self.offer_router.get_cta(offer_name, Language.english),
            tier=self.offer_router.get_tier(company.sector.value),
        )

        assets = self.asset_factory.generate_full_package(company, persona, offer_data)

        filtered_assets: dict[str, ChannelAsset] = {}
        for asset_key, asset in assets.items():
            quality_ok = self.quality_gate.passes(asset, company)
            compliant, _ = self.compliance_gate.check(asset, company)
            if quality_ok and compliant:
                asset.quality_score = self.quality_gate.score(asset, company)
                filtered_assets[asset_key] = asset

        if not filtered_assets:
            return None

        brief_score = sum(a.quality_score for a in filtered_assets.values()) / len(
            filtered_assets
        )

        return OmniChannelBrief(
            company=company,
            buyer_persona=persona,
            channel_decision=channel_decision,
            offer_name=offer_name,
            angle=angle,
            assets=filtered_assets,
            brief_score=brief_score,
        )

    def _route_brief(
        self,
        brief: OmniChannelBrief,
        result: PipelineResult,
        quota: DailyQuota,
    ) -> None:
        """Route assets to founder queue (sensitive) or auto queue (inbound only)."""
        auto_assets = [a for a in brief.assets.values() if a.is_auto_sendable]
        manual_assets = [a for a in brief.assets.values() if not a.is_auto_sendable]

        result.auto_queued.extend(auto_assets)

        if manual_assets:
            primary_ch = (
                brief.channel_decision.primary_channels[0]
                if brief.channel_decision.primary_channels
                else ChannelType.email
            )
            backup_ch = (
                brief.channel_decision.primary_channels[1]
                if len(brief.channel_decision.primary_channels) > 1
                else None
            )

            asset_ready_types: list[AssetType] = []
            for k in brief.assets:
                try:
                    asset_ready_types.append(AssetType(k))
                except ValueError:
                    pass

            item = FounderReviewItem(
                company=brief.company.name,
                country=brief.company.country.value,
                sector=brief.company.sector.value,
                language=brief.company.language,
                buyer_title=(
                    brief.buyer_persona.typical_titles[0]
                    if brief.buyer_persona.typical_titles
                    else "Decision Maker"
                ),
                best_channel=primary_ch,
                backup_channel=backup_ch,
                offer_name=brief.offer_name,
                angle=brief.angle,
                asset_ready=asset_ready_types,
                quality_score=brief.brief_score,
                risk_level=RiskLevel.medium,
                recommended_action=ReviewAction.review_and_send,
                assets={
                    k: v for k, v in brief.assets.items() if not v.is_auto_sendable
                },
            )
            result.founder_queue.append(item)

        for asset in brief.assets.values():
            _update_quota(quota, asset.asset_type.value)


def _update_quota(quota: DailyQuota, asset_type: str) -> None:
    """Increment the matching quota counter for the given asset type."""
    if "email" in asset_type:
        quota.email_drafts_done += 1
    elif "linkedin" in asset_type:
        quota.linkedin_drafts_done += 1
    elif "website_form" in asset_type:
        quota.website_form_drafts_done += 1
    elif "whatsapp" in asset_type:
        quota.whatsapp_drafts_done += 1
    elif "call_script" in asset_type:
        quota.call_scripts_done += 1
    elif "partner" in asset_type:
        quota.partner_intros_done += 1
    elif "content" in asset_type or "founder" in asset_type:
        quota.content_assets_done += 1
    elif "proposal" in asset_type:
        quota.proposal_seeds_done += 1


__all__ = ["OmniChannelOrchestrator", "PipelineResult", "_update_quota"]
