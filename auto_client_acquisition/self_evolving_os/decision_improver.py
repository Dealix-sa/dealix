"""Decision improver — derive shadow-mode improvement suggestions from feedback.

The improver reads the learning store, finds layer-level patterns, and
produces :class:`ImprovementSuggestion` records. Suggestions are advisory
only — they are NEVER applied automatically. They flow into the improvement
proposal queue (``ai_improvement_proposals``) and require explicit founder
approval to take effect.

Doctrine guarantee: this module does not import or call ``model_router``,
``agent_mesh``, or any production execution surface. The only side effect
is to write candidate proposals when given a writer. Tests assert this.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.self_evolving_os.feedback_ingestion import OutcomeKind
from auto_client_acquisition.self_evolving_os.learning_store import (
    InMemoryLearningStore,
    LayerOutcomeSummary,
)


@dataclass(frozen=True, slots=True)
class ImprovementSuggestion:
    """A shadow-mode suggestion derived from learning store statistics."""

    suggestion_id: str
    tenant_id: str
    target_layer: str
    title: str
    rationale: str
    severity: str  # "info" | "watch" | "act"
    proposed_change: Mapping[str, Any] = field(default_factory=dict)
    evidence_summary: Mapping[str, Any] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["proposed_change"] = dict(self.proposed_change)
        data["evidence_summary"] = dict(self.evidence_summary)
        return data


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _severity_for_layer(summary: LayerOutcomeSummary, *, threshold_doctrine: int) -> str:
    """Classify how loudly a layer is failing.

    * any doctrine violation → ``act`` (highest)
    * success rate < 30% with > 10 events → ``act``
    * success rate < 60% with > 5 events → ``watch``
    * else → ``info``
    """
    if summary.doctrine_violations >= threshold_doctrine and summary.doctrine_violations > 0:
        return "act"
    if summary.total > 10 and summary.success_rate() < 0.30:
        return "act"
    if summary.total > 5 and summary.success_rate() < 0.60:
        return "watch"
    return "info"


def _suggestion_from_summary(
    *,
    tenant_id: str,
    summary: LayerOutcomeSummary,
    severity: str,
) -> ImprovementSuggestion:
    """Render an explanatory suggestion from one layer summary."""
    success = summary.by_kind.get(OutcomeKind.SUCCESS.value, 0)
    confirmed = summary.by_kind.get(OutcomeKind.CUSTOMER_CONFIRMED.value, 0)
    rejected = summary.by_kind.get(OutcomeKind.CUSTOMER_REJECTED.value, 0)
    failures = summary.by_kind.get(OutcomeKind.FAILURE.value, 0)

    title = f"layer {summary.layer}: review routing/handler"
    rationale_parts: list[str] = [
        f"total={summary.total}",
        f"success={success}",
        f"customer_confirmed={confirmed}",
        f"customer_rejected={rejected}",
        f"failures={failures}",
        f"doctrine_violations={summary.doctrine_violations}",
        f"success_rate={summary.success_rate():.2%}",
    ]
    rationale = "; ".join(rationale_parts)

    proposed_change: dict[str, Any] = {
        "layer": summary.layer,
        "review_handler": True,
        "consider_fallback_provider": summary.success_rate() < 0.6,
        "add_human_review_gate": summary.doctrine_violations > 0,
    }

    evidence_summary = summary.to_dict()

    return ImprovementSuggestion(
        suggestion_id=f"sg_{uuid.uuid4().hex[:16]}",
        tenant_id=tenant_id,
        target_layer=summary.layer,
        title=title,
        rationale=rationale,
        severity=severity,
        proposed_change=proposed_change,
        evidence_summary=evidence_summary,
        created_at=_now_iso(),
    )


def derive_suggestions(
    *,
    tenant_id: str,
    store: InMemoryLearningStore | None = None,
    since_days: int | None = 30,
    threshold_doctrine: int = 1,
    minimum_severity: str = "info",
) -> list[ImprovementSuggestion]:
    """Read the learning store and emit a list of shadow-mode suggestions.

    ``minimum_severity`` filters which suggestions are returned:
        * ``info``: return all suggestions.
        * ``watch``: return only ``watch`` and ``act``.
        * ``act``: return only ``act``.
    """
    if store is None:
        from auto_client_acquisition.self_evolving_os.learning_store import get_default_store

        store = get_default_store()
    summaries = store.summarize_all_layers(tenant_id=tenant_id, since_days=since_days)
    severity_rank = {"info": 0, "watch": 1, "act": 2}
    min_rank = severity_rank.get(minimum_severity, 0)
    out: list[ImprovementSuggestion] = []
    for summary in summaries.values():
        if summary.total == 0:
            continue
        severity = _severity_for_layer(summary, threshold_doctrine=threshold_doctrine)
        if severity_rank[severity] < min_rank:
            continue
        out.append(
            _suggestion_from_summary(
                tenant_id=tenant_id,
                summary=summary,
                severity=severity,
            )
        )
    out.sort(key=lambda s: severity_rank.get(s.severity, 0), reverse=True)
    return out


# --- Shadow-mode safety guard -------------------------------------------------
#
# A doctrine-guarded sentinel that screams if anything in the codebase tries to
# call the improver in "apply" mode. The improver itself never applies; this
# constant exists so tests can assert nothing imports an "apply" path.

SELF_EVOLVING_SHADOW_ONLY: bool = True


class ShadowModeViolationError(RuntimeError):
    """Raised when caller attempts to apply a suggestion without approval."""


def assert_shadow_mode() -> None:
    """Guard: any code path that wants to mutate behavior MUST pass approval."""
    if not SELF_EVOLVING_SHADOW_ONLY:
        raise ShadowModeViolationError(
            "self-evolving must remain in shadow mode — see governance_os "
            "for the approval workflow"
        )


__all__ = [
    "SELF_EVOLVING_SHADOW_ONLY",
    "ImprovementSuggestion",
    "ShadowModeViolationError",
    "assert_shadow_mode",
    "derive_suggestions",
]
