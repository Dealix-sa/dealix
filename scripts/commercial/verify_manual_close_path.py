#!/usr/bin/env python3
"""Verify the evidence-first manual close path without sending or charging."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "dealix/config/phase_0_1_active_deal.yaml"
HELPER = ROOT / "scripts/phase_0_1_close_helper.py"
TRACKER = ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
DOD = ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md"
SOP = ROOT / "docs/commercial/MANUAL_PAYMENT_CLOSE_PATH_AR.md"
EXAMPLE = ROOT / "data/commercial/examples/manual_close_event.example.json"
CHECKOUT = ROOT / "landing/checkout.html"
SUCCESS = ROOT / "landing/checkout-success.html"
REQUIRED_FILES = (CONFIG, HELPER, TRACKER, DOD, SOP, EXAMPLE, CHECKOUT, SUCCESS)
REQUIRED_EVENTS = ("invoice_sent", "payment_received", "proof_pack_delivered")
INTERNAL_COMPANIES = {
    "dealix founder commercial day",
    "dealix internal go-live validation",
    "founder_launch_day",
}


def _secret_tokens() -> tuple[str, ...]:
    """Construct scanner tokens without embedding secret signatures in source."""

    prefixes = tuple(f"{family}_{mode}_" for family in ("sk", "pk") for mode in ("live", "test"))
    return (*prefixes, "akia", "begin private key", "cvv")


def _normalize(value: str | None) -> str:
    return " ".join((value or "").strip().casefold().split())


def _is_real_company(value: str | None) -> bool:
    normalized = _normalize(value)
    return bool(normalized) and normalized not in INTERNAL_COMPANIES


def validate_company_sequence(rows: Iterable[dict[str, str]], company: str) -> list[str]:
    """Validate event order for one company; closed_won is optional but governed."""

    target = _normalize(company)
    seen_invoice = False
    seen_payment = False
    seen_proof = False
    errors: list[str] = []
    for row in rows:
        if _normalize(row.get("company")) != target:
            continue
        event = _normalize(row.get("event_type"))
        if event == "invoice_sent":
            seen_invoice = True
        elif event == "payment_received":
            if not seen_invoice:
                errors.append(f"{company}: payment_received appears before invoice_sent")
            seen_payment = True
        elif event == "proof_pack_delivered":
            if not seen_payment:
                errors.append(f"{company}: proof_pack_delivered appears before payment_received")
            seen_proof = True
        elif event == "closed_won":
            if not seen_payment or not seen_proof:
                errors.append(f"{company}: closed_won appears before payment_received and proof_pack_delivered")
    return errors


def _load_tracker() -> list[dict[str, str]]:
    with TRACKER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _audit_tracker() -> tuple[list[str], list[str], dict[str, object]]:
    rows = _load_tracker()
    companies: dict[str, str] = {}
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        company = row.get("company")
        if _is_real_company(company):
            companies[_normalize(company)] = (company or "").strip()
            counts[_normalize(row.get("event_type"))] += 1
    errors = [error for company in companies.values() for error in validate_company_sequence(rows, company)]
    warnings = [] if companies else ["No real-company evidence rows are present yet; expected before the first close."]
    return errors, warnings, {
        "rows_total": len(rows),
        "real_companies": sorted(companies.values()),
        "real_event_counts": dict(sorted(counts.items())),
    }


def _audit_config() -> tuple[list[str], list[str], dict[str, object]]:
    errors: list[str] = []
    warnings: list[str] = []
    payload = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return ["phase_0_1_active_deal.yaml must contain a mapping"], warnings, {}
    for section in ("active_deal", "close_path", "payment", "proof"):
        if not isinstance(payload.get(section), dict):
            errors.append(f"config section {section!r} is required")
    active = payload.get("active_deal") if isinstance(payload.get("active_deal"), dict) else {}
    payment = payload.get("payment") if isinstance(payload.get("payment"), dict) else {}
    company = str(active.get("company") or "").strip()
    method = str(payment.get("method") or "").strip()
    payment_ref = str(payment.get("payment_ref") or "").strip()
    if not company:
        warnings.append("active_deal.company is empty; configure only a real approved deal before appending evidence.")
    if payment_ref:
        errors.append("Committed config must not contain payment_ref; retain sensitive references in an approved system.")
    if method and method not in {"manual_transfer", "moyasar_sandbox", "moyasar_live"}:
        errors.append("payment.method must be manual_transfer, moyasar_sandbox, moyasar_live, or empty")
    return errors, warnings, {
        "active_company_configured": bool(company),
        "payment_method": method or None,
        "payment_reference_committed": bool(payment_ref),
    }


def _audit_example() -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    raw = EXAMPLE.read_text(encoding="utf-8")
    payload = json.loads(raw)
    if payload.get("example_only") is not True:
        errors.append("manual close example must declare example_only=true")
    for field in ("invoice_or_transfer_reference", "payment_received_at", "proof_pack_path"):
        if payload.get(field):
            errors.append(f"manual close example must leave {field} empty")
    if payload.get("founder_approval_id") != "REQUIRED_BEFORE_EXTERNAL_ACTION":
        errors.append("manual close example must retain the approval placeholder")
    folded = raw.casefold()
    errors.extend(
        f"manual close example contains secret-like token: {token}"
        for token in _secret_tokens()
        if token in folded
    )
    return errors, {
        "example_only": payload.get("example_only"),
        "state": payload.get("state"),
        "offer_price_sar": payload.get("offer_price_sar"),
    }


def _audit_public_contract() -> list[str]:
    checkout = CHECKOUT.read_text(encoding="utf-8")
    success = SUCCESS.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in (
        "REQUEST ≠ INVOICE ≠ REVENUE",
        "NO_LIVE_CHARGE",
        "bank_transfer_manual",
        "form.reportValidity()",
        "/api/v1/payment-ops/invoice-intent",
    ):
        if marker not in checkout:
            errors.append(f"checkout contract marker missing: {marker}")
    for marker in ("test_request_recorded", "request_id", "لم يتم خصم أي مبلغ", "لم تصدر فاتورة حية"):
        if marker not in success:
            errors.append(f"checkout success marker missing: {marker}")
    if "invoice_id" in success:
        errors.append("checkout success must not treat a TEST request as invoice_id")
    return errors


def _audit_docs_and_helper() -> list[str]:
    helper = HELPER.read_text(encoding="utf-8")
    dod = DOD.read_text(encoding="utf-8")
    sop = SOP.read_text(encoding="utf-8")
    errors: list[str] = []
    for event in REQUIRED_EVENTS:
        if event not in helper:
            errors.append(f"close helper does not support required event: {event}")
        if event not in dod:
            errors.append(f"DoD does not mention required event: {event}")
        if event not in sop:
            errors.append(f"manual close SOP does not mention required event: {event}")
    for marker in ("REQUEST ≠ INVOICE ≠ REVENUE", "same-company evidence", "لا أسرار"):
        if marker.casefold() not in sop.casefold():
            errors.append(f"manual close SOP missing governance marker: {marker}")
    return errors


def verify() -> dict[str, object]:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        return {"verdict": "FAIL", "errors": [f"missing required file: {item}" for item in missing], "warnings": []}
    config_errors, config_warnings, config = _audit_config()
    tracker_errors, tracker_warnings, tracker = _audit_tracker()
    example_errors, example = _audit_example()
    errors = config_errors + tracker_errors + example_errors + _audit_public_contract() + _audit_docs_and_helper()
    return {
        "verdict": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": config_warnings + tracker_warnings,
        "config": config,
        "tracker": tracker,
        "example": example,
        "external_action_performed": False,
        "payment_capture_enabled": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"MANUAL_CLOSE_PATH={result['verdict']}")
        for warning in result.get("warnings", []):
            print(f"WARN: {warning}")
        for error in result.get("errors", []):
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
