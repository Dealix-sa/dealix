"""First-touch marketing attribution — bounded, governed capture for funnel leads.

Attribution is captured client-side (``frontend/src/lib/utm.ts``) on the visitor's
first touch and attached to the public lead payload at submit time. This module
sanitizes that untrusted dict *before* it enters the governed autopilot store:

  * only allow-listed keys survive (standard UTM + common ad-click ids + minimal
    first-touch context) — everything else is dropped;
  * values are coerced to ``str``, stripped, and length-capped, so attribution can
    never become an unbounded data sink.

It performs no external send and adds no PII beyond what the lead form already
collects — it only records *where the lead came from* alongside the existing
governed lead record (Decision Passport / Revenue OS system of record).
"""

from __future__ import annotations

from typing import Any

# Allow-listed attribution keys: standard UTM params + common ad-click identifiers
# + minimal first-touch context. Anything not in this tuple is silently dropped.
ALLOWED_ATTRIBUTION_KEYS: tuple[str, ...] = (
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "gclid",
    "fbclid",
    "msclkid",
    "ttclid",
    "referrer",
    "landing_path",
    "first_seen_at",
)

_MAX_VALUE_LEN = 512


def sanitize_attribution(raw: Any) -> dict[str, str]:
    """Return a bounded ``{key: str}`` dict limited to :data:`ALLOWED_ATTRIBUTION_KEYS`.

    Non-dict input → ``{}``. Values are stringified, stripped, length-capped to
    ``512`` chars, and empty values are dropped. Output key order follows the
    allow-list for stable JSON serialization in the autopilot store.
    """
    if not isinstance(raw, dict):
        return {}
    out: dict[str, str] = {}
    for key in ALLOWED_ATTRIBUTION_KEYS:
        if key not in raw:
            continue
        val = raw.get(key)
        if val is None:
            continue
        text = str(val).strip()[:_MAX_VALUE_LEN]
        if text:
            out[key] = text
    return out


def attribution_summary(attribution: dict[str, str]) -> str:
    """Compact audit string like ``google/cpc/spring-launch`` (``""`` when empty)."""
    parts = [
        attribution.get("utm_source", ""),
        attribution.get("utm_medium", ""),
        attribution.get("utm_campaign", ""),
    ]
    return "/".join(p for p in parts if p)
