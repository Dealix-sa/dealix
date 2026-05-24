"""Verify registries/agent_registry.yaml is sound.

Refuses to ship if any agent that can take external action is missing:
    * requires_policy
    * requires_integration_gate
    * requires_live_send_safety
    * audit_required
    * kill_switch
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    VerifierReport,
    load_yaml,
    main_cli,
    must_be_file,
    repo_path,
)

REGISTRY = "registries/agent_registry.yaml"
VALID_CLASSES = {"A0", "A1", "A2", "A3"}


def run() -> VerifierReport:
    r = VerifierReport(verifier="Agent Registry")
    if not must_be_file(r, "registry_file", REGISTRY):
        return r
    data = load_yaml(repo_path(REGISTRY))
    agents = data.get("agents") or []
    if not agents:
        r.fail("agents_declared", "registry has no agents")
        return r
    r.pass_("agents_declared", f"{len(agents)} agents")

    seen_ids: set[str] = set()
    for a in agents:
        aid = a.get("id", "<unknown>")
        if aid in seen_ids:
            r.fail(f"agent[{aid}]_unique", "duplicate agent id")
            continue
        seen_ids.add(aid)
        cls = a.get("approval_class_max")
        if cls not in VALID_CLASSES:
            r.fail(f"agent[{aid}]_class", f"approval_class_max invalid: {cls}")
            continue
        if not a.get("kill_switch", False):
            r.fail(f"agent[{aid}]_kill_switch", "kill_switch must be true")
            continue
        if not a.get("audit_required", False):
            r.fail(f"agent[{aid}]_audit", "audit_required must be true")
            continue
        if not a.get("eval_required", False):
            r.fail(f"agent[{aid}]_eval", "eval_required must be true")
            continue
        if a.get("external_action_allowed"):
            for must in ("requires_policy", "requires_integration_gate",
                         "requires_live_send_safety"):
                if not a.get(must):
                    r.fail(f"agent[{aid}]_{must}",
                           f"agent has external_action_allowed=true but {must} unset",
                           hint="See policies/dealix_control_policy.yaml")
                    break
            else:
                r.pass_(f"agent[{aid}]", "external action fully gated")
            continue
        r.pass_(f"agent[{aid}]", f"{cls}, internal-only")

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_agent_registry"))
