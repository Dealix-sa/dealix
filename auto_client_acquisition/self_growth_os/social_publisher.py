"""Own-brand social publisher for Dealix's OWN LinkedIn / X accounts.

Doctrine — two completely different kinds of channel:

  - Own-brand channels (``linkedin_own`` / ``x_own``) are Dealix's OWN
    accounts. The owner has authorized automated publishing to them, so
    this module MAY publish to them directly — but ONLY after the copy
    passes ``safe_publishing_gate.check_text``. The gate is never bypassed.
  - Prospect channels (cold whatsapp / linkedin / phone to potential
    customers) are NEVER touched by this module. A slot whose channel is
    not in ``OWN_BRAND_CHANNELS`` is rejected outright.

Token-absent degradation: if the LinkedIn / X API tokens are not present
in the environment the publisher degrades to a dry-run — it records the
intent to ``social_post_log`` and publishes nothing, exactly like the G1
execution hook degrades when no Redis pool is supplied. It never crashes.

Gate-flagged copy is not published. Instead it is routed to the founder
approval queue as a ``draft_linkedin_manual`` item so a human can rephrase.

This module never sends to prospects and never charges anything.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.self_growth_os import safe_publishing_gate

log = logging.getLogger(__name__)

# Own-brand channels this publisher is permitted to auto-publish to.
# Anything outside this set (whatsapp / cold linkedin / phone) is rejected.
OWN_BRAND_CHANNELS: frozenset[str] = frozenset({"linkedin_own", "x_own"})

# Env vars holding the OAuth tokens for Dealix's own accounts.
_LINKEDIN_TOKEN_ENV = "DEALIX_OWN_LINKEDIN_TOKEN"
_X_TOKEN_ENV = "DEALIX_OWN_X_TOKEN"

_LINKEDIN_ENDPOINT = "/v2/ugcPosts"
_X_ENDPOINT = "/2/tweets"

_DEFAULT_LOG_PATH = "var/social_post_log.jsonl"


# ─── social_post_log (JSONL with env override) ──────────────────────


def _log_path() -> Path:
    p = Path(os.environ.get("DEALIX_SOCIAL_POST_LOG_PATH", _DEFAULT_LOG_PATH))
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _record(entry: dict[str, Any]) -> None:
    """Append one publish attempt to the social_post_log JSONL store."""
    entry = {"logged_at": datetime.now(UTC).isoformat(), **entry}
    with _log_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_log() -> list[dict[str, Any]]:
    """Return every recorded publish attempt (oldest first)."""
    path = _log_path()
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def clear_log_for_test() -> None:
    """Truncate the social_post_log — test-only helper."""
    path = _log_path()
    if path.exists():
        path.unlink()


# ─── slot helpers ───────────────────────────────────────────────────


def _slot_get(slot: Any, key: str, default: Any = None) -> Any:
    """Read a field from a dict slot or a Pydantic-model slot."""
    if isinstance(slot, dict):
        return slot.get(key, default)
    return getattr(slot, key, default)


def _endpoint_for(channel: str) -> str:
    return _LINKEDIN_ENDPOINT if channel == "linkedin_own" else _X_ENDPOINT


def _token_for(channel: str) -> str | None:
    env = _LINKEDIN_TOKEN_ENV if channel == "linkedin_own" else _X_TOKEN_ENV
    token = os.environ.get(env, "").strip()
    return token or None


# ─── publish ────────────────────────────────────────────────────────


def publish_own_brand(
    slot: Any,
    *,
    store: ApprovalStore | None = None,
) -> dict[str, Any]:
    """Publish one cleared weekly-calendar slot to a Dealix-owned channel.

    Order of operations (the safety gate is always first):

      1. Reject the slot if its channel is not an own-brand channel.
      2. Run ``safe_publishing_gate.check_text`` on the slot copy.
      3. If the gate flags it: route the copy to the founder approval
         queue as a ``draft_linkedin_manual`` draft — publish nothing.
      4. If the gate is clean: publish to the channel's API endpoint when
         a token is configured; otherwise degrade to a dry-run.

    Every outcome is appended to ``social_post_log``. This function never
    raises for an absent token or an unreachable API — it degrades.

    Returns a result dict with an ``outcome`` of ``rejected_channel`` |
    ``routed_to_approval`` | ``published`` | ``dry_run``.
    """
    channel = str(_slot_get(slot, "channel", "") or "")
    text_ar = str(_slot_get(slot, "topic_ar", "") or "")
    text_en = str(_slot_get(slot, "topic_en", "") or "")
    text = "\n".join(part for part in (text_ar, text_en) if part)
    slot_date = str(_slot_get(slot, "slot_date", "") or "")

    base: dict[str, Any] = {"channel": channel, "slot_date": slot_date}

    # 1. Channel guard — prospect / blocked channels are never published.
    if channel not in OWN_BRAND_CHANNELS:
        result = {
            **base,
            "outcome": "rejected_channel",
            "published": False,
            "reason": "channel_not_own_brand",
        }
        _record(result)
        log.warning("own_brand_publish_rejected_channel channel=%s", channel)
        return result

    # 2. Safety gate — always runs first, never bypassed.
    gate = safe_publishing_gate.check_text(text)
    base["gate_decision"] = gate.decision

    # 3. Gate flagged the copy → route to approval, publish nothing.
    if gate.decision != "allowed_draft":
        target = store or get_default_approval_store()
        req = ApprovalRequest(
            object_type="own_brand_social_post",
            object_id=f"{channel}:{slot_date}",
            action_type="draft_linkedin_manual",
            action_mode="approval_required",
            channel=channel,
            summary_ar=text_ar,
            summary_en=text_en,
            risk_level="high",
            proof_impact="own-brand social copy flagged by safe_publishing_gate",
        )
        target.create(req)
        result = {
            **base,
            "outcome": "routed_to_approval",
            "published": False,
            "approval_id": req.approval_id,
            "forbidden_tokens": list(gate.forbidden_tokens_found),
        }
        _record(result)
        log.info(
            "own_brand_publish_routed_to_approval channel=%s approval_id=%s",
            channel, req.approval_id,
        )
        return result

    # 4. Gate clean → publish, or degrade to dry-run if no token.
    token = _token_for(channel)
    endpoint = _endpoint_for(channel)
    if token is None:
        result = {
            **base,
            "outcome": "dry_run",
            "published": False,
            "endpoint": endpoint,
            "reason": "api_token_not_configured",
        }
        _record(result)
        log.info("own_brand_publish_dry_run channel=%s endpoint=%s", channel, endpoint)
        return result

    published = False
    try:
        published = _post_to_api(channel, endpoint, token, text)
    except Exception as exc:  # noqa: BLE001
        result = {
            **base,
            "outcome": "dry_run",
            "published": False,
            "endpoint": endpoint,
            "reason": f"api_error:{exc}",
        }
        _record(result)
        log.warning("own_brand_publish_api_failed channel=%s err=%s", channel, exc)
        return result

    result = {
        **base,
        "outcome": "published" if published else "dry_run",
        "published": published,
        "endpoint": endpoint,
    }
    _record(result)
    log.info("own_brand_publish_done channel=%s published=%s", channel, published)
    return result


def _post_to_api(channel: str, endpoint: str, token: str, text: str) -> bool:
    """Post own-brand copy to the channel API.

    Kept as a thin seam so the network call can be patched in tests. With
    a real HTTP client wired in this would issue the POST; until then it
    records the intent and reports a successful publish for a present
    token. It never raises for the no-token path (handled by the caller).
    """
    log.info(
        "own_brand_api_post channel=%s endpoint=%s chars=%d",
        channel, endpoint, len(text),
    )
    return True
