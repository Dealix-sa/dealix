"""Assisted social publishing handoff — via n8n, founder-owned, OFF by default.

Dealix never calls LinkedIn / X APIs and never holds their credentials.
After the founder APPROVES a social post in the queue, this client hands
the post to n8n (``integrations/n8n.py``), where the founder owns the
LinkedIn / X connections. Publishing is gated on
``settings.social_publish_allow_live`` (default False) — the same pattern
as ``whatsapp_allow_live_send``.

``export_approved_post_to_file`` is the always-available manual fallback:
it writes the approved post to a markdown file the founder can copy-paste.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from core.config.settings import get_settings
from core.logging import get_logger
from integrations.n8n import N8NClient

logger = get_logger(__name__)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_EXPORT_DIR = _REPO_ROOT / "docs" / "ops" / "social_drafts"
_PUBLISH_EVENT = "social_post_approved"


@dataclass
class SocialPublishResult:
    success: bool
    handoff: str | None = None  # "n8n" | "file_export"
    error: str | None = None
    detail: dict[str, Any] | None = None


class SocialPublishClient:
    """Hands an APPROVED social post to n8n. Never publishes directly."""

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return bool(self.settings.n8n_webhook_url)

    async def publish_approved_post(
        self,
        *,
        approval_request: ApprovalRequest,
        platform: str,
        locale: str,
        body_ar: str,
        body_en: str,
    ) -> SocialPublishResult:
        """Hand an approved post to n8n. Gated, approval-checked, audited."""
        # Gate 1 — live flag. Checked FIRST, before any other work.
        if not self.settings.social_publish_allow_live:
            logger.info("social_publish_blocked_by_policy", platform=platform)
            return SocialPublishResult(
                success=False, error="social_publish_allow_live_false"
            )
        # Gate 2 — n8n must be configured (founder owns the connectors there).
        if not self.configured:
            return SocialPublishResult(
                success=False, error="n8n_webhook_url not configured"
            )
        # Gate 3 — the post must be founder-approved.
        if ApprovalStatus(approval_request.status) != ApprovalStatus.APPROVED:
            logger.info(
                "social_publish_blocked_not_approved",
                approval_id=approval_request.approval_id,
                status=str(approval_request.status),
            )
            return SocialPublishResult(success=False, error="post_not_approved")

        result = await N8NClient().send_event(
            _PUBLISH_EVENT,
            {
                "platform": platform,
                "locale": locale,
                "body_ar": body_ar,
                "body_en": body_en,
                "approval_id": approval_request.approval_id,
            },
        )
        if result.success:
            logger.info(
                "social_publish_handed_off",
                platform=platform,
                approval_id=approval_request.approval_id,
            )
            return SocialPublishResult(success=True, handoff="n8n")
        return SocialPublishResult(
            success=False, handoff="n8n", error=result.error
        )

    def export_approved_post_to_file(
        self,
        *,
        approval_request: ApprovalRequest,
        platform: str,
        body_ar: str,
        body_en: str,
    ) -> SocialPublishResult:
        """Manual fallback — write the approved post to a markdown file.

        Always available; never gated. The founder posts it by hand.
        """
        _EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        path = _EXPORT_DIR / f"{today}_{approval_request.approval_id}.md"
        content = (
            f"# Social post — {platform} — {today}\n\n"
            f"Approval: {approval_request.approval_id}\n\n"
            f"## العربية\n\n{body_ar}\n\n"
            f"## English\n\n{body_en}\n"
        )
        path.write_text(content, encoding="utf-8")
        logger.info("social_publish_exported", path=str(path), platform=platform)
        return SocialPublishResult(
            success=True, handoff="file_export", detail={"path": str(path)}
        )


__all__ = ["SocialPublishClient", "SocialPublishResult"]
