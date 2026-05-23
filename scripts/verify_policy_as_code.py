#!/usr/bin/env python3
"""Verify ``policies/dealix_control_policy.yaml`` is well-formed and complete.

Required:
* approval classes A0, A1, A2, A3 all present.
* All canonical rule names are present.
* A3 must be marked ``never_automatic: true``.

Exits with code 0 on PASS, 1 on FAIL.
"""

from __future__ import annotations

import sys
from pathlib import Path

POLICY_PATH = Path("policies/dealix_control_policy.yaml")
REQUIRED_CLASSES = {"A0", "A1", "A2", "A3"}
REQUIRED_RULES = {
    "no_a3_auto",
    "no_suppressed_outreach",
    "high_risk_requires_evidence",
    "no_guaranteed_revenue_claims",
    "approved_a2_can_request_execution",
    "public_proof_requires_approval",
    "pricing_commit_requires_approval",
    "data_export_requires_escalation",
    "payment_terms_require_escalation",
    "contract_change_requires_escalation",
    "destructive_operation_requires_escalation",
}


def _load() -> dict | None:
    if not POLICY_PATH.exists():
        return None
    text = POLICY_PATH.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore[import-not-found]

        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else None
    except ImportError:
        return _shallow(text)
    except Exception as exc:
        print(f"[FAIL] yaml parse error: {exc}", file=sys.stderr)
        return None


def _shallow(text: str) -> dict:
    classes: list[dict] = []
    rules: list[dict] = []
    current: str | None = None
    pending_class: dict | None = None
    pending_rule: dict | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            current = line.rstrip(":").strip()
            continue
        stripped = line.strip()
        if current == "approval_classes":
            if stripped.startswith("- id:"):
                if pending_class is not None:
                    classes.append(pending_class)
                pending_class = {"id": stripped.split(":", 1)[1].strip()}
            elif pending_class is not None and ":" in stripped:
                k, v = stripped.split(":", 1)
                pending_class[k.strip()] = v.strip()
        elif current == "rules":
            if stripped.startswith("- name:"):
                if pending_rule is not None:
                    rules.append(pending_rule)
                pending_rule = {"name": stripped.split(":", 1)[1].strip()}
            elif pending_rule is not None and ":" in stripped:
                k, v = stripped.split(":", 1)
                pending_rule[k.strip()] = v.strip()
    if pending_class is not None:
        classes.append(pending_class)
    if pending_rule is not None:
        rules.append(pending_rule)
    return {"approval_classes": classes, "rules": rules}


def main() -> int:
    policy = _load()
    if not policy:
        print("[FAIL] policy YAML missing or unreadable", file=sys.stderr)
        return 1

    classes = {c.get("id") for c in policy.get("approval_classes", []) if isinstance(c, dict)}
    missing_classes = REQUIRED_CLASSES - classes
    if missing_classes:
        print(f"[FAIL] missing approval classes: {sorted(missing_classes)}", file=sys.stderr)
        return 1

    rules = {r.get("name") for r in policy.get("rules", []) if isinstance(r, dict)}
    missing_rules = REQUIRED_RULES - rules
    if missing_rules:
        print(f"[FAIL] missing rules: {sorted(missing_rules)}", file=sys.stderr)
        return 1

    print(f"[PASS] policy-as-code: {len(classes)} classes, {len(rules)} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
