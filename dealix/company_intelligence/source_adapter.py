"""Fail-closed adapter from operational SourcePassport to canonical Source truth.

Bridges ``auto_client_acquisition.trust_os.source_passport.SourcePassport``
into ``CanonicalSource`` without escalating authority. The operational passport
carries policy and sensitivity metadata; this adapter normalises it into the
tenant-scoped, policy-governed, deduplicated shape that the rest of the
Company Intelligence provenance registry expects.

Key constraints:
  - A ``SourcePassport`` carries coarse ``source_type`` strings (e.g.
    ``client_upload``, ``google_api``, ``manual``). An explicit mapping is
    maintained; unknown types fail-closed to ``MANUAL``.
  - ``policy_status`` is derived from the passport's ``allowed_use``,
    ``external_use_allowed``, and ``ai_access_allowed`` fields.  Sources
    that disallow AI access are at most ``RESEARCH_ONLY``; sources that
    disallow external use are at most ``RESEARCH_ONLY``.
  - PII-containing sources start at ``REVIEW_REQUIRED`` unless they
    have explicit approval indicators.
  - The adapter never activates a blocked source.
  - Both ``authority_score`` and ``verifiability_score`` start at 50
    (neutral) — enrichment is a separate concern.
"""
from __future__ import annotations

from typing import Any

from dealix.company_intelligence.source_contracts import (
    CanonicalSource,
    SourcePolicyStatus,
    SourceType,
    build_source,
)

# ---------------------------------------------------------------------------
# Mapping tables
# ---------------------------------------------------------------------------

_SOURCE_TYPE_MAP: dict[str, SourceType] = {
    # Client and internal sources
    "client_upload": SourceType.CLIENT_PROVIDED,
    "client_provided": SourceType.CLIENT_PROVIDED,
    "client_data": SourceType.CLIENT_PROVIDED,
    "crm": SourceType.CRM,
    "crm_export": SourceType.CRM,
    "hubspot": SourceType.CRM,
    "salesforce": SourceType.CRM,
    "pipedrive": SourceType.CRM,
    "email": SourceType.EMAIL,
    "email_inbox": SourceType.EMAIL,
    "internal": SourceType.INTERNAL_SYSTEM,
    "internal_system": SourceType.INTERNAL_SYSTEM,
    "dealix": SourceType.INTERNAL_SYSTEM,
    "owned": SourceType.OWNED,
    # Public and research sources
    "google_api": SourceType.PUBLIC_REGISTRY,
    "google_places": SourceType.PUBLIC_REGISTRY,
    "google_maps": SourceType.PUBLIC_REGISTRY,
    "government_registry": SourceType.PUBLIC_REGISTRY,
    "cr_registry": SourceType.PUBLIC_REGISTRY,
    "company_website": SourceType.COMPANY_WEBSITE,
    "website": SourceType.COMPANY_WEBSITE,
    "open_data": SourceType.OPEN_DATA,
    "public": SourceType.OPEN_DATA,
    "news": SourceType.NEWS,
    "news_feed": SourceType.NEWS,
    "jobs": SourceType.JOBS,
    "job_board": SourceType.JOBS,
    "event": SourceType.EVENT,
    "conference": SourceType.EVENT,
    # Partner and referral sources
    "partner": SourceType.PARTNER,
    "referral": SourceType.PARTNER,
    "warm_intro": SourceType.PARTNER,
    # Manual and fallback
    "manual": SourceType.MANUAL,
    "csv": SourceType.MANUAL,
    "form": SourceType.MANUAL,
    "api": SourceType.INTERNAL_SYSTEM,
    "whatsapp": SourceType.OWNED,
}


def _resolve_source_type(raw_type: str) -> SourceType:
    """Map an operational source type string to a canonical SourceType.

    Unknown types fail-closed to ``MANUAL``.
    """
    return _SOURCE_TYPE_MAP.get(raw_type.lower().strip(), SourceType.MANUAL)


