"""Dealix Commercial Launch Operating System.

A review-only daily draft factory for the Saudi/GCC B2B market.

Hard guarantees enforced across this package:
  * The system NEVER sends anything externally (no SMTP, no API send,
    no browser automation, no scraping).
  * Every generated draft carries send_allowed=False,
    external_send_blocked=True and requires_founder_approval=True.
  * The founder reviews and sends manually. Nothing here is autonomous outreach.
"""

from __future__ import annotations

__all__ = [
    "engine",
    "safety",
    "review",
    "readiness",
    "leads",
]
