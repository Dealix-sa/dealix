"""خادم Hermes — Sovereignty evaluator (Sami's check).

Spec §38 (L0–L6 permissions) + §39 (critical-risk triggers) collapse to a
five-level sovereignty ladder:

    S0_AUTONOMOUS     — agent executes immediately
    S1_NOTIFY_SAMI    — agent executes, Sami is notified
    S2_SAMI_APPROVAL  — agent waits for Sami approval
    S3_SAMI_ONLY      — only Sami may act
    S4_NEVER          — blocked entirely; needs board/regulatory path

The Sovereignty.evaluate(...) classmethod is the single entry point. It
takes a context dict + classification flags and returns a
SovereigntyVerdict explaining the required level, the human reasons, and
how many approvers are needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from typing import Any

from dealix.hermes.core.schemas import RiskLevel


class SovereigntyLevel(StrEnum):
    S0_AUTONOMOUS = "s0_autonomous"
    S1_NOTIFY_SAMI = "s1_notify_sami"
    S2_SAMI_APPROVAL = "s2_sami_approval"
    S3_SAMI_ONLY = "s3_sami_only"
    S4_NEVER = "s4_never"

    @property
    def numeric(self) -> int:
        return {
            "s0_autonomous": 0,
            "s1_notify_sami": 1,
            "s2_sami_approval": 2,
            "s3_sami_only": 3,
            "s4_never": 4,
        }[self.value]

    def at_least(self, other: SovereigntyLevel) -> bool:
        return self.numeric >= other.numeric


@dataclass(frozen=True)
class SovereigntyVerdict:
    """The Sovereignty evaluator's structured output."""

    level: SovereigntyLevel
    reasons: list[str] = field(default_factory=list)
    required_approvers: int = 0
    requires_evidence_pack: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level.value,
            "reasons": list(self.reasons),
            "required_approvers": self.required_approvers,
            "requires_evidence_pack": self.requires_evidence_pack,
        }


# ─────────────────────────────────────────────────────────────
# Trigger thresholds + tables
# ─────────────────────────────────────────────────────────────


# Spec §38 — how many approvers each sovereignty level demands.
_REQUIRED_APPROVERS: dict[SovereigntyLevel, int] = {
    SovereigntyLevel.S0_AUTONOMOUS: 0,
    SovereigntyLevel.S1_NOTIFY_SAMI: 0,
    SovereigntyLevel.S2_SAMI_APPROVAL: 1,
    SovereigntyLevel.S3_SAMI_ONLY: 1,
    SovereigntyLevel.S4_NEVER: 2,
}

# Critical-risk trigger keys (spec §39).
_CRITICAL_TRIGGERS: tuple[str, ...] = (
    "sensitive_data",
    "legal_commitment",
    "strategic_partnership",
    "public_api",
    "mcp_external",
    "financial_transfer",
)

# Monetary thresholds (SAR) routed via spec §39 "enterprise price" trigger.
_ENTERPRISE_PRICE_SAR: Decimal = Decimal("25000")
_BLOCKED_PRICE_SAR: Decimal = Decimal("250000")


# Sovereignty levels that demand an EvidencePack (§40).
_EVIDENCE_LEVELS: frozenset[SovereigntyLevel] = frozenset(
    {
        SovereigntyLevel.S2_SAMI_APPROVAL,
        SovereigntyLevel.S3_SAMI_ONLY,
        SovereigntyLevel.S4_NEVER,
    }
)


def requires_evidence_pack(level: SovereigntyLevel) -> bool:
    """Whether a SovereigntyLevel must be accompanied by an evidence pack."""
    return level in _EVIDENCE_LEVELS


def is_blocking(level: SovereigntyLevel) -> bool:
    """S4 blocks; anything else may eventually proceed."""
    return level == SovereigntyLevel.S4_NEVER


# ─────────────────────────────────────────────────────────────
# Evaluator
# ─────────────────────────────────────────────────────────────


def _coerce_money(value: Any) -> Decimal | None:
    if value is None:
        return None
    if hasattr(value, "amount"):
        try:
            return Decimal(str(value.amount))
        except Exception:  # pragma: no cover - defensive
            return None
    try:
        return Decimal(str(value))
    except Exception:  # pragma: no cover - defensive
        return None


def _max_level(*levels: SovereigntyLevel) -> SovereigntyLevel:
    return max(levels, key=lambda lvl: lvl.numeric)


