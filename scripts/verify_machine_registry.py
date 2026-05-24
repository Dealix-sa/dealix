"""Verify registries/machine_registry.yaml is sound."""
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

REGISTRY = "registries/machine_registry.yaml"
REQUIRED_FIELDS = ("id", "name", "purpose", "schedule", "approval_class_max",
                   "external_action_allowed", "owner", "script")


def run() -> VerifierReport:
    r = VerifierReport(verifier="Machine Registry")
    if not must_be_file(r, "registry_file", REGISTRY):
        return r
    data = load_yaml(repo_path(REGISTRY))
    machines = data.get("machines") or []
    if not machines:
        r.fail("machines_declared", "registry has no machines")
        return r
    r.pass_("machines_declared", f"{len(machines)} machines")

    seen: set[str] = set()
    for m in machines:
        mid = m.get("id", "<unknown>")
        if mid in seen:
            r.fail(f"machine[{mid}]_unique", "duplicate machine id")
            continue
        seen.add(mid)
        for f in REQUIRED_FIELDS:
            if f not in m:
                r.fail(f"machine[{mid}]_{f}", f"missing field: {f}")
                break
        else:
            if m.get("external_action_allowed"):
                r.fail(f"machine[{mid}]_no_external",
                       "machines (cron jobs) must not take external action; route through outreach_executor + founder approval")
                continue
            script = m.get("script")
            if script and not repo_path(script).exists():
                r.warn(f"machine[{mid}]_script", f"script not present yet: {script}",
                       hint="add the file or remove from registry")
                continue
            r.pass_(f"machine[{mid}]", str(m.get("schedule")))
    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_machine_registry"))
