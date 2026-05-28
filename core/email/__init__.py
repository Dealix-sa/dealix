"""Transactional email helpers — wrap integrations/email.py with doctrine
policy gates (no_live_send) and bilingual templates."""

from core.email.invites import send_invite_email

__all__ = ["send_invite_email"]
