"""Hermes tool registry seeds.

Whitelisted tools the Hermes agents may request. Sensitivity is one of
`low`, `medium`, `high`. Tools flagged `requires_approval` must travel
through the approval gate before any external side effect.
"""

from __future__ import annotations

from typing import Any

TOOLS: list[dict[str, Any]] = [
    {
        "id": "lead_lookup",
        "description": (
            "Read-only lookup of stored leads by id, account, or ICP "
            "fingerprint."
        ),
        "sensitivity": "low",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "crm_write_draft",
        "description": (
            "Create or update draft CRM records. Drafts only — promoting "
            "to live requires founder approval."
        ),
        "sensitivity": "medium",
        "owner": "founder",
        "requires_approval": True,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "email_draft_only",
        "description": (
            "Compose email drafts. Sending is explicitly out of scope; "
            "drafts route through transactional whitelist or founder."
        ),
        "sensitivity": "medium",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "whatsapp_draft_only",
        "description": (
            "Compose WhatsApp message drafts for warm threads. Cold "
            "WhatsApp is forbidden by doctrine."
        ),
        "sensitivity": "high",
        "owner": "founder",
        "requires_approval": True,
        "allowed_actor_kinds": ["internal_user", "founder"],
    },
    {
        "id": "calendar_read",
        "description": "Read availability windows from the founder calendar.",
        "sensitivity": "low",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "pricing_lookup",
        "description": (
            "Read offer pricing bands from the offer registry."
        ),
        "sensitivity": "low",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "partner_lookup",
        "description": (
            "Read-only lookup of registered partners and revenue share "
            "terms."
        ),
        "sensitivity": "low",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "invoice_lookup_readonly",
        "description": (
            "Read-only access to invoice metadata and payment confirms "
            "for revenue verification."
        ),
        "sensitivity": "medium",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "market_signal_pull",
        "description": (
            "Pull pre-approved market signals (intake events, public "
            "sources) registered via SourcePassport only."
        ),
        "sensitivity": "medium",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
    {
        "id": "evidence_pack_read",
        "description": (
            "Read assembled ProofPacks and supporting evidence for "
            "trust evaluation."
        ),
        "sensitivity": "low",
        "owner": "founder",
        "requires_approval": False,
        "allowed_actor_kinds": ["agent", "internal_user", "founder"],
    },
]


__all__ = ["TOOLS"]
