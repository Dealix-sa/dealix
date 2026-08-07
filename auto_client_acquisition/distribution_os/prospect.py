"""Prospect Operating System — qualified-prospect lifecycle + JSONL store.

A prospect only advances to ``drafted`` once it clears the qualification gate
(known sector, clear pain, a catalog-backed offer, a permitted channel, and a
risk that is not high). No prospect is acquired by scraping — sources are
founder-provided; see governance/source registry.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso

_VALID_CHANNELS: frozenset[str] = frozenset({"email", "whatsapp", "linkedin", "phone", "proposal"})
_VALID_RISK: frozenset[str] = frozenset({"low", "medium", "high"})


class ProspectStatus(StrEnum):
    NEW = "new"
    QUALIFIED = "qualified"
    DRAFTED = "drafted"
    CONTACTED = "contacted"
    REPLIED = "replied"
    DISCOVERY_BOOKED = "discovery_booked"
    PROPOSAL_NEEDED = "proposal_needed"
    PROPOSAL_SENT = "proposal_sent"
    PAYMENT_HANDOFF = "payment_handoff"
    WON = "won"
    LOST = "lost"
    NURTURE = "nurture"


@dataclass
class Prospect:
    id: str = field(default_factory=lambda: f"pros_{uuid4().hex[:12]}")
    company: str = ""
    sector: str = ""
    region: str = ""
    source: str = ""
    decision_maker: str = ""
    status: str = ProspectStatus.NEW.value
    pain_hypothesis: str = ""
    offer_angle: str = ""  # a catalog product id or product name
    estimated_value_sar: int = 0
    confidence: float = 0.0
    preferred_channel: str = "email"
    last_contact_at: str = ""
    next_action: str = ""
    next_action_date: str = ""
    risk: str = "medium"
    evidence_level: int = 0  # L0–L5
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class QualificationResult:
    qualified: bool
    reasons: tuple[str, ...]


_store = JsonlStore(
    env_var="DEALIX_PROSPECTS_PATH", default_rel="var/prospects.jsonl", id_field="id"
)


def qualify(prospect: Prospect) -> QualificationResult:
    """Gate a prospect for entry into the draft factory (plan section 4).

    Required: known sector, clear pain hypothesis, a chosen offer angle, a
    permitted channel, and a risk that is not ``high``.
    """
    reasons: list[str] = []
    if not prospect.sector.strip():
        reasons.append("missing_sector")
    if not prospect.pain_hypothesis.strip():
        reasons.append("missing_pain_hypothesis")
    if not prospect.offer_angle.strip():
        reasons.append("missing_offer_angle")
    if prospect.preferred_channel not in _VALID_CHANNELS:
        reasons.append(f"invalid_channel:{prospect.preferred_channel}")
    if prospect.risk not in _VALID_RISK:
        reasons.append(f"invalid_risk:{prospect.risk}")
    elif prospect.risk == "high":
        reasons.append("risk_too_high")
    return QualificationResult(qualified=not reasons, reasons=tuple(reasons))


def add_prospect(**kwargs: Any) -> Prospect:
    prospect = Prospect(**kwargs)
    if prospect.preferred_channel not in _VALID_CHANNELS:
        raise ValueError(f"invalid_channel:{prospect.preferred_channel}")
    if prospect.risk not in _VALID_RISK:
        raise ValueError(f"invalid_risk:{prospect.risk}")
    _store.append(prospect.to_dict())
    return prospect


def list_prospects(*, status: str | None = None, sector: str | None = None) -> list[Prospect]:
    def _match(rec: dict[str, Any]) -> bool:
        return (status is None or rec.get("status") == status) and (
            sector is None or rec.get("sector") == sector
        )

    # last write wins per id
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list(predicate=_match):
        latest[str(rec.get("id"))] = rec
    return [Prospect(**rec) for rec in latest.values()]


def get_prospect(prospect_id: str) -> Prospect | None:
    rec = _store.get(prospect_id)
    return Prospect(**rec) if rec else None


def update_status(prospect_id: str, status: str | ProspectStatus) -> Prospect | None:
    value = status.value if isinstance(status, ProspectStatus) else str(status)
    if value not in {s.value for s in ProspectStatus}:
        raise ValueError(f"invalid_status:{value}")
    rec = _store.patch(prospect_id, {"status": value})
    return Prospect(**rec) if rec else None


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "Prospect",
    "ProspectStatus",
    "QualificationResult",
    "add_prospect",
    "clear_for_test",
    "get_prospect",
    "list_prospects",
    "qualify",
    "update_status",
]
