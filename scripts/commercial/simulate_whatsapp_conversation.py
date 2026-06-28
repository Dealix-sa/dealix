#!/usr/bin/env python3
"""Simulate a full WhatsApp interactive-button conversation (no send)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import whatsapp_loop as wl
from app.commercial.lead_sourcing import load_accounts


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    # Pick an opted-in WhatsApp account.
    acct = None
    for a in load_accounts(records):
        if a.whatsapp and a.whatsapp_opt_in:
            acct = a
            break
    if acct is None:
        dump({"error": "no opt-in WhatsApp account in sample"})
        return 0

    transcript = []
    conv, opener = wl.start(acct)
    transcript.append({"step": "opener", "stage": conv.stage,
                       "payload": opener.to_dict(),
                       "wa_payload": wl.build_interactive_payload(opener.body_ar, opener.buttons)})

    # Simulated inbound sequence: press 'interested', then price objection.
    events = [
        {"button_id": "btn_yes", "button_intent": "interested", "text": "نعم"},
        {"text": "بس السعر غالي شوي"},
    ]
    for ev in events:
        nxt = wl.step(conv, ev, account=acct)
        transcript.append({"step": f"inbound:{ev.get('button_intent') or ev.get('text')}",
                           "stage": conv.stage, "action": conv.next_action,
                           "buttons": [b["title"] for b in nxt.buttons],
                           "safe_to_send_now": nxt.safety.get("allowed", False)})

    dump({"account_id": acct.account_id, "transcript": transcript,
          "note": "draft-only — no WhatsApp message was transmitted"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
