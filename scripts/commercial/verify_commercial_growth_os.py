#!/usr/bin/env python3
"""Verify the Commercial Growth OS safety posture and end-to-end wiring.

Checks (all must pass):
  * environment is safe-by-default (no live-send flags),
  * the orchestrator runs and produces a snapshot,
  * every card has an owner_decision and a next_action,
  * proposals require approval and never allow a final price,
  * negotiation drafts cannot approve discounts / final terms,
  * booking options do not enable calendar write by default,
  * accounts without source_url are not send-ready,
  * WhatsApp without opt-in cannot go live,
  * no blocked claim leaks into any draft.

Exits non-zero if any check fails.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.commercial import lead_sourcing, safety
from app.commercial.negotiation_desk import FORBIDDEN_COMMITMENTS
from app.commercial.orchestrator import run_growth_os

DATA_DIR = REPO_ROOT / "data" / "commercial"


def _load(name: str, key: str):
    import json

    p = DATA_DIR / name
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get(key, []) if isinstance(data, dict) else data


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))

    # 1. Safe defaults.
    check("safe_default_environment", safety.is_safe_default_environment())

    accounts = _load("accounts.sample.json", "accounts")
    replies = _load("replies.sample.json", "replies")
    result = run_growth_os(accounts, replies)

    check("orchestrator_safety_ok", result.safety_ok, ";".join(result.safety_violations))
    check("snapshot_built", result.snapshot is not None)
    check("cards_produced", len(result.cards) > 0)

    # Every card has owner_decision + next_action.
    cards_ok = all(c.owner_decision and c.next_action for c in result.cards)
    check("cards_have_decision_and_next_action", cards_ok)

    # Proposals require approval and forbid a final price.
    props_ok = all(
        (p.approval_required and not p.final_price_allowed) for p in result.proposals
    )
    check("proposals_require_approval_no_final_price", props_ok)

    # Negotiation cannot approve discounts / final terms.
    nego_ok = all(
        "approve_discount" in d.forbidden_commitments
        and "set_final_price" in d.forbidden_commitments
        and d.approval_required
        for d in result.negotiation_drafts
    ) and "approve_discount" in FORBIDDEN_COMMITMENTS
    check("negotiation_guardrails_enforced", nego_ok or not result.negotiation_drafts)

    # Booking options: no calendar write by default.
    book_ok = all(not b.calendar_write_enabled for b in result.booking_options)
    check("booking_no_calendar_write_default", book_ok)

    # Missing source_url ⇒ not send-ready.
    built = lead_sourcing.load_accounts(accounts)
    no_source = [a for a in built if not a.source_url]
    src_ok = all(not lead_sourcing.is_send_ready(a) for a in no_source)
    check("missing_source_blocks_send", src_ok)

    # WhatsApp without opt-in cannot go live.
    wa = safety.can_send_whatsapp(
        {"message_status": "approved", "owner_decision": "send", "text": "hi"},
        account={"source_url": "x", "verification_status": "verified", "whatsapp_opt_in": False},
    )
    check("whatsapp_requires_opt_in", not wa.allowed)

    # No blocked claim in any draft.
    claim_ok = True
    for c in result.cards:
        if safety.contains_blocked_claim(c.draft_message_ar) or safety.contains_blocked_claim(
            c.draft_message_en
        ):
            claim_ok = False
    check("no_blocked_claims_in_drafts", claim_ok)

    # ── Living engagement layer ─────────────────────────────────────────────
    from app.commercial.channels import normalise_buttons
    from app.commercial.engagement_engine import run_engagement
    from app.commercial.reasoning import HeuristicBrain, get_brain

    # Default brain is the deterministic heuristic.
    check("default_brain_is_heuristic", isinstance(get_brain(), HeuristicBrain))

    eng = run_engagement(accounts, inbound_by_account=_load("inbound_events.sample.json", "inbound_by_account") if (DATA_DIR / "inbound_events.sample.json").exists() else {})
    check("engagement_runs_safe", eng.safety_ok, ";".join(eng.safety_violations))
    check("engagement_has_action_plan", len(eng.action_plan) > 0)

    # Every prepared payload is a non-sendable draft.
    payloads_ok = all(
        p["requires_approval"] and p["send_status"] in ("draft", "blocked")
        and not p["safety"].get("allowed", False)
        for p in eng.payloads
    )
    check("engagement_payloads_all_draft", payloads_ok)

    # WhatsApp interactive buttons are capped at 3.
    buttons_ok = len(normalise_buttons([{"id": f"b{i}", "title": f"opt{i}"} for i in range(6)])) == 3
    check("whatsapp_buttons_capped_at_3", buttons_ok)

    # Opt-out account is told to stop, not contacted.
    optout_actions = {a["account_id"]: a["recommended_action"] for a in eng.action_plan}
    check(
        "optout_account_honoured",
        optout_actions.get("acct_005", "honour_optout") == "honour_optout",
    )

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        line = f"[{status}] {name}"
        if detail and not ok:
            line += f" — {detail}"
        print(line)

    print(f"\nCOMMERCIAL_GROWTH_OS_VERIFY={'1' if not failed else '0'}")
    print(f"CHECKS_PASSED={len(checks) - len(failed)}/{len(checks)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
