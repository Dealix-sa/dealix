"""PartnerEnablement — onboarding artifacts handed to a new partner."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PartnerEnablement:
    partner_id: str
    package_ids: tuple[str, ...]
    approved_claims: tuple[str, ...]
    playbook_ids: tuple[str, ...]
    sandbox_workspace_id: str
    certification_required: bool
    materials: tuple[str, ...] = field(default_factory=tuple)
