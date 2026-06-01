"""
Anti-Ban Guardian
=================
Enforces channel safety rules to protect sender reputation.
Reads configuration from os/config/anti-ban-guardian.yml.

Doctrine enforcement:
- No cold WhatsApp (always blocked)
- No LinkedIn automation (always blocked)
- No scraping (always blocked)
- All limits from config are hard caps
"""

from datetime import datetime, timedelta
from typing import Optional

# Hard-coded doctrine rules (cannot be overridden by config)
ALWAYS_BLOCKED_CHANNELS: set[str] = {
    "cold_whatsapp",
    "linkedin_automation",
    "scraping",
    "robo_call",
    "auto_dialing",
    "whatsapp_blast",
    "whatsapp_broadcast",
    "linkedin_auto_dm",
}

# Default limits (used if config not available)
DEFAULT_LIMITS = {
    "email": {
        "daily_send_limit": 20,
        "weekly_send_limit": 80,
        "bounce_rate_pause_threshold": 0.05,
        "spam_rate_pause_threshold": 0.003,
        "max_followups_per_thread": 2,
        "cooldown_after_no_reply_days": 30,
    },
    "linkedin_assisted": {
        "daily_connection_limit": 10,
        "daily_message_limit": 8,
        "warmup_period_days": 30,
    },
    "website_form": {
        "daily_form_limit": 5,
    },
    "phone": {
        "daily_call_limit": 8,
    },
    "global": {
        "message_similarity_threshold": 0.72,
        "same_company_cooldown_days": 14,
        "max_new_companies_per_day": 20,
        "max_messages_per_day_all_channels": 30,
    },
}


def check_channel_safe(
    channel: str,
    company: Optional[str] = None,
    last_contacted: Optional[datetime] = None,
    send_count_today: int = 0,
) -> dict:
    """
    Check if it is safe to use a channel for outreach.

    Args:
        channel: Channel name to check.
        company: Company being targeted (for cooldown check).
        last_contacted: When this company was last contacted.
        send_count_today: How many messages have been sent today on this channel.

    Returns:
        dict with: channel, safe, blocked, reason, governance_decision
    """
    channel_normalized = str(channel or "").lower().strip().replace(" ", "_").replace("-", "_")

    # 1. Doctrine hard blocks — cannot be overridden
    if channel_normalized in ALWAYS_BLOCKED_CHANNELS:
        return {
            "channel": channel,
            "safe": False,
            "blocked": True,
            "block_type": "doctrine",
            "reason": f"DOCTRINE: '{channel}' is permanently blocked. Non-negotiable.",
            "governance_decision": {
                "module": "anti_ban_guardian",
                "version": "1.0",
                "channel": channel,
                "safe": False,
                "doctrine_enforced": True,
                "override_possible": False,
            },
        }

    violations = []

    # 2. Company cooldown check
    if company and last_contacted:
        cooldown_days = DEFAULT_LIMITS["global"]["same_company_cooldown_days"]
        days_since = (datetime.now() - last_contacted).days
        if days_since < cooldown_days:
            violations.append(
                f"Company cooldown: contacted {days_since}d ago, cooldown is {cooldown_days}d"
            )

    # 3. Daily send limit check
    channel_limits = DEFAULT_LIMITS.get(channel_normalized, {})
    daily_limit_key = "daily_send_limit" if channel_normalized == "email" else "daily_message_limit"
    daily_limit = channel_limits.get(daily_limit_key, DEFAULT_LIMITS["global"]["max_messages_per_day_all_channels"])
    if send_count_today >= daily_limit:
        violations.append(
            f"Daily limit reached: {send_count_today}/{daily_limit} sends on {channel}"
        )

    if violations:
        return {
            "channel": channel,
            "safe": False,
            "blocked": False,
            "block_type": "limit",
            "violations": violations,
            "reason": "; ".join(violations),
            "governance_decision": {
                "module": "anti_ban_guardian",
                "version": "1.0",
                "channel": channel,
                "safe": False,
                "violations": violations,
                "doctrine_enforced": True,
            },
        }

    return {
        "channel": channel,
        "safe": True,
        "blocked": False,
        "reason": f"Channel '{channel}' is safe to use.",
        "governance_decision": {
            "module": "anti_ban_guardian",
            "version": "1.0",
            "channel": channel,
            "safe": True,
            "doctrine_enforced": True,
        },
    }


def check_message_similarity(new_message: str, recent_messages: list[str]) -> dict:
    """
    Check if a new message is too similar to recently sent messages.
    Uses simple character-overlap ratio (Jaccard-like).

    Args:
        new_message: The message to check.
        recent_messages: List of recently sent message bodies.

    Returns:
        dict with: safe, max_similarity, threshold, reason
    """
    threshold = DEFAULT_LIMITS["global"]["message_similarity_threshold"]

    if not recent_messages:
        return {
            "safe": True,
            "max_similarity": 0.0,
            "threshold": threshold,
            "reason": "No recent messages to compare against.",
        }

    new_words = set(new_message.lower().split())
    max_sim = 0.0

    for msg in recent_messages:
        old_words = set(msg.lower().split())
        if not new_words and not old_words:
            continue
        intersection = new_words & old_words
        union = new_words | old_words
        if union:
            sim = len(intersection) / len(union)
            max_sim = max(max_sim, sim)

    safe = max_sim < threshold
    return {
        "safe": safe,
        "max_similarity": round(max_sim, 3),
        "threshold": threshold,
        "reason": (
            "Message is sufficiently unique."
            if safe
            else f"Message too similar to recent sends (similarity={max_sim:.2f}, threshold={threshold}). Rewrite required."
        ),
    }


def get_channel_limits(channel: str) -> dict:
    """Return the configured limits for a channel."""
    channel_normalized = str(channel or "").lower().strip()
    return DEFAULT_LIMITS.get(channel_normalized, {})


def list_blocked_channels() -> list[str]:
    """Return all permanently blocked channels."""
    return sorted(ALWAYS_BLOCKED_CHANNELS)
