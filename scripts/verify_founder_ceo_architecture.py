#!/usr/bin/env python3
"""Verify the 14-layer Dealix Founder/CEO Operating System architecture.

Pure stdlib. Read-only. Exits 0 on PASS, 1 on FAIL.

Bilingual (AR + EN) summary at the end. Supports --summary (single line)
and --json (machine-readable report) for CI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES: list[str] = [
    "docs/founder/CEO_OPERATING_MODEL.md",
    "docs/founder/CEO_COMMAND_CENTER.md",
    "docs/founder/CEO_KPI_TREE.md",
    "docs/founder/CEO_BUSINESS_AUDIT.md",
    "docs/founder/CEO_MASTER_DASHBOARD.md",
    "docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md",
    "docs/founder/CEO_NOT_NOW_LIST.md",
    "docs/founder/KILL_LIST.md",
    "docs/strategy/STRATEGIC_THESIS.md",
    "docs/strategy/DEALIX_GROWTH_SYSTEM.md",
    "docs/strategy/MARKET_ENTRY_DECISION.md",
    "docs/strategy/MOAT_SYSTEM.md",
    "docs/revenue/REVENUE_COMMAND_CENTER.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/BAD_REVENUE_FILTER.md",
    "docs/finance/FINANCE_COMMAND_CENTER.md",
    "docs/finance/FINANCIAL_MODEL_V1.md",
    "docs/finance/CAPITAL_ALLOCATION_SYSTEM.md",
    "docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md",
    "docs/delivery/revenue_sprint/DELIVERY_CONTROL_SYSTEM.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/trust/TRUST_COMMAND_CENTER.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/ai_management/AI_COMMAND_CENTER.md",
    "docs/ai_management/AI_RISK_REGISTER.md",
    "docs/ai_management/AI_AGENT_RELEASE_GATE.md",
    "docs/learning/LEARNING_COMMAND_CENTER.md",
    "docs/learning/LEARNING_ROUTER.md",
    "docs/learning/EXPERIMENT_SYSTEM.md",
    "docs/product/PRODUCTIZATION_COMMAND_CENTER.md",
    "docs/product/PRODUCTIZATION_ENGINE.md",
    "docs/product/NO_OVERBUILD_POLICY.md",
    "docs/content/CONTENT_COMMAND_CENTER.md",
    "docs/content/PROOF_LIBRARY.md",
    "docs/client_success/CLIENT_SUCCESS_COMMAND_CENTER.md",
    "docs/client_success/CLIENT_HEALTH_SCORE.md",
    "docs/people/DELEGATION_COMMAND_CENTER.md",
    "docs/people/HIRING_TRIGGERS.md",
    "docs/partners/PARTNER_COMMAND_CENTER.md",
    "docs/investor/DATA_ROOM_INDEX.md",
    "docs/investor/RISK_REGISTER.md",
]

MIN_SIZE_BYTES = 250
REQUIRED_HEADERS = ("## Purpose", "## Rules")

# ANSI colors (skip when stdout is not a tty)
_TTY = sys.stdout.isatty()
GREEN = "\033[92m" if _TTY else ""
RED = "\033[91m" if _TTY else ""
RESET = "\033[0m" if _TTY else ""


def check_file(rel_path: str) -> tuple[bool, str]:
    """Return (ok, reason). reason is empty string on success."""
    path = REPO_ROOT / rel_path
    if not path.exists():
        return False, "missing file"
    try:
        size = path.stat().st_size
    except OSError as exc:
        return False, f"stat failed: {exc}"
    if size < MIN_SIZE_BYTES:
        return False, f"too small ({size} bytes, need >= {MIN_SIZE_BYTES})"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return False, f"unreadable: {exc}"
    for header in REQUIRED_HEADERS:
        if header not in text:
            return False, f"missing section header {header!r}"
    return True, ""


def run() -> dict:
    """Execute all checks; return a structured report dict."""
    failures: list[dict] = []
    passed = 0
    for rel in REQUIRED_FILES:
        ok, reason = check_file(rel)
        if ok:
            passed += 1
        else:
            failures.append({"path": rel, "reason": reason})
    total = len(REQUIRED_FILES)
    verdict = "PASS" if not failures else "FAIL"
    return {
        "verdict": verdict,
        "total": total,
        "passed": passed,
        "failed": len(failures),
        "failures": failures,
    }


def print_human(report: dict) -> None:
    total = report["total"]
    passed = report["passed"]
    failed = report["failed"]
    if report["verdict"] == "PASS":
        print(f"{GREEN}PASS: Founder/CEO architecture is ready{RESET}")
        print(f"{GREEN}نجاح: هيكلية المؤسس/الرئيس التنفيذي جاهزة{RESET}")
        print(f"  {passed}/{total} files OK")
    else:
        print(f"{RED}FAIL: Founder/CEO architecture verification failed{RESET}")
        print(f"{RED}فشل: التحقق من هيكلية المؤسس/الرئيس التنفيذي{RESET}")
        print(f"  {passed}/{total} passed, {failed} failed")
        print("Failures / حالات الفشل:")
        for item in report["failures"]:
            print(f"  - {item['path']}: {item['reason']}")


def print_summary(report: dict) -> None:
    verdict = report["verdict"]
    color = GREEN if verdict == "PASS" else RED
    print(
        f"{color}{verdict}{RESET} "
        f"founder_ceo_architecture {report['passed']}/{report['total']}"
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    want_json = "--json" in argv
    want_summary = "--summary" in argv

    report = run()

    if want_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif want_summary:
        print_summary(report)
    else:
        print_human(report)

    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
