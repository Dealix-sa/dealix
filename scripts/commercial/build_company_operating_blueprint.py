from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "dealix" / "registers" / "company_operating_blueprint_registry.json"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return value is not None


def _bounded_score(value: Any, *, minimum: int = 0, maximum: int = 5) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return minimum
    return max(minimum, min(maximum, number))


def assess_function(
    function: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    maturity = _bounded_score(evidence.get("maturity"))
    business_impact = _bounded_score(evidence.get("business_impact"))
    urgency = _bounded_score(evidence.get("urgency"))
    owner_readiness = _bounded_score(evidence.get("owner_readiness"))
    data_readiness = _bounded_score(evidence.get("data_readiness"))
    risk = _bounded_score(evidence.get("risk"))

    source_refs = evidence.get("source_refs", [])
    named_owner = evidence.get("named_owner")
    problem = evidence.get("problem")
    target_metric = evidence.get("target_metric")
    baseline = evidence.get("baseline")

    evidence_complete = bool(source_refs and named_owner and problem)
    priority_score = (
        business_impact * 3
        + urgency * 2
        + owner_readiness
        + data_readiness
        + (5 - maturity)
        - risk
    )

    if not evidence_complete:
        readiness = "unverified"
        recommended_action = "complete_diagnostic"
    elif not _present(baseline) or not _present(target_metric):
        readiness = "diagnostic_ready"
        recommended_action = "define_baseline_and_target"
    elif owner_readiness < 3 or data_readiness < 2:
        readiness = "diagnostic_ready"
        recommended_action = "resolve_owner_or_access_blocker"
    else:
        readiness = "pilot_ready"
        recommended_action = "design_bounded_pilot"

    return {
        "function_id": function["id"],
        "function_name": function["name"],
        "primary_loop": function["primary_loop"],
        "commercial_module": function["commercial_module"],
        "maturity": maturity,
        "business_impact": business_impact,
        "urgency": urgency,
        "risk": risk,
        "owner_readiness": owner_readiness,
        "data_readiness": data_readiness,
        "priority_score": priority_score,
        "readiness": readiness,
        "recommended_action": recommended_action,
        "named_owner": named_owner,
        "problem": problem,
        "baseline": baseline,
        "target_metric": target_metric,
        "source_refs": source_refs,
        "diagnostic_questions": function["diagnostic_questions"],
        "expected_outputs": function["core_outputs"],
    }


def select_initial_scope(assessments: list[dict[str, Any]], maximum: int = 2) -> list[dict[str, Any]]:
    eligible = [item for item in assessments if item["readiness"] != "unverified"]
    ordered = sorted(
        eligible,
        key=lambda item: (
            item["readiness"] == "pilot_ready",
            item["priority_score"],
            item["business_impact"],
        ),
        reverse=True,
    )
    return ordered[:maximum]


def build_phased_roadmap(initial_scope: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not initial_scope:
        return [
            {
                "phase": "diagnostic",
                "goal": "Establish verified company context and select one bounded priority.",
                "functions": [],
                "exit_gate": "At least one function is diagnostic-ready with a named owner and evidence sources.",
            }
        ]

    functions = [item["function_id"] for item in initial_scope]
    return [
        {
            "phase": "diagnostic",
            "goal": "Validate problem, owner, sources, baseline, target metric, risk, and approval boundaries.",
            "functions": functions,
            "exit_gate": "One bounded loop is approved for pilot design.",
        },
        {
            "phase": "pilot",
            "goal": "Run one primary company loop in draft-only or controlled mode with action, approval, outcome, and proof records.",
            "functions": functions[:1],
            "exit_gate": "Delivery is verified and the agreed metric improves or a clear no-go is proven.",
        },
        {
            "phase": "implementation",
            "goal": "Install the Company Brain, selected modules, roles, connectors, governance, and Daily Command rhythm.",
            "functions": functions,
            "exit_gate": "The loop is repeatable, owned, measured, and supportable.",
        },
        {
            "phase": "managed_service",
            "goal": "Operate weekly command, exceptions, approvals, proof review, learning, and renewal readiness.",
            "functions": functions,
            "exit_gate": "Expansion is supported by verified adoption, value evidence, and operating capacity.",
        },
    ]


def build_operating_blueprint(
    company: dict[str, Any],
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    registry = registry or load_registry()
    evidence_by_function = company.get("function_evidence", {})

    assessments = [
        assess_function(function, evidence_by_function.get(function["id"], {}))
        for function in registry["functions"]
    ]
    initial_scope = select_initial_scope(
        assessments,
        maximum=registry["expansion_rules"]["maximum_initial_functions"],
    )
    unverified = [item["function_id"] for item in assessments if item["readiness"] == "unverified"]

    approval_items: list[dict[str, str]] = []
    if initial_scope:
        approval_items = [
            {"type": "diagnostic_scope", "status": "pending"},
            {"type": "data_and_source_access", "status": "pending"},
            {"type": "pilot_design", "status": "pending"},
            {"type": "commercial_terms", "status": "pending"},
            {"type": "external_send", "status": "pending"},
        ]

    if not _present(company.get("company_name")):
        decision = "blocked"
        next_step = "provide_named_company"
    elif not initial_scope:
        decision = "diagnostic_required"
        next_step = "collect_function_evidence"
    elif any(item["readiness"] == "pilot_ready" for item in initial_scope):
        decision = "pilot_design_ready"
        next_step = "prepare_bounded_pilot_and_internal_quote"
    else:
        decision = "diagnostic_ready"
        next_step = "complete_baseline_target_and_access_gaps"

    return {
        "schema_version": "1.0",
        "mode": "draft_only",
        "company_context": {
            "company_name": company.get("company_name"),
            "sector": company.get("sector"),
            "country": company.get("country", "Saudi Arabia"),
            "strategic_goals": company.get("strategic_goals", []),
            "source_refs": company.get("source_refs", []),
        },
        "decision": decision,
        "company_maturity_assessment": assessments,
        "initial_scope": initial_scope,
        "phased_roadmap": build_phased_roadmap(initial_scope),
        "commercial_path": registry["commercial_paths"],
        "approval_items": approval_items,
        "unverified_functions": unverified,
        "enterprise_expansion_allowed": False,
        "enterprise_expansion_gate": registry["expansion_rules"]["expansion_requires"],
        "forbidden_patterns": registry["expansion_rules"]["forbidden"],
        "next_step": next_step,
        "external_actions_executed": 0,
        "quote_generated": False,
        "readiness_claims_generated": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a governed Dealix company operating blueprint from verified company evidence."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    company = json.loads(args.input.read_text(encoding="utf-8"))
    result = build_operating_blueprint(company)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
