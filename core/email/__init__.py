"""Transactional email helpers with explicit external-action gates."""

from core.email.invites import InviteEmailResult, send_invite_email

__all__ = ["InviteEmailResult", "send_invite_email"]
