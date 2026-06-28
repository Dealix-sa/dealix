"""Proof Pack — assemble a truthful, non-fabricated evidence summary.

The proof pack documents *what the system actually produced* in a run:
counts, send-readiness, decision queue size and the active safety posture.
It never invents clients, testimonials, ROI figures or case studies.
"""

from __future__ import annotations

from typing import Any

from app.commercial.safety import safe_defaults


def build_proof_pack(
    *,
    accounts: list[Any],
    cards: list[Any],
    replies: list[Any],
    booking_options: list[Any],
    proposals: list[Any],
    followups: list[Any],
    decisions_required: list[Any],
) -> dict[str, Any]:
    """Return a factual proof-pack dict for the command room."""
    return {
        "kind": "commercial_growth_os_proof_pack",
        "claims_policy": "factual_only_no_fabrication",
        "produced": {
            "accounts": len(accounts),
            "growth_cards": len(cards),
            "replies_classified": len(replies),
            "booking_options": len(booking_options),
            "proposal_briefs": len(proposals),
            "followup_tasks": len(followups),
            "decisions_required": len(decisions_required),
        },
        "safety_posture": safe_defaults(),
        "guarantees": "none — Dealix does not promise guaranteed revenue or ROI",
        "evidence_basis": "counts derived directly from this run's artefacts",
    }
