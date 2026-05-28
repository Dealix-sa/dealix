"""Invite email helper — bilingual template + doctrine gate.

Doctrine #1 (no_live_send): when settings.email_allow_live_send is False
(the default), this function returns a draft result without contacting
any external provider. The caller must surface invite_token to the
admin who manually shares it.

When EMAIL_ALLOW_LIVE_SEND=1, the call delegates to integrations.email
which already handles Resend / SendGrid / SMTP.

Usage:
    from core.email import send_invite_email
    result = await send_invite_email(
        to_email="dr@hospital.sa",
        invite_token="abc123",
        invited_by_name="Sami",
        accept_url="https://dealix.me/invite?token=abc123",
    )
    if result.delivered:
        ...   # email actually sent
    elif result.blocked_by_policy:
        ...   # founder must hand-deliver the token
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.config.settings import get_settings
from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class InviteEmailResult:
    delivered: bool
    blocked_by_policy: bool
    provider: str
    message_id: str | None = None
    error: str | None = None


def _render_invite_html(
    *, invited_by_name: str, accept_url: str
) -> str:
    """Minimal bilingual HTML — Arabic primary, English fallback."""
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<body style="font-family:-apple-system,sans-serif;line-height:1.6;max-width:520px;margin:32px auto;color:#1a1a1a;">
  <h2 style="margin-top:0;">دعوة للانضمام إلى Dealix</h2>
  <p>دعاك <strong>{invited_by_name}</strong> للانضمام إلى مساحة عملكم على Dealix.</p>
  <p><a href="{accept_url}" style="display:inline-block;padding:12px 24px;background:#0a7;color:#fff;text-decoration:none;border-radius:6px;">قبول الدعوة</a></p>
  <hr style="border:none;border-top:1px solid #ddd;margin:24px 0;">
  <p dir="ltr" style="font-size:14px;color:#666;">
    <strong>You're invited to Dealix.</strong><br>
    {invited_by_name} has invited you to their workspace.<br>
    <a href="{accept_url}">Accept the invitation</a>
  </p>
  <p style="font-size:12px;color:#999;">إذا لم تتعرّف على هذه الدعوة، تجاهل هذه الرسالة.</p>
</body>
</html>"""


def _render_invite_text(
    *, invited_by_name: str, accept_url: str
) -> str:
    return (
        f"دعاك {invited_by_name} للانضمام إلى Dealix.\n"
        f"اقبل الدعوة هنا: {accept_url}\n\n"
        f"---\n"
        f"{invited_by_name} invited you to Dealix.\n"
        f"Accept: {accept_url}\n"
    )


async def send_invite_email(
    *,
    to_email: str,
    invite_token: str,  # noqa: ARG001 — caller embeds in accept_url; kept for audit log
    invited_by_name: str,
    accept_url: str,
) -> InviteEmailResult:
    """Send (or queue, when policy blocks) an invite email.

    Returns InviteEmailResult with delivered/blocked_by_policy flags
    so the caller can decide whether to surface the invite_token to
    the admin for manual sharing.
    """
    settings = get_settings()

    if not settings.email_allow_live_send:
        logger.info(
            "invite_email_blocked_by_policy",
            to_prefix=to_email.split("@")[0][:3],
            reason="EMAIL_ALLOW_LIVE_SEND=False",
        )
        return InviteEmailResult(
            delivered=False,
            blocked_by_policy=True,
            provider=settings.email_provider,
            error="email_allow_live_send=False — share invite_token manually",
        )

    try:
        # Lazy import — avoids httpx/tenacity overhead in test envs that
        # never need to send mail.
        from integrations.email import EmailClient

        client = EmailClient()
        result = await client.send(
            to=to_email,
            subject="دعوة Dealix · Dealix invitation",
            body_text=_render_invite_text(
                invited_by_name=invited_by_name, accept_url=accept_url
            ),
            body_html=_render_invite_html(
                invited_by_name=invited_by_name, accept_url=accept_url
            ),
        )
        return InviteEmailResult(
            delivered=result.success,
            blocked_by_policy=False,
            provider=result.provider,
            message_id=result.message_id,
            error=result.error,
        )
    except Exception as exc:
        logger.exception("invite_email_send_failed")
        return InviteEmailResult(
            delivered=False,
            blocked_by_policy=False,
            provider=settings.email_provider,
            error=f"{type(exc).__name__}: {exc}",
        )


def _public_api_summary() -> dict[str, Any]:
    """Return a summary safe for inclusion in /api/v1/auth/invite responses."""
    settings = get_settings()
    return {
        "email_provider": settings.email_provider,
        "email_allow_live_send": settings.email_allow_live_send,
    }
