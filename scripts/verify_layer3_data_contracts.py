#!/usr/bin/env python3
"""L3 — Data Contracts verifier.

Imports Pydantic models in dealix/contracts/, asserts the high-stakes evidence
validator (decision.py:118-127), and diffs each model's in-memory JSON schema
against the checked-in dealix/contracts/schemas/*.schema.json files.
Exit 0=PASS, 1=FAIL.
"""

from __future__ import annotations

import argparse
import json
import sys
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
    """Generate JSON schemas in-memory from Pydantic models and diff against checked-in files."""
    errors: list[str] = []
    schema_dir = REPO / "dealix" / "contracts" / "schemas"
    if not schema_dir.is_dir():
        return [f"missing schema dir: {schema_dir.relative_to(REPO)}"]

    try:
        from dealix.contracts import (
            AuditEntry,
            DecisionOutput,
            EventEnvelope,
            EvidencePack,
        )
    except Exception as e:
        return [f"contract import error: {e!r}"]

    targets = {
        "decision_output.schema.json": DecisionOutput,
        "event_envelope.schema.json": EventEnvelope,
        "evidence_pack.schema.json": EvidencePack,
        "audit_entry.schema.json": AuditEntry,
    }

    for filename, model in targets.items():
        expected = schema_dir / filename
        if not expected.exists():
            errors.append(f"missing schema file: {filename}")
            continue
        try:
            want = json.loads(expected.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{filename}: parse error {e}")
            continue
        generated = model.model_json_schema()
        # match what dump_schemas.py adds (lines 28-29)
        generated["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        generated["$id"] = f"https://dealix.sa/schemas/{filename}"
        if want != generated:
            errors.append(
                f"schema drift: {filename} (regenerate via `python -m dealix.contracts.dump_schemas`)"
            )
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
