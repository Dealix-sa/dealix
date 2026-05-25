"""A/B message variant ledger with verified-revenue attribution."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

_VARIANTS: dict[str, "MessageVariant"] = {}
_OUTCOMES: list["VariantOutcome"] = []


@dataclass(frozen=True)
class MessageVariant:
    variant_id: str
    campaign_id: str
    label: str
    body: str
    created_at: float = 0.0


@dataclass(frozen=True)
class VariantOutcome:
    variant_id: str
    verified_revenue_sar: float
    evidence_pack_id: str
    notes: str = ""
    recorded_at: float = 0.0
    metadata: dict[str, str] = field(default_factory=dict)


def register_variant(campaign_id: str, label: str, body: str) -> MessageVariant:
    """Register a message variant for an A/B test."""
    v = MessageVariant(
        variant_id=f"var_{uuid.uuid4().hex[:8]}",
        campaign_id=campaign_id,
        label=label,
        body=body,
        created_at=time.time(),
    )
    _VARIANTS[v.variant_id] = v
    return v


def record_outcome(variant_id: str, verified_revenue_sar: float, evidence_pack_id: str, notes: str = "") -> VariantOutcome:
    """Record verified revenue attached to a variant (evidence_pack_id required)."""
    if not evidence_pack_id:
        raise ValueError("evidence_pack_id is required to record an outcome")
    if variant_id not in _VARIANTS:
        raise KeyError(f"unknown variant {variant_id}")
    out = VariantOutcome(
        variant_id=variant_id,
        verified_revenue_sar=float(verified_revenue_sar),
        evidence_pack_id=evidence_pack_id,
        notes=notes,
        recorded_at=time.time(),
    )
    _OUTCOMES.append(out)
    return out


def attribution_for(variant_id: str) -> float:
    """Return total verified revenue attributed to a variant."""
    return sum(o.verified_revenue_sar for o in _OUTCOMES if o.variant_id == variant_id)


def reset() -> None:
    """Clear variants and outcomes (test helper)."""
    _VARIANTS.clear()
    _OUTCOMES.clear()