def _resolve_policy_status(
    *,
    allowed_use: list[str],
    ai_access_allowed: bool,
    external_use_allowed: bool,
    contains_pii: bool,
) -> SourcePolicyStatus:
    """Derive canonical policy status from passport policy fields.

    Rules (applied in order):
      1. If ``ai_access_allowed`` is False → BLOCKED (cannot feed any
         canonical entity).
      2. If ``external_use_allowed`` is False → at most RESEARCH_ONLY.
      3. If ``contains_pii`` is True and no explicit ``internal_analysis``
         use → REVIEW_REQUIRED.
      4. If allowed_use contains ``internal_analysis`` or ``approved`` →
         at most RESEARCH_ONLY (PII present) or APPROVED (no PII).
      5. Fallback → REVIEW_REQUIRED.
    """
    if not ai_access_allowed:
        return SourcePolicyStatus.BLOCKED

    use_set = {u.strip().lower() for u in allowed_use}

    # Explicit approval indicator
    has_approval = "approved" in use_set or "full_use" in use_set
    has_analysis = "internal_analysis" in use_set or "analysis" in use_set

    if not external_use_allowed:
        # Cannot go above RESEARCH_ONLY
        if has_approval or has_analysis:
            return SourcePolicyStatus.RESEARCH_ONLY
        return SourcePolicyStatus.REVIEW_REQUIRED

    if contains_pii:
        # PII sources need explicit review even with some use approval
        if has_approval:
            return SourcePolicyStatus.RESEARCH_ONLY
        return SourcePolicyStatus.REVIEW_REQUIRED

    # Non-PII, AI allowed, external allowed
    if has_approval:
        return SourcePolicyStatus.APPROVED
    if has_analysis:
        return SourcePolicyStatus.RESEARCH_ONLY
    return SourcePolicyStatus.REVIEW_REQUIRED


def _derive_allowed_use(allowed_use: list[str]) -> str:
    """Collapse the list of allowed uses into a single canonical string."""
    use_set = {u.strip().lower() for u in allowed_use if u.strip()}
    if "full_use" in use_set or "approved" in use_set:
        return "approved"
    if "internal_analysis" in use_set or "analysis" in use_set:
        return "internal_analysis"
    if "draft_only" in use_set:
        return "draft_only"
    if "research_only" in use_set:
        return "research_only"
    return "research_only"


def normalize_source_passport(
    passport: Any,
    *,
    tenant_id: str,
) -> CanonicalSource:
    """Normalize a ``SourcePassport`` into a ``CanonicalSource``.

    Parameters
    ----------
    passport:
        A ``SourcePassport`` or any duck-typed object with ``source_id``,
        ``source_type``, ``owner``, ``allowed_use``, ``contains_pii``,
        ``sensitivity``, ``relationship_status``, ``retention_policy``,
        ``ai_access_allowed``, ``external_use_allowed``.
    tenant_id:
        The tenant scope for the resulting canonical source.
    """
    source_id_raw = str(getattr(passport, "source_id", "") or "").strip()
    if not source_id_raw:
        raise ValueError("passport must have a non-empty source_id")

    source_type_raw = str(getattr(passport, "source_type", "") or "").strip()
    source_type = _resolve_source_type(source_type_raw)

    owner = str(getattr(passport, "owner", "") or "").strip()
    name = f"{source_type_raw}:{owner}" if owner else source_type_raw
    if not name:
        name = "unknown_source"

    allowed_use = list(getattr(passport, "allowed_use", []) or [])
    contains_pii = bool(getattr(passport, "contains_pii", False))
    ai_access_allowed = bool(getattr(passport, "ai_access_allowed", True))
    external_use_allowed = bool(getattr(passport, "external_use_allowed", False))

    policy_status = _resolve_policy_status(
        allowed_use=allowed_use,
        ai_access_allowed=ai_access_allowed,
        external_use_allowed=external_use_allowed,
        contains_pii=contains_pii,
    )

    canonical_allowed_use = _derive_allowed_use(allowed_use)

    # Sensitivity → freshness mapping (conservative)
    sensitivity = str(getattr(passport, "sensitivity", "") or "").strip().lower()
    freshness_days = {
        "high": 30,
        "medium": 90,
        "low": 180,
    }.get(sensitivity, 90)

    # Retention → retention_days mapping
    retention_raw = str(getattr(passport, "retention_policy", "") or "").strip().lower()
    retention_days = {
        "project_duration": 90,
        "90_days": 90,
        "180_days": 180,
        "1_year": 365,
        "permanent": 730,
        "indefinite": 730,
    }.get(retention_raw, 365)

    # Blocked sources cannot be active — use BLOCKED status
    from dealix.company_intelligence.source_contracts import SourceStatus

    status = SourceStatus.BLOCKED if policy_status == SourcePolicyStatus.BLOCKED else SourceStatus.ACTIVE

    return build_source(
        tenant_id=tenant_id,
        deduplication_key=source_id_raw,
        name=name,
        source_type=source_type,
        description=f"Source passport: {source_id_raw}",
        policy_status=policy_status,
        allowed_use=canonical_allowed_use,
        freshness_days=freshness_days,
        retention_days=retention_days,
        confidence=0.5,
        status=status,
    )
