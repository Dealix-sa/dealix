"""Strategy registry for Dealix autonomous growth execution."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Strategy:
    name: str
    goal: str
    priority: int
    target_customer: str
    allowed_actions: list[str] = field(default_factory=list)
    blocked_actions: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    kpis: list[str] = field(default_factory=list)
    approval_required_for: list[str] = field(default_factory=list)
    proof_required: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_STRATEGIES: tuple[Strategy, ...] = (
    Strategy(
        name="technical_trust",
        goal="Keep GitHub, CI, Railway, smoke tests, and production trust stable before scaling growth.",
        priority=100,
        target_customer="Founder / production operations",
        allowed_actions=["read_context", "generate_report", "write_action_queue", "write_proof_log"],
        blocked_actions=["merge_pr", "change_production"],
        outputs=["technical blocker summary", "PR priority list", "safe fix prompt"],
        kpis=["critical blockers count", "green checks count", "deploy health"],
        approval_required_for=["merge PR", "production deploy", "Railway config change"],
        proof_required=["workflow run", "healthcheck", "PR status"],
    ),
    Strategy(
        name="saudi_market_access",
        goal="Build Saudi Opportunity Graph entries and identify market-entry targets for foreign and local companies.",
        priority=95,
        target_customer="Foreign B2B companies and Saudi growth operators",
        allowed_actions=["score_targets", "draft_outreach", "generate_report", "write_approval_queue"],
        blocked_actions=["cold_whatsapp", "scrape_linkedin"],
        outputs=["top targets", "draft messages", "market access notes"],
        kpis=["targets scored", "hot targets", "drafts needing approval"],
        approval_required_for=["external outreach", "partner intro"],
        proof_required=["source URL", "score rationale"],
    ),
    Strategy(
        name="revenue_sprint",
        goal="Turn qualified interest into Snapshot, Sprint, and Retainer paths.",
        priority=90,
        target_customer="Saudi SMEs and inbound prospects",
        allowed_actions=["draft_outreach", "generate_report", "write_action_queue", "write_proof_log"],
        blocked_actions=["guaranteed_revenue", "live_payment"],
        outputs=["proposal draft", "follow-up queue", "proof-pack checklist"],
        kpis=["qualified leads", "proposals drafted", "proof items"],
        approval_required_for=["price quote", "payment link", "send proposal"],
        proof_required=["client pain", "owner present", "data available"],
    ),
    Strategy(
        name="content_factory",
        goal="Convert proof, market signals, and founder learnings into compliant content drafts.",
        priority=75,
        target_customer="Dealix audience and warm prospects",
        allowed_actions=["draft_content", "generate_report", "write_approval_queue"],
        blocked_actions=["auto_post", "fake_case_study"],
        outputs=["LinkedIn draft", "X thread draft", "newsletter idea", "short video script"],
        kpis=["drafts created", "proof-backed claims", "approval-ready content"],
        approval_required_for=["publish post", "use client name"],
        proof_required=["source artifact", "claim evidence"],
    ),
    Strategy(
        name="proof_pack",
        goal="Record what happened, what was drafted, what was approved, and what evidence supports the next step.",
        priority=85,
        target_customer="Founder and clients",
        allowed_actions=["write_proof_log", "generate_report", "write_learning_notes"],
        blocked_actions=["fake_proof"],
        outputs=["proof log", "weekly proof pack", "learning notes"],
        kpis=["evidence count", "approved actions", "next decisions"],
        approval_required_for=["client-facing proof pack"],
        proof_required=["source links", "dates", "decision log"],
    ),
)


def load_strategy_registry() -> list[Strategy]:
    """Return the built-in strategy registry.

    Future versions may load YAML from dealix/strategy_execution/strategies, but
    this built-in registry keeps the first implementation zero-dependency.
    """

    return sorted(DEFAULT_STRATEGIES, key=lambda item: item.priority, reverse=True)


def write_strategy_snapshot(path: Path) -> None:
    """Write a markdown snapshot of the strategy registry."""

    strategies = load_strategy_registry()
    lines = ["# Dealix Strategy Registry", ""]
    for strategy in strategies:
        lines.extend(
            [
                f"## {strategy.name}",
                "",
                f"- Goal: {strategy.goal}",
                f"- Priority: {strategy.priority}",
                f"- Target customer: {strategy.target_customer}",
                f"- Outputs: {', '.join(strategy.outputs)}",
                f"- KPIs: {', '.join(strategy.kpis)}",
                f"- Approval required for: {', '.join(strategy.approval_required_for)}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
