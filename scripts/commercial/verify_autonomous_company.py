#!/usr/bin/env python3
"""Verify the Autonomous Company OS is correct and safe.

Checks (with synthetic in-memory deals — no repo state touched):
  - stage is derived from evidence (payment_received => WON)
  - revenue is recognized only on payment_received
  - a not-opted-in NEW lead is never given an outreach draft (approval)
  - a WON deal's next action is internal (deliver), not a send
  - a cycle refuses to run if a live-send flag is enabled
  - Command Room render contains no live-send language

Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.autonomous_company import command_room, decision_engine, pipeline, revenue
from dealix.autonomous_company.company_os import _safety_violations, run_cycle
from dealix.autonomous_company.schemas import Deal, DealEvent, DealStage


def _deal(name, events, opted_in=True, value=499):
    return Deal(
        id=name,
        account_name=name,
        opted_in=opted_in,
        value_sar=value,
        events=[DealEvent(event=e, at="2026-07-01") for e in events],
    )


def verify() -> list[str]:
    f: list[str] = []
    today = date(2026, 7, 8)

    paid = _deal("paid", ["lead_identified", "message_sent_manually", "call_booked", "invoice_sent", "payment_received"], value=5000)
    new_cold = _deal("cold", ["lead_identified"], opted_in=False)
    new_warm = _deal("warm", ["lead_identified"], opted_in=True)

    # Stage derivation.
    if pipeline.derive_stage(paid) != DealStage.WON:
        f.append("payment_received did not derive WON stage.")
    if pipeline.derive_stage(new_cold) != DealStage.NEW:
        f.append("lead_identified did not derive NEW stage.")

    # Revenue recognition.
    if revenue.recognized_revenue([new_warm]) != 0:
        f.append("Revenue recognized without payment_received.")
    if revenue.recognized_revenue([paid]) != 5000:
        f.append("payment_received did not recognize revenue.")

    deals = [paid, new_cold, new_warm]
    decision = decision_engine.decide(deals, today, top_n=10)
    by_id = {r.deal_id: r for r in decision.recommendations}

    # Not-opted-in NEW lead must not get an approval/outreach draft.
    if by_id["cold"].requires_approval or by_id["cold"].draft:
        f.append("Not-opted-in lead was given an outreach draft.")
    # Warm NEW lead should get an approval-gated outreach draft.
    if not by_id["warm"].requires_approval or not by_id["warm"].draft:
        f.append("Warm lead did not get an approval-gated outreach draft.")
    # WON deal's action is internal delivery, not a send.
    if by_id["paid"].requires_approval:
        f.append("WON deal action incorrectly requires send approval.")

    # Safety gate: a live flag blocks the cycle.
    import os

    os.environ["WHATSAPP_SEND_ENABLED"] = "true"
    try:
        if not _safety_violations():
            f.append("Live flag did not register as a safety violation.")
        try:
            run_cycle(write=False, strict_safety=True)
            f.append("Cycle ran despite an enabled live-send flag.")
        except RuntimeError:
            pass
    finally:
        os.environ.pop("WHATSAPP_SEND_ENABLED", None)

    # Command Room render is clean.
    kpis = revenue.compute_kpis(deals, today)
    md = command_room.render_markdown(today, kpis, decision, ["note"])
    for bad in ("auto-send", "sent automatically", "charged automatically"):
        if bad in md.lower():
            f.append(f"Command Room contains unsafe phrase: {bad}")

    return f


def main() -> int:
    failures = verify()
    if failures:
        print("AUTONOMOUS_COMPANY_VERIFY=FAIL")
        for x in failures:
            print(f"FAIL: {x}")
        return 1
    print("AUTONOMOUS_COMPANY_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
