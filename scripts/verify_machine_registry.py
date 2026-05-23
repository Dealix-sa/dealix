"""Verify registries/machine_registry.yaml structure & invariants.

Checks:
  - YAML loads.
  - Required keys present per machine.
  - All required canonical machines present (per Master Prompt v11).
  - disable_switch defined and non-empty.
  - approval_class in {low, medium, high}.
  - trust_gate in {none, review, hard_block}.
  - No duplicate IDs.

Exits 0 on PASS, non-zero on FAIL.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "id", "name", "layer", "purpose", "owner", "input", "output",
    "source_of_truth", "approval_class", "trust_gate", "worker",
    "kpi", "failure_mode", "recovery_path", "disable_switch",
}

REQUIRED_MACHINES = {
    "brand_system", "founder_console", "control_plane",
    "ceo_copilot", "market_intelligence", "account_scoring",
    "outbound_draft", "linkedin_queue", "email_draft", "contact_form_queue",
    "followup", "reply_router",
    "sample_factory", "proposal_factory", "payment_capture",
    "delivery_qa", "retention", "proof_approval", "partner_referral",
    "content_to_demand", "eval_gate", "policy_as_code", "audit_log",
    "worker_orchestrator", "finance_os", "data_quality", "security_gate",
    "launch_command",
}

VALID_APPROVAL = {"low", "medium", "high"}
VALID_TRUST = {"none", "review", "hard_block"}


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError:
        sys.stderr.write("[fail] PyYAML not installed (`pip install pyyaml`).\n")
        sys.exit(2)
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"machine_registry.yaml not found at {path}"]
    data = _load_yaml(path)
    machines = data.get("machines") or []
    if not isinstance(machines, list):
        return ["`machines` must be a list"]

    seen: set[str] = set()
    for i, m in enumerate(machines):
        if not isinstance(m, dict):
            errors.append(f"machine[{i}] not a dict")
            continue
        missing = REQUIRED_FIELDS - set(m.keys())
        if missing:
            errors.append(f"machine '{m.get('id', f'<#{i}>')}' missing fields: {sorted(missing)}")
        mid = m.get("id")
        if mid in seen:
            errors.append(f"duplicate machine id: {mid}")
        seen.add(mid)

        if (m.get("approval_class") or "").lower() not in VALID_APPROVAL:
            errors.append(f"{mid}: approval_class invalid ({m.get('approval_class')})")
        if (m.get("trust_gate") or "").lower() not in VALID_TRUST:
            errors.append(f"{mid}: trust_gate invalid ({m.get('trust_gate')})")
        if not (m.get("disable_switch") or "").strip():
            errors.append(f"{mid}: disable_switch missing")
        if not (m.get("kpi") or "").strip():
            errors.append(f"{mid}: kpi missing")

    missing_canonical = REQUIRED_MACHINES - seen
    if missing_canonical:
        errors.append(f"missing canonical machines: {sorted(missing_canonical)}")
    return errors


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    path = Path(argv[0]) if argv else Path("registries/machine_registry.yaml")
    errors = verify(path)
    if errors:
        sys.stdout.write("[fail] machine_registry verification:\n")
        for e in errors:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"[pass] machine_registry.yaml verified ({path})\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