class Sovereignty:
    """Static evaluator — call `Sovereignty.evaluate(ctx)`."""

    @classmethod
    def evaluate(
        cls,
        *,
        risk_level: RiskLevel | str = RiskLevel.LOW,
        sensitivity: str = "internal",
        monetary_amount: Any = None,
        external_visibility: bool = False,
        entity_type: str = "internal",
        flags: dict[str, Any] | None = None,
    ) -> SovereigntyVerdict:
        """Evaluate the required sovereignty level for an action.

        Parameters mirror spec §39:
          * risk_level: LOW / MEDIUM / HIGH / CRITICAL
          * sensitivity: "public" / "internal" / "confidential" / "regulated"
          * monetary_amount: Money | numeric | None
          * external_visibility: action visible outside the company
          * entity_type: 'internal' / 'customer' / 'partner' / 'public' / 'regulator'
          * flags: optional dict for §39 critical-risk triggers
        """
        flags = dict(flags or {})
        reasons: list[str] = []
        level = SovereigntyLevel.S0_AUTONOMOUS

        risk = RiskLevel(risk_level) if isinstance(risk_level, str) else risk_level

        # 1) Risk-level baseline
        risk_map = {
            RiskLevel.LOW: SovereigntyLevel.S0_AUTONOMOUS,
            RiskLevel.MEDIUM: SovereigntyLevel.S1_NOTIFY_SAMI,
            RiskLevel.HIGH: SovereigntyLevel.S2_SAMI_APPROVAL,
            RiskLevel.CRITICAL: SovereigntyLevel.S3_SAMI_ONLY,
        }
        level = _max_level(level, risk_map[risk])
        reasons.append(f"baseline risk_level={risk.value} → {risk_map[risk].value}")

        # 2) Sensitivity adjustments
        sensitivity = sensitivity.lower().strip()
        if sensitivity in {"confidential", "commercial"}:
            level = _max_level(level, SovereigntyLevel.S2_SAMI_APPROVAL)
            reasons.append("confidential data → S2 minimum")
        if sensitivity in {"regulated", "personal", "pdpl"}:
            level = _max_level(level, SovereigntyLevel.S3_SAMI_ONLY)
            reasons.append("regulated/personal data → S3 minimum")

        # 3) Monetary triggers
        amount = _coerce_money(monetary_amount)
        if amount is not None:
            if amount >= _BLOCKED_PRICE_SAR:
                level = _max_level(level, SovereigntyLevel.S4_NEVER)
                reasons.append(f"amount {amount} >= blocked threshold {_BLOCKED_PRICE_SAR}")
            elif amount >= _ENTERPRISE_PRICE_SAR:
                level = _max_level(level, SovereigntyLevel.S2_SAMI_APPROVAL)
                reasons.append(f"enterprise price {amount} >= {_ENTERPRISE_PRICE_SAR}")

        # 4) External visibility lift
        if external_visibility and level.numeric < SovereigntyLevel.S2_SAMI_APPROVAL.numeric:
            level = _max_level(level, SovereigntyLevel.S2_SAMI_APPROVAL)
            reasons.append("external visibility → S2 minimum")

        # 5) Entity type
        if entity_type == "regulator":
            level = _max_level(level, SovereigntyLevel.S3_SAMI_ONLY)
            reasons.append("regulator-facing entity → S3 minimum")
        if entity_type == "public":
            level = _max_level(level, SovereigntyLevel.S2_SAMI_APPROVAL)
            reasons.append("public-facing entity → S2 minimum")

        # 6) §39 critical-risk triggers
        for trigger in _CRITICAL_TRIGGERS:
            if flags.get(trigger):
                level = _max_level(level, SovereigntyLevel.S3_SAMI_ONLY)
                reasons.append(f"critical trigger '{trigger}' fired")

        # 7) Explicit kill switches
        if flags.get("forbidden"):
            level = SovereigntyLevel.S4_NEVER
            reasons.append("explicit forbidden flag set → S4 NEVER")
        if flags.get("strategic_partnership"):
            level = _max_level(level, SovereigntyLevel.S2_SAMI_APPROVAL)
            reasons.append("strategic partnership flag → S2 minimum")

        approvers = _REQUIRED_APPROVERS[level]
        return SovereigntyVerdict(
            level=level,
            reasons=reasons,
            required_approvers=approvers,
            requires_evidence_pack=requires_evidence_pack(level),
        )


__all__ = [
    "Sovereignty",
    "SovereigntyLevel",
    "SovereigntyVerdict",
    "is_blocking",
    "requires_evidence_pack",
]
