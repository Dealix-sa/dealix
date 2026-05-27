"""Money Module — cash + revenue engine (section 116).

Reuses the kernel objects:

  Signal      → ``CashSignal`` payloads
  Opportunity → scored with the Money Score formula
  Decision    → ``send_proposal`` / ``followup`` / ``invoice``
  Execution   → handled by the agents listed in the spec
  Outcome     → won/lost + revenue_sar
  Asset       → reusable proposals, follow-up snippets, pricing curves
"""

from dealix.hermes.money.cash_scout import CashScout, CashSignalPayload
from dealix.hermes.money.cashflow import CashflowForecast, ForecastEntry
from dealix.hermes.money.dashboard import MoneyDashboard, MoneyDashboardView
from dealix.hermes.money.deal_room import DealRoom, DealStage
from dealix.hermes.money.followup import FollowUp, FollowUpTracker
from dealix.hermes.money.invoice import Invoice, InvoiceLedger, InvoiceStatus
from dealix.hermes.money.investor_update import InvestorUpdate, InvestorUpdateBuilder
from dealix.hermes.money.offer_matcher import OfferMatcher
from dealix.hermes.money.pricing import PricingPolicy, PriceBand
from dealix.hermes.money.proposal_factory import Proposal, ProposalFactory
from dealix.hermes.money.revenue_hunter import RevenueHunter

__all__ = [
    "CashScout",
    "CashSignalPayload",
    "CashflowForecast",
    "ForecastEntry",
    "DealRoom",
    "DealStage",
    "FollowUp",
    "FollowUpTracker",
    "Invoice",
    "InvoiceLedger",
    "InvoiceStatus",
    "InvestorUpdate",
    "InvestorUpdateBuilder",
    "MoneyDashboard",
    "MoneyDashboardView",
    "OfferMatcher",
    "PricingPolicy",
    "PriceBand",
    "Proposal",
    "ProposalFactory",
    "RevenueHunter",
]
