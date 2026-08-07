from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "dealix" / "registers" / "commercial_readiness_registry.json"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return value is not None


def qualify_account(account: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    mapping = {
        "named_company": account.get("company_name"),
        "named_business_problem": account.get("business_problem"),
        "economic_or_operational_impact": account.get("impact_hypothesis"),
        "responsible_owner": account.get("owner"),
        "access_to_relevant_process_or_data": account.get("available_sources"),
        "willingness_to_run_a_bounded_pilot": account.get("bounded_pilot_willingness"),
    }
    missing = [name for name in registry["qualification"]["required"] if not _present(mapping[name])]

    violations: list[str] = []
    requested = set(account.get("requested_capabilities", []))
    if "uncontrolled_mass_outbound" in requested:
        violations.append("request_for_uncontrolled_mass_outbound")
    if account.get("requires_guaranteed_revenue") is True:
        violations.append("request_for_guaranteed_revenue")
    if account.get("legal_or_compliance_risk") is True:
        violations.append("illegal_or_non_compliant_use_case")
    if not _present(account.get("company_name")):
        violations.append("anonymous_or_unverifiable_company")

    if violations:
        decision = "not_qualified"
    elif missing:
        decision = "uncertain"
    else:
        decision = "qualified"

    return {
        "decision": decision,
        "route": registry["qualification"]["decision"][decision],
        "missing_requirements": missing,
        "disqualifiers": sorted(set(violations)),
    }


def select_persona(account: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    requested = account.get("buyer_persona")
    personas = registry["buyer_personas"]
    if requested:
        for persona in personas:
            if persona["id"] == requested:
                return persona
    return personas[0]


def select_offer(
    account: dict[str, Any],
    registry: dict[str, Any],
    qualification: dict[str, Any],
    persona: dict[str, Any],
) -> dict[str, Any] | None:
    if qualification["decision"] == "not_qualified":
        return None

    desired = account.get("requested_offer") or persona["best_entry_offer"]
    if qualification["decision"] == "uncertain":
        desired = "saudi_opportunity_snapshot"

    return next((offer for offer in registry["offers"] if offer["id"] == desired), None)


def build_pilot_scope(account: dict[str, Any], offer: dict[str, Any] | None) -> dict[str, Any]:
    if offer is None:
        return {"status": "withheld", "reason": "account_not_qualified"}

    scope = account.get("pilot_scope", {})
    required = [
        "business_problem",
        "baseline",
        "target_metric",
        "scope_in",
        "scope_out",
        "data_sources",
        "owner",
        "approval_boundaries",
        "delivery_checkpoints",
        "acceptance_criteria",
        "proof_requirements",
        "rollback_or_stop_rule",
    ]
    normalized = {
        "business_problem": scope.get("business_problem") or account.get("business_problem"),
        "baseline": scope.get("baseline") or account.get("baseline"),
        "target_metric": scope.get("target_metric") or account.get("target_metric"),
        "scope_in": scope.get("scope_in"),
        "scope_out": scope.get("scope_out"),
        "data_sources": scope.get("data_sources") or account.get("available_sources"),
        "owner": scope.get("owner") or account.get("owner"),
        "approval_boundaries": scope.get("approval_boundaries"),
        "delivery_checkpoints": scope.get("delivery_checkpoints"),
        "acceptance_criteria": scope.get("acceptance_criteria"),
        "proof_requirements": scope.get("proof_requirements"),
        "rollback_or_stop_rule": scope.get("rollback_or_stop_rule"),
    }
    missing = [field for field in required if not _present(normalized[field])]
    return {
        "status": "ready_for_quote" if not missing else "discovery_required",
        "fields": normalized,
        "missing_fields": missing,
        "bounded": not missing,
        "recommended_duration": "30_days_or_less_when_scope_allows",
    }


def build_value_case(account: dict[str, Any]) -> dict[str, Any]:
    value_inputs = {
        "current_loss_or_cost": account.get("current_loss_or_cost"),
        "frequency": account.get("frequency"),
        "affected_volume": account.get("affected_volume"),
        "decision_value": account.get("decision_value"),
        "time_to_value": account.get("time_to_value"),
    }
    missing = [name for name, value in value_inputs.items() if not _present(value)]
    return {
        "status": "supported_hypothesis" if not missing else "inputs_required",
        "inputs": value_inputs,
        "missing_inputs": missing,
        "roi_claim_allowed": False,
        "note": "Dealix may frame a value hypothesis, but must not claim ROI without verified customer inputs and post-delivery evidence.",
    }


def build_sale_ready_pack(account: dict[str, Any], registry: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = registry or load_registry()
    qualification = qualify_account(account, registry)
    persona = select_persona(account, registry)
    offer = select_offer(account, registry, qualification, persona)
    pilot_scope = build_pilot_scope(account, offer)
    value_case = build_value_case(account)

    approval_items: list[dict[str, str]] = []
    if offer is not None and pilot_scope["status"] == "ready_for_quote":
        approval_items.extend(
            [
                {"type": "proposal_scope", "status": "pending"},
                {"type": "commercial_terms", "status": "pending"},
                {"type": "external_send", "status": "pending"},
            ]
        )

    if qualification["decision"] == "not_qualified":
        next_step = "decline_or_refer"
    elif pilot_scope["status"] == "discovery_required":
        next_step = "complete_discovery_and_missing_pilot_fields"
    else:
        next_step = "prepare_internal_quote_and_approval_pack"

    return {
        "schema_version": "1.0",
        "mode": "draft_only",
        "account_context": {
            "company_name": account.get("company_name"),
            "sector": account.get("sector"),
            "country": account.get("country", "Saudi Arabia"),
            "source_urls": account.get("source_urls", []),
        },
        "buyer_persona": persona,
        "problem_statement": account.get("business_problem"),
        "impact_hypothesis": account.get("impact_hypothesis"),
        "qualification_result": qualification,
        "recommended_offer": offer,
        "pilot_scope": pilot_scope,
        "success_metrics": {
            "baseline": account.get("baseline"),
            "target_metric": account.get("target_metric"),
            "acceptance_criteria": pilot_scope.get("fields", {}).get("acceptance_criteria"),
        },
        "value_case": value_case,
        "proof_plan": {
            "required": pilot_scope.get("fields", {}).get("proof_requirements", []),
            "revenue_proof_required": True,
            "delivery_proof_required": True,
            "value_proof_requires_baseline": True,
        },
        "risks_and_assumptions": {
            "risks": account.get("risks", []),
            "assumptions": account.get("assumptions", []),
            "unsupported_claims_withheld": ["guaranteed_revenue", "guaranteed_roi", "government_access"],
        },
        "approval_items": approval_items,
        "next_step": next_step,
        "external_actions_executed": 0,
        "quote_generated": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a governed Dealix sale-ready pack from account JSON.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    account = json.loads(args.input.read_text(encoding="utf-8"))
    result = build_sale_ready_pack(account)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
