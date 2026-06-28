"""Dealix Commercial Growth OS v2.

A connected, safe-by-default commercial operating system: lead sourcing,
ICP scoring, account qualification, Growth Cards, smart-reply / negotiation
desk, booking desk, proposal factory, follow-up engine, pipeline, delivery
handoff, proof pack and a command-room snapshot.

Doctrine: draft-only by default. No external send, no calendar write and no
binding proposal price without explicit, recorded approval. See
:mod:`app.commercial.safety`.
"""

from __future__ import annotations

from app.commercial import (
    booking_desk,
    command_snapshot,
    delivery_handoff,
    followup_engine,
    growth_cards,
    icp_scoring,
    lead_sourcing,
    negotiation_desk,
    pipeline,
    proof_pack,
    proposal_factory,
    reply_classifier,
    safety,
    schemas,
)

__all__ = [
    "booking_desk",
    "command_snapshot",
    "delivery_handoff",
    "followup_engine",
    "growth_cards",
    "icp_scoring",
    "lead_sourcing",
    "negotiation_desk",
    "pipeline",
    "proof_pack",
    "proposal_factory",
    "reply_classifier",
    "safety",
    "schemas",
]

__version__ = "2.0.0"
