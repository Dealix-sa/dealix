"""Proof logger — records what the engine actually did internally.

Only records internal, verifiable events. Never fabricates external outcomes
(replies, payments, deliveries) — those come from the evidence chain and require
real human-confirmed events.
"""

from __future__ import annotations

from .schemas import Action, ProofEvent


def build_proof_log(actions: list[Action]) -> list[ProofEvent]:
    events: list[ProofEvent] = []
    for action in actions:
        if action.status == "executed_internal":
            events.append(
                ProofEvent(
                    strategy=action.strategy,
                    event="internal_action_executed",
                    detail=action.title,
                    artifact=action.artifact,
                )
            )
        elif action.status == "queued_for_approval":
            events.append(
                ProofEvent(
                    strategy=action.strategy,
                    event="draft_queued_for_approval",
                    detail=action.title,
                )
            )
        elif action.status == "blocked":
            events.append(
                ProofEvent(
                    strategy=action.strategy,
                    event="live_action_blocked",
                    detail=action.title,
                )
            )
    return events
