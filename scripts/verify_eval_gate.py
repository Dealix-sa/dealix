"""Verify evals/gates/dealix_agent_eval_gate.yaml is intact and references real cases."""
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

GATE = "evals/gates/dealix_agent_eval_gate.yaml"
AGENTS = "registries/agent_registry.yaml"


def run() -> VerifierReport:
    r = VerifierReport(verifier="Eval Gate")
    if not must_be_file(r, "gate_file", GATE):
        return r
    if not must_be_file(r, "agents_file", AGENTS):
        return r

    gate = load_yaml(repo_path(GATE))
    agents = load_yaml(repo_path(AGENTS))

    g = gate.get("global_thresholds") or {}
    required_thresholds = (
        "prompt_injection_resistance_min",
        "hallucination_rate_max",
        "policy_compliance_min",
        "forbidden_phrase_leak_max",
    )
    for t in required_thresholds:
        if t not in g:
            r.fail(f"global[{t}]", "missing global threshold")
        else:
            r.pass_(f"global[{t}]", str(g[t]))

    # forbidden phrases must include the no-guarantee set
    forbidden = {x.lower() for x in (gate.get("forbidden_phrases") or [])}
    must_forbid = {"guaranteed revenue", "guaranteed sales", "guaranteed meetings"}
    missing = must_forbid - forbidden
    if missing:
        r.fail("forbidden_phrases", f"missing: {sorted(missing)}")
    else:
        r.pass_("forbidden_phrases", f"{len(forbidden)} phrases")

    # required agents must match registry
    declared = {a.get("id") for a in (agents.get("agents") or []) if isinstance(a, dict)}
    required = set(gate.get("required_agents") or [])
    missing_in_registry = required - declared
    if missing_in_registry:
        r.fail("required_agents_in_registry",
               f"agents in eval gate but not registered: {sorted(missing_in_registry)}")
    else:
        r.pass_("required_agents_in_registry", f"{len(required)} required, all in registry")

    suites = gate.get("eval_suites") or {}
    for agent_id in required:
        suite = suites.get(agent_id)
        if not suite:
            r.fail(f"suite[{agent_id}]", "no eval suite declared")
            continue
        cases_file = suite.get("cases_file")
        if not cases_file:
            r.fail(f"suite[{agent_id}]_cases", "cases_file unset")
            continue
        if not repo_path(cases_file).exists():
            r.warn(f"suite[{agent_id}]_cases",
                   f"cases file not present yet: {cases_file}",
                   hint="add the cases file or update the gate")
            continue
        r.pass_(f"suite[{agent_id}]", cases_file)

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_eval_gate"))
