"""
Check script for Client Delivery Acceptance.

Usage:
    python scripts/checks/check_client_delivery_acceptance.py --client "ABC Training"

Exit codes:
    0  all checks passed
    1  one or more checks failed
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Repo root is two levels above this file (scripts/checks/check_client_delivery_acceptance.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ACCEPTANCE_FILE = BASE_DIR / "data" / "delivery" / "client_acceptance.jsonl"
UAT_FILE = BASE_DIR / "data" / "delivery" / "client_uat_results.jsonl"
SIGN_OFF_FILE = BASE_DIR / "data" / "delivery" / "client_sign_offs.jsonl"
HEALTH_SCORE_FILE = BASE_DIR / "data" / "delivery" / "delivery_health_scores.jsonl"
REPORTS_DELIVERY_DIR = BASE_DIR / "reports" / "delivery"

MIN_HEALTH_SCORE = 90


# ── JSONL helpers ──────────────────────────────────────────────────────────────

def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read every non-empty line from a JSONL file and return parsed records."""
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped:
                try:
                    records.append(json.loads(stripped))
                except json.JSONDecodeError:
                    pass
    return records


def find_record_for_client(
    records: list[dict[str, Any]], client_name: str
) -> dict[str, Any] | None:
    """Return the first record whose client_name matches (case-insensitive)."""
    needle = client_name.strip().lower()
    for rec in records:
        if rec.get("client_name", "").strip().lower() == needle:
            return rec
    return None


# ── Client slug (for weekly report filename matching) ──────────────────────────

def client_slug(client_name: str) -> str:
    """Convert a client name to the slug used in weekly report filenames."""
    return client_name.strip().lower().replace(" ", "_").replace("-", "_")


# ── Individual checks ──────────────────────────────────────────────────────────

CheckResult = tuple[bool, str]


def check_acceptance_record_exists(client_name: str) -> CheckResult:
    """Verify a client_acceptance record exists for the client."""
    records = load_jsonl(ACCEPTANCE_FILE)
    rec = find_record_for_client(records, client_name)
    if rec is None:
        return False, f"No record in client_acceptance.jsonl for client '{client_name}'."
    return True, "client_acceptance record found."


def check_acceptance_required_fields(client_name: str) -> CheckResult:
    """Verify acceptance record has system, scope, required_inputs, deliverables, acceptance_criteria."""
    records = load_jsonl(ACCEPTANCE_FILE)
    rec = find_record_for_client(records, client_name)
    if rec is None:
        return False, "No acceptance record found; cannot check required fields."
    missing: list[str] = []
    for field in ("system", "scope", "required_inputs", "deliverables", "acceptance_criteria"):
        if not rec.get(field):
            missing.append(field)
    if missing:
        return False, f"Missing or empty fields in acceptance record: {', '.join(missing)}."
    return True, "All required acceptance fields present."


def check_required_inputs_complete(client_name: str) -> CheckResult:
    """Verify all required_inputs have received=true."""
    records = load_jsonl(ACCEPTANCE_FILE)
    rec = find_record_for_client(records, client_name)
    if rec is None:
        return False, "No acceptance record found; cannot check required_inputs."
    inputs: list[dict[str, Any]] = rec.get("required_inputs", [])
    if not inputs:
        return False, "required_inputs list is empty."
    incomplete = [inp.get("name", "<unnamed>") for inp in inputs if not inp.get("received", False)]
    if incomplete:
        return False, f"required_inputs not yet received: {', '.join(incomplete)}."
    return True, f"All {len(inputs)} required_inputs received."


def check_uat_record_exists(client_name: str) -> CheckResult:
    """Verify a UAT result record exists for the client."""
    records = load_jsonl(UAT_FILE)
    rec = find_record_for_client(records, client_name)
    if rec is None:
        return False, f"No UAT result in client_uat_results.jsonl for client '{client_name}'."
    return True, "UAT result record found."


def check_sign_off_exists(client_name: str) -> CheckResult:
    """Verify a sign-off record with a decision field exists for the client."""
    records = load_jsonl(SIGN_OFF_FILE)
    rec = find_record_for_client(records, client_name)
    if rec is None:
        return False, f"No sign-off in client_sign_offs.jsonl for client '{client_name}'."
    if not rec.get("decision"):
        return False, "sign-off record found but 'decision' field is missing or empty."
    return True, f"Sign-off found with decision='{rec['decision']}'."


def check_health_score(client_name: str) -> CheckResult:
    """Verify health score record exists and total_score >= 90."""
    records = load_jsonl(HEALTH_SCORE_FILE)
    rec = find_record_for_client(records, client_name)
    if rec is None:
        return False, f"No health score in delivery_health_scores.jsonl for client '{client_name}'."
    total = rec.get("total_score")
    if total is None:
        return False, "Health score record found but 'total_score' field is missing."
    if total < MIN_HEALTH_SCORE:
        return (
            False,
            f"total_score={total} is below required threshold of {MIN_HEALTH_SCORE}.",
        )
    return True, f"Health score total_score={total} (status: {rec.get('status', 'unknown')})."


def check_weekly_report_exists(client_name: str) -> CheckResult:
    """Verify at least one weekly report file exists for the client in reports/delivery/."""
    if not REPORTS_DELIVERY_DIR.exists():
        return False, f"Directory {REPORTS_DELIVERY_DIR} does not exist."
    slug = client_slug(client_name)
    prefix = f"client_{slug}_WEEKLY"
    matches = [f for f in REPORTS_DELIVERY_DIR.iterdir() if f.name.startswith(prefix)]
    if not matches:
        return (
            False,
            f"No weekly value report found in reports/delivery/ starting with '{prefix}'.",
        )
    names = ", ".join(f.name for f in sorted(matches))
    return True, f"Weekly report(s) found: {names}."


# ── Runner ─────────────────────────────────────────────────────────────────────

_CHECKS = [
    ("Acceptance record exists", check_acceptance_record_exists),
    ("Acceptance required fields present", check_acceptance_required_fields),
    ("All required_inputs received", check_required_inputs_complete),
    ("UAT result exists", check_uat_record_exists),
    ("Sign-off with decision exists", check_sign_off_exists),
    (f"Health score >= {MIN_HEALTH_SCORE}", check_health_score),
    ("Weekly value report file present", check_weekly_report_exists),
]


def run_checks(client_name: str) -> int:
    """
    Run all delivery acceptance checks for a client.

    Returns 0 if all checks pass, 1 if any fail.
    """
    separator = "-" * 60
    print(separator)
    print(f"  Delivery Acceptance Check — client: {client_name!r}")
    print(separator)

    passed = 0
    failed = 0

    for label, fn in _CHECKS:
        ok, detail = fn(client_name)
        symbol = "OK" if ok else "FAIL"
        print(f"  [{symbol}] {label}")
        if not ok:
            print(f"        Reason: {detail}")
        else:
            print(f"        {detail}")
        if ok:
            passed += 1
        else:
            failed += 1

    print(separator)
    print(f"  Checks passed : {passed}/{passed + failed}")
    if failed == 0:
        print("  RESULT        : SUCCESS")
    else:
        print(f"  RESULT        : FAIL ({failed} check(s) failed)")
    print(separator)

    return 0 if failed == 0 else 1


# ── Entry point ────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check client delivery acceptance status.",
    )
    parser.add_argument(
        "--client",
        required=True,
        help="Client name exactly as stored in client_acceptance.jsonl (case-insensitive).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse CLI args and run checks. Returns exit code."""
    args = _build_parser().parse_args(argv)
    return run_checks(args.client)


if __name__ == "__main__":
    sys.exit(main())
