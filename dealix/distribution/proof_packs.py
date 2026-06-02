"""Proof Pack Factory — assembles a leakage→quick-win→measurement evidence pack.

Evidence discipline (reuses the canonical ladder):
  - generated packs default to **L1 internal draft** (not customer-ready);
  - promoting a pack to public (L4+) goes through
    :func:`auto_client_acquisition.proof_engine.evidence.assert_public_proof_allowed`,
    which requires L4 minimum **and** explicit consent;
  - no fake proof — fields describe the *plan to measure*, not invented numbers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from auto_client_acquisition.proof_engine.evidence import (
    EvidenceLevel,
    assert_public_proof_allowed,
)
from dealix.distribution import sectors as sectors_mod
from dealix.distribution.doctrine import STATUS_PENDING, assert_distribution_safe
from dealix.distribution.ledger import append_record, new_id, now_iso, read_records, update_status
from dealix.distribution.paths import PROOF_PACKS_LEDGER
from dealix.distribution.prospects import load_prospects

# Prospects worth a proof pack: contacted or further along.
ELIGIBLE_STATUSES = {"contacted", "qualified", "proposal", "won"}


def build_proof_pack(prospect: dict[str, Any]) -> dict[str, Any]:
    """Build an L1 (internal-draft) proof pack for a prospect."""
    assert_distribution_safe()
    sector_key = str(prospect.get("sector") or "")
    sector = sectors_mod.get_sector(sector_key) or {}
    pain = str(prospect.get("pain_hypothesis") or sector.get("pain") or "").strip()

    return {
        "id": new_id("proof"),
        "prospect_id": str(prospect.get("id") or ""),
        "company": str(prospect.get("company") or "").strip(),
        "sector": sector_key,
        "current_workflow": "متابعة يدوية متفرقة عبر قنوات متعددة (افتراض أولي يُؤكَّد في الـ discovery)",
        "leakage_points": [
            pain or "تأخر المتابعة وتشتت المسؤوليات",
            "غياب أولوية واضحة للفرص",
            "لا تقرير موحد يوضح أين يتسرب الـ pipeline",
        ],
        "quick_win": str(sector.get("first_workflow") or "أول workflow متابعة محكوم خلال أسبوع"),
        "measurement_plan": (
            "قياس قبل/بعد على عينة (زمن أول رد، نسبة المتابعة، الفرص المعاد تفعيلها) "
            "— أرقام حقيقية فقط بعد التشغيل"
        ),
        "before_after": "يُملأ بعد القياس الفعلي (لا أرقام مفترضة)",
        "evidence_level": int(EvidenceLevel.L1_INTERNAL_DRAFT),
        "consent_public": False,
        "risks": ["النتيجة تعتمد على جودة البيانات والوصول"],
        "status": STATUS_PENDING,
        "created_at": now_iso(),
    }


def promote_to_public(
    proof_id: str,
    *,
    level: int,
    consent_public: bool,
    ledger: Path | None = None,
) -> dict[str, Any] | None:
    """Promote a pack for public/case-study use — enforces the L4 + consent gate."""
    assert_public_proof_allowed(level, consent_public=consent_public)
    return update_status(
        ledger or PROOF_PACKS_LEDGER,
        proof_id,
        "approved",
        evidence_level=int(level),
        consent_public=bool(consent_public),
    )


def run_generation(
    prospects_path: Path | None = None,
    *,
    ledger: Path | None = None,
) -> dict[str, Any]:
    """Generate proof-pack drafts for eligible prospects (dedupe per prospect)."""
    led = ledger or PROOF_PACKS_LEDGER
    prospects = load_prospects(prospects_path)
    existing = read_records(led)
    have = {str(p.get("prospect_id")) for p in existing}
    new_packs: list[dict[str, Any]] = []
    for pr in prospects:
        if str(pr.get("status") or "") not in ELIGIBLE_STATUSES:
            continue
        if str(pr.get("id") or "") in have:
            continue
        new_packs.append(build_proof_pack(pr))
    for p in new_packs:
        append_record(led, p)
    return {
        "prospects": len(prospects),
        "new_proof_packs": len(new_packs),
        "ids": [p["id"] for p in new_packs],
        "default_evidence_level": int(EvidenceLevel.L1_INTERNAL_DRAFT),
    }


def all_proof_packs(ledger: Path | None = None) -> list[dict[str, Any]]:
    return read_records(ledger or PROOF_PACKS_LEDGER)


__all__ = [
    "ELIGIBLE_STATUSES",
    "all_proof_packs",
    "build_proof_pack",
    "promote_to_public",
    "run_generation",
]
