"""Asset builder — turn every outcome into a reusable asset.

The rule: no outcome is allowed to leave the kernel without being
considered for asset creation. This module owns the mapping
`Outcome → Asset(kind, body)` and an in-process asset store so the
console and the tests can read assets without booting a database.
"""

from __future__ import annotations

from threading import RLock

from dealix.hermes.core.schemas import (
    Asset,
    AssetKind,
    Outcome,
    OutcomeKind,
)

_OUTCOME_TO_KIND: dict[OutcomeKind, AssetKind] = {
    OutcomeKind.DEAL_WON: AssetKind.CASE_STUDY,
    OutcomeKind.PILOT_STARTED: AssetKind.CASE_STUDY,
    OutcomeKind.UPSELL_ACCEPTED: AssetKind.PLAYBOOK,
    OutcomeKind.MEETING_BOOKED: AssetKind.TEMPLATE,
    OutcomeKind.REPLY_RECEIVED: AssetKind.TEMPLATE,
    OutcomeKind.OBJECTION_RAISED: AssetKind.PLAYBOOK,
    OutcomeKind.DEAL_LOST: AssetKind.PLAYBOOK,
    OutcomeKind.NO_REPLY: AssetKind.PLAYBOOK,
    OutcomeKind.PILOT_FAILED: AssetKind.PLAYBOOK,
}


def _summarise(outcome: Outcome) -> str:
    parts = [f"outcome={outcome.kind.value}"]
    if outcome.sector:
        parts.append(f"sector={outcome.sector}")
    if outcome.offer:
        parts.append(f"offer={outcome.offer}")
    if outcome.value_sar:
        parts.append(f"value_sar={outcome.value_sar:.0f}")
    return " | ".join(parts)


def build_from_outcome(outcome: Outcome) -> Asset:
    """Map an outcome to a candidate asset. Always returns an asset.

    The caller decides whether to publish it (assets stored as
    `reusable=False` are kept private to the kernel).
    """
    kind = _OUTCOME_TO_KIND.get(outcome.kind, AssetKind.PLAYBOOK)
    reusable = outcome.kind in {
        OutcomeKind.DEAL_WON,
        OutcomeKind.PILOT_STARTED,
        OutcomeKind.UPSELL_ACCEPTED,
        OutcomeKind.MEETING_BOOKED,
        OutcomeKind.REPLY_RECEIVED,
        OutcomeKind.OBJECTION_RAISED,
    }
    title = f"{kind.value.replace('_', ' ').title()} — {outcome.offer or outcome.sector or 'general'}"
    body = {
        "trigger": outcome.kind.value,
        "notes": outcome.notes or "",
        "sector": outcome.sector,
        "offer": outcome.offer,
        "value_sar": outcome.value_sar,
        "links": {
            "outcome_id": outcome.id,
            "decision_id": outcome.decision_id,
            "opportunity_id": outcome.opportunity_id,
        },
    }
    return Asset(
        kind=kind,
        title=title,
        summary=_summarise(outcome),
        source_outcome_id=outcome.id,
        body=body,
        reusable=reusable,
    )


class AssetStore:
    """Tiny in-process asset store. Thread-safe, deterministic order."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._items: list[Asset] = []

    def add(self, asset: Asset) -> Asset:
        with self._lock:
            self._items.append(asset)
        return asset

    def all(self) -> list[Asset]:
        with self._lock:
            return list(self._items)

    def by_kind(self, kind: AssetKind) -> list[Asset]:
        with self._lock:
            return [a for a in self._items if a.kind == kind]

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_store = AssetStore()


def default_store() -> AssetStore:
    return _default_store
