"""Signed list of approved claims partners may use about Dealix."""

from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass, field


def _secret() -> bytes:
    return os.environ.get("DEALIX_HERMES_SECRET", "dealix-hermes-dev-secret").encode("utf-8")


@dataclass(frozen=True)
class ApprovedClaim:
    claim_id: str
    text: str
    evidence_pack_id: str
    signature: str


_CLAIMS: dict[str, ApprovedClaim] = {}


def _sign(claim_id: str, text: str, evidence_pack_id: str) -> str:
    msg = f"{claim_id}|{text}|{evidence_pack_id}".encode("utf-8")
    return hmac.new(_secret(), msg, hashlib.sha256).hexdigest()


def approve(claim_id: str, text: str, evidence_pack_id: str) -> ApprovedClaim:
    """Register an approved claim, signed with HMAC and bound to an evidence_pack_id."""
    if not evidence_pack_id:
        raise ValueError("evidence_pack_id required for any approved claim")
    claim = ApprovedClaim(
        claim_id=claim_id,
        text=text,
        evidence_pack_id=evidence_pack_id,
        signature=_sign(claim_id, text, evidence_pack_id),
    )
    _CLAIMS[claim_id] = claim
    return claim


def is_approved(claim_id: str, text: str) -> bool:
    """Return True when (claim_id, text) matches the signed registry."""
    claim = _CLAIMS.get(claim_id)
    if claim is None or claim.text != text:
        return False
    expected = _sign(claim.claim_id, claim.text, claim.evidence_pack_id)
    return hmac.compare_digest(expected, claim.signature)


def reset() -> None:
    """Clear the approved-claims registry (test helper)."""
    _CLAIMS.clear()
