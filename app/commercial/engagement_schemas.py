"""Data models for the *living* engagement layer of the Commercial Growth OS.

These extend the static artefacts in :mod:`app.commercial.schemas` with the
stateful, multi-turn, multi-channel objects the system needs in order to
*think, converse, persuade, negotiate and reply* across WhatsApp, email and
LinkedIn — while staying draft-only and fail-closed.

Nothing here sends anything. Outbound objects are *prepared payloads* that a
gated sender (see :mod:`app.commercial.channels`) may transmit only once every
safety condition in :mod:`app.commercial.safety` passes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

# ── Conversation stages (the engine's state machine) ───────────────────────────

CONVERSATION_STAGES = (
    "opener",          # first touch prepared
    "qualifying",      # discovering fit / need
    "value",           # framing value to the pain
    "objection",       # handling a concern
    "negotiation",     # guardrailed scope/price-range talk
    "booking",         # proposing meeting options
    "proposal",        # proposal brief shared
    "closing",         # moving to decision
    "won",             # deal agreed (approval-gated)
    "lost",            # closed lost (approval-gated)
    "nurture",         # long-term hold
    "opted_out",       # contact asked to stop — terminal
)

# Directions for a conversation turn.
DIRECTIONS = ("inbound", "outbound")

# Outbound payload kinds.
PAYLOAD_KINDS = ("text", "interactive_buttons", "email", "linkedin_manual", "phone_task")


def _d(obj: Any) -> Any:
    return asdict(obj)


@dataclass
class InteractiveButton:
    """A single WhatsApp-style interactive reply button.

    WhatsApp limits: max 3 buttons per message, title <= 20 chars. The channel
    layer enforces these; this model just carries the data.
    """

    id: str
    title: str
    intent: str = ""  # maps a press back to a conversation intent

    def to_dict(self) -> dict[str, Any]:
        return _d(self)


@dataclass
class ConversationTurn:
    turn_id: str
    direction: str  # inbound | outbound
    channel: str
    text: str = ""
    buttons: list[dict[str, Any]] = field(default_factory=list)
    intent: str = ""
    stage_before: str = ""
    stage_after: str = ""
    is_draft: bool = True
    reasoning: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _d(self)


@dataclass
class Conversation:
    conversation_id: str
    account_id: str
    motion: str
    channel: str
    stage: str = "opener"
    status: str = "active"  # active | paused | won | lost | opted_out
    turns: list[dict[str, Any]] = field(default_factory=list)
    opt_in: bool = False
    opted_out: bool = False
    last_intent: str = ""
    owner_decision: str = "pending"  # pending | approved | hold | discard
    next_action: str = ""
    risk_level: str = "low"

    def to_dict(self) -> dict[str, Any]:
        return _d(self)


@dataclass
class OutboundPayload:
    """An exact, ready-to-send payload — but never sent here."""

    payload_id: str
    conversation_id: str
    account_id: str
    channel: str
    kind: str  # PAYLOAD_KINDS
    subject: str = ""               # email only
    body_ar: str = ""
    body_en: str = ""
    buttons: list[dict[str, Any]] = field(default_factory=list)
    headers: dict[str, str] = field(default_factory=dict)  # e.g. List-Unsubscribe
    to_ref: str = "redacted"        # never store raw PII in the report
    requires_approval: bool = True
    send_status: str = "draft"      # draft | approved | blocked | sent
    safety: dict[str, Any] = field(default_factory=dict)  # SafetyDecision.to_dict()
    manual_instructions: str = ""   # for linkedin_manual / phone_task

    def to_dict(self) -> dict[str, Any]:
        return _d(self)


@dataclass
class PersuasionStrategy:
    angle: str
    message_points: list[str] = field(default_factory=list)
    proof_points: list[str] = field(default_factory=list)  # truthful-only
    avoid: list[str] = field(default_factory=list)
    cta: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _d(self)


@dataclass
class ActionRecommendation:
    """The brain's decision for an account/conversation: what to do next & why."""

    ref_id: str                 # conversation_id or account_id
    account_id: str
    recommended_action: str     # e.g. send_opener | handle_objection | propose_booking
    motion: str
    channel: str
    rationale: list[str] = field(default_factory=list)
    confidence: float = 0.0     # 0..1
    priority: int = 3           # 1 (highest) .. 5
    persuasion_angle: str = ""
    next_stage: str = ""
    risk_level: str = "low"
    requires_approval: bool = True
    source: str = "heuristic"   # heuristic | llm

    def to_dict(self) -> dict[str, Any]:
        return _d(self)


@dataclass
class EmailThread:
    thread_id: str
    account_id: str
    subject: str = ""
    messages: list[dict[str, Any]] = field(default_factory=list)
    stage: str = "opener"
    status: str = "active"

    def to_dict(self) -> dict[str, Any]:
        return _d(self)
