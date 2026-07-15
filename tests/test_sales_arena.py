from __future__ import annotations

import asyncio
import json

from core.llm.base import LLMResponse
from dealix.company_os.sales_arena import DEFAULT_CHALLENGES, run_sales_arena


def _excellent_response() -> dict:
    facts = [
        {"claim": f"fact_{index}", "source_ref": f"E{index}"}
        for index in range(1, 6)
    ]
    return {
        "facts": facts,
        "source_refs": [f"E{index}" for index in range(1, 6)],
        "inferences": ["فرضية تحتاج اختبار"],
        "unknowns": ["صاحب القرار"],
        "discovery_questions": [f"q{index}" for index in range(1, 6)],
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
            "measurement": "measure",
        },
        "objections": [f"o{index}" for index in range(1, 5)],
        "negotiation": {
            "customer_priorities": ["outcome"],
            "our_priorities": ["evidence"],
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
            "decision": "review pilot",
            "approval_required": True,
        },
        "channel_policy": {
            "channel": "research_only",
            "consent_verified": False,
            "opt_out_checked": True,
            "external_send": False,
        },
        "escalations": [],
        "decision_trace": [
            {"decision": "pilot", "because": "نحتاج baseline"}
        ],
        "agent_message_ar": "أقترح أن نبدأ بقياس خط الأساس قبل أي التزام.",
    }


def test_sales_arena_uses_real_router_contract_and_never_sends() -> None:
    class FakeRouter:
        def available_providers(self):
            return ["fake"]

        async def run(self, task, messages, **kwargs):
            return LLMResponse(
                content=json.dumps(_excellent_response(), ensure_ascii=False),
                provider="fake",
                model="fake-model",
            )

    run = asyncio.run(run_sales_arena(router=FakeRouter()))
    assert run.total_turns == len(DEFAULT_CHALLENGES)
    assert run.passed_turns == run.total_turns
    assert run.average_score == 100
    assert run.production_recommendation == "eligible_for_founder_loopback"
    assert run.external_actions_performed == 0


def test_sales_arena_refuses_to_fake_when_no_model_is_configured() -> None:
    class EmptyRouter:
        def available_providers(self):
            return []

    try:
        asyncio.run(run_sales_arena(router=EmptyRouter()))
    except RuntimeError as exc:
        assert str(exc) == "no_llm_provider_configured"
    else:
        raise AssertionError("arena must not run without a real model provider")
