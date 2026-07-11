"""Transparent strategy metrics from proof records.

This module does not mutate strategy definitions or priorities. It produces
inspectable evidence for a later human-reviewed change.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class StrategyMetrics:
    strategy_id: str
    internal_executed: int
    drafts_prepared: int
    approvals_requested: int
    approved: int
    rejected: int
    blocked: int
    outcomes_recorded: int
    approval_rate: float | None
    block_rate: float | None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.approval_rate is not None:
            payload["approval_rate"] = round(self.approval_rate, 4)
        if self.block_rate is not None:
            payload["block_rate"] = round(self.block_rate, 4)
        return payload


def compute_strategy_metrics(records: Iterable[dict[str, Any]]) -> tuple[StrategyMetrics, ...]:
    counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "internal_executed": 0,
            "drafts_prepared": 0,
            "approvals_requested": 0,
            "approved": 0,
            "rejected": 0,
            "blocked": 0,
            "outcomes_recorded": 0,
        }
    )
    for record in records:
        if not isinstance(record, dict):
            continue
        event_type = str(record.get("event_type") or "").strip().casefold()
        payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
        strategy_id = str(payload.get("strategy_id") or record.get("strategy_id") or "_unknown").strip().casefold()
        bucket = counts[strategy_id or "_unknown"]
        if event_type == "internal_executed":
            bucket["internal_executed"] += 1
        elif event_type in {"action_drafted", "draft_prepared"}:
            bucket["drafts_prepared"] += 1
        elif event_type == "approval_requested":
            bucket["approvals_requested"] += 1
        elif event_type == "approval_decided":
            decision = payload.get("approved")
            if decision is True:
                bucket["approved"] += 1
            elif decision is False:
                bucket["rejected"] += 1
        elif event_type in {"step_blocked", "action_blocked"}:
            bucket["blocked"] += 1
        elif event_type in {"outcome_recorded", "commercial_outcome"}:
            bucket["outcomes_recorded"] += 1

    metrics = []
    for strategy_id, bucket in sorted(counts.items()):
        decided = bucket["approved"] + bucket["rejected"]
        routed = bucket["internal_executed"] + bucket["drafts_prepared"] + bucket["approvals_requested"] + bucket["blocked"]
        metrics.append(
            StrategyMetrics(
                strategy_id=strategy_id,
                **bucket,
                approval_rate=(bucket["approved"] / decided) if decided else None,
                block_rate=(bucket["blocked"] / routed) if routed else None,
            )
        )
    return tuple(metrics)


def learning_summary(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    strategies = compute_strategy_metrics(records)
    return {
        "strategies": [item.to_dict() for item in strategies],
        "totals": {
            "strategies_seen": len(strategies),
            "internal_executed": sum(item.internal_executed for item in strategies),
            "drafts_prepared": sum(item.drafts_prepared for item in strategies),
            "approvals_requested": sum(item.approvals_requested for item in strategies),
            "blocked": sum(item.blocked for item in strategies),
            "outcomes_recorded": sum(item.outcomes_recorded for item in strategies),
        },
        "automatic_strategy_mutation": False,
        "requires_human_review_for_policy_change": True,
    }
