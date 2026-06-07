"""Dealix Now — the deterministic daily founder operating engine.

Turns Dealix's doctrine into a runnable, offline daily pack: load real demo
targets, score them (os/05), route an offer (os/03 + os/01), write a company
brief and an approval-first Arabic outreach draft (high/medium tiers only),
run rule-based email safety, and assemble the Founder Daily Brief (os/10).

Zero external API keys: no LLM calls, no network. Dealix never auto-sends —
every draft awaits founder approval and every decision is logged.

Public API:
    build_now_pack, score_company, route_offer, write_company_brief,
    write_outreach_draft, check_draft_safety, render_daily_brief_markdown,
    and the ledger functions (record_decision, list_decisions, approve, reject).
"""

from __future__ import annotations

from dealix.now.brief import write_company_brief
from dealix.now.daily_brief import render_daily_brief_markdown
from dealix.now.draft import write_outreach_draft
from dealix.now.ledger import (
    approve,
    list_decisions,
    record_decision,
    reject,
)
from dealix.now.offer_router import route_offer
from dealix.now.pack import build_now_pack
from dealix.now.safety import check_draft_safety
from dealix.now.scoring import score_company
from dealix.now.seed import load_targets

__all__ = [
    "approve",
    "build_now_pack",
    "check_draft_safety",
    "list_decisions",
    "load_targets",
    "record_decision",
    "reject",
    "render_daily_brief_markdown",
    "route_offer",
    "score_company",
    "write_company_brief",
    "write_outreach_draft",
]
