"""Typed data model for the Strategy Execution OS.

Stdlib-only. No network, no secrets, no external side effects.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class AutonomyLevel(enum.IntEnum):
    """How much the engine is allowed to do on its own."""

    OBSERVE = 0
    ANALYZE = 1
    DRAFT = 2
    INTERNAL_EXECUTION = 3
    REPO_EXECUTION = 4
    EXTERNAL_EXECUTION = 5  # BLOCKED — never runs live


# The engine will never enable external execution automatically.
MAX_ENABLED_AUTONOMY_LEVEL = AutonomyLevel.REPO_EXECUTION

# Actions the engine must never perform itself, regardless of level. These are
# only ever emitted as *drafts* / *approval items*.
FORBIDDEN_LIVE_ACTIONS = frozenset(
    {
        "send_whatsapp",
        "send_email",
        "send_sms",
        "publish_social",
        "post_linkedin",
        "post_x",
        "charge_customer",
        "issue_invoice_live",
        "change_production",
        "merge_pr",
        "scrape",
    }
)

# Required evidence-chain events (revenue is only real once payment_received).
EVIDENCE_CHAIN = (
    "lead_identified",
    "message_drafted",
    "human_approved",
    "message_sent_manually",
    "call_booked",
    "invoice_sent",
    "payment_received",
    "work_delivered",
    "proof_pack_delivered",
    "follow_up_scheduled",
)

REVENUE_RECOGNITION_EVENT = "payment_received"


@dataclass
class Strategy:
    """A loaded strategy definition (from a YAML file)."""

    name: str
    goal: str
    target_customer: str
    priority: int
    inputs: list[str] = field(default_factory=list)
    allowed_actions: list[str] = field(default_factory=list)
    blocked_actions: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    kpis: list[str] = field(default_factory=list)
    approval_required_for: list[str] = field(default_factory=list)
    stop_conditions: list[str] = field(default_factory=list)
    proof_required: list[str] = field(default_factory=list)
    learning_rule: str = ""
    safety_notes: str = ""
    max_autonomy_level: int = int(AutonomyLevel.INTERNAL_EXECUTION)
    source_file: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_file: str = "") -> "Strategy":
        return cls(
            name=str(data.get("name", "")).strip(),
            goal=str(data.get("goal", "")).strip(),
            target_customer=str(data.get("target_customer", "")).strip(),
            priority=int(data.get("priority", 100)),
            inputs=list(data.get("inputs", []) or []),
            allowed_actions=list(data.get("allowed_actions", []) or []),
            blocked_actions=list(data.get("blocked_actions", []) or []),
            steps=list(data.get("steps", []) or []),
            outputs=list(data.get("outputs", []) or []),
            kpis=list(data.get("kpis", []) or []),
            approval_required_for=list(data.get("approval_required_for", []) or []),
            stop_conditions=list(data.get("stop_conditions", []) or []),
            proof_required=list(data.get("proof_required", []) or []),
            learning_rule=str(data.get("learning_rule", "")).strip(),
            safety_notes=str(data.get("safety_notes", "")).strip(),
            max_autonomy_level=int(
                data.get("max_autonomy_level", int(AutonomyLevel.INTERNAL_EXECUTION))
            ),
            source_file=source_file,
        )


@dataclass
class Action:
    """A single planned unit of work for a strategy."""

    strategy: str
    title: str
    action_type: str
    autonomy_level: int
    requires_approval: bool
    status: str = "planned"  # planned | executed_internal | queued_for_approval | blocked
    detail: str = ""
    artifact: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy,
            "title": self.title,
            "action_type": self.action_type,
            "autonomy_level": self.autonomy_level,
            "requires_approval": self.requires_approval,
            "status": self.status,
            "detail": self.detail,
            "artifact": self.artifact,
        }


@dataclass
class ApprovalItem:
    """A draft that a human must review before anything leaves the building."""

    strategy: str
    title: str
    action_type: str
    reason: str
    draft: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy,
            "title": self.title,
            "action_type": self.action_type,
            "reason": self.reason,
            "draft": self.draft,
        }


@dataclass
class ProofEvent:
    """An immutable-ish record of something the engine actually did (internal)."""

    strategy: str
    event: str
    detail: str = ""
    artifact: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy,
            "event": self.event,
            "detail": self.detail,
            "artifact": self.artifact,
        }
