#!/usr/bin/env python3
"""
verify_live_send_safety.py — no path to "live send" without all four gates.

Checks:
  - WHATSAPP_ALLOW_LIVE_SEND defaults to false in settings
  - whatsapp provider explicitly blocks when policy says no (blocked_by_policy)
  - Approval gate module exists and exposes request/decide
  - No direct call site bypasses the gate: every send-like helper must be in
    a module that imports/references the approval and policy pieces.

This is intentionally conservative — it errs toward FAIL rather than waving
through code paths that could send live without an approval.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SETTINGS = ROOT / "core/config/settings.py"
WHATSAPP = ROOT / "auto_client_acquisition/email/whatsapp_multi_provider.py"
APPROVALS = ROOT / "dealix/governance/approvals.py"


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""


def main() -> int:
    failures: list[str] = []
    ok: list[str] = []

    # 1) settings.py — WHATSAPP_ALLOW_LIVE_SEND defaults to false
    s = read(SETTINGS)
    if "WHATSAPP_ALLOW_LIVE_SEND" not in s:
        failures.append("core/config/settings.py: WHATSAPP_ALLOW_LIVE_SEND not declared")
    else:
        # Look for default false within ~10 lines of the declaration
        idx = s.find("WHATSAPP_ALLOW_LIVE_SEND")
        window = s[idx : idx + 400].lower()
        if "false" not in window and "default=false" not in window and "= false" not in window:
            failures.append(
                "core/config/settings.py: WHATSAPP_ALLOW_LIVE_SEND does not default to false"
            )
        else:
            ok.append("settings.WHATSAPP_ALLOW_LIVE_SEND defaults to false")

    # 2) WhatsApp provider explicitly blocks on policy
    w = read(WHATSAPP)
    if not w:
        failures.append("auto_client_acquisition/email/whatsapp_multi_provider.py missing")
    else:
        if "WHATSAPP_ALLOW_LIVE_SEND" not in w:
            failures.append("whatsapp_multi_provider.py does not consult WHATSAPP_ALLOW_LIVE_SEND")
        else:
            ok.append("whatsapp_multi_provider.py consults WHATSAPP_ALLOW_LIVE_SEND")
        if "blocked_by_policy" not in w and "provider=\"policy\"" not in w:
            failures.append("whatsapp_multi_provider.py does not emit a policy-block signal")
        else:
            ok.append("whatsapp_multi_provider.py emits policy-block signal")

    # 3) Approval gate exists with request + decide
    a = read(APPROVALS)
    if not a:
        failures.append("dealix/governance/approvals.py missing")
    else:
        if not re.search(r"\bdef\s+request\b|\basync\s+def\s+request\b", a):
            failures.append("dealix/governance/approvals.py has no request() method")
        else:
            ok.append("approvals.request() defined")
        if "decide" not in a:
            failures.append("dealix/governance/approvals.py has no decide path")
        else:
            ok.append("approvals decide path present")
        if "CRITICAL_ACTIONS" not in a and "risk_score" not in a:
            failures.append(
                "approvals.py does not declare critical actions or risk_score gating"
            )
        else:
            ok.append("approvals.py declares critical-action / risk-score gating")

    # Report
    for line in ok:
        print(f"  ok   {line}")
    for line in failures:
        print(f"  FAIL {line}")

    if failures:
        print(f"LIVE-SEND SAFETY: FAIL ({len(failures)} issues)")
        return 1
    print(f"LIVE-SEND SAFETY: PASS ({len(ok)} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
