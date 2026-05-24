#!/usr/bin/env python3
"""Generate AI Governance Board Pack."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, repo_root, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate AI Governance Board Pack").parse_args()
    ws = workspace_root()
    rr = repo_root()
    policy = (rr / "policies" / "dealix_control_policy.yaml").exists()
    agent_reg = (rr / "registries" / "agent_registry.yaml").exists()
    machine_reg = (rr / "registries" / "machine_registry.yaml").exists()
    gate = (rr / "evals" / "gates" / "dealix_agent_eval_gate.yaml").exists()
    flags = read_csv_rows(ws / "trust" / "trust_flags.csv")
    incidents = read_csv_rows(ws / "trust" / "incidents.csv")
    body = (
        "# AI Governance Board Pack\n\n"
        "## NIST AI RMF anchors\n"
        "Govern · Map · Measure · Manage — applied to every Dealix agent.\n\n"
        "## Artifacts\n"
        + md_table(
            ["artifact", "present"],
            [
                ["policies/dealix_control_policy.yaml", str(policy)],
                ["registries/agent_registry.yaml", str(agent_reg)],
                ["registries/machine_registry.yaml", str(machine_reg)],
                ["evals/gates/dealix_agent_eval_gate.yaml", str(gate)],
            ],
        )
        + f"\n## Trust ledger\n\n- open trust flags: {len(flags)}\n- open incidents: {len(incidents)}\n"
    )
    out = write_doc("docs/ai_governance/BOARD_PACK.md", body, [rr / "policies" / "dealix_control_policy.yaml"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
