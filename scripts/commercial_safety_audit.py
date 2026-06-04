#!/usr/bin/env python3
"""Safety audit — proves the Commercial Launch OS cannot send externally.

Scans commercial/media scripts, configs and workflows for:
  - actual external-send code (smtplib, sendgrid, twilio, selenium, etc.)
  - forbidden draft flag states (send_allowed=true, no_auto_send=false, ...)
And verifies the latest generated draft batch carries the immutable safety
flags on every record.

This file and `config/commercial_risk_terms.json` are excluded from the code
scan because they DEFINE the patterns (definitions, not violations).

Exit code 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import json
import sys

import commercial_launch_lib as lib

REPO_ROOT = lib.REPO_ROOT


def _load_terms() -> dict:
    return lib.load_config("commercial_risk_terms.json")


def _scan_files(terms: dict) -> list[dict]:
    """Scan commercial/media artifacts for real send-code and bad flag states.

    Code-send patterns (imports + send calls) are matched against .py files
    only, so prose mentions of "WhatsApp"/"LinkedIn" inside config or doc text
    never false-positive. Forbidden flag states are matched against every
    scanned file; the GOOD states (``false``) never match the forbidden
    (``true``) patterns.
    """
    violations: list[dict] = []
    exclude = set(terms["scan_exclude"])
    code_patterns = [p.lower() for p in terms["import_send_patterns"] + terms["call_send_patterns"]]
    flag_states = [f.lower() for f in terms["forbidden_flag_states"]]

    for glob in terms["scan_globs"]:
        for path in sorted(REPO_ROOT.glob(glob)):
            rel = str(path.relative_to(REPO_ROOT))
            if rel in exclude or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            if path.suffix == ".py":
                for pat in code_patterns:
                    if pat in text:
                        violations.append({"file": rel, "type": "send_code", "pattern": pat})
            for fs in flag_states:
                if fs in text:
                    violations.append({"file": rel, "type": "forbidden_flag", "pattern": fs})
    return violations


def _scan_latest_batch() -> tuple[list[dict], int]:
    """Check the most recent draft_queue.jsonl, if present."""
    violations: list[dict] = []
    checked = 0
    root = lib.OUTPUT_ROOT
    if not root.exists():
        return violations, checked
    batches = sorted([p for p in root.iterdir() if p.is_dir()], reverse=True)
    for batch in batches:
        queue = batch / "draft_queue.jsonl"
        if not queue.exists():
            continue
        with queue.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                checked += 1
                if d.get("send_allowed") is not False:
                    violations.append({"draft_id": d.get("draft_id"), "issue": "send_allowed_not_false"})
                if d.get("external_send_blocked") is not True:
                    violations.append({"draft_id": d.get("draft_id"), "issue": "external_send_not_blocked"})
                if d.get("no_auto_send") is not True:
                    violations.append({"draft_id": d.get("draft_id"), "issue": "no_auto_send_not_true"})
                if d.get("requires_founder_approval") is not True:
                    violations.append({"draft_id": d.get("draft_id"), "issue": "approval_not_required"})
        break  # only the most recent batch
    return violations, checked


def run_audit() -> dict:
    terms = _load_terms()
    code_violations = _scan_files(terms)
    batch_violations, checked = _scan_latest_batch()
    all_violations = code_violations + batch_violations
    return {
        "verdict": "PASS" if not all_violations else "FAIL",
        "code_violations": code_violations,
        "batch_violations": batch_violations,
        "drafts_checked": checked,
        "scanned_globs": terms["scan_globs"],
    }


def main(argv: list[str] | None = None) -> int:
    result = run_audit()
    out_path = REPO_ROOT / "outputs" / "commercial_launch" / "safety_audit.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if result["verdict"] == "PASS":
        print(f"✅ Safety audit PASS. Drafts checked: {result['drafts_checked']}. No external-send code or bad flags.")
        return 0
    print("❌ Safety audit FAIL:", file=sys.stderr)
    for v in result["code_violations"] + result["batch_violations"]:
        print(f"   {v}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
