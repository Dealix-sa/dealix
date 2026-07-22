"""Regression tests for the evidence-first manual payment close path."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "commercial" / "verify_manual_close_path.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("manual_close_path_verifier", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_valid_same_company_close_sequence_passes() -> None:
    module = _load_module()
    rows = [
        {"company": "Approved Client", "event_type": "invoice_sent"},
        {"company": "Approved Client", "event_type": "payment_received"},
        {"company": "Approved Client", "event_type": "proof_pack_delivered"},
        {"company": "Approved Client", "event_type": "closed_won"},
    ]

    assert module.validate_company_sequence(rows, "Approved Client") == []


def test_payment_before_invoice_is_rejected() -> None:
    module = _load_module()
    rows = [
        {"company": "Approved Client", "event_type": "payment_received"},
        {"company": "Approved Client", "event_type": "invoice_sent"},
    ]

    errors = module.validate_company_sequence(rows, "Approved Client")

    assert any("payment_received appears before invoice_sent" in error for error in errors)


def test_proof_from_different_company_does_not_close_paid_company() -> None:
    module = _load_module()
    rows = [
        {"company": "Paid Company", "event_type": "invoice_sent"},
        {"company": "Paid Company", "event_type": "payment_received"},
        {"company": "Other Company", "event_type": "proof_pack_delivered"},
    ]

    paid_errors = module.validate_company_sequence(rows, "Paid Company")
    other_errors = module.validate_company_sequence(rows, "Other Company")

    assert paid_errors == []
    assert any("proof_pack_delivered appears before payment_received" in error for error in other_errors)


def test_closed_won_before_same_company_proof_is_rejected() -> None:
    module = _load_module()
    rows = [
        {"company": "Approved Client", "event_type": "invoice_sent"},
        {"company": "Approved Client", "event_type": "payment_received"},
        {"company": "Approved Client", "event_type": "closed_won"},
        {"company": "Other Client", "event_type": "proof_pack_delivered"},
    ]

    errors = module.validate_company_sequence(rows, "Approved Client")

    assert any("closed_won appears before payment_received and proof_pack_delivered" in error for error in errors)


def test_repository_manual_close_contract_passes_without_external_action() -> None:
    module = _load_module()

    result = module.verify()

    assert result["verdict"] == "PASS", result["errors"]
    assert result["external_action_performed"] is False
    assert result["payment_capture_enabled"] is False
    assert result["example"]["example_only"] is True
