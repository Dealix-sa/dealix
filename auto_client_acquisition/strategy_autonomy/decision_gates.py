"""Strategic gate evaluator — snapshot into CEO-tier decisions.

Applies each :class:`GateRule` to a :class:`StrategicSignalSnapshot`,
skipping gates that are not yet due. Each gate decision is cross-checked
against the existing strategy decision score and the board decision
scorers — when the gate decision and the scorer hint disagree on a
non-HOLD move, the result is downgraded to HOLD with a warning. The
doctrine non-negotiables are enforced before any decision is finalized.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from auto_client_acquisition.board_decision_os.decision_engine import (
    offer_scorecard_strategic_decision,
)
from auto_client_acquisition.intelligence_os.strategy_decision import (
    compute_strategy_decision_score,
    strategy_decision_band,
)
from auto_client_acquisition.safe_send_gateway import (
    enforce_doctrine_non_negotiables,
)
from auto_client_acquisition.strategy_autonomy.decision_types import (
    StrategicDecisionType,
    from_compounding,
)
from auto_client_acquisition.strategy_autonomy.gate_catalog import (
    STRATEGIC_GATE_CATALOG,
    GateRule,
)
from auto_client_acquisition.strategy_autonomy.signal_aggregator import (
    StrategicSignalSnapshot,
)

_HOLD = StrategicDecisionType.HOLD.value

# Decision types the strategy/board scorers can natively express. A gate
# whose decision falls in this set is cross-checked against the scorer
# hint and downgraded to HOLD on conflict. Gates whose decision the
# scorers cannot express (HIRE / CREATE_BUSINESS_UNIT / CREATE_VENTURE_
# CANDIDATE) are not downgraded on a vocabulary mismatch — they remain
# valid recommendations but stay approval-gated when irreversible.
_SCORER_EXPRESSIBLE: frozenset[str] = frozenset(
    {
        StrategicDecisionType.SCALE.value,
        StrategicDecisionType.BUILD.value,
        StrategicDecisionType.KILL.value,
        StrategicDecisionType.HOLD.value,
        StrategicDecisionType.RAISE_PRICE.value,
        StrategicDecisionType.OFFER_RETAINER.value,
    }
)


@dataclass(frozen=True, slots=True)
class GateEvaluation:
    """The outcome of evaluating one strategic gate."""

    gate_id: str
    source: str
    title_ar: str
    title_en: str
    due: bool
    passed: bool
    metric: str
    metric_value: float
    comparator: str
    threshold: float
    decision_type: str
    scorer_hint: str
    conflict: bool
    score: float
    decision_band: str
    severity: str
    evidence: tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = list(self.evidence)
        return data


def _compare(value: float, comparator: str, threshold: float) -> bool:
    if comparator == "gte":
        return value >= threshold
    if comparator == "lte":
        return value <= threshold
    if comparator == "eq":
        return value == threshold
    return False


def _metric_value(snapshot: StrategicSignalSnapshot, metric: str) -> float:
    raw = getattr(snapshot, metric, None)
    if raw is None:
        return 0.0
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.0


def _scorer_hint(snapshot: StrategicSignalSnapshot) -> tuple[str, float, str]:
    """Return (scorer decision_type, composite score, band) for cross-check."""
    inputs = snapshot.as_strategy_inputs()
    score = compute_strategy_decision_score(inputs)
    band = strategy_decision_band(score)
    governance_safe = snapshot.governance_risk_index <= 50.0
    offer_hint = offer_scorecard_strategic_decision(
        int(round(score)), governance_safe=governance_safe
    )
    hint_type = from_compounding(offer_hint)
    # The band itself is the primary scorer hint; fall back to the offer
    # scorecard hint when the band is ambiguous.
    band_type = from_compounding(band.value)
    if band_type == StrategicDecisionType.HOLD:
        return hint_type.value, score, band.value
    return band_type.value, score, band.value


def evaluate_strategic_gates(
    snapshot: StrategicSignalSnapshot,
) -> list[GateEvaluation]:
    """Evaluate every catalog gate against ``snapshot``.

    Gates whose ``window_day`` exceeds ``snapshot.days_since_launch`` are
    marked not-due and skipped. Each due gate is cross-checked against the
    strategy decision scorers; a non-HOLD gate decision that disagrees
    with the scorer hint is downgraded to HOLD. Doctrine non-negotiables
    are enforced before any non-HOLD decision is finalized.
    """
    scorer_decision, score, band = _scorer_hint(snapshot)
    results: list[GateEvaluation] = []

    for gate in STRATEGIC_GATE_CATALOG:
        results.append(_evaluate_one(gate, snapshot, scorer_decision, score, band))
    return results


def _evaluate_one(
    gate: GateRule,
    snapshot: StrategicSignalSnapshot,
    scorer_decision: str,
    score: float,
    band: str,
) -> GateEvaluation:
    due = gate.window_day is None or snapshot.days_since_launch >= gate.window_day
    metric_value = _metric_value(snapshot, gate.metric)

    if not due:
        return GateEvaluation(
            gate_id=gate.gate_id,
            source=gate.source,
            title_ar=gate.title_ar,
            title_en=gate.title_en,
            due=False,
            passed=False,
            metric=gate.metric,
            metric_value=metric_value,
            comparator=gate.comparator,
            threshold=gate.threshold,
            decision_type=_HOLD,
            scorer_hint=scorer_decision,
            conflict=False,
            score=round(score, 1),
            decision_band=band,
            severity=gate.severity,
            evidence=(),
            notes=(
                f"gate not yet due: day {snapshot.days_since_launch} "
                f"< window {gate.window_day}"
            ),
        )

    passed = _compare(metric_value, gate.comparator, gate.threshold)
    raw_decision = gate.on_pass if passed else gate.on_fail

    evidence = (
        f"{gate.gate_id}: {gate.metric}={metric_value} "
        f"{gate.comparator} {gate.threshold} -> {'pass' if passed else 'fail'}",
        f"strategy_decision_score={round(score, 1)} band={band}",
        f"source={gate.source}",
    )

    # Cross-check: a non-HOLD decision the scorers can express must agree
    # with the scorer hint, else it is downgraded to HOLD. Decisions the
    # scorers cannot express (e.g. HIRE) are not downgraded on a
    # vocabulary mismatch — they stand and stay approval-gated.
    conflict = False
    decision = raw_decision
    notes = ""
    if (
        raw_decision != _HOLD
        and raw_decision in _SCORER_EXPRESSIBLE
        and raw_decision != scorer_decision
    ):
        conflict = True
        decision = _HOLD
        notes = (
            f"downgraded to hold: gate decision '{raw_decision}' "
            f"conflicts with scorer hint '{scorer_decision}'"
        )
    elif raw_decision != _HOLD and raw_decision not in _SCORER_EXPRESSIBLE:
        notes = (
            f"scorer cannot express '{raw_decision}'; gate stands "
            f"as an approval-gated recommendation"
        )

    # Hard gate: enforce doctrine non-negotiables before finalizing a
    # non-HOLD recommendation. Any violation collapses to HOLD.
    if decision != _HOLD:
        try:
            enforce_doctrine_non_negotiables()
        except ValueError as exc:  # noqa: BLE001
            decision = _HOLD
            conflict = True
            notes = f"doctrine block: {exc}"

    return GateEvaluation(
        gate_id=gate.gate_id,
        source=gate.source,
        title_ar=gate.title_ar,
        title_en=gate.title_en,
        due=True,
        passed=passed,
        metric=gate.metric,
        metric_value=metric_value,
        comparator=gate.comparator,
        threshold=gate.threshold,
        decision_type=decision,
        scorer_hint=scorer_decision,
        conflict=conflict,
        score=round(score, 1),
        decision_band=band,
        severity=gate.severity,
        evidence=evidence,
        notes=notes,
    )


__all__ = ["GateEvaluation", "evaluate_strategic_gates"]
