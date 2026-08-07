"""Proof Pack Factory — evidence-level discipline over the proof_os surface.

Every commercial claim ties to an evidence level L0–L5 (plan section 9). This
module records a lightweight proof pack and validates the evidence level; the
canonical 14-section pack lives in ``proof_os`` / ``proof_architecture_os``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso

# L0 hypothesis → L5 paid result.
EVIDENCE_LEVELS: dict[int, str] = {
    0: "فرضية / hypothesis",
    1: "ملف داخلي أو وثيقة / internal file or document",
    2: "مخرجات اختبار أو سكربت / script or test output",
    3: "إشارة من staging أو production / staging or production signal",
    4: "بيانات عميل محتمل أو عميل / prospect or customer data",
    5: "نتيجة مدفوعة / paid result",
}


def evidence_level_valid(level: int) -> bool:
    return level in EVIDENCE_LEVELS


def evidence_level_label(level: int) -> str:
    return EVIDENCE_LEVELS.get(level, "unknown")


@dataclass
class ProofPack:
    id: str = field(default_factory=lambda: f"proof_{uuid4().hex[:12]}")
    customer_id: str = ""
    current_process: str = ""
    leakage_points: list[str] = field(default_factory=list)
    quick_win: str = ""
    before_after: str = ""
    measurement_method: str = ""
    evidence_level: int = 0
    risk: str = "low"
    recommended_pilot: str = ""
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(
    env_var="DEALIX_PROOF_PACKS_PATH", default_rel="var/proof_packs.jsonl", id_field="id"
)


def build_proof_pack(
    *,
    customer_id: str,
    current_process: str = "",
    leakage_points: list[str] | None = None,
    quick_win: str = "",
    before_after: str = "",
    measurement_method: str = "",
    evidence_level: int = 0,
    risk: str = "low",
    recommended_pilot: str = "",
) -> ProofPack:
    if not evidence_level_valid(evidence_level):
        raise ValueError(f"invalid_evidence_level:{evidence_level} (allowed L0–L5)")
    pack = ProofPack(
        customer_id=customer_id,
        current_process=current_process,
        leakage_points=leakage_points or [],
        quick_win=quick_win,
        before_after=before_after,
        measurement_method=measurement_method,
        evidence_level=evidence_level,
        risk=risk,
        recommended_pilot=recommended_pilot,
    )
    _store.append(pack.to_dict())
    return pack


def get_proof_pack(pack_id: str) -> ProofPack | None:
    rec = _store.get(pack_id)
    return ProofPack(**rec) if rec else None


def list_proof_packs(*, customer_id: str | None = None) -> list[ProofPack]:
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list():
        latest[str(rec.get("id"))] = rec
    packs = [ProofPack(**rec) for rec in latest.values()]
    if customer_id is not None:
        packs = [p for p in packs if p.customer_id == customer_id]
    return packs


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "EVIDENCE_LEVELS",
    "ProofPack",
    "build_proof_pack",
    "clear_for_test",
    "evidence_level_label",
    "evidence_level_valid",
    "get_proof_pack",
    "list_proof_packs",
]
