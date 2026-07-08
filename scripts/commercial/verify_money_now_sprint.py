#!/usr/bin/env python3
"""Verify the Money Now Sprint is revenue-safe and evidence-based.

Checks:
  - a plan can be generated with a closeable top offer
  - revenue is only recognized when a payment_received event exists
  - no live charge is enabled
  - manual payment SOP and proof-pack delivery are required
  - no auto-send

Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.strategy_execution import money_now
from dealix.strategy_execution.money_now import EvidenceEvent
from dealix.strategy_execution.safety_gate import assert_no_live_send_enabled


def verify() -> list[str]:
    failures: list[str] = []

    plan = money_now.build_plan()
    if not plan.top_offer.get("name") or not plan.top_offer.get("price_sar"):
        failures.append("Top offer missing name/price.")
    if len(plan.prospects) > 10:
        failures.append("More than 10 prospects generated.")
    if not plan.payment_checklist or not plan.proof_pack_checklist:
        failures.append("Payment or proof-pack checklist missing.")

    # Revenue recognition rule: no payment event -> zero revenue.
    no_events = money_now.recognized_revenue([])
    if no_events != 0:
        failures.append("Revenue recognized without any payment_received event.")

    # A message_sent event alone must NOT create revenue.
    only_sent = money_now.recognized_revenue(
        [EvidenceEvent(prospect="X", event="message_sent_manually")]
    )
    if only_sent != 0:
        failures.append("Revenue recognized without payment_received (only sent).")

    # A payment_received event DOES create recognized revenue.
    paid = money_now.recognized_revenue(
        [EvidenceEvent(prospect="X", event="payment_received")]
    )
    if paid != money_now.TOP_OFFER["price_sar"]:
        failures.append("payment_received did not recognize the offer price.")

    # No live send flags enabled.
    failures.extend(assert_no_live_send_enabled(dict(os.environ)))

    # SOP language present.
    sop = " ".join(plan.payment_checklist).lower()
    if "manual" not in sop:
        failures.append("Payment checklist does not enforce a manual SOP.")
    if "no live charge" not in sop:
        failures.append("Payment checklist does not state 'no live charge'.")

    return failures


def main() -> int:
    failures = verify()
    if failures:
        print("MONEY_NOW_SPRINT_VERIFY=FAIL")
        for f in failures:
            print(f"FAIL: {f}")
        return 1
    print("MONEY_NOW_SPRINT_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
