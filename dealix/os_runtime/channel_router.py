"""
Channel Router
==============
Selects the best outreach channel(s) for a given company profile.
Enforces anti-ban and doctrine rules: no cold WhatsApp, no LinkedIn automation.
"""

from typing import Optional


# Channel definitions with allowed/blocked rules
CHANNEL_RULES: dict[str, dict] = {
    "email": {
        "allowed": True,
        "requires_approval": True,
        "auto_send": False,
        "note": "Formal email — draft prepared, founder approves before send",
    },
    "website_form": {
        "allowed": True,
        "requires_approval": True,
        "auto_send": False,
        "note": "Website contact form — founder reviews content before submit",
    },
    "phone_intro": {
        "allowed": True,
        "requires_approval": True,
        "auto_send": False,
        "note": "Phone call — founder makes the call; agent prepares brief",
    },
    "referral": {
        "allowed": True,
        "requires_approval": False,
        "auto_send": False,
        "note": "Referral via warm contact — no cold outreach risk",
    },
    "linkedin_assisted": {
        "allowed": True,
        "requires_approval": True,
        "auto_send": False,
        "note": "LinkedIn — MANUAL send by founder only; no automation",
    },
    "executive_email": {
        "allowed": True,
        "requires_approval": True,
        "auto_send": False,
        "note": "Executive-level email — high personalization, founder approves",
    },
    "partner_referral": {
        "allowed": True,
        "requires_approval": False,
        "auto_send": False,
        "note": "Via established partner — pre-approved channel",
    },
    # Blocked channels — doctrine non-negotiables
    "cold_whatsapp": {
        "allowed": False,
        "requires_approval": False,
        "auto_send": False,
        "blocked_reason": "DOCTRINE: No cold WhatsApp automation. Non-negotiable.",
    },
    "linkedin_automation": {
        "allowed": False,
        "requires_approval": False,
        "auto_send": False,
        "blocked_reason": "DOCTRINE: No LinkedIn automation. Non-negotiable.",
    },
    "scraping": {
        "allowed": False,
        "requires_approval": False,
        "auto_send": False,
        "blocked_reason": "DOCTRINE: No scraping systems. Non-negotiable.",
    },
}

# Profile-based routing: sector → channel preference order
SECTOR_CHANNEL_MAP: dict[str, list[str]] = {
    "legal": ["referral", "email", "website_form"],
    "legal_local_arabic": ["website_form", "email", "referral"],
    "facilities_management": ["email", "phone_intro", "linkedin_assisted"],
    "maintenance": ["email", "phone_intro", "linkedin_assisted"],
    "contracting": ["email", "linkedin_assisted", "phone_intro"],
    "consulting": ["linkedin_assisted", "executive_email", "referral"],
    "real_estate": ["email", "phone_intro", "linkedin_assisted"],
    "international": ["linkedin_assisted", "executive_email", "partner_referral"],
    "international_company": ["linkedin_assisted", "executive_email", "partner_referral"],
    "b2b_services": ["email", "linkedin_assisted", "phone_intro"],
    "accounting": ["referral", "email", "website_form"],
    "healthcare_admin": ["email", "website_form", "phone_intro"],
}

# Country-specific overrides
COUNTRY_CHANNEL_PREFERENCES: dict[str, list[str]] = {
    "ksa": ["email", "website_form", "phone_intro", "referral", "linkedin_assisted"],
    "uae": ["linkedin_assisted", "executive_email", "partner_referral", "email"],
    "qatar": ["email", "referral", "linkedin_assisted"],
    "kuwait": ["email", "referral", "phone_intro"],
    "bahrain": ["email", "linkedin_assisted", "referral"],
    "oman": ["email", "website_form", "referral"],
}

_DEFAULT_CHANNELS = ["email", "website_form", "phone_intro"]


def _normalize(val: str) -> str:
    return str(val or "").lower().strip().replace(" ", "_")


def route_channels(company: dict) -> dict:
    """
    Select ranked channels for a company profile.

    Args:
        company: dict with optional 'sector', 'country', 'inbound' keys.

    Returns:
        dict with: company, sector, country, recommended_channels,
                   blocked_channels, primary_channel, governance_decision
    """
    sector = _normalize(company.get("sector", ""))
    country = _normalize(company.get("country", ""))
    is_inbound = bool(company.get("inbound", False))

    # Inbound opt-in leads can use more channels
    if is_inbound:
        channels = ["email", "phone_intro", "linkedin_assisted", "referral"]
        note = "Inbound lead — full channel set available with approval"
    else:
        # Try sector routing, then country, then default
        channels = (
            SECTOR_CHANNEL_MAP.get(sector)
            or COUNTRY_CHANNEL_PREFERENCES.get(country)
            or _DEFAULT_CHANNELS
        )
        note = f"Sector routing: {sector}" if sector in SECTOR_CHANNEL_MAP else f"Country routing: {country}"

    # Verify all channels are allowed
    allowed = [c for c in channels if CHANNEL_RULES.get(c, {}).get("allowed", False)]
    blocked_attempted = [c for c in channels if not CHANNEL_RULES.get(c, {}).get("allowed", True)]

    # Always block cold channels
    always_blocked = ["cold_whatsapp", "linkedin_automation", "scraping"]

    primary = allowed[0] if allowed else "email"

    return {
        "company": company.get("company") or company.get("name") or "",
        "sector": sector or "unknown",
        "country": country or "unknown",
        "recommended_channels": allowed,
        "primary_channel": primary,
        "blocked_channels": always_blocked,
        "channel_note": note,
        "requires_founder_approval": True,
        "governance_decision": {
            "module": "channel_router",
            "version": "1.0",
            "inbound": is_inbound,
            "channels_selected": allowed,
            "always_blocked": always_blocked,
            "doctrine_enforced": True,
        },
    }


def check_channel_allowed(channel: str) -> dict:
    """Check if a specific channel is allowed under doctrine."""
    normalized = _normalize(channel)
    rule = CHANNEL_RULES.get(normalized)
    if rule is None:
        return {
            "channel": channel,
            "allowed": False,
            "reason": "Unknown channel — not in approved channel list",
        }
    return {
        "channel": channel,
        "allowed": rule["allowed"],
        "requires_approval": rule.get("requires_approval", True),
        "note": rule.get("note") or rule.get("blocked_reason", ""),
    }
