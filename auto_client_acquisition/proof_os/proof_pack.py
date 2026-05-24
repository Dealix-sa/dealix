"""Proof Pack v2 surface — canonical 14-section bilingual proof artifact.

This module wraps the underlying ``proof_architecture_os.proof_pack_v2``
sections and adds:

* :func:`build_empty_proof_pack_v2` — empty skeleton.
* :func:`merge_proof_pack_v2` — strict merge that only accepts canonical keys.
* :class:`ProofPackV2` — bilingual proof pack with metadata, AR/EN sections,
  rendering helpers, and a stable JSON shape.
* :func:`render_markdown` — bilingual Markdown render (AR primary, EN secondary).
* :func:`render_json` — stable JSON shape for ledger and downstream consumers.

The class is intentionally light — it does not call an LLM and does not
mutate. All operations return a new dict / string.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    proof_pack_v2_sections_complete,
)

# Bilingual labels for the 14 canonical sections.
# Order matches PROOF_PACK_V2_SECTIONS — do NOT re-order without updating the
# underlying source-of-truth tuple in proof_architecture_os.
SECTION_LABELS_AR: dict[str, str] = {
    "executive_summary": "الملخص التنفيذي",
    "problem": "المشكلة",
    "inputs": "المدخلات",
    "source_passports": "جوازات المصدر",
    "work_completed": "العمل المنجز",
    "outputs": "المخرجات",
    "quality_scores": "درجات الجودة",
    "governance_decisions": "قرارات الحوكمة",
    "blocked_risks": "المخاطر المحجوبة",
    "value_metrics": "مقاييس القيمة",
    "limitations": "الحدود",
    "recommended_next_step": "الخطوة التالية الموصى بها",
    "retainer_expansion_path": "مسار توسع الـ retainer",
    "capital_assets_created": "الأصول الرأسمالية المُنتجة",
}

SECTION_LABELS_EN: dict[str, str] = {
    "executive_summary": "Executive Summary",
    "problem": "Problem",
    "inputs": "Inputs",
    "source_passports": "Source Passports",
    "work_completed": "Work Completed",
    "outputs": "Outputs",
    "quality_scores": "Quality Scores",
    "governance_decisions": "Governance Decisions",
    "blocked_risks": "Blocked Risks",
    "value_metrics": "Value Metrics",
    "limitations": "Limitations",
    "recommended_next_step": "Recommended Next Step",
    "retainer_expansion_path": "Retainer Expansion Path",
    "capital_assets_created": "Capital Assets Created",
}


def build_empty_proof_pack_v2() -> dict[str, str]:
    """Return an empty section dictionary keyed by canonical section names."""
    return dict.fromkeys(PROOF_PACK_V2_SECTIONS, "")


def merge_proof_pack_v2(
    base: Mapping[str, str],
    updates: Mapping[str, str],
) -> dict[str, str]:
    """Merge ``updates`` into ``base``; unknown keys in updates are dropped."""
    out = build_empty_proof_pack_v2()
    out.update({k: (base.get(k) or "").strip() for k in PROOF_PACK_V2_SECTIONS})
    for k, v in updates.items():
        if k in PROOF_PACK_V2_SECTIONS:
            out[k] = str(v).strip()
    return out


@dataclass(slots=True)
class ProofPackV2:
    """A bilingual proof artifact assembled at the end of an AI Stack run.

    Sections are stored once per language; the public surface guarantees
    that both ``sections_ar`` and ``sections_en`` are always present (empty
    strings allowed). Customer-facing renders are always bilingual.
    """

    pack_id: str
    tenant_id: str
    customer_handle: str
    offer_tier: str
    sections_ar: dict[str, str] = field(default_factory=build_empty_proof_pack_v2)
    sections_en: dict[str, str] = field(default_factory=build_empty_proof_pack_v2)
    proof_score: int = 0
    governance_decisions: tuple[str, ...] = field(default_factory=tuple)
    decision_passport_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_head_hash: str = ""
    created_at: str = ""
    completed_at: str | None = None

    def is_complete(self) -> tuple[bool, tuple[str, ...]]:
        """Both AR and EN versions must have every section filled."""
        ok_ar, missing_ar = proof_pack_v2_sections_complete(self.sections_ar)
        ok_en, missing_en = proof_pack_v2_sections_complete(self.sections_en)
        if ok_ar and ok_en:
            return True, ()
        missing = tuple(
            f"{section}({lang})"
            for lang, items in (("ar", missing_ar), ("en", missing_en))
            for section in items
        )
        return False, missing

    def set_section(self, key: str, *, ar: str = "", en: str = "") -> None:
        if key not in PROOF_PACK_V2_SECTIONS:
            raise ValueError(f"unknown section: {key!r}")
        if ar:
            self.sections_ar[key] = ar.strip()
        if en:
            self.sections_en[key] = en.strip()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["governance_decisions"] = list(self.governance_decisions)
        data["decision_passport_ids"] = list(self.decision_passport_ids)
        return data


VALID_OFFER_TIERS: frozenset[str] = frozenset(
    {
        "free_diagnostic",
        "sprint_499",
        "data_pack_1500",
        "managed_ops",
        "custom_ai",
    }
)


def new_proof_pack(
    *,
    tenant_id: str,
    customer_handle: str,
    offer_tier: str,
) -> ProofPackV2:
    """Construct a fresh, empty bilingual proof pack ready to be filled in."""
    if offer_tier not in VALID_OFFER_TIERS:
        raise ValueError(
            f"unknown offer_tier: {offer_tier!r} (allowed: {sorted(VALID_OFFER_TIERS)})"
        )
    if not tenant_id or not tenant_id.strip():
        raise ValueError("tenant_id is required")
    if not customer_handle or not customer_handle.strip():
        raise ValueError("customer_handle is required")
    return ProofPackV2(
        pack_id=f"pp_{uuid.uuid4().hex[:16]}",
        tenant_id=tenant_id.strip(),
        customer_handle=customer_handle.strip(),
        offer_tier=offer_tier,
        created_at=datetime.now(UTC).isoformat(),
    )


def _render_section_markdown(
    section: str,
    *,
    sections_ar: Mapping[str, str],
    sections_en: Mapping[str, str],
) -> str:
    label_ar = SECTION_LABELS_AR[section]
    label_en = SECTION_LABELS_EN[section]
    body_ar = (sections_ar.get(section) or "").strip() or "_(لا يوجد محتوى)_"
    body_en = (sections_en.get(section) or "").strip() or "_(no content)_"
    return (
        f"## {label_ar} — {label_en}\n\n"
        f"**العربية:**\n\n{body_ar}\n\n"
        f"**English:**\n\n{body_en}\n"
    )


def render_markdown(pack: ProofPackV2) -> str:
    """Render the full bilingual proof pack as Markdown.

    Layout: title block → metadata → 14 sections in canonical order.
    """
    header = (
        f"# Proof Pack — حزمة الإثبات\n\n"
        f"- **Pack ID / المعرف**: `{pack.pack_id}`\n"
        f"- **Customer / العميل**: `{pack.customer_handle}`\n"
        f"- **Tenant / المستأجر**: `{pack.tenant_id}`\n"
        f"- **Offer Tier / المستوى**: `{pack.offer_tier}`\n"
        f"- **Proof Score / درجة الإثبات**: **{pack.proof_score}/100**\n"
        f"- **Created / أُنشئ**: `{pack.created_at}`\n"
        f"- **Evidence Head / رأس الأدلة**: `{pack.evidence_head_hash or 'n/a'}`\n\n"
        f"---\n\n"
    )
    body = "\n".join(
        _render_section_markdown(
            section,
            sections_ar=pack.sections_ar,
            sections_en=pack.sections_en,
        )
        for section in PROOF_PACK_V2_SECTIONS
    )
    return header + body


def render_json(pack: ProofPackV2) -> str:
    """Stable JSON serialization for ledger storage / API responses."""
    return json.dumps(pack.to_dict(), ensure_ascii=False, sort_keys=True)


__all__ = [
    "PROOF_PACK_V2_SECTIONS",
    "SECTION_LABELS_AR",
    "SECTION_LABELS_EN",
    "VALID_OFFER_TIERS",
    "ProofPackV2",
    "build_empty_proof_pack_v2",
    "merge_proof_pack_v2",
    "new_proof_pack",
    "proof_pack_v2_sections_complete",
    "render_json",
    "render_markdown",
]
