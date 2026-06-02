#!/usr/bin/env python3
"""Verify policies/dealix_control_policy.yaml schema + referenced files.

Schema assertions:
  - autonomy_classes contains A1, A2, A3
  - banned_claims has both english + arabic lists, both non-empty
  - external_send block exists with default=blocked
  - kill_switch block exists
  - audit block exists with retention_days >= 90
  - referenced legacy policy files exist on disk
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]

POLICY_PATH = REPO / "policies" / "dealix_control_policy.yaml"

LEGACY_REFERENCES = (
    "dealix/config/approval_policy.yaml",
    "dealix/config/claim_policy.yaml",
    "dealix/config/agent_permissions.yaml",
    "dealix/registers/no_overclaim.yaml",
)


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)


def main() -> int:
    if not POLICY_PATH.is_file():
        _fail(f"missing_policy:{POLICY_PATH.relative_to(REPO)}")
        print("POLICY_AS_CODE_PASS=false")
        return 1

    try:
        data = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        _fail(f"policy_yaml_error:{exc}")
        print("POLICY_AS_CODE_PASS=false")
        return 1

    errors: list[str] = []

    classes = (data.get("autonomy_classes") or {}).keys()
    for cls in ("A1", "A2", "A3"):
        if cls not in classes:
            errors.append(f"missing_autonomy_class:{cls}")

    banned = data.get("banned_claims") or {}
    if not banned.get("english"):
        errors.append("banned_claims_english_empty")
    if not banned.get("arabic"):
        errors.append("banned_claims_arabic_empty")
    for required_term in ("guaranteed meetings", "guaranteed revenue"):
        if required_term not in (banned.get("english") or []):
            errors.append(f"missing_banned_term_en:{required_term}")
    for required_term in ("ضمان مبيعات", "ضمان اجتماعات", "ضمان إيراد"):
        if required_term not in (banned.get("arabic") or []):
            errors.append(f"missing_banned_term_ar:{required_term}")

    external = data.get("external_send") or {}
    if external.get("default") != "blocked":
        errors.append("external_send_default_not_blocked")

    if "kill_switch" not in data:
        errors.append("missing_kill_switch_block")

    audit = data.get("audit") or {}
    if not audit.get("every_a2_action_logged"):
        errors.append("audit_a2_logging_disabled")
    if int(audit.get("retention_days") or 0) < 90:
        errors.append("audit_retention_too_short")

    for ref in LEGACY_REFERENCES:
        if not (REPO / ref).is_file():
            errors.append(f"missing_referenced_file:{ref}")

    for err in errors:
        _fail(err)

    ok = not errors
    print(f"POLICY_AS_CODE_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
