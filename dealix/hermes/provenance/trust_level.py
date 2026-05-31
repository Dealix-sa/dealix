"""
Trust levels for provenance sources.
"""

from __future__ import annotations

from enum import StrEnum


class TrustLevel(StrEnum):
    TRUSTED = "trusted"          # internal Dealix workflows, signed artifacts
    VERIFIED = "verified"        # vetted partner sources / signed manifests
    UNTRUSTED = "untrusted"      # external websites, raw user input, scrapes
    QUARANTINED = "quarantined"  # flagged by detector — never used as instructions


# Sources that ship trusted-by-default. Everything else starts UNTRUSTED.
_TRUSTED_SOURCES = frozenset(
    {
        "dealix_internal",
        "dealix_approved_kb",
        "dealix_audit_log",
        "dealix_signed_artifact",
    }
)
_VERIFIED_SOURCES = frozenset(
    {
        "partner_signed_feed",
        "customer_supplied_signed",
    }
)


def score_trust_level(source: str) -> TrustLevel:
    if source in _TRUSTED_SOURCES:
        return TrustLevel.TRUSTED
    if source in _VERIFIED_SOURCES:
        return TrustLevel.VERIFIED
    return TrustLevel.UNTRUSTED
