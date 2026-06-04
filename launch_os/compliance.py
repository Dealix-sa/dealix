"""Shared compliance primitives: forbidden claims and external-send terms.

These lists are the single source of truth used by the draft factory,
the safety audit, the site static check, and the secret/risk scanner.
"""

from __future__ import annotations

import re

# Overclaim / exaggerated marketing language that must never appear in any
# customer-facing draft, page, or proposal. Lowercased for case-insensitive
# substring matching.
FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "guaranteed roi",
    "guaranteed results",
    "guaranteed revenue",
    "100% guaranteed",
    "replace your team",
    "replace your sales team",
    "automate everything",
    "fully automated sales",
    "no human needed",
    "no humans needed",
    "zero effort",
    "instant millions",
    "get rich",
)

# A narrower set used for website copy where a bare "100%" is also disallowed.
SITE_FORBIDDEN_CLAIMS: tuple[str, ...] = FORBIDDEN_CLAIMS + (
    "100%",
)

# Terms that indicate real external sending / outbound automation. Their
# presence in *new commercial-launch code* is a hard failure — the whole
# system is review-only. We match on identifier-ish patterns to avoid
# flagging documentation prose that merely names the prohibition.
EXTERNAL_SEND_PATTERNS: tuple[str, ...] = (
    r"smtplib",
    r"smtp\.send",
    r"sendmail\s*\(",
    r"send_email\s*\(",
    r"send_whatsapp\s*\(",
    r"whatsapp[._]send",
    r"twilio\.",
    r"linkedin[._](?:send|connect|invite|automation)",
    r"requests\.post\([^)]*(?:mail|whatsapp|linkedin)",
    r"\.send_message\s*\(",
)


def find_forbidden_claims(text: str, claims: tuple[str, ...] = FORBIDDEN_CLAIMS) -> list[str]:
    """Return the list of forbidden claim phrases found in ``text``."""
    low = text.lower()
    return [c for c in claims if c in low]


def find_external_send(text: str) -> list[str]:
    """Return external-send code patterns found in ``text``."""
    hits: list[str] = []
    for pat in EXTERNAL_SEND_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            hits.append(pat)
    return hits
