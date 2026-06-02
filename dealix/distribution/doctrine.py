"""Distribution doctrine — the safety spine of the Revenue Execution OS.

This module does **not** invent a new doctrine. It *reuses* the canonical
non-negotiables enforced repo-wide in
:mod:`auto_client_acquisition.safe_send_gateway` and the canonical evidence
levels in :mod:`auto_client_acquisition.proof_engine.evidence`, then adds two
distribution-specific, fully governed pieces:

  1. ``CHANNEL_AUTOMATION_POLICY`` — what each channel may/ may not do
     (email/whatsapp/linkedin/phone/proposals). Drafting is always allowed;
     automated external sending is never allowed.
  2. ``BANNED_CLAIM_PHRASES`` — overclaim / spam phrases that must never appear
     in a generated draft (mirrors the existing content-draft generator).

``assert_distribution_safe()`` is the single fail-fast call every generator
uses before writing anything to a ledger.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.proof_engine.evidence import (
    EVIDENCE_LEVEL_DESCRIPTIONS_AR,
    EVIDENCE_LEVEL_DESCRIPTIONS_EN,
    EvidenceLevel,
)
from auto_client_acquisition.safe_send_gateway import (
    doctrine_violations_for_revenue_intelligence,
    enforce_doctrine_non_negotiables,
)

# Operating mode for everything this package writes.
OPERATING_MODE = "draft_only_no_auto_send"

# Canonical pending/approval statuses shared across record types.
STATUS_PENDING = "draft_pending_approval"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_COPIED = "copied_manual_send"  # founder copied the draft for a manual send

# ── Channel automation policy ──────────────────────────────────────────
# allow = governed actions the OS performs; deny = actions that are forbidden
# at the platform level (defense in depth on top of safe_send_gateway).
CHANNEL_AUTOMATION_POLICY: dict[str, dict[str, list[str]]] = {
    "email": {
        "allow": ["generate_draft", "save_draft", "manual_send_after_approval"],
        "deny": ["auto_send_without_approval", "bulk_blast", "guaranteed_claims"],
    },
    "whatsapp": {
        "allow": ["generate_draft", "manual_copy_send", "founder_reminder"],
        "deny": ["cold_whatsapp_automation", "bulk_send", "agent_auto_send"],
    },
    "linkedin": {
        "allow": ["generate_draft", "manual_copy_send"],
        "deny": ["linkedin_automation", "scraping", "mass_connect"],
    },
    "phone": {
        "allow": ["call_script", "discovery_notes", "objection_tracker"],
        "deny": ["auto_dialer_without_consent"],
    },
    "proposal": {
        "allow": ["proposal_draft", "proof_pack", "payment_handoff_draft"],
        "deny": ["contract_commitment_without_approval", "auto_send_payment_link"],
    },
}

# Overclaim / spam phrases that must never appear in a generated draft.
# Mirrors scripts/generate_weekly_content_drafts.py BANNED_PHRASES and the
# repo guaranteed-claims perimeter (نضمن / guaranteed / blast).
BANNED_CLAIM_PHRASES: tuple[str, ...] = (
    "نضمن",
    "مضمون",
    "guaranteed roi",
    "ضمان إيراد",
    "نضمن لك",
    "cold blast",
    "blast",
    "واتساب بارد",
    "auto dm",
    "إرسال تلقائي",
    "إرسال جماعي",
)


def channel_allows(channel: str, action: str) -> bool:
    """True only if ``action`` is on the channel's allow-list (deny wins)."""
    policy = CHANNEL_AUTOMATION_POLICY.get(channel.lower())
    if not policy:
        return False
    if action in policy.get("deny", []):
        return False
    return action in policy.get("allow", [])


def assert_distribution_safe(**flags: bool) -> None:
    """Fail-fast guard reused by every generator before writing to a ledger.

    Delegates to the canonical :func:`enforce_doctrine_non_negotiables` so the
    distribution layer can never drift from the repo-wide doctrine. Raises
    ``ValueError`` (callers / routers map to HTTP 403) if any line is crossed.
    """
    enforce_doctrine_non_negotiables(**flags)


def scan_text_for_banned_claims(text: str) -> list[str]:
    """Return the banned phrases present in ``text`` (case-insensitive)."""
    lowered = (text or "").lower()
    return [p for p in BANNED_CLAIM_PHRASES if p.lower() in lowered]


def evidence_level_label(level: int) -> dict[str, Any]:
    """Bilingual label for a 0–5 evidence level (clamped to the valid range)."""
    lev = max(0, min(int(level), 5))
    return {
        "level": lev,
        "code": EvidenceLevel(lev).name,
        "ar": EVIDENCE_LEVEL_DESCRIPTIONS_AR.get(lev, ""),
        "en": EVIDENCE_LEVEL_DESCRIPTIONS_EN.get(lev, ""),
    }


def doctrine_snapshot() -> dict[str, Any]:
    """Machine-readable doctrine block for reports / API / CI."""
    codes, _ = doctrine_violations_for_revenue_intelligence()
    return {
        "operating_mode": OPERATING_MODE,
        "clean": codes == (),
        "channel_policy": CHANNEL_AUTOMATION_POLICY,
        "banned_claim_phrases": list(BANNED_CLAIM_PHRASES),
        "evidence_levels": [evidence_level_label(i) for i in range(6)],
        "public_proof_min_level": int(EvidenceLevel.L4_PUBLIC_APPROVED),
        "statuses": {
            "pending": STATUS_PENDING,
            "approved": STATUS_APPROVED,
            "rejected": STATUS_REJECTED,
            "copied": STATUS_COPIED,
        },
    }


__all__ = [
    "BANNED_CLAIM_PHRASES",
    "CHANNEL_AUTOMATION_POLICY",
    "OPERATING_MODE",
    "STATUS_APPROVED",
    "STATUS_COPIED",
    "STATUS_PENDING",
    "STATUS_REJECTED",
    "assert_distribution_safe",
    "channel_allows",
    "doctrine_snapshot",
    "evidence_level_label",
    "scan_text_for_banned_claims",
]
