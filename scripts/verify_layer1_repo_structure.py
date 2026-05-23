#!/usr/bin/env python3
"""L1 — Repository Structure verifier.

Checks canonical artifacts (files, dirs, schemas, doctrine tests) exist.
Pure pathlib; no subprocess. Exit 0=PASS, 1=FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

REQUIRED_PATHS: list[tuple[str, str]] = [
    # (path, kind) where kind in {"file","dir","dir_nonempty"}
    ("README.md", "file"),
    ("Makefile", "file"),
    ("AGENTS.md", "file"),
    (".github/workflows", "dir_nonempty"),
    ("docs", "dir"),
    ("scripts", "dir"),
    ("tests", "dir"),
    ("evals", "dir"),
    # contracts + classifications
    ("dealix/classifications/__init__.py", "file"),
    ("dealix/contracts/decision.py", "file"),
    ("dealix/contracts/schemas/decision_output.schema.json", "file"),
    ("dealix/contracts/schemas/evidence_pack.schema.json", "file"),
    ("dealix/contracts/schemas/event_envelope.schema.json", "file"),
    ("dealix/contracts/schemas/audit_entry.schema.json", "file"),
    # safety + governance
    ("auto_client_acquisition/safety_v10/eval_cases.py", "file"),
    ("platform_core/governance.py", "file"),
    # evals
    ("evals/governance_eval.yaml", "file"),
    ("evals/outreach_quality_eval.yaml", "file"),
    ("evals/arabic_quality_eval.yaml", "file"),
    ("evals/lead_intelligence_eval.yaml", "file"),
    ("evals/company_brain_eval.yaml", "file"),
    # agent definitions
    (".claude/agents/dealix-pm.md", "file"),
    # existing master verifiers wrapped by this system
    ("scripts/v10_master_verify.sh", "file"),
    ("scripts/revenue_os_master_verify.sh", "file"),
    ("scripts/run_evals.py", "file"),
    ("scripts/check_alembic_single_head.py", "file"),
    # doctrine tests
    ("tests/test_no_scraping_engine.py", "file"),
    ("tests/test_no_cold_whatsapp.py", "file"),
    ("tests/test_no_linkedin_automation.py", "file"),
    ("tests/test_no_linkedin_scraper_string_anywhere.py", "file"),
    ("tests/test_no_pii_in_logs.py", "file"),
    ("tests/test_no_guaranteed_claims.py", "file"),
    ("tests/test_no_source_passport_no_ai.py", "file"),
    ("tests/test_no_source_no_answer.py", "file"),
    ("tests/test_landing_forbidden_claims.py", "file"),
    ("tests/test_doctrine_guardrails.py", "file"),
]

MIN_FILE_BYTES = 50


def check(rel: str, kind: str) -> str | None:
    p = REPO / rel
    if not p.exists():
        return f"missing: {rel}"
    if kind == "file":
        if not p.is_file():
            return f"not a file: {rel}"
        if p.stat().st_size < MIN_FILE_BYTES:
            return f"too small (<{MIN_FILE_BYTES}B): {rel}"
    elif kind == "dir":
        if not p.is_dir():
            return f"not a dir: {rel}"
    elif kind == "dir_nonempty":
        if not p.is_dir():
            return f"not a dir: {rel}"
        if not any(p.iterdir()):
            return f"empty dir: {rel}"
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--private-ops", default=None, help="ignored at L1")
    ap.add_argument("--strict", action="store_true", help="reserved for future optional checks")
    args = ap.parse_args()

    failures: list[str] = []
    checked = 0
    for rel, kind in REQUIRED_PATHS:
        err = check(rel, kind)
        checked += 1
        if err:
            failures.append(err)

    verdict = "PASS" if not failures else "FAIL"
    summary = f"{checked - len(failures)}/{checked} required artifacts present"
    if args.json:
        print(json.dumps({"layer": 1, "verdict": verdict, "checked": checked, "missing": failures, "summary": summary}))
    else:
        print(summary)
        for f in failures:
            print(f"  - {f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
