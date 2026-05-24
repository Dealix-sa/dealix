"""Layer 8 — Growth signals from founder-supplied inputs only.

This layer NEVER scrapes. It receives warm signals (referrals, replies, event
attendances, manual research notes) from the founder and ranks them by
acceptance criteria + recency.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult

_KIND_WEIGHT = {
    "warm_intro": 10,
    "referral": 9,
    "reply_to_post": 6,
    "event_attendee": 5,
    "manual_research_note": 4,
    "newsletter_subscriber": 3,
    "inbound_form": 8,
}

_ALLOWED_KINDS = frozenset(_KIND_WEIGHT.keys())


def _age_decay_days(ts_iso: str) -> int:
    try:
        ts = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return max(0, (now - ts).days)
    except Exception:
        return 999


def _score_signal(sig: dict[str, Any]) -> int:
    kind = str(sig.get("kind", ""))
    base = _KIND_WEIGHT.get(kind, 0)
    age = _age_decay_days(str(sig.get("timestamp", "")))
    # Decay 1 point per 3 days, floor at 0.
    decayed = max(0, base - age // 3)
    return decayed


def run(ctx: LayerContext) -> LayerResult:
    """Rank growth signals.

    Expected payload keys:
        signals: list[dict] — each {kind, timestamp (ISO), account_hint, source_ref}.

    Forbidden kinds: anything not in _ALLOWED_KINDS → rejected with reason.
    """
    signals = list(ctx.payload.get("signals", []) or [])

    if not signals:
        return LayerResult(
            layer="growth_signals",
            customer_id=ctx.customer_id,
            ok=True,
            governance_decision="ALLOW",
            output={"ranked": [], "rejected": []},
            notes=("no_signals_provided",),
        )

    # Reject any signal that suggests scraping / cold automation upstream.
    rejected: list[dict[str, Any]] = []
    accepted: list[dict[str, Any]] = []
    for s in signals:
        kind = str(s.get("kind", ""))
        if kind not in _ALLOWED_KINDS:
            rejected.append({"signal": s, "reason": f"forbidden_kind:{kind}"})
            continue
        if not s.get("source_ref"):
            rejected.append({"signal": s, "reason": "missing_source_ref"})
            continue
        accepted.append(s)

    ranked = sorted(accepted, key=_score_signal, reverse=True)
    output_ranked = [
        {
            "kind": s.get("kind"),
            "account_hint": s.get("account_hint", ""),
            "timestamp": s.get("timestamp"),
            "source_ref": s.get("source_ref"),
            "score": _score_signal(s),
        }
        for s in ranked
    ]

    decision = "ALLOW" if not rejected else "ALLOW_WITH_REVIEW"
    return LayerResult(
        layer="growth_signals",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision=decision,
        output={
            "ranked": output_ranked,
            "rejected": rejected,
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
        },
        notes=(f"{len(accepted)} accepted, {len(rejected)} rejected",),
        capital_asset_candidates=("productization_signal",) if accepted else (),
    )
