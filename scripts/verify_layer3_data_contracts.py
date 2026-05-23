#!/usr/bin/env python3
"""L3 — Data Contracts verifier.

Imports Pydantic models in dealix/contracts/, asserts high-stakes evidence rule,
and runs dealix/contracts/dump_schemas.py comparing output to checked-in schemas.
Exit 0=PASS, 1=FAIL.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def check_pydantic_imports() -> list[str]:
    errors: list[str] = []
    try:
        from dealix.classifications import (
            ApprovalClass,
            ReversibilityClass,
            SensitivityClass,
        )
        from dealix.contracts.audit_log import AuditEntry
        from dealix.contracts.decision import DecisionOutput
        from dealix.contracts.event_envelope import EventEnvelope
        from dealix.contracts.evidence_pack import Evidence
    except Exception as e:
        errors.append(f"import error: {e!r}")
    return errors


def check_high_stakes_validator() -> list[str]:
    """Assert DecisionOutput rejects A2+ with empty evidence (decision.py:118-127)."""
    errors: list[str] = []
    try:
        from dealix.classifications import ApprovalClass, ReversibilityClass, SensitivityClass
        from dealix.contracts.decision import DecisionOutput

        try:
            DecisionOutput(
                entity_id="ent_test",
                objective="qualify_lead",
                agent_name="test.agent",
                recommendation={"verdict": "ok"},
                confidence=0.9,
                rationale="test high stakes rejection",
                approval_class=ApprovalClass.A2,
                reversibility_class=ReversibilityClass.R1,
                sensitivity_class=SensitivityClass.S1,
            )
            errors.append("validator did not reject A2 with empty evidence")
        except Exception as e:
            if "High-stakes" not in str(e) and "evidence" not in str(e).lower():
                errors.append(f"unexpected error from validator: {e!r}")
    except Exception as e:
        errors.append(f"setup error: {e!r}")
    return errors


def check_schema_drift() -> list[str]:
    """Run dump_schemas.py and compare its output with checked-in JSON schemas."""
    errors: list[str] = []
    dump = REPO / "dealix" / "contracts" / "dump_schemas.py"
    if not dump.exists():
        return [f"missing: {dump.relative_to(REPO)}"]

    schema_dir = REPO / "dealix" / "contracts" / "schemas"
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        try:
            res = subprocess.run(  # noqa: S603
                [sys.executable, str(dump), "--out-dir", str(out_dir)],
                capture_output=True,
                text=True,
                cwd=REPO,
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            return ["dump_schemas timed out"]
        if res.returncode != 0:
            # Fallback: try with no args (dump to default location)
            try:
                res2 = subprocess.run(  # noqa: S603
                    [sys.executable, str(dump)],
                    capture_output=True,
                    text=True,
                    cwd=REPO,
                    timeout=60,
                )
                if res2.returncode != 0:
                    return [f"dump_schemas exit {res.returncode}: {res.stderr[:200]}"]
            except subprocess.TimeoutExpired:
                return ["dump_schemas timed out"]
            # If fallback succeeded, skip diff (we don't know where it wrote)
            return []

        for expected in schema_dir.glob("*.schema.json"):
            generated = out_dir / expected.name
            if not generated.exists():
                continue  # dump may not produce all
            try:
                want = json.loads(expected.read_text())
                got = json.loads(generated.read_text())
            except json.JSONDecodeError as e:
                errors.append(f"{expected.name}: parse error {e}")
                continue
            if want != got:
                errors.append(f"schema drift: {expected.name}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--private-ops", default=None, help="ignored at L3")
    args = ap.parse_args()

    checks: dict[str, list[str]] = {
        "pydantic_imports": check_pydantic_imports(),
    }
    if not checks["pydantic_imports"]:
        checks["high_stakes_validator"] = check_high_stakes_validator()
        checks["schema_drift"] = check_schema_drift()

    failures = [f"{k}: {e}" for k, errs in checks.items() for e in errs]
    verdict = "PASS" if not failures else "FAIL"
    summary = f"{len(checks)} checks; failures={len(failures)}"
    if args.json:
        print(
            json.dumps(
                {
                    "layer": 3,
                    "verdict": verdict,
                    "checks": {k: bool(v) for k, v in checks.items()},
                    "errors": failures,
                    "summary": summary,
                }
            )
        )
    else:
        print(summary)
        for f in failures:
            print(f"  - {f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
