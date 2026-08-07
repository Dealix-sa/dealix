"""Thin adapters to existing intelligence modules.

Verifies actual class/function names before use. All new OS modules import from
here — never directly from the source modules — so symbol renames are isolated.
"""

from __future__ import annotations

from intelligence.competitor_battlecards import CompetitorBattlecards
from intelligence.customer_success_scorecard import CustomerSuccessScorecard
from intelligence.gtm_campaign_orchestrator import GTMCampaignOrchestrator
from intelligence.pricing_engine import PackageTier, PricingEngine, PricingRecommendation
from intelligence.product_led_growth import PLGRecommendation, ProductLedGrowthFlow
from intelligence.proposal_generator import GeneratedProposal, ProposalGeneratorAgent
from intelligence.revenue_forecasting import RevenueForecast, RevenueForecastingEngine
from intelligence.saudi_lead_machine import EnrichedLead, SaudiLeadMachine

# Re-export with stable names
PricingAdapter = PricingEngine
BattlecardsAdapter = CompetitorBattlecards
ForecastingAdapter = RevenueForecastingEngine
CSScorecard = CustomerSuccessScorecard
GTMAdapter = GTMCampaignOrchestrator
PLGAdapter = ProductLedGrowthFlow
LeadMachineAdapter = SaudiLeadMachine
ProposalsAdapter = ProposalGeneratorAgent

PackageTier = PackageTier
PricingRecommendation = PricingRecommendation
GeneratedProposal = GeneratedProposal
PLGRecommendation = PLGRecommendation
EnrichedLead = EnrichedLead
RevenueForecast = RevenueForecast


def get_price_book() -> dict[str, dict[str, float]]:
    """Single source of truth for allowed SKUs and prices."""
    return PricingAdapter().PRICE_BOOK


def validate_sku(package: str) -> bool:
    """Returns True only if package exists in the price book."""
    return package in get_price_book()


def list_packages() -> list[str]:
    return list(get_price_book().keys())
