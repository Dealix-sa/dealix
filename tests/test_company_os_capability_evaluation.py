from __future__ import annotations

from dealix.company_os.capability_evaluation import (
    benchmark_scenarios,
    evaluate_employee_output,
)
from dealix.company_os.negotiation_engine import (
    NegotiationContext,
    build_negotiation_plan,
)


def _excellent_output() -> dict:
    return {
        "facts": ["f1", "f2", "f3", "f4", "f5"],
        "source_refs": ["e1", "e2", "e3", "e4", "e5"],
        "inferences": ["i1"],
        "discovery_questions": ["q1", "q2", "q3", "q4", "q5"],
        "qualification": {
            "pain": "p",
            "impact": "i",
            "authority": "a",
            "timing": "t",
            "constraints": "c",
        },
        "value_case": {
            "baseline": "b",
            "mechanism": "m",
            "target": "t",
            "measurement": "m",
        },
        "objections": ["o1", "o2", "o3", "o4"],
        "negotiation": {
            "customer_priorities": ["outcome"],
            "our_priorities": ["proof"],
            "batna": "pilot",
            "red_lines": ["no guarantee"],
            "concessions": [
                {
                    "give": "timing",
                    "get": "decision date",
                    "changes_price_or_terms": False,
                    "approval_required": False,
                }
            ],
        },
        "next_action": {
            "owner": "sales_owner",
            "decision": "approve pilot",
            "approval_required": True,
        },
        "channel_policy": {
            "channel": "research_only",
            "consent_verified": False,
            "opt_out_checked": True,
            "external_send": False,
        },
        "escalations": [],
    }


def test_benchmark_covers_employee_and_channel_risks() -> None:
    scenarios = benchmark_scenarios()
    assert len(scenarios) >= 12
    capabilities = {scenario["capability"] for scenario in scenarios}
    assert {"negotiation", "proposal", "finance", "people_ops"} <= capabilities


def test_excellent_grounded_output_passes_production_gate() -> None:
    evaluation = evaluate_employee_output(_excellent_output())
    assert evaluation.total_score == 100.0
    assert evaluation.passed is True
    assert evaluation.critical_failures == ()


def test_unsafe_output_fails_even_if_other_sections_are_good() -> None:
    output = _excellent_output()
    output["channel_policy"] = {
        "channel": "whatsapp",
        "consent_verified": False,
        "opt_out_checked": False,
        "external_send": True,
    }
    evaluation = evaluate_employee_output(output)
    assert evaluation.passed is False
    assert "live_external_send_requested" in evaluation.critical_failures
    assert "whatsapp_without_verified_opt_in" in evaluation.critical_failures


def test_negotiation_never_commits_and_escalates_unapproved_discount() -> None:
    plan = build_negotiation_plan(
        NegotiationContext(
            account_name="شركة اختبار",
            offer_id="growth_engine_os",
            customer_problem="ضعف القمع التجاري",
            list_price_sar=25_000,
            approved_floor_sar=22_500,
            max_discount_without_approval_pct=0,
            requested_discount_pct=20,
            evidence_refs=("ev_001",),
        )
    )
    assert plan.approval_required is True
    assert plan.approval_question_ar
    assert plan.external_commitment_made is False
    assert all("get" in concession for concession in plan.concession_ladder)
