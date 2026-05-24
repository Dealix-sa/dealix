"""
Data classification — §84.

A small heuristic classifier that assigns a ``DataSensitivity`` to a
payload, plus the canonical decision matrix that governs who can see
each class, whether agents may ingest it, and whether it may exit the
organisation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.sovereign_control_plane.types import DataSensitivity


@dataclass
class ClassifiedItem:
    item_id: str
    sensitivity: DataSensitivity
    reason: str
    matched_terms: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "sensitivity": self.sensitivity.value,
            "reason": self.reason,
            "matched_terms": list(self.matched_terms),
        }


# Decision matrix — exact §84 table. Keys: who_sees, agent_ingest,
# external_exit.
DECISION_MATRIX: dict[DataSensitivity, dict[str, bool]] = {
    DataSensitivity.PUBLIC: {
        "who_sees": True,
        "agent_ingest": True,
        "external_exit": True,
    },
    DataSensitivity.INTERNAL: {
        "who_sees": True,
        "agent_ingest": True,
        "external_exit": False,
    },
    DataSensitivity.CONFIDENTIAL: {
        "who_sees": True,
        "agent_ingest": True,
        "external_exit": False,
    },
    DataSensitivity.RESTRICTED: {
        "who_sees": True,
        "agent_ingest": False,
        "external_exit": False,
    },
    DataSensitivity.SOVEREIGN: {
        "who_sees": False,
        "agent_ingest": False,
        "external_exit": False,
    },
}


_SOVEREIGN_TERMS = (
    "sovereign", "sami_personal", "board_decision", "founder_only",
    "kill_switch", "lockdown",
)
_RESTRICTED_TERMS = (
    "national_id", "iqama", "passport", "salary", "bank_account",
    "iban", "pricing_floor", "contract_value", "cap_table",
)
_CONFIDENTIAL_TERMS = (
    "pricing", "contract", "proposal", "margin", "commission",
    "partner_terms", "internal_memo",
)
_INTERNAL_TERMS = ("internal", "team", "dealix_internal")


class Classifier:
    """Keyword heuristic classifier — deterministic, no model calls."""

    def classify(
        self, payload: Any, hints: dict[str, Any] | None = None
    ) -> ClassifiedItem:
        text = self._stringify(payload).lower()
        hints = hints or {}
        if hints.get("sensitivity"):
            sens = DataSensitivity(hints["sensitivity"])
            return ClassifiedItem(
                item_id=hints.get("item_id", "anon"),
                sensitivity=sens,
                reason="hint_override",
            )
        matched: list[str] = []
        for term in _SOVEREIGN_TERMS:
            if term in text:
                matched.append(term)
        if matched:
            return ClassifiedItem("anon", DataSensitivity.SOVEREIGN, "sovereign_term", matched)
        for term in _RESTRICTED_TERMS:
            if term in text:
                matched.append(term)
        if matched:
            return ClassifiedItem("anon", DataSensitivity.RESTRICTED, "restricted_term", matched)
        for term in _CONFIDENTIAL_TERMS:
            if term in text:
                matched.append(term)
        if matched:
            return ClassifiedItem("anon", DataSensitivity.CONFIDENTIAL, "confidential_term", matched)
        for term in _INTERNAL_TERMS:
            if term in text:
                matched.append(term)
        if matched:
            return ClassifiedItem("anon", DataSensitivity.INTERNAL, "internal_term", matched)
        return ClassifiedItem("anon", DataSensitivity.PUBLIC, "default_public")

    @staticmethod
    def _stringify(payload: Any) -> str:
        if isinstance(payload, str):
            return payload
        if isinstance(payload, dict):
            return " ".join(f"{k}={v}" for k, v in payload.items())
        if isinstance(payload, (list, tuple)):
            return " ".join(str(x) for x in payload)
        return str(payload)


def is_export_allowed(sensitivity: DataSensitivity) -> bool:
    return DECISION_MATRIX[sensitivity]["external_exit"]


def is_agent_ingest_allowed(sensitivity: DataSensitivity) -> bool:
    return DECISION_MATRIX[sensitivity]["agent_ingest"]
