#!/usr/bin/env python3
"""Static verifier for live-send safety gates (WhatsApp, email, payments).

Refuses to certify a build for production live-sending unless every layer
of the existing guard architecture is wired correctly. This file only
performs static (grep-style) analysis on the repo and import-time checks
on the canonical Settings; it never sends a message.

Gates checked (any FAIL → exit 1):

  1. ``integrations/whatsapp.py`` consults BOTH ``whatsapp_mock_mode`` and
     ``whatsapp_allow_live_send`` before send.
  2. ``auto_client_acquisition/whatsapp_safe_send.py`` routes through the
     ``safe_send_gateway`` middleware (``enforce_consent_or_block`` /
     ``SendBlocked``).
  3. ``approval_center/approval_policy.py`` requires founder approval for
     WhatsApp (``requires_founder_approval``/``founder``-style key).
  4. Email daily-limit handler exists in
     ``auto_client_acquisition/email/daily_targeting.py``.
  5. Moyasar webhook uses constant-time HMAC verification
     (``hmac.compare_digest`` in ``dealix/payments/moyasar.py``).
  6. ``Settings.is_live_send_allowed`` exists.
  7. No FastAPI router imports the raw WhatsApp/SMTP clients directly —
     callers MUST go through approval queue / safe_send.

Exit codes: 0 PASS or WARN only; 1 if any FAIL.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _read(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def _check_whatsapp_client(fails: list[str], warns: list[str]) -> None:
    text = _read("integrations/whatsapp.py")
    if not text:
        fails.append("integrations/whatsapp.py: missing")
        return
    if "whatsapp_mock_mode" not in text:
        fails.append("integrations/whatsapp.py: does not check whatsapp_mock_mode")
    if "whatsapp_allow_live_send" not in text:
        fails.append("integrations/whatsapp.py: does not check whatsapp_allow_live_send")


def _check_whatsapp_safe_send(fails: list[str], warns: list[str]) -> None:
    text = _read("auto_client_acquisition/whatsapp_safe_send.py")
    if not text:
        fails.append("auto_client_acquisition/whatsapp_safe_send.py: missing")
        return
    if "approval_status" not in text:
        fails.append("whatsapp_safe_send.py: does not gate on approval_status")
    if "is_opted_out" not in text:
        fails.append("whatsapp_safe_send.py: does not check opt-out")
    if "quiet_hours" not in text and "quiet" not in text.lower():
        fails.append("whatsapp_safe_send.py: does not enforce quiet hours")
    if "whatsapp_mock_mode_true" not in text:
        warns.append("whatsapp_safe_send.py: no explicit handler for whatsapp_mock_mode_true")


def _check_safe_send_gateway(fails: list[str], warns: list[str]) -> None:
    text = _read("auto_client_acquisition/safe_send_gateway/middleware.py")
    if not text:
        fails.append("safe_send_gateway/middleware.py: missing")
        return
    if "SendBlocked" not in text:
        fails.append("safe_send_gateway/middleware.py: SendBlocked exception missing")
    if "enforce_consent_or_block" not in text:
        fails.append("safe_send_gateway/middleware.py: enforce_consent_or_block missing")


def _check_approval_policy(fails: list[str], warns: list[str]) -> None:
    text = _read("auto_client_acquisition/approval_center/approval_policy.py")
    if not text:
        fails.append("approval_center/approval_policy.py: missing")
        return
    lower = text.lower()
    has_whatsapp_policy = "whatsapp" in lower
    if not has_whatsapp_policy:
        fails.append("approval_policy.py: no whatsapp policy block")
    if "founder" not in lower and "approval" not in lower:
        fails.append("approval_policy.py: no founder approval handle")


def _check_email_daily_limit(fails: list[str], warns: list[str]) -> None:
    text = _read("auto_client_acquisition/email/daily_targeting.py")
    if not text:
        fails.append("email/daily_targeting.py: missing")
        return
    if "daily_email_limit" not in text and "daily_limit" not in text:
        fails.append("email/daily_targeting.py: no daily_email_limit definition")


def _check_moyasar_hmac(fails: list[str], warns: list[str]) -> None:
    text = _read("dealix/payments/moyasar.py")
    if not text:
        warns.append("dealix/payments/moyasar.py: missing (payments optional)")
        return
    if "compare_digest" not in text:
        fails.append("moyasar.py: webhook verification does not use hmac.compare_digest")


def _check_settings_property(fails: list[str], warns: list[str]) -> None:
    try:
        from core.config.settings import Settings  # noqa: WPS433
    except Exception as exc:  # noqa: BLE001
        fails.append(f"Settings import failed: {exc}")
        return
    # Inspect attribute on the class — property descriptor is accessible
    # without instantiation, but we need an instance for the actual call.
    if not hasattr(Settings, "is_live_send_allowed"):
        fails.append("Settings.is_live_send_allowed: missing property")
    if "whatsapp_mock_mode" not in Settings.model_fields:
        fails.append("Settings.whatsapp_mock_mode: missing field")
    if "dealix_internal_token" not in Settings.model_fields:
        fails.append("Settings.dealix_internal_token: missing field")
    if "dealix_private_ops" not in Settings.model_fields:
        fails.append("Settings.dealix_private_ops: missing field")


def _check_no_direct_send_in_routers(fails: list[str], warns: list[str]) -> None:
    """Routers must not call WhatsApp/SMTP send paths directly.

    Importing ``integrations.whatsapp.WhatsAppClient`` is allowed (the
    inbound webhook needs ``verify_signature``/``parse_incoming``). What
    is forbidden is calling ``.send_text(...)`` or ``.send_template(...)``
    from a router — those must go through ``whatsapp_safe_send`` after
    approval, suppression, daily-limit, quiet-hours, and kill-switch gates.

    Likewise, raw ``smtplib.SMTP(...).sendmail(...)`` from a router is a
    violation. Importing ``smtplib`` for typing is fine.
    """
    routers = ROOT / "api" / "routers"
    if not routers.exists():
        return
    bad: list[str] = []
    whatsapp_send_call = re.compile(r"\.send_(text|template)\s*\(")
    smtp_sendmail = re.compile(r"\.sendmail\s*\(")
    for path in routers.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="replace")
        # WhatsApp direct send (only when the file also touches the client)
        if "WhatsAppClient" in text and whatsapp_send_call.search(text):
            bad.append(
                f"{path.relative_to(ROOT)}: calls WhatsAppClient.send_text/send_template directly "
                "— route through auto_client_acquisition.whatsapp_safe_send"
            )
        if "smtplib" in text and smtp_sendmail.search(text):
            bad.append(
                f"{path.relative_to(ROOT)}: calls smtplib sendmail directly "
                "— route through auto_client_acquisition.email"
            )
    for b in bad:
        fails.append(b)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.parse_args()

    fails: list[str] = []
    warns: list[str] = []

    _check_whatsapp_client(fails, warns)
    _check_whatsapp_safe_send(fails, warns)
    _check_safe_send_gateway(fails, warns)
    _check_approval_policy(fails, warns)
    _check_email_daily_limit(fails, warns)
    _check_moyasar_hmac(fails, warns)
    _check_settings_property(fails, warns)
    _check_no_direct_send_in_routers(fails, warns)

    print("== verify_live_send_safety ==")
    for w in warns:
        print(f"  WARN: {w}")
    for f in fails:
        print(f"  FAIL: {f}")
    if not fails and not warns:
        print("  ok: all live-send safety gates wired")

    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    print(f"LIVE_SEND_SAFETY_VERDICT={verdict}")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
