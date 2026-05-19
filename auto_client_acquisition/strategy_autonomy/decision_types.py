"""Strategic decision taxonomy — CEO/board-tier decision categories.

A small, code-backed enum that bridges the operational
``intelligence_compounding_os.CompoundingDecision`` taxonomy to the
strategic autonomy layer. Decisions classified as :data:`IRREVERSIBLE`
are never auto-executed — they always route to the founder approval
queue.
"""

from __future__ import annotations

from enum import StrEnum

from auto_client_acquisition.intelligence_compounding_os import CompoundingDecision


class StrategicDecisionType(StrEnum):
    """CEO/board-tier strategic decision categories."""

    SCALE = "scale"
    BUILD = "build"
    KILL = "kill"
    HOLD = "hold"
    RAISE_PRICE = "raise_price"
    OFFER_RETAINER = "offer_retainer"
    HIRE = "hire"
    CREATE_BUSINESS_UNIT = "create_business_unit"
    CREATE_VENTURE_CANDIDATE = "create_venture_candidate"


# Decisions that are commercially or organizationally irreversible. These
# are RECOMMENDED autonomously but NEVER auto-executed — they always sit
# behind a founder approval gate.
IRREVERSIBLE: frozenset[StrategicDecisionType] = frozenset(
    {
        StrategicDecisionType.KILL,
        StrategicDecisionType.HIRE,
        StrategicDecisionType.RAISE_PRICE,
        StrategicDecisionType.CREATE_BUSINESS_UNIT,
        StrategicDecisionType.CREATE_VENTURE_CANDIDATE,
    }
)


def is_irreversible(decision_type: StrategicDecisionType | str) -> bool:
    """Return True if ``decision_type`` is an irreversible strategic move."""
    if isinstance(decision_type, str) and not isinstance(
        decision_type, StrategicDecisionType
    ):
        try:
            decision_type = StrategicDecisionType(decision_type)
        except ValueError:
            return False
    return decision_type in IRREVERSIBLE


# Mapping from the operational compounding taxonomy to the strategic one.
_COMPOUNDING_MAP: dict[str, StrategicDecisionType] = {
    CompoundingDecision.SCALE.value: StrategicDecisionType.SCALE,
    CompoundingDecision.BUILD.value: StrategicDecisionType.BUILD,
    CompoundingDecision.PILOT.value: StrategicDecisionType.HOLD,
    CompoundingDecision.HOLD.value: StrategicDecisionType.HOLD,
    CompoundingDecision.KILL.value: StrategicDecisionType.KILL,
    CompoundingDecision.RAISE_PRICE.value: StrategicDecisionType.RAISE_PRICE,
    CompoundingDecision.OFFER_RETAINER.value: StrategicDecisionType.OFFER_RETAINER,
    CompoundingDecision.CREATE_PLAYBOOK.value: StrategicDecisionType.BUILD,
    CompoundingDecision.CREATE_BENCHMARK.value: StrategicDecisionType.BUILD,
    CompoundingDecision.CREATE_BUSINESS_UNIT.value: (
        StrategicDecisionType.CREATE_BUSINESS_UNIT
    ),
    CompoundingDecision.CREATE_VENTURE_CANDIDATE.value: (
        StrategicDecisionType.CREATE_VENTURE_CANDIDATE
    ),
}


def from_compounding(
    decision: CompoundingDecision | str | None,
) -> StrategicDecisionType:
    """Bridge a :class:`CompoundingDecision` to a :class:`StrategicDecisionType`.

    Unknown or missing inputs collapse to the safe ``HOLD`` decision.
    """
    if decision is None:
        return StrategicDecisionType.HOLD
    value = decision.value if isinstance(decision, CompoundingDecision) else str(decision)
    return _COMPOUNDING_MAP.get(value, StrategicDecisionType.HOLD)


__all__ = [
    "IRREVERSIBLE",
    "StrategicDecisionType",
    "from_compounding",
    "is_irreversible",
]
