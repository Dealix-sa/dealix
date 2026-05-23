"""
Evidence Pack — manifest for any A3 (public claim) action.

A claim that reaches a public surface (LinkedIn, web, case study, proposal)
must point to an evidence pack on file. This module produces and validates
the manifest format described in `docs/trust/CLAIMS_GUIDE.md` and
`docs/content/PROOF_LIBRARY.md`.

The manifest is intentionally small and human-readable. The pack itself
(sources, methodology) is markdown in the proof library; this module
only validates that the required pieces exist.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class EvidencePack:
    pack_id: str
    claim_text: str
    sources: list[str] = field(default_factory=list)  # URLs / internal references
    methodology: str = ""
    sanitization_notes: str = ""
    approver: str = ""
    approved_at: datetime | None = None
    notes: str = ""

    def is_complete(self) -> bool:
        return all(
            [
                self.pack_id,
                self.claim_text.strip(),
                len(self.sources) >= 1,
                self.methodology.strip(),
                self.approver,
                self.approved_at is not None,
            ]
        )

    def missing_fields(self) -> list[str]:
        missing: list[str] = []
        if not self.pack_id:
            missing.append("pack_id")
        if not self.claim_text.strip():
            missing.append("claim_text")
        if not self.sources:
            missing.append("sources (need at least 1)")
        if not self.methodology.strip():
            missing.append("methodology")
        if not self.approver:
            missing.append("approver")
        if self.approved_at is None:
            missing.append("approved_at")
        return missing


def new_pack(pack_id: str, claim_text: str) -> EvidencePack:
    """Start a new evidence pack scaffold."""
    return EvidencePack(pack_id=pack_id, claim_text=claim_text)


def approve(pack: EvidencePack, approver: str) -> EvidencePack:
    """Mark a pack as approved by `approver` at the current time."""
    pack.approver = approver
    pack.approved_at = datetime.now(UTC)
    return pack


def assert_complete(pack: EvidencePack) -> None:
    """Raise ValueError if the pack is not complete enough to back an A3 claim."""
    if not pack.is_complete():
        raise ValueError(
            f"Evidence pack {pack.pack_id!r} is incomplete: missing {pack.missing_fields()}"
        )


__all__ = [
    "EvidencePack",
    "approve",
    "assert_complete",
    "new_pack",
]
