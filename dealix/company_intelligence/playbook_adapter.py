"""Fail-closed adapter from SectorPlaybook to canonical PlaybookVersion.

Bridges ``auto_client_acquisition.revenue_graph.sector_playbooks.SectorPlaybook``
into ``CanonicalPlaybookVersion`` without escalating authority. A
SectorPlaybook is a static configuration record; this adapter normalises
it as a version-1 baseline registration in the canonical playbook
versioning system.

Key constraints:
  - Status always PROPOSED — the adapter never auto-approves a playbook.
  - Evidence references are derived from benchmarks, case study presence,
    and objection library coverage.
  - Confidence is derived from benchmark completeness.
  - The adapter never invents data: pain points, opening lines, and
    channel mix are summarised, not fabricated.
"""
from __future__ import annotations

from typing import Any

from dealix.company_intelligence.playbook_contracts import (
    CanonicalPlaybookVersion,
    PlaybookApprovalStatus,
    build_playbook_version,
)

# ---------------------------------------------------------------------------
# Evidence derivation
# ---------------------------------------------------------------------------

_EXPECTED_BENCHMARKS = frozenset({
    "reply_rate_p50",
    "meeting_rate_p50",
    "win_rate_p50",
    "cycle_days_p50",
})


def _derive_evidence_refs(playbook: Any) -> tuple[str, ...]:
    """Build evidence references from playbook data quality signals.

    Each evidence ref identifies a concrete data point that grounds
    the playbook — benchmarks, objection coverage, case studies, etc.
    """
    refs: list[str] = []

    benchmarks = dict(getattr(playbook, "benchmarks", {}) or {})
    for key in sorted(_EXPECTED_BENCHMARKS):
        if key in benchmarks:
            refs.append(f"benchmark:{key}={benchmarks[key]}")

    objections = tuple(getattr(playbook, "top_objections", ()) or ())
    if objections:
        refs.append(f"objection_coverage:{len(objections)}")

    case_study = str(getattr(playbook, "case_study_template_ar", "") or "")
    if case_study:
        refs.append("case_study_template:present")

    channel_mix = dict(getattr(playbook, "recommended_channel_mix", {}) or {})
    if channel_mix:
        refs.append(f"channel_mix:{len(channel_mix)}_channels")

    # Ensure at least one evidence ref (required by contract)
    if not refs:
        refs.append("manual_observation")

    return tuple(refs)


def _derive_confidence(playbook: Any) -> float:
    """Derive confidence from benchmark completeness and data quality.

    - Full benchmarks (all 4 keys): base 0.6
    - + objections indexed: +0.1
    - + case study template: +0.1
    - + channel mix present: +0.1
    - + avg_deal_value_sar > 0: +0.1
    Clamped to [0.1, 1.0].
    """
    confidence = 0.2  # base for having a playbook at all

    benchmarks = dict(getattr(playbook, "benchmarks", {}) or {})
    covered = len(_EXPECTED_BENCHMARKS & set(benchmarks.keys()))
    confidence += 0.1 * covered  # up to +0.4

    objections = tuple(getattr(playbook, "top_objections", ()) or ())
    if objections:
        confidence += 0.1

    case_study = str(getattr(playbook, "case_study_template_ar", "") or "")
    if case_study:
        confidence += 0.1

    channel_mix = dict(getattr(playbook, "recommended_channel_mix", {}) or {})
    if channel_mix:
        confidence += 0.1

    return max(0.1, min(1.0, confidence))


def _compose_description(playbook: Any) -> str:
    """Build a description from sector identifiers."""
    sector_id = str(getattr(playbook, "sector_id", "") or "").strip()
    sector_ar = str(getattr(playbook, "sector_ar", "") or "").strip()
    sector_en = str(getattr(playbook, "sector_en", "") or "").strip()

    parts: list[str] = []
    if sector_en:
        parts.append(sector_en)
    if sector_ar:
        parts.append(sector_ar)
    if not parts and sector_id:
        parts.append(sector_id)

    return " — ".join(parts) if parts else "Sector playbook"


def _compose_changes_summary(playbook: Any) -> str:
    """Build a changes summary from playbook content dimensions."""
    parts: list[str] = []

    pain_points = tuple(getattr(playbook, "pain_points_ar", ()) or ())
    if pain_points:
        parts.append(f"{len(pain_points)} pain points")

    opening_lines = tuple(getattr(playbook, "opening_lines_ar", ()) or ())
    if opening_lines:
        parts.append(f"{len(opening_lines)} opening lines")

    channel_mix = dict(getattr(playbook, "recommended_channel_mix", {}) or {})
    if channel_mix:
        primary = max(channel_mix.items(), key=lambda kv: kv[1])[0]
        parts.append(f"primary channel: {primary}")

    tone = str(getattr(playbook, "whatsapp_tone", "") or "").strip()
    if tone:
        parts.append(f"tone: {tone}")

    avg_deal = int(getattr(playbook, "avg_deal_value_sar", 0) or 0)
    if avg_deal > 0:
        parts.append(f"avg deal: {avg_deal} SAR")

    avg_cycle = int(getattr(playbook, "avg_cycle_days", 0) or 0)
    if avg_cycle > 0:
        parts.append(f"avg cycle: {avg_cycle}d")

    return " | ".join(parts)


def normalize_sector_playbook(
    playbook: Any,
    *,
    tenant_id: str,
    source_id: str = "sector_playbooks",
    version: int = 1,
) -> CanonicalPlaybookVersion:
    """Normalize a ``SectorPlaybook`` into a ``CanonicalPlaybookVersion``.

    Parameters
    ----------
    playbook:
        A ``SectorPlaybook`` or any duck-typed object with ``sector_id``,
        ``sector_ar``, ``sector_en``, ``pain_points_ar``, ``benchmarks``,
        ``recommended_channel_mix``, and optionally other sector fields.
    tenant_id:
        The tenant scope for the resulting canonical playbook version.
    source_id:
        Source identity for provenance tracking (default: "sector_playbooks").
    version:
        Playbook version number (default: 1 — baseline registration).
    """
    sector_id = str(getattr(playbook, "sector_id", "") or "").strip()
    if not sector_id:
        raise ValueError("playbook must have a non-empty sector_id")

    sector_en = str(getattr(playbook, "sector_en", "") or "").strip()
    playbook_name = f"sector:{sector_id}" if not sector_en else f"sector:{sector_id}:{sector_en}"

    description = _compose_description(playbook)
    changes_summary = _compose_changes_summary(playbook)
    evidence_refs = _derive_evidence_refs(playbook)
    confidence = _derive_confidence(playbook)

    return build_playbook_version(
        tenant_id=tenant_id,
        playbook_name=playbook_name,
        version=version,
        change_reason=f"Baseline registration of {sector_id} sector playbook",
        source_id=source_id,
        evidence_refs=evidence_refs,
        description=description,
        changes_summary=changes_summary,
        approval_status=PlaybookApprovalStatus.PROPOSED,
        confidence=confidence,
    )
