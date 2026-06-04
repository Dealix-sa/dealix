#!/usr/bin/env python3
"""Shared helpers for Dealix V9 Strategic Moat & Enterprise Readiness OS verifiers.

All V9 verify scripts are static, read-only checks. They:
  * confirm required operating files exist and have substantive content,
  * scan for forbidden / unverified claims (the non-negotiables),
  * write a machine-readable JSON report under outputs/v9_verification/,
  * print a single-line VERDICT and return an exit code.

No secrets, no network, no external sending. Founder-approval-first by design.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO / "outputs" / "v9_verification"

# Minimum byte size for a doc to count as "substantive" content.
MIN_DOC_BYTES = 400

# Forbidden / unverified-claim patterns. Kept deliberately specific so the
# non-negotiables can be referenced (e.g. "we do NOT guarantee ROI") without
# tripping the scanner — only affirmative bad claims match.
FORBIDDEN_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"guaranteed\s+roi", "guaranteed ROI claim"),
    (r"\bwe\s+guarantee\s+(?:a\s+)?(?:\d+\s*%|return|revenue|results?)\b", "guaranteed results claim"),
    (r"\b(?:soc\s?2|iso\s?27001|pci[-\s]?dss)\s+certified\b", "unverified certification claim"),
    (r"\b100%\s+secure\b", "absolute security claim"),
    (r"\bfully\s+automated\s+(?:outreach|sending|outbound)\b", "blind automation claim"),
    (r"\bauto[-\s]?send(?:s|ing)?\s+(?:to\s+)?(?:customers?|clients?|leads?)\b", "auto-send claim"),
    (r"\bscrap(?:e|es|ing)\s+(?:linkedin|leads?|contacts?|emails?)\b", "scraping claim"),
)

ALLOW_NEGATION_WINDOW = 60  # chars before a match scanned for negation context.
NEGATION_HINTS = ("no ", "not ", "never", "without", "ممنوع", "لا ", "بدون", "do not", "don't", "doesn't")


def scan_forbidden(text: str) -> list[str]:
    """Return list of forbidden-claim descriptions found as affirmative claims."""
    violations: list[str] = []
    lowered = text.lower()
    for pattern, label in FORBIDDEN_PATTERNS:
        for m in re.finditer(pattern, lowered):
            window = lowered[max(0, m.start() - ALLOW_NEGATION_WINDOW): m.start()]
            if any(hint in window for hint in NEGATION_HINTS):
                continue  # negated / policy statement — allowed
            violations.append(f"{label}: '...{lowered[max(0, m.start()-20):m.end()+20].strip()}...'")
    return violations


def check_file(rel_path: str) -> dict:
    """Check a single required file: existence, size, forbidden claims."""
    path = REPO / rel_path
    entry: dict = {"path": rel_path, "exists": path.is_file()}
    if not entry["exists"]:
        entry.update(bytes=0, substantive=False, violations=[])
        return entry
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    entry["bytes"] = len(raw)
    entry["substantive"] = len(raw) >= MIN_DOC_BYTES
    entry["violations"] = scan_forbidden(text)
    return entry


def check_json(rel_path: str, required_keys: Iterable[str] = ()) -> dict:
    """Check a config JSON: existence, parseability, required top-level keys."""
    path = REPO / rel_path
    entry: dict = {"path": rel_path, "exists": path.is_file()}
    if not entry["exists"]:
        entry.update(valid_json=False, missing_keys=list(required_keys))
        return entry
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        entry["valid_json"] = True
        entry["missing_keys"] = [k for k in required_keys if k not in data]
        entry["violations"] = scan_forbidden(json.dumps(data, ensure_ascii=False))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:  # pragma: no cover
        entry["valid_json"] = False
        entry["missing_keys"] = list(required_keys)
        entry["error"] = str(exc)
    return entry


def run_system_check(
    system: str,
    required_files: Iterable[str],
    required_configs: Iterable[tuple[str, tuple[str, ...]]] = (),
    output_name: str | None = None,
) -> dict:
    """Run the standard V9 check for a system and persist a JSON report.

    Returns the report dict with a top-level ``verdict`` of PASS/FAIL.
    """
    file_results = [check_file(p) for p in required_files]
    config_results = [check_json(p, keys) for p, keys in required_configs]

    missing = [r["path"] for r in file_results if not r["exists"]]
    thin = [r["path"] for r in file_results if r["exists"] and not r["substantive"]]
    bad_json = [r["path"] for r in config_results if not r.get("valid_json")]
    missing_keys = [
        {"path": r["path"], "missing": r["missing_keys"]}
        for r in config_results
        if r.get("missing_keys")
    ]
    violations = [
        {"path": r["path"], "violations": r["violations"]}
        for r in (file_results + config_results)
        if r.get("violations")
    ]

    passed = not (missing or thin or bad_json or missing_keys or violations)
    report = {
        "system": system,
        "date": date.today().isoformat(),
        "verdict": "PASS" if passed else "FAIL",
        "summary": {
            "files_required": len(file_results),
            "files_present": sum(1 for r in file_results if r["exists"]),
            "configs_required": len(config_results),
            "missing": missing,
            "thin": thin,
            "bad_json": bad_json,
            "missing_keys": missing_keys,
            "violations": violations,
        },
        "files": file_results,
        "configs": config_results,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    name = output_name or system.lower().replace(" ", "_")
    (OUTPUT_DIR / f"{name}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


def print_and_exit(report: dict) -> int:
    """Print a human verdict line and return an exit code (0 PASS / 1 FAIL)."""
    s = report["summary"]
    print(f"[{report['system']}] verdict={report['verdict']} "
          f"files={s['files_present']}/{s['files_required']}")
    if s["missing"]:
        print(f"  missing: {s['missing']}")
    if s["thin"]:
        print(f"  thin: {s['thin']}")
    if s["bad_json"]:
        print(f"  bad_json: {s['bad_json']}")
    if s["missing_keys"]:
        print(f"  missing_keys: {s['missing_keys']}")
    if s["violations"]:
        print(f"  violations: {s['violations']}")
    print(f"{report['system'].upper().replace(' ', '_')}_VERDICT={report['verdict']}")
    return 0 if report["verdict"] == "PASS" else 1
