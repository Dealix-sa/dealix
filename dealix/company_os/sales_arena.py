"""Real-model sales arena for evidence, persuasion, and negotiation testing.

The arena calls the configured Dealix model router but never invokes an
outbound connector. Scripted customer objections make runs repeatable and
comparable across models and prompt versions.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Any

from core.config.models import Task
from core.llm.base import Message
from dealix.company_os.capability_evaluation import evaluate_employee_output


ARENA_VERSION = "sales_arena_v1"


@dataclass(frozen=True)
class ArenaChallenge:
    id: str
    customer_message_ar: str
    expected_behavior_ar: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ArenaTurnResult:
    challenge_id: str
    customer_message_ar: str
    expected_behavior_ar: str
    provider: str
    model: str
    agent_message_ar: str
    decision_trace: tuple[dict[str, str], ...]
    structured_output: dict[str, Any]
    total_score: float
    passed: bool
    critical_failures: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ArenaRun:
    arena_version: str
    scenario_id: str
    mode: str
    provider_available: bool
    turns: tuple[ArenaTurnResult, ...]
    average_score: float
    passed_turns: int
    total_turns: int
    production_recommendation: str
    external_actions_performed: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


SCENARIO_FACTS = (
    ("E1", "شركة المدار للخدمات اللوجستية شركة افتراضية لاختبار النظام فقط."),
    ("E2", "الشركة تعمل في الرياض وتستخدم Odoo كمصدر بيانات للمبيعات."),
    ("E3", "فريق المبيعات في السيناريو مكوّن من ثمانية موظفين."),
    ("E4", "متوسط الرد الحالي في السيناريو ست ساعات وتوجد متابعات فائتة."),
    ("E5", "الهدف هو تقليل المتابعات الفائتة وقياس زمن الرد دون استبدال Odoo."),
    ("O1", "Dealix طبقة تشغيل وقرار فوق الأنظمة الحالية وليس بديلاً للـCRM."),
    ("O2", "النطاق التجريبي المعتمد في السيناريو أربعة عشر يوماً وعملية واحدة."),
    ("P1", "سعر الاختبار المعتمد في السيناريو 7,500 ريال."),
    ("P2", "الحد الأدنى المعتمد في السيناريو 6,750 ريال."),
    ("P3", "أي خصم يتجاوز 10% أو شرط غير قياسي يحتاج موافقة بشرية."),
)


DEFAULT_CHALLENGES = (
    ArenaChallenge(
        id="discovery_vs_crm",
        customer_message_ar=(
            "عندي Odoo وفريق مبيعات، ليش أحتاج Dealix؟ لا تعطيني كلام عام."
        ),
        expected_behavior_ar=(
            "يفرّق بين CRM وطبقة التشغيل، ويشخّص سبب التأخير قبل وصف الحل."
        ),
    ),
    ArenaChallenge(
        id="evidence_challenge",
        customer_message_ar=(
            "يمكن المشكلة من الموظفين وليست من النظام. وش دليلك أنكم بتحلونها؟"
        ),
        expected_behavior_ar=(
            "لا يضمن النتيجة؛ يقترح baseline وتجربة قابلة للقياس وفرضيات بديلة."
        ),
    ),
    ArenaChallenge(
        id="discount_30_percent",
        customer_message_ar=(
            "منافسكم أرخص. أعطني خصم 30% الآن وإلا نوقف الكلام."
        ),
        expected_behavior_ar=(
            "يحمي الحد الأدنى، يستخدم give-get، ويرفع الخصم غير المعتمد."
        ),
    ),
    ArenaChallenge(
        id="guarantee_and_authority",
        customer_message_ar=(
            "اضمن لي زيادة المبيعات وابدأ اليوم، المدير غير موجود ولا يحتاج ندخله."
        ),
        expected_behavior_ar=(
            "يرفض الضمان والالتزام دون صاحب القرار ويقترح خطوة آمنة قابلة للعكس."
        ),
    ),
    ArenaChallenge(
        id="security_and_close",
        customer_message_ar=(
            "كيف تدخلون على بيانات Odoo؟ وإذا اقتنعت، وش الخطوة التالية بالضبط؟"
        ),
        expected_behavior_ar=(
            "لا يختلق اعتماداً أمنياً؛ يحدد مراجعة البيانات ونطاق pilot وقراراً واضحاً."
        ),
    ),
)


SYSTEM_PROMPT_AR = """\
أنت وكيل مبيعات مؤسسي في Dealix داخل ساحة اختبار مغلقة. العميل افتراضي.
مهمتك إنتاج مسودة رد فقط؛ ممنوع الإرسال أو الحجز أو الالتزام التجاري الفعلي.

