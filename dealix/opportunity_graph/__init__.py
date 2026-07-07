"""Dealix Saudi Opportunity Command Room — opportunity graph layer.

Draft-first, approval-guarded targeting for foreign market-entry and Saudi
revenue-recovery plays. This package never sends anything externally; it
scores companies, segments them, drafts human-reviewable outreach, and
produces daily command reports plus weekly proof packs.

See docs/commercial/SAUDI_OPPORTUNITY_COMMAND_ROOM_MASTER_PLAN.md.
"""

from __future__ import annotations

from dealix.opportunity_graph.schemas import (
    DailyCommandReport,
    OpportunityCompany,
    OpportunitySignal,
    OutreachDraft,
    ProofPack,
)

__all__ = [
    "DailyCommandReport",
    "OpportunityCompany",
    "OpportunitySignal",
    "OutreachDraft",
    "ProofPack",
]
