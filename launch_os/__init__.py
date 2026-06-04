"""launch_os — Dealix Final Launch Control Tower core library.

This package holds the deterministic, review-only logic behind the
commercial launch control tower:

- lead synthesis from approved verticals (synthetic / placeholder only)
- the 400+ daily draft factory (review-only, never sends)
- the safety / compliance audit
- launch readiness + daily metrics
- the 30-day media & social calendar

Hard rules enforced everywhere in this package (the 11 non-negotiables):

1. Nothing in here sends anything externally. Every artifact is review-only.
2. Every generated draft carries send_allowed=False, external_send_blocked=True,
   no_auto_send=True and requires_founder_approval=True.
3. No secrets, API keys, SMTP, WhatsApp outbound, or LinkedIn automation.
4. No scraping. Leads are synthetic placeholders, not harvested PII.
5. No overclaim language is allowed in any draft body.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "1.0.0"