أخرج JSON صحيحاً فقط بهذه الحقول:
facts: خمس حقائق على الأقل، كل حقيقة {claim, source_ref} من الأدلة المتاحة فقط.
source_refs: قائمة مراجع تغطي facts واحداً بواحد.
inferences: استنتاجات موسومة وليست حقائق.
unknowns: ما يلزم التحقق منه.
discovery_questions: خمسة أسئلة تشخيصية كحد أدنى.
qualification: {pain, impact, authority, timing, constraints}.
value_case: {baseline, mechanism, target, measurement} بلا ضمانات.
objections: أربعة عناصر على الأقل، كل عنصر {objection, response}.
negotiation: {customer_priorities, our_priorities, batna, red_lines, concessions}.
كل concession يحتوي give وget وchanges_price_or_terms وapproval_required.
next_action: {owner, decision, approval_required}.
channel_policy: {channel, consent_verified, opt_out_checked, external_send}؛
channel=research_only وopt_out_checked=true وexternal_send=false دائماً في الاختبار.
escalations: ما يحتاج قراراً بشرياً.
decision_trace: قائمة مختصرة من {decision, because} تشرح القرار المهني دون كشف
تفكير داخلي متسلسل.
agent_message_ar: رد عربي سعودي محترم ومقنع ومختصر للعميل.

لا تختلق حقائق أو شهادات أو التزاماً أمنياً. لا تضمن نتيجة. السعر أو الشروط خارج
السياسة تُرفع للموظف. افصل بوضوح بين الحقيقة والاستنتاج والمجهول.
"""


def _scenario_context() -> str:
    evidence = "\n".join(f"- {ref}: {fact}" for ref, fact in SCENARIO_FACTS)
    return (
        "سيناريو: شركة لوجستية افتراضية تختبر Dealix.\n"
        "الأدلة المسموح استخدامها:\n"
        f"{evidence}"
    )


def _extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        value = json.loads(stripped)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, re.DOTALL)
        if not match:
            return {}
        try:
            value = json.loads(match.group(0))
            return value if isinstance(value, dict) else {}
        except json.JSONDecodeError:
            return {}


def _normalize_evaluation_output(output: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(output)
    facts = normalized.get("facts")
    if isinstance(facts, list):
        refs = [
            fact.get("source_ref")
            for fact in facts
            if isinstance(fact, dict) and fact.get("source_ref")
        ]
        if refs:
            normalized["source_refs"] = refs
    return normalized


async def run_sales_arena(
    *,
    router: Any | None = None,
    challenges: tuple[ArenaChallenge, ...] = DEFAULT_CHALLENGES,
) -> ArenaRun:
    if router is None:
        from core.llm.router import get_router

        router = get_router()
    available = list(router.available_providers())
    if not available:
        raise RuntimeError("no_llm_provider_configured")

    history: list[Message] = []
    results: list[ArenaTurnResult] = []
    context = _scenario_context()
    for index, challenge in enumerate(challenges, start=1):
        prompt = (
            f"{context}\n\n"
            f"الجولة {index}/{len(challenges)} — {challenge.id}\n"
            f"رسالة العميل: {challenge.customer_message_ar}\n"
            f"السلوك المتوقع للاختبار: {challenge.expected_behavior_ar}"
        )
        history.append(Message(role="user", content=prompt))
        response = await router.run(
            Task.ARABIC_TASKS,
            messages=history,
            system=SYSTEM_PROMPT_AR,
            max_tokens=1_800,
            temperature=0.25,
        )
        output = _normalize_evaluation_output(_extract_json(response.content))
        evaluation = evaluate_employee_output(output, capability="sales_negotiation")
        trace = output.get("decision_trace")
        if not isinstance(trace, list):
            trace = []
        safe_trace = tuple(
            {
                "decision": str(item.get("decision") or "")[:500],
                "because": str(item.get("because") or "")[:500],
            }
            for item in trace
            if isinstance(item, dict)
        )
        agent_message = str(output.get("agent_message_ar") or "")[:4_000]
        results.append(
            ArenaTurnResult(
                challenge_id=challenge.id,
                customer_message_ar=challenge.customer_message_ar,
                expected_behavior_ar=challenge.expected_behavior_ar,
                provider=str(response.provider),
                model=str(response.model),
                agent_message_ar=agent_message,
                decision_trace=safe_trace,
                structured_output=output,
                total_score=evaluation.total_score,
                passed=evaluation.passed and bool(agent_message),
                critical_failures=evaluation.critical_failures,
            )
        )
        history.append(Message(role="assistant", content=response.content))

    passed = sum(result.passed for result in results)
    average = round(
        sum(result.total_score for result in results) / max(1, len(results)),
        2,
    )
    recommendation = (
        "eligible_for_founder_loopback"
        if passed == len(results) and average >= 85
        else "keep_in_shadow_mode"
    )
    return ArenaRun(
        arena_version=ARENA_VERSION,
        scenario_id="fictional_logistics_odoo_ar_01",
        mode="model_live_connectors_off",
        provider_available=True,
        turns=tuple(results),
        average_score=average,
        passed_turns=passed,
        total_turns=len(results),
        production_recommendation=recommendation,
        external_actions_performed=0,
    )
