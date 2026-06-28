"""Dealix Commercial Growth OS v2.

A connected, safe-by-default commercial operating system: lead sourcing,
ICP scoring, account qualification, Growth Cards, smart-reply / negotiation
desk, booking desk, proposal factory, follow-up engine, pipeline, delivery
handoff, proof pack and a command-room snapshot.

The *living* engagement layer adds a reasoning brain, a multi-turn conversation
engine, a WhatsApp interactive button loop, an email desk, multi-channel
preparation (WhatsApp / email / LinkedIn / phone) and an engagement engine that
drives the next best action across channels.

Doctrine: draft-only by default. No external send, no calendar write and no
binding proposal price without explicit, recorded approval. See
:mod:`app.commercial.safety`.
"""

from __future__ import annotations

from app.commercial import (
    booking_desk,
    channels,
    command_snapshot,
    conversation,
    delivery_handoff,
    email_desk,
    engagement_engine,
    engagement_schemas,
    followup_engine,
    growth_cards,
    icp_scoring,
    lead_sourcing,
    negotiation_desk,
    persuasion,
    pipeline,
    proof_pack,
    proposal_factory,
    reasoning,
    reply_classifier,
    safety,
    schemas,
    whatsapp_loop,
)

__all__ = [
    "booking_desk",
    "channels",
    "command_snapshot",
    "conversation",
    "delivery_handoff",
    "email_desk",
    "engagement_engine",
    "engagement_schemas",
    "followup_engine",
    "growth_cards",
    "icp_scoring",
    "lead_sourcing",
    "negotiation_desk",
    "persuasion",
    "pipeline",
    "proof_pack",
    "proposal_factory",
    "reasoning",
    "reply_classifier",
    "safety",
    "schemas",
    "whatsapp_loop",
]

__version__ = "2.1.0"
