"""Trust guardrails — block overclaim, runaway pricing, unverified
partnerships and other foot-guns before any external commitment ships.

Every external-facing artifact (proposal, outreach message, partner
announcement) MUST pass these checks. The check is pure-functional and
deterministic, so it doubles as a test fixture.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.core.schemas import TrustCheckOutcome, TrustCheckResult
from dealix.hermes.sovereignty import (
    SOVEREIGN_ONLY_ACTIONS,
    SovereigntyLevel,
)
from dealix.hermes.sovereignty import (
    evaluate as evaluate_sovereignty,
)

# Phrases that strongly suggest overclaim. Conservative: short and
# unambiguous Arabic/English markers only.
OVERCLAIM_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(guaranteed|guarantee)\b", re.IGNORECASE),
    re.compile(r"\b100%\s*roi\b", re.IGNORECASE),
    re.compile(r"\bzero\s+risk\b", re.IGNORECASE),
    re.compile(r"\bcertified\s+by\b", re.IGNORECASE),
    re.compile(r"\bgovernment\s+backed\b", re.IGNORECASE),
    re.compile(r"مضمون\s*(?:النتائج|100%|تمامًا)?", re.IGNORECASE),
    re.compile(r"بدون\s+(?:مخاطر|مخاطره)", re.IGNORECASE),
    re.compile(r"معتمد\s+من\s+(?:الحكومة|الوزارة)", re.IGNORECASE),
)

UNVERIFIED_PARTNER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"official\s+partner\s+of", re.IGNORECASE),
    re.compile(r"شريك\s+(?:رسمي|معتمد)\s+(?:ل|مع)", re.IGNORECASE),
)

# Pricing floor for any external SAR proposal. Below this we escalate
# so the founder confirms intent.
PRICING_FLOOR_SAR = 499.0
PRICING_CEILING_AUTONOMOUS_SAR = 5_000.0


@dataclass
class TrustContext:
    """Inputs to the trust check.

    Either provide a free-text `text` blob or a structured `payload`
    (proposal/message). Whatever you pass we will inspect.
    """

    target_id: str
    target_kind: str
    text: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    action: str | None = None
    verified_partners: list[str] = field(default_factory=list)


def _scan_overclaim(text: str) -> list[str]:
    return [
        f"overclaim_pattern:{pat.pattern}"
        for pat in OVERCLAIM_PATTERNS
        if pat.search(text)
    ]


def _scan_unverified_partner(text: str, verified: list[str]) -> list[str]:
    hits = [pat.pattern for pat in UNVERIFIED_PARTNER_PATTERNS if pat.search(text)]
    if not hits:
        return []
    # If verified partners are explicitly named in the same blob we let it pass.
    if verified and any(name.lower() in text.lower() for name in verified):
        return []
    return [f"unverified_partner_claim:{h}" for h in hits]


def _scan_pricing(payload: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    price = payload.get("price_sar") or payload.get("estimated_value_sar")
    if price is None:
        return violations
    try:
        price_f = float(price)
    except (TypeError, ValueError):
        return [f"pricing_invalid:{price!r}"]
    if price_f <= 0:
        violations.append(f"pricing_non_positive:{price_f}")
    elif price_f < PRICING_FLOOR_SAR:
        violations.append(f"pricing_below_floor:{price_f}<{PRICING_FLOOR_SAR}")
    elif price_f > PRICING_CEILING_AUTONOMOUS_SAR:
        violations.append(
            f"pricing_above_autonomous_ceiling:{price_f}>{PRICING_CEILING_AUTONOMOUS_SAR}"
        )
    return violations


def _scan_external_commitment(action: str | None) -> list[str]:
    if not action:
        return []
    if action in SOVEREIGN_ONLY_ACTIONS:
        return [f"sovereign_only_action:{action}"]
    decision = evaluate_sovereignty(
        action, agent_max_level=SovereigntyLevel.L2_INTERNAL_TASK
    )
    if decision.is_blocked and decision.level >= SovereigntyLevel.L4_EXTERNAL_APPROVAL:
        return [f"requires_approval:{action}"]
    return []


def trust_check(ctx: TrustContext) -> TrustCheckResult:
    """Run all guardrails. Returns a `TrustCheckResult`.

    The result is `DENY` for unambiguous violations (overclaim, sovereign
    action, invalid price); `ESCALATE` when the action only needs founder
    approval; `ALLOW` otherwise.
    """
    text = ctx.text or _stringify_payload(ctx.payload)
    violations: list[str] = []
    violations += _scan_overclaim(text)
    violations += _scan_unverified_partner(text, ctx.verified_partners)
    violations += _scan_pricing(ctx.payload)
    violations += _scan_external_commitment(ctx.action)

    outcome = TrustCheckOutcome.ALLOW
    if any(
        v.startswith(("overclaim_pattern", "unverified_partner_claim", "pricing_"))
        for v in violations
    ):
        outcome = TrustCheckOutcome.DENY
    elif any(
        v.startswith(("sovereign_only_action", "requires_approval"))
        for v in violations
    ):
        outcome = TrustCheckOutcome.ESCALATE

    return TrustCheckResult(
        target_id=ctx.target_id,
        target_kind=ctx.target_kind,  # type: ignore[arg-type]
        outcome=outcome,
        violations=violations,
        notes=None if violations else "clean",
    )


def _stringify_payload(payload: dict[str, Any]) -> str:
    """Flatten a payload to a searchable text blob."""
    parts: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, str):
            parts.append(node)
        elif isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, (list, tuple)):
            for v in node:
                walk(v)

    walk(payload)
    return "\n".join(parts)
