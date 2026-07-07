"""
WhatsApp draft adapter (Evolution API shape) — DRAFT FORMATTING ONLY.

This adapter deliberately has **no send capability**. It formats an approved
message into the payload shape a WhatsApp/Evolution executor *would* accept, so
a founder can review exactly what would go out — but it cannot transmit it.

Guarantees:
- No method here performs any network send. There is no `send`, no HTTP client.
- Every produced payload carries `will_send=false` and `status="draft_only"`.
- Building a draft requires an explicit consent flag from the caller; without
  it, the draft is marked `blocked` (still never sent, just flagged).

Actual sending, if ever enabled, is a separate, independently-audited executor
gated by the platform outbound-safety flags and the Approval Queue.
"""

from __future__ import annotations

import os
from typing import Any

from .base import Adapter, AdapterResult, AdapterStatus


class WhatsAppDraftAdapter(Adapter):
    name = "whatsapp_draft"

    def __init__(self, env: dict[str, str] | None = None) -> None:
        self._env = env if env is not None else dict(os.environ)

    def is_available(self) -> bool:
        # Draft formatting is always available; it needs no external service.
        return True

    def status(self) -> AdapterStatus:
        return AdapterStatus(
            name=self.name,
            available=True,
            mode="draft_only",
            detail="formats WhatsApp payload drafts; no send capability",
        )

    def build_draft(
        self,
        *,
        to_label: str,
        message: str,
        account_id: str | None = None,
        consent_confirmed: bool = False,
    ) -> AdapterResult:
        """Return a review-ready WhatsApp payload draft. Never sends."""
        payload = {
            "channel": "whatsapp",
            "to_label": to_label,  # human label, not a raw number, for review
            "account_id": account_id,
            "message": message,
            "status": "blocked" if not consent_confirmed else "draft_only",
            "will_send": False,
            "requires_founder_approval": True,
            "safety": (
                "This is a draft. It will not be sent. Sending requires founder "
                "approval, confirmed opt-in consent, and a controlled-live executor."
            ),
        }
        if not consent_confirmed:
            payload["block_reason"] = "consent not confirmed for this contact/channel"
            return AdapterResult(
                ok=True,
                mode="draft_only",
                data=payload,
                meta={"note": "draft prepared but flagged blocked pending consent"},
            )
        return AdapterResult(ok=True, mode="draft_only", data=payload)
