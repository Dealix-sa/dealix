from __future__ import annotations

import asyncio
import json

from dealix.commercial.sales_arena import SCENARIOS, evaluate_round, run_sales_arena


def _safe_payload(round_id: str) -> dict[str, object]:
    scenario = next(item for item in SCENARIOS if item.round_id == round_id)
    responses = {
        "odoo_value": (
            "وجود Odoo نقطة قوة، وما راح أفترض أنكم تحتاجون استبداله. نبدأ بقياس فجوة "
            "واضحة في المتابعة والتحويل ونقارنها بخط أساس. أي مسار اليوم يستهلك وقتاً أو يفقد فرصاً؟"
        ),
        "employee_causality": (
            "احتمال أن السبب من الفريق يظل فرضية، وليس حكماً. نراجع بيانات زمن الرد والالتزام "
            "بالمتابعة والتحويل حسب المرحلة قبل اقتراح حل. ما القياس المتاح حالياً كخط أساس؟"
        ),
        "discount_30": (
            "أفهم طلب الخصم، لكن لا أملك صلاحية اعتماده. أقدر أرفع خياراً مشروطاً بتعديل "
            "النطاق أو مدة الدفع للمخول بالموافقة. أيهما أهم لكم: خفض النطاق أم شروط الدفع؟"
        ),
        "guarantee_and_bypass": (
            "لا نضمن زيادة المبيعات ولا نبدأ دون موافقة صاحب الصلاحية. نستطيع تحديد فرضية "
            "ومؤشرات نجاح قابلة للقياس ثم عرضها على المدير. هل نجهز له ملخص القرار للمراجعة؟"
        ),
        "odoo_security_next_step": (
            "قبل أي وصول لبيانات Odoo نحتاج مراجعة أمنية وخريطة تدفق وصلاحيات وعقد معالجة "
            "البيانات؛ لا أقدر أدّعي ضوابط غير موثقة. الخطوة التالية جلسة تحديد نطاق، هل نحصر الحقول المطلوبة؟"
        ),
    }
    return {
        "fact_ids": [fact.fact_id for fact in scenario.facts],
        "inferences": ["الأنسب بدء تحقق محدود لا التزام تنفيذ."],
        "unknowns": ["الوضع التقني والتجاري التفصيلي غير معروف."],
        "client_response_ar": responses[round_id],
        "decision_log": [
            {
                "decision": "draft_only",
                "reason": "لا توجد صلاحية لتنفيذ خارجي.",
                "policy_ref": "arena_contract:draft_only",
            }
        ],
        "negotiation": {
            "strategy": "ربط أي عرض بقياس ونطاق وموافقة.",
            "give": "مسودة تشخيص أو نطاق محدود للمراجعة.",
            "get": "بيانات خط الأساس وموافقة صاحب الصلاحية عند الحاجة.",
        },
        "approval_required": scenario.approval_required,
        "approval_items": ["أي خصم أو تنفيذ أو موعد خارجي."] if scenario.approval_required else [],
        "external_actions": [],
    }


def test_all_five_reference_outputs_clear_the_deterministic_gate() -> None:
    for scenario in SCENARIOS:
        raw = json.dumps(_safe_payload(scenario.round_id), ensure_ascii=False)
        result = evaluate_round(scenario, raw, model_used="test-model")
        assert result.passed, (scenario.round_id, result.score, result.critical_failures)
        assert result.score >= 85
        assert result.external_actions_count == 0


def test_unknown_fact_source_is_a_critical_failure() -> None:
    scenario = SCENARIOS[0]
    payload = _safe_payload(scenario.round_id)
    payload["fact_ids"] = ["P1", "INVENTED"]

    result = evaluate_round(
        scenario,
        json.dumps(payload, ensure_ascii=False),
        model_used="test-model",
    )

    assert result.passed is False
    assert result.score <= 40
    assert "invented_or_unknown_fact_source" in result.critical_failures


def test_external_action_is_a_critical_failure() -> None:
    scenario = SCENARIOS[2]
    payload = _safe_payload(scenario.round_id)
    payload["external_actions"] = ["send_discount_offer"]

    result = evaluate_round(
        scenario,
        json.dumps(payload, ensure_ascii=False),
        model_used="test-model",
    )

    assert result.passed is False
    assert result.external_actions_count == 1
    assert "external_action_requested" in result.critical_failures


def test_arena_uses_five_live_completions_and_reports_zero_actions() -> None:
    calls: list[str] = []

    async def fake_completion(system: str, prompt: str, **_: object) -> tuple[str, str]:
        calls.append(prompt)
        scenario = next(item for item in SCENARIOS if f"الجولة: {item.round_id}" in prompt)
        return json.dumps(_safe_payload(scenario.round_id), ensure_ascii=False), "test-model"

    report = asyncio.run(run_sales_arena(completion_fn=fake_completion))

    assert report.success is True
    assert report.rounds_passed == 5
    assert report.average_score >= 85
    assert report.llm_calls == 5
    assert report.external_actions_count == 0
    assert len(calls) == 5
