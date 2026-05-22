"""Tests for scripts/founder_create_payment_link.py.

These tests:
  - Do NOT call Moyasar (no network).
  - Exercise the dry-run path (default safe state).
  - Validate the SAR→halalas conversion.
  - Validate the no-live-charge gate (DEALIX_MOYASAR_MODE).
  - Confirm a payment_ops invoice-intent record is created.
"""
from __future__ import annotations

import argparse
import importlib
import os
import sys
from pathlib import Path

import pytest

# Make /scripts importable as a module path
_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))

# Import the script module after the path is set up
founder_create_payment_link = importlib.import_module("founder_create_payment_link")


def _args(**overrides):
    defaults = dict(
        customer="Test Co",
        amount_sar=999.0,
        description="Dealix Pilot — 7 days",
        callback_url=None,
        dry_run=True,
        moyasar_test=False,
        live=False,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_sar_to_halalas_roundtrip():
    assert founder_create_payment_link._sar_to_halalas(1.0) == 100
    assert founder_create_payment_link._sar_to_halalas(999.0) == 99900
    # rounding (no float drift)
    assert founder_create_payment_link._sar_to_halalas(10.005) == 1001


def test_sar_to_halalas_rejects_non_positive():
    with pytest.raises(ValueError):
        founder_create_payment_link._sar_to_halalas(0.0)
    with pytest.raises(ValueError):
        founder_create_payment_link._sar_to_halalas(-5.0)


def test_sar_to_halalas_caps_at_one_million():
    with pytest.raises(ValueError):
        founder_create_payment_link._sar_to_halalas(1_000_001.0)


def test_dry_run_returns_planned_invoice_and_no_moyasar_call():
    result = founder_create_payment_link.run(_args())
    assert result["mode"] == "dry_run"
    assert result["moyasar_invoice"] is None
    assert result["payment_url"] is None
    planned = result["planned_invoice"]
    assert planned["customer_handle"] == "Test Co"
    assert planned["amount_sar"] == 999.0
    assert planned["amount_halalas"] == 99900
    assert planned["status"] == "invoice_intent"
    assert planned["payment_id"].startswith("pay_")
    assert planned["invoice_intent_id"].startswith("inv_intent_")
    # default method when no live/test flag set
    assert planned["method"] == "manual_other"
    # doctrine guard preserved
    assert result["safety_summary"] == "no_live_charge_no_fake_revenue"


def test_dry_run_with_moyasar_test_flag_uses_test_method():
    result = founder_create_payment_link.run(_args(dry_run=True, moyasar_test=True))
    assert result["planned_invoice"]["method"] == "moyasar_test"


def test_live_requires_dealix_moyasar_mode_env(monkeypatch):
    # The CLI gate is in main(); run() trusts the orchestrator's enforcement,
    # which raises ValueError when method=moyasar_live without the env var.
    monkeypatch.delenv("DEALIX_MOYASAR_MODE", raising=False)
    with pytest.raises(ValueError, match="DEALIX_MOYASAR_MODE=live"):
        founder_create_payment_link.run(_args(dry_run=False, live=True))


def test_live_and_moyasar_test_are_mutually_exclusive():
    with pytest.raises(ValueError, match="mutually exclusive"):
        founder_create_payment_link.run(_args(dry_run=False, live=True, moyasar_test=True))


def test_main_blocks_live_without_env_var(monkeypatch, capsys):
    monkeypatch.delenv("DEALIX_MOYASAR_MODE", raising=False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "founder_create_payment_link.py",
            "--customer", "Test Co",
            "--amount-sar", "999",
            "--description", "Dealix Pilot",
            "--live",
        ],
    )
    rc = founder_create_payment_link.main()
    assert rc == 2
    err = capsys.readouterr().err
    assert "NO_LIVE_CHARGE" in err


def test_main_dry_run_prints_json(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "founder_create_payment_link.py",
            "--customer", "Test Co",
            "--amount-sar", "999",
            "--description", "Dealix Pilot",
        ],
    )
    rc = founder_create_payment_link.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert '"mode": "dry_run"' in out
    assert '"amount_halalas": 99900' in out
