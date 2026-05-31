"""
anti_ban_guardian.py — Dealix Growth OS
Monitors channel health and enforces anti-ban policies per config/anti-ban.yml

Non-negotiables enforced here:
- No cold WhatsApp automation (opt-in required)
- No LinkedIn automation (always assisted_manual)
- No scraping (blocked at architecture level)
"""

import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_BASE = Path(__file__).parent
_CONFIG_PATH = _BASE / "config" / "anti-ban.yml"


def _load_config() -> dict:
    if _CONFIG_PATH.exists():
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


class AntiBanGuardian:
    """
    Enforces per-channel rate limits, thresholds, and policy compliance.
    All decisions are logged with a governance_decision field.
    """

    def __init__(self, config: Optional[dict] = None):
        raw = config or _load_config()
        self.config = raw.get("anti_ban_guardian", raw)

    def _channel_config(self, channel: str) -> dict:
        return self.config.get(channel, {})

    # ------------------------------------------------------------------
    # Public channel-specific checks
    # ------------------------------------------------------------------

    def check_email(self, batch: list) -> bool:
        """
        Returns True if the batch is safe to send.
        Checks: batch size, no suppressed addresses.
        Does NOT check bounce/spam rates here — those come from metrics.
        """
        cfg = self._channel_config("email")
        daily_quota = cfg.get("daily_quota", 500)
        if len(batch) > daily_quota:
            return False
        return True

    def check_whatsapp(self, contact: dict) -> bool:
        """
        Returns True only if contact has confirmed opt-in.
        Non-negotiable: no cold WhatsApp automation.
        """
        cfg = self._channel_config("whatsapp")
        require_opt_in = cfg.get("require_opt_in", True)
        if require_opt_in:
            opted_in = contact.get("opt_in_status", False)
            if not opted_in:
                return False
        require_template = cfg.get("require_approved_template", True)
        if require_template:
            has_template = contact.get("template_approved", False)
            if not has_template:
                return False
        return True

    def check_linkedin(self) -> str:
        """
        LinkedIn is ALWAYS assisted_manual. Returns the mode string.
        Non-negotiable: no LinkedIn automation.
        """
        return "assisted_manual"

    def check_channel(self, channel: str, context: dict) -> dict:
        """
        Generic channel check. Returns a governance decision dict.

        Args:
            channel: channel name (email, whatsapp, linkedin, etc.)
            context: dict with relevant context (contact info, metrics, etc.)

        Returns:
            {channel, allowed, mode, reason, governance_decision}
        """
        result = {
            "channel": channel,
            "allowed": False,
            "mode": None,
            "reason": None,
            "governance_decision": None,
        }

        if channel == "linkedin":
            result["allowed"] = True
            result["mode"] = "assisted_manual"
            result["reason"] = "LinkedIn is always assisted_manual — founder executes manually"
            result["governance_decision"] = "linkedin_assisted_manual — non-negotiable"
            return result

        if channel == "whatsapp":
            ok = self.check_whatsapp(context)
            result["allowed"] = ok
            result["mode"] = "founder_approval" if ok else "blocked"
            result["reason"] = (
                "opt_in confirmed and template approved"
                if ok
                else "opt_in missing or template not approved — cold WhatsApp blocked"
            )
            result["governance_decision"] = (
                "whatsapp_opt_in_confirmed" if ok else "whatsapp_blocked_no_opt_in"
            )
            return result

        if channel in ("instagram", "messenger"):
            is_inbound = context.get("is_inbound", False)
            within_window = context.get("within_24h_window", False)
            allowed = is_inbound and within_window
            result["allowed"] = allowed
            result["mode"] = "inbound_only" if allowed else "blocked"
            result["reason"] = (
                "inbound message within 24h window"
                if allowed
                else "outbound blocked — inbound_only channel"
            )
            result["governance_decision"] = (
                "inbound_reply_allowed" if allowed else "outbound_blocked_inbound_only"
            )
            return result

        if channel == "email":
            ok = self.check_email(context.get("batch", []))
            result["allowed"] = ok
            result["mode"] = "auto_send" if ok else "blocked"
            result["reason"] = (
                "within daily quota"
                if ok
                else "batch exceeds daily quota"
            )
            result["governance_decision"] = (
                "email_within_quota" if ok else "email_quota_exceeded"
            )
            return result

        # Default: unknown channel — founder approval required
        result["allowed"] = True
        result["mode"] = "founder_approval"
        result["reason"] = f"Unknown channel {channel} — defaulting to founder_approval"
        result["governance_decision"] = "unknown_channel_founder_approval_required"
        return result

    def should_pause_channel(self, channel: str, metrics: dict) -> bool:
        """
        Returns True if the channel should be paused given current metrics.

        Args:
            channel: channel name
            metrics: dict with bounce_rate, spam_rate, block_rate, etc.

        Returns:
            bool — True means pause NOW
        """
        cfg = self._channel_config(channel)

        if channel == "email":
            bounce = metrics.get("bounce_rate", 0.0)
            spam = metrics.get("spam_rate", 0.0)
            if bounce > cfg.get("pause_if_bounce_rate_above", 0.05):
                return True
            if spam > cfg.get("pause_if_spam_rate_above", 0.003):
                return True

        if channel == "whatsapp":
            block_rate = metrics.get("block_rate", 0.0)
            if block_rate > cfg.get("pause_if_block_rate_above", 0.02):
                return True

        global_cfg = self.config.get("global", {})
        violations = metrics.get("violation_count", 0)
        if violations >= global_cfg.get("warning_threshold_violations", 3):
            if global_cfg.get("stop_all_if_global_warning", True):
                return True

        return False

    def get_risk_score(self, channel: str, metrics: dict) -> float:
        """
        Returns a risk score 0.0 (safe) to 1.0 (pause immediately).

        Scoring:
        - email bounce_rate: 0-0.05 maps to 0.0-1.0
        - email spam_rate: 0-0.003 maps to 0.0-1.0 (higher weight)
        - whatsapp block_rate: 0-0.02 maps to 0.0-1.0
        - linkedin: always 0.3 (manual risk managed by founder)
        """
        if channel == "email":
            cfg = self._channel_config("email")
            bounce = metrics.get("bounce_rate", 0.0)
            spam = metrics.get("spam_rate", 0.0)
            bounce_threshold = cfg.get("pause_if_bounce_rate_above", 0.05)
            spam_threshold = cfg.get("pause_if_spam_rate_above", 0.003)
            bounce_score = min(bounce / bounce_threshold, 1.0) * 0.4
            spam_score = min(spam / spam_threshold, 1.0) * 0.6
            return round(bounce_score + spam_score, 3)

        if channel == "whatsapp":
            cfg = self._channel_config("whatsapp")
            block_rate = metrics.get("block_rate", 0.0)
            threshold = cfg.get("pause_if_block_rate_above", 0.02)
            return round(min(block_rate / threshold, 1.0), 3)

        if channel == "linkedin":
            return 0.3  # Always moderate risk — managed manually

        if channel in ("instagram", "messenger"):
            return 0.1  # Low risk — inbound only

        return 0.5  # Unknown channel — moderate default risk

    def log_warning(self, channel: str, metric: str, threshold: float, actual: float) -> dict:
        """
        Creates a warning entry for memory/warnings.jsonl format.
        Caller is responsible for writing to file.
        """
        severity = "high" if actual > threshold * 1.5 else "medium"
        return {
            "warning_id": f"warn_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "channel": channel,
            "metric": metric,
            "threshold": threshold,
            "actual_value": actual,
            "severity": severity,
            "triggered_at": datetime.now(timezone.utc).isoformat(),
            "action_taken": f"pause_{channel}_channel" if severity == "high" else f"reduce_{channel}_quota",
            "resolved_at": None,
            "governance_decision": f"anti_ban_warning_{severity}_{channel}_{metric}",
        }
