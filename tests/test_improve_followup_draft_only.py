"""Doctrine tests for the improve -> follow-up bridge.

These pin the non-negotiable: the bridge builds the full outbound pipeline up to
the human approval gate and CANNOT auto-send. Draft-only by construction.
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "auto_client_acquisition" / "gtm_os" / "improve_followup.py"

_spec = importlib.util.spec_from_file_location("improve_followup", MODULE_PATH)
assert _spec and _spec.loader
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def _finding(**over: object) -> dict:
    base = {"id": "F1", "title": "تكرار منطق في مسارين", "evidence": "a.py:31"}
    base.update(over)
    return base


def test_card_is_draft_only_and_requires_approval() -> None:
    card = mod.build_followup_card(finding=_finding(), recipient_ref="crm_998")
    assert card["outbound_mode"] == "draft_only"
    assert card["governance_decision"] == "approval_required"
    assert card["send_status"] == "draft"
    assert card["requires_approval"] is True
    assert card["dispatchable"] is False


def test_guaranteed_claim_finding_is_blocked() -> None:
    card = mod.build_followup_card(
        finding=_finding(title="عائد مضمون 40%"), recipient_ref="crm_1"
    )
    assert card["blocked"] is True
    assert "GUARANTEED" in card["block_reason"].upper() or card["block_reason"]
    # Even a blocked card is never dispatchable.
    assert card["dispatchable"] is False


def test_raw_email_recipient_rejected() -> None:
    try:
        mod.build_followup_card(finding=_finding(), recipient_ref="ceo@acme.sa")
    except ValueError as e:
        assert "PII" in str(e) or "opaque" in str(e)
    else:
        raise AssertionError("raw email recipient must be rejected")


def test_raw_phone_recipient_rejected() -> None:
    try:
        mod.build_followup_card(finding=_finding(), recipient_ref="+966500000000")
    except ValueError:
        pass
    else:
        raise AssertionError("raw phone recipient must be rejected")


def test_disallowed_channel_rejected() -> None:
    try:
        mod.build_followup_card(
            finding=_finding(), recipient_ref="crm_1", channel="telegram"
        )
    except ValueError:
        pass
    else:
        raise AssertionError("unknown channel must be rejected")


def test_module_has_no_send_capability() -> None:
    """Structural guarantee: no send/dispatch/transmit function exists."""
    banned = ("send", "dispatch", "transmit", "deliver", "post_message")
    for name, obj in inspect.getmembers(mod, inspect.isfunction):
        assert not any(b in name.lower() for b in banned), f"forbidden fn: {name}"
    src = MODULE_PATH.read_text(encoding="utf-8")
    # No network clients imported.
    for net in ("requests", "httpx", "smtplib", "urllib.request", "socket"):
        assert f"import {net}" not in src, f"network import present: {net}"


def test_queue_stamps_every_card() -> None:
    findings = [_finding(id=f"F{i}") for i in range(5)]
    queue = mod.build_approval_queue(findings, recipient_ref="crm_42")
    assert len(queue) == 5
    assert all(c["dispatchable"] is False for c in queue)
    assert all(c["requires_approval"] is True for c in queue)


def test_draft_text_uses_hypothesis_language() -> None:
    card = mod.build_followup_card(finding=_finding(), recipient_ref="crm_7")
    assert "نتوقّع" in card["draft_text"] or "سنقيس" in card["draft_text"]
    assert not mod.has_guaranteed_claim(card["draft_text"])
