"""Policy-gated transactional delivery for tenant invitations.

The default is fail-closed: no provider is contacted unless
``EMAIL_ALLOW_LIVE_SEND`` is explicitly enabled. This module may be called from
production code safely while Dealix remains approval-first.
"""

from __future__ import annotations

import html
import os
from dataclasses import dataclass

from core.config.settings import get_settings
from core.logging import get_logger

logger = get_logger(__name__)
_TRUE_VALUES = {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class InviteEmailResult:
    delivered: bool
    blocked_by_policy: bool
    provider: str
    message_id: str | None = None
    error: str | None = None


def live_invite_email_enabled() -> bool:
    """Return true only after an explicit operator opt-in."""
    return os.getenv("EMAIL_ALLOW_LIVE_SEND", "false").strip().lower() in _TRUE_VALUES


def _render_invite_text(*, invited_by_name: str, accept_url: str) -> str:
    return (
        f"دعاك {invited_by_name} للانضمام إلى مساحة عملكم على Dealix.\n"
        f"قبول الدعوة: {accept_url}\n\n"
        "إذا لم تتعرّف على هذه الدعوة فتجاهل الرسالة.\n\n"
        "---\n"
        f"{invited_by_name} invited you to your Dealix workspace.\n"
        f"Accept the invitation: {accept_url}\n"
        "Ignore this message if you do not recognize the invitation.\n"
    )


def _render_invite_html(*, invited_by_name: str, accept_url: str) -> str:
    safe_name = html.escape(invited_by_name, quote=True)
    safe_url = html.escape(accept_url, quote=True)
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<body style="font-family:Arial,sans-serif;line-height:1.7;max-width:560px;margin:32px auto;color:#111827">
  <h2>دعوة للانضمام إلى Dealix</h2>
  <p>دعاك <strong>{safe_name}</strong> للانضمام إلى مساحة عملكم على Dealix.</p>
  <p><a href="{safe_url}" style="display:inline-block;padding:12px 20px;background:#111827;color:#fff;text-decoration:none;border-radius:6px">قبول الدعوة</a></p>
  <p style="font-size:12px;color:#6b7280">إذا لم تتعرّف على هذه الدعوة فتجاهل الرسالة.</p>
  <hr style="border:0;border-top:1px solid #e5e7eb;margin:24px 0">
  <div dir="ltr">
    <h3>You're invited to Dealix</h3>
    <p><strong>{safe_name}</strong> invited you to your Dealix workspace.</p>
    <p><a href="{safe_url}">Accept the invitation</a></p>
  </div>
</body>
</html>"""


async def send_invite_email(
    *,
    to_email: str,
    invited_by_name: str,
    accept_url: str,
) -> InviteEmailResult:
    """Deliver an invite only when the external-action policy is enabled."""
    settings = get_settings()
    if not live_invite_email_enabled():
        logger.info(
            "invite_email_blocked_by_policy",
            recipient_domain=to_email.rsplit("@", 1)[-1] if "@" in to_email else "invalid",
        )
        return InviteEmailResult(
            delivered=False,
            blocked_by_policy=True,
            provider=settings.email_provider,
            error="EMAIL_ALLOW_LIVE_SEND is disabled",
        )

    try:
        from integrations.email import EmailClient

        result = await EmailClient().send(
            to=to_email,
            subject="دعوة Dealix · Dealix invitation",
            body_text=_render_invite_text(
                invited_by_name=invited_by_name,
                accept_url=accept_url,
            ),
            body_html=_render_invite_html(
                invited_by_name=invited_by_name,
                accept_url=accept_url,
            ),
        )
        return InviteEmailResult(
            delivered=result.success,
            blocked_by_policy=False,
            provider=result.provider,
            message_id=result.message_id,
            error=result.error,
        )
    except Exception as exc:  # provider failures must preserve manual fallback
        logger.exception("invite_email_delivery_failed", error_type=type(exc).__name__)
        return InviteEmailResult(
            delivered=False,
            blocked_by_policy=False,
            provider=settings.email_provider,
            error=f"{type(exc).__name__}: {exc}",
        )
