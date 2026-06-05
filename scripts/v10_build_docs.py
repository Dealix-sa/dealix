#!/usr/bin/env python3
"""Materialize all Dealix V10 Institutional Scale & Market Domination OS docs.

Follows the existing repo convention (see generate_layered_execution_docs.py /
generate_scale_phase_docs.py): a committed generator that writes real, reviewed
markdown into docs/. Re-runnable and idempotent.

Run:  python scripts/v10_build_docs.py

Every document carries the unbreakable rule and contains no forbidden claims
(no guaranteed ROI, no fake traction, no unverified security/compliance claims).
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

NON_NEGOTIABLE = (
    "AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. "
    "المؤسس يراجع ويعتمد ويوقّع ويبيع ويرسل يدويًا ويقرر. "
    "النظام لا يرسل خارجيًا أبدًا."
)

SAFETY = [
    "لا إرسال خارجي (Email / WhatsApp / LinkedIn) من النظام أو من GitHub Actions.",
    "لا secrets ولا API keys ولا SMTP.",
    "لا scraping ولا auto-submit ولا أتمتة LinkedIn.",
    "لا إعلانات مدفوعة حيّة، ولا traction مزيّفة، ولا ROI مضمون.",
    "لا ادعاءات أمنية/امتثال غير مثبتة. كل المخرجات draft للمراجعة والاعتماد من المؤسس.",
]


def _doc(
    title: str,
    purpose: str,
    sections: list[tuple[str, list[str]]],
    links: list[str] | None = None,
) -> str:
    """Standard V10 document body."""
    parts: list[str] = [f"# {title}", ""]
    parts += ["## الغرض", "", purpose, ""]
    parts += ["## القاعدة غير القابلة للكسر", "", f"> {NON_NEGOTIABLE}", ""]
    for heading, bullets in sections:
        parts.append(f"## {heading}")
        parts.append("")
        for b in bullets:
            parts.append(f"- {b}")
        parts.append("")
    parts += ["## حدود الأمان (Safety Boundaries)", ""]
    for s in SAFETY:
        parts.append(f"- {s}")
    parts.append("")
    parts += ["## التحقق (Verification)", ""]
    parts.append(
        "- يُفحص هذا المستند ضمن سكربتات V10 verify ويُرفع تقريره في `outputs/v10_verification/`."
    )
    parts.append(
        "- المرجع الأعلى: `docs/master-command-center/` و`outputs/v10_verification/V10_MASTER_VERIFICATION.md`."
    )
    parts.append("")
    if links:
        parts += ["## روابط", ""]
        for ln in links:
            parts.append(f"- {ln}")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def _report(
    title: str,
    what_added: list[str],
    why: list[str],
    verification: list[str],
    risks: list[str],
    blockers: list[str],
    next_actions: list[str],
    go: list[str],
    no_go: list[str],
) -> str:
    parts = [f"# {title}", ""]
    parts += ["## القاعدة غير القابلة للكسر", "", f"> {NON_NEGOTIABLE}", ""]
    for h, items in [
        ("ما الذي أُضيف (What was added)", what_added),
        ("لماذا يهم (Why it matters)", why),
        ("حالة التحقق (Verification status)", verification),
        ("المخاطر (Risks)", risks),
        ("العوائق (Blockers)", blockers),
        ("الخطوات التالية (Next actions)", next_actions),
    ]:
        parts.append(f"## {h}")
        parts.append("")
        for it in items:
            parts.append(f"- {it}")
        parts.append("")
    parts += ["## GO / NO-GO", "", "### GO"]
    for g in go:
        parts.append(f"- {g}")
    parts.append("")
    parts.append("### NO-GO")
    for n in no_go:
        parts.append(f"- {n}")
    parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def _std_report(title: str, summary: str, go: list[str], no_go: list[str]) -> str:
    return _report(
        title=title,
        what_added=[summary, "مستندات تشغيلية + سكربت/اختبار تحقق حيث ينطبق + ربط بالمؤشرات."],
        why=[
            "يغلق فجوة مؤسسية في رحلة Dealix من شركة جاهزة للتشغيل إلى شركة قابلة للتوسع المؤسسي.",
            "يحافظ على الجودة والربحية والثقة أثناء التوسع دون كسر قاعدة الإرسال اليدوي.",
        ],
        verification=[
            "PASS عند توفر كل المستندات والعلامات المطلوبة وغياب الادعاءات الممنوعة.",
            "يُرفع التقرير ضمن `outputs/v10_verification/`.",
        ],
        risks=[
            "التوسع قبل readiness.",
            "تضخيم الادعاءات أو استخدام أسماء عملاء بدون إذن.",
        ],
        blockers=["لا عوائق تقنية؛ يتطلب مراجعة المؤسس قبل أي استخدام خارجي."],
        next_actions=[
            "مراجعة المؤسس واعتماد المستندات.",
            "تشغيل سكربتات V10 verify والتأكد من PASS.",
        ],
        go=go,
        no_go=no_go,
    )


DEFAULT_NO_GO = [
    "الإرسال الخارجي أو الأتمتة على المنصّات.",
    "traction مزيّفة أو إعلانات مدفوعة حيّة.",
    "ادعاءات قانونية/أمنية غير مراجَعة.",
]


# ---------------------------------------------------------------------------
# Doc specifications. Each entry: (rel_dir, filename, title, purpose, sections)
# Reports (99_*) handled via a parallel structure.
# ---------------------------------------------------------------------------

DOCS: list[tuple[str, str, str, str, list[tuple[str, list[str]]]]] = []


def add(dir_: str, fname: str, title: str, purpose: str, sections):
    DOCS.append((dir_, fname, title, purpose, sections))


# === 1. Institutional Scale OS ===
S = "institutional-scale-os"
add(
    S,
    "00_INSTITUTIONAL_SCALE_OS.md",
    "Institutional Scale OS — نظام التوسع المؤسسي",
    "الفهرس الرئيسي لطبقة التوسع المؤسسي: كيف ينتقل Dealix من founder-led إلى team-led ومن process إلى platform دون فقدان الجودة.",
    [
        (
            "المكوّنات",
            [
                "01 — أطروحة التوسع (Scale Thesis).",
                "02 — نموذج التشغيل المرحلي (Stage-Based Operating Model).",
                "03 — دليل 0→10 عملاء.",
                "04 — دليل 10→50 عميل.",
                "05 — نموذج تشغيل 50+ عميل.",
                "06 — انتقال من مؤسس إلى فريق.",
                "07 — انتقال من Process إلى Platform.",
                "08 — سجل مخاطر التوسع.",
            ],
        ),
        (
            "مبادئ الحوكمة",
            [
                "لا توسع قبل readiness مُثبَت بمؤشرات.",
                "كل delivery متكرر يتحول إلى module قبل إضافة فريق.",
                "الجودة قبل الحجم؛ السعر يرتفع مع البرهان لا مع الرغبة.",
            ],
        ),
    ],
)
add(
    S,
    "01_SCALE_THESIS.md",
    "Scale Thesis — أطروحة التوسع",
    "لماذا وكيف يتوسع Dealix: التوسع على أساس البرهان (proof) والربحية (margin) وليس على أساس النشاط.",
    [
        (
            "الأطروحة",
            [
                "Dealix يبيع نتائج إيراد وعمليات عبر AI مع موافقة بشرية؛ التوسع يضاعف القيمة لا الضوضاء.",
                "كل عميل ناجح يولّد learning assets وtemplates تخفض كلفة التسليم التالي.",
                "الموات (moat) = عمق القطاع + إعادة استخدام القوالب + أصول الثقة + سلطة الفئة.",
            ],
        ),
        (
            "شروط التوسع",
            [
                "هامش إجمالي مستقر فوق الحد الأدنى للسعر.",
                "معدّل إعادة استخدام التسليم (delivery reuse rate) يرتفع.",
                "خط أنابيب مؤهَّل كافٍ قبل إضافة طاقة.",
            ],
        ),
    ],
)
add(
    S,
    "02_STAGE_BASED_OPERATING_MODEL.md",
    "Stage-Based Operating Model — نموذج التشغيل المرحلي",
    "تعريف كل مرحلة نمو بمؤشراتها وقراراتها ومحفّزاتها.",
    [
        (
            "المراحل",
            [
                "Stage A (0→10): founder-led، إثبات التكرار.",
                "Stage B (10→50): team-assisted، productization.",
                "Stage C (50+): platform-led، حوكمة وتشغيل ممنهج.",
            ],
        ),
        (
            "محفّزات الانتقال",
            [
                "زيادة الفريق عند تجاوز طاقة المؤسس مع pipeline مؤهَّل.",
                "فتح قطاع جديد بعد فوز واضح في القطاع الأول (beachhead).",
                "رفع السعر عند تراكم البرهان وارتفاع الطلب.",
            ],
        ),
    ],
)
add(
    S,
    "03_0_TO_10_CLIENTS_PLAYBOOK.md",
    "0→10 Clients Playbook — دليل أول عشرة عملاء",
    "كيفية إثبات التكرار وبناء أول أصول التعلّم قبل أي توسع.",
    [
        (
            "الأهداف",
            [
                "إثبات أن نفس التسليم ينجح عبر عملاء مختلفين.",
                "توليد أول 5–10 templates قابلة لإعادة الاستخدام.",
                "تثبيت سعر الأرضية والهامش.",
            ],
        ),
        (
            "المؤشرات",
            [
                "وقت التسليم لكل عرض.",
                "نسبة القبول (acceptance) من المحاولة الأولى.",
                "عدد learning assets المُنتَجة لكل عميل.",
            ],
        ),
    ],
)
add(
    S,
    "04_10_TO_50_CLIENTS_PLAYBOOK.md",
    "10→50 Clients Playbook — دليل التوسع المبكر",
    "كيفية تحويل التسليم المتكرر إلى product modules وإضافة طاقة بأمان.",
    [
        (
            "التحركات",
            [
                "productize أعلى 3 عمليات تكرارًا.",
                "إدخال bench المقاولين عبر role-based task packs.",
                "تثبيت بوابات القبول وضبط النطاق (scope control).",
            ],
        ),
        (
            "المؤشرات",
            [
                "delivery reuse rate ≥ هدف داخلي.",
                "الهامش الإجمالي لكل عرض.",
                "وقت دورة من lead إلى delivery.",
            ],
        ),
    ],
)
add(
    S,
    "05_50_PLUS_CLIENTS_OPERATING_MODEL.md",
    "50+ Clients Operating Model — نموذج تشغيل النطاق",
    "تشغيل ممنهج بحوكمة، board reporting، وplatform tooling.",
    [
        (
            "الركائز",
            [
                "حوكمة شهرية عبر Board Governance OS.",
                "CEO Cockpit لقرارات أسبوعية/يومية.",
                "platform/client portal roadmap لتقليل العمل اليدوي المسموح.",
            ],
        ),
        (
            "المؤشرات",
            [
                "موثوقية التسليم عبر الفرق.",
                "نسبة المخاطر المفتوحة المعالَجة.",
                "صحّة unit economics.",
            ],
        ),
    ],
)
add(
    S,
    "06_FOUNDER_TO_TEAM_TRANSITION.md",
    "Founder → Team Transition — انتقال المسؤولية",
    "كيف يفوّض المؤسس دون فقدان الجودة أو السيطرة على القرار النهائي.",
    [
        (
            "الانتقال",
            [
                "توثيق كل SOP قبل التفويض.",
                "الفريق يجهّز ويقترح؛ المؤسس يبقى صاحب قرار البيع والإرسال.",
                "QA إلزامي على كل تسليم خارجي قبل اعتماد المؤسس.",
            ],
        ),
        (
            "متى تضيف فريقًا",
            [
                "pipeline مؤهَّل يتجاوز الطاقة الحالية.",
                "تكرار delivery يبرّر دورًا متخصصًا.",
            ],
        ),
    ],
)
add(
    S,
    "07_PROCESS_TO_PLATFORM_TRANSITION.md",
    "Process → Platform Transition — من العملية إلى المنصّة",
    "كيف يتحول التسليم اليدوي المتكرر إلى modules وأدوات داخلية.",
    [
        (
            "الخطوات",
            [
                "رصد العمليات الأكثر تكرارًا.",
                "تحويلها إلى templates ثم scripts داخلية (generate/score/report فقط).",
                "بناء client portal للقراءة والاعتماد دون إرسال خارجي.",
            ],
        ),
        (
            "الحدود",
            [
                "الأتمتة مسموحة داخليًا فقط: generate/rank/score/validate/summarize/report.",
                "ممنوع send/submit/publish/launch.",
            ],
        ),
    ],
)
add(
    S,
    "08_SCALE_RISK_REGISTER.md",
    "Scale Risk Register — سجل مخاطر التوسع",
    "سجل مخاطر التوسع مع الشدّة والاحتمال والمعالجة.",
    [
        (
            "مخاطر رئيسية",
            [
                "تدهور الجودة عند زيادة الحجم — معالجة: QA gates + DoD.",
                "scope creep — معالجة: Scope Control OS.",
                "تآكل الهامش — معالجة: Profitability OS + pricing floor.",
                "اعتماد مفرط على المؤسس — معالجة: SOPs + bench.",
                "ادعاءات غير مثبتة — معالجة: Case Study Governance + no-overclaim register.",
            ],
        )
    ],
)

# === 2. Board Governance OS ===
B = "board-governance-os"
add(
    B,
    "00_BOARD_GOVERNANCE_OS.md",
    "Board Governance OS — نظام حوكمة المجلس",
    "إطار تقارير المجلس الشهرية، مذكّرات القرار، ومراجعة المخاطر مع سياسة نزاهة المؤشرات.",
    [
        (
            "المكوّنات",
            [
                "قالب حزمة المجلس (Board Packet).",
                "المراجعة الشهرية، مذكّرة القرار، مراجعة المخاطر.",
                "سياسة نزاهة المؤشرات ونظام مساءلة المؤسس.",
            ],
        )
    ],
)
add(
    B,
    "01_BOARD_PACKET_TEMPLATE.md",
    "Board Packet Template — قالب حزمة المجلس",
    "القالب القياسي الذي يولّده `scripts/board_packet_generate.py`.",
    [
        (
            "الأقسام الإلزامية",
            [
                "executive summary، revenue activity، pipeline quality.",
                "delivery status، product progress، site/media progress.",
                "risks، cash assumptions، hiring triggers.",
                "decisions required، evidence links.",
                "سياسة لا traction مزيّفة (no fake traction).",
            ],
        )
    ],
)
add(
    B,
    "02_MONTHLY_BOARD_REVIEW.md",
    "Monthly Board Review — المراجعة الشهرية",
    "إيقاع شهري لمراجعة الأداء والقرارات بحوكمة واضحة.",
    [
        (
            "الأجندة",
            [
                "مراجعة المؤشرات مقابل الافتراضات.",
                "القرارات المطلوبة هذا الشهر.",
                "المخاطر المفتوحة ومعالجتها.",
            ],
        )
    ],
)
add(
    B,
    "03_DECISION_MEMO_TEMPLATE.md",
    "Decision Memo Template — قالب مذكّرة القرار",
    "هيكل قرار واحد: السياق، الخيارات، التوصية، المخاطر، القرار.",
    [
        (
            "الهيكل",
            [
                "السياق والمشكلة.",
                "الخيارات مع المقايضات.",
                "توصية AI (تجهيز) + قرار المؤسس (اعتماد).",
            ],
        )
    ],
)
add(
    B,
    "04_RISK_REVIEW_TEMPLATE.md",
    "Risk Review Template — قالب مراجعة المخاطر",
    "مراجعة دورية للمخاطر بالشدّة والاحتمال والمالك والمعالجة.",
    [("الحقول", ["الخطر", "الشدّة×الاحتمال", "المالك", "المعالجة", "الحالة"])],
)
add(
    B,
    "05_METRIC_INTEGRITY_POLICY.md",
    "Metric Integrity Policy — سياسة نزاهة المؤشرات",
    "كل رقم يُعرض على المجلس يجب أن يكون قابلًا للتتبّع إلى مصدر أو يُعلَّم كافتراض.",
    [
        (
            "القواعد",
            [
                "لا أرقام إيراد حقيقية مُختلقة؛ inputs يدوية/example فقط في المستودع.",
                "كل تقدير يُوسَم assumption صراحةً.",
                "لا traction مزيّفة ولا نتائج بدون evidence.",
            ],
        )
    ],
)
add(
    B,
    "06_FOUNDER_ACCOUNTABILITY_SYSTEM.md",
    "Founder Accountability System — نظام مساءلة المؤسس",
    "كيف يبقى المؤسس مسؤولًا أمام المجلس عن القرارات والالتزامات.",
    [
        (
            "الآلية",
            [
                "كل قرار مجلس له مالك وموعد ومخرج متوقع.",
                "مراجعة الالتزامات السابقة في بداية كل اجتماع.",
            ],
        )
    ],
)

# === 3. Market Domination OS ===
M = "market-domination-os"
add(
    M,
    "00_MARKET_DOMINATION_OS.md",
    "Market Domination OS — نظام السيطرة على السوق",
    "كيف يفوز Dealix بأول قطاع ثم يصبح المرجع في فئة AI Revenue & Operations OS في السعودية والخليج.",
    [
        (
            "المكوّنات",
            [
                "beachhead strategy، vertical domination، thought leadership moat.",
                "proof asset distribution، referral & partner loop.",
                "local market credibility، category education.",
            ],
        )
    ],
)
add(
    M,
    "01_BEACHHEAD_STRATEGY.md",
    "Beachhead Strategy — استراتيجية رأس الجسر",
    "كيف نفوز بأول قطاع بعمق قبل التوسع الأفقي.",
    [
        (
            "المبادئ",
            [
                "اختيار قطاع واحد قابل للتكرار وله ألم إيراد واضح.",
                "تركيز كل proof assets والمحتوى عليه.",
                "معيار الانتقال: فوز متكرر + طلب وارد.",
            ],
        )
    ],
)
add(
    M,
    "02_VERTICAL_DOMINATION_PLAN.md",
    "Vertical Domination Plan — خطة السيطرة القطاعية",
    "كيف نعرف أن القطاع يستحق التوسع وكيف نعمّق الحضور فيه.",
    [
        (
            "الإشارات",
            [
                "تكرار نفس الألم عبر عملاء القطاع.",
                "ارتفاع نسبة الإحالات داخل القطاع.",
                "قوالب القطاع تخفض وقت التسليم.",
            ],
        )
    ],
)
add(
    M,
    "03_THOUGHT_LEADERSHIP_MOAT.md",
    "Thought Leadership Moat — موات القيادة الفكرية",
    "كيف نصبح معروفين في فئة AI Revenue & Operations OS عبر محتوى تعليمي موثوق.",
    [
        (
            "التحركات",
            [
                "محتوى يشرح المنهج لا يبيع مباشرة.",
                "نشر مسؤول يدويًا باعتماد المؤسس (لا أتمتة LinkedIn).",
                "تحويل كل درس تسليم إلى محتوى فئة.",
            ],
        )
    ],
)
add(
    M,
    "04_PROOF_ASSET_DISTRIBUTION.md",
    "Proof Asset Distribution — توزيع أصول البرهان",
    "كيف نحوّل proof packs وحالات الاستخدام إلى توزيع — ضمن حوكمة الحالات.",
    [
        (
            "القواعد",
            [
                "لا اسم عميل بدون إذن موثّق.",
                "أرقام نتائج فقط مع evidence.",
                "حالات مجهّلة (anonymized) عند الحاجة.",
            ],
        )
    ],
)
add(
    M,
    "05_REFERRAL_AND_PARTNER_LOOP.md",
    "Referral & Partner Loop — حلقة الإحالة والشركاء",
    "كيف نستفيد من الشركاء والإحالات لتوزيع منضبط.",
    [
        (
            "الحلقة",
            [
                "تحديد شركاء التوزيع المحتملين.",
                "drafts للتواصل تُعتمد وتُرسل يدويًا من المؤسس.",
                "تتبّع الإحالات دون حوافز مضلّلة.",
            ],
        )
    ],
)
add(
    M,
    "06_LOCAL_MARKET_CREDIBILITY.md",
    "Local Market Credibility — مصداقية السوق المحلي",
    "كيف نبني مصداقية في السعودية والخليج بإشارات ثقة محلية.",
    [
        (
            "الإشارات",
            [
                "لغة عربية تنفيذية وسياق محلي.",
                "التزام PDPL/ZATCA-aware في الخطاب (دون ادعاء امتثال كامل غير مراجَع).",
                "أمثلة قطاعية محلية.",
            ],
        )
    ],
)
add(
    M,
    "07_CATEGORY_EDUCATION_PLAN.md",
    "Category Education Plan — خطة تعليم الفئة",
    "كيف نستخدم المحتوى لتعليم السوق بفئة AI Revenue & Operations OS.",
    [
        (
            "الخطة",
            [
                "سلسلة محتوى تشرح المشكلة قبل الحل.",
                "ربط كل محتوى بأصل برهان قابل للمراجعة.",
            ],
        )
    ],
)

# === 4. Enterprise Sales Room OS ===
E = "enterprise-sales-room-os"
add(
    E,
    "00_ENTERPRISE_SALES_ROOM_OS.md",
    "Enterprise Sales Room OS — غرفة المبيعات المؤسسية",
    "نظام إعداد صفقات المؤسسات: stakeholders، business case، security/legal، procurement، proposal، pilot، close plan — كله draft للمراجعة.",
    [
        (
            "المخرجات",
            [
                "stakeholder_map، business_case، executive_proposal.",
                "security_legal_pack، procurement_pack، pilot_governance، close_plan.",
                "يولّدها `scripts/enterprise_sales_room_generate.py`.",
            ],
        )
    ],
)
add(
    E,
    "01_ENTERPRISE_SALES_PROCESS.md",
    "Enterprise Sales Process — عملية البيع المؤسسي",
    "مراحل البيع المؤسسي من discovery إلى close مع بوابات حوكمة.",
    [
        (
            "المراحل",
            ["discovery", "business case", "security/legal", "procurement", "pilot", "close"],
        )
    ],
)
add(
    E,
    "02_STAKEHOLDER_MAP.md",
    "Stakeholder Map — خريطة أصحاب القرار",
    "تحديد الراعي، المستخدم، الحارس، والمعارض داخل المؤسسة.",
    [
        (
            "الأدوار",
            [
                "economic buyer",
                "champion",
                "technical/security gatekeeper",
                "procurement",
                "end users",
            ],
        )
    ],
)
add(
    E,
    "03_BUSINESS_CASE_TEMPLATE.md",
    "Business Case Template — قالب الحالة التجارية",
    "حالة تجارية مبنية على افتراضات معلَّمة بوضوح دون ROI مضمون.",
    [
        (
            "الأقسام",
            [
                "المشكلة وكلفتها الحالية (assumptions).",
                "النطاق المقترح والمخرجات.",
                "تقدير الأثر مع وسم كل رقم كافتراض.",
            ],
        )
    ],
)
add(
    E,
    "04_SECURITY_AND_LEGAL_PACK.md",
    "Security & Legal Pack — حزمة الأمن والقانون",
    "ملخّص وضع الأمن والخصوصية بصدق دون شهادات غير موجودة.",
    [
        (
            "المحتوى",
            [
                "ممارسات أمنية مرجعية (NIST CSF / OWASP) كأطر تحقق لا كشهادات.",
                "وضع PDPL-aware دون ادعاء امتثال كامل غير مراجَع.",
                "لا ادعاء ISO/SOC2 ما لم يوجد فعليًا.",
            ],
        )
    ],
)
add(
    E,
    "05_PROCUREMENT_PACK.md",
    "Procurement Pack — حزمة المشتريات",
    "مستندات تسهّل مسار المشتريات: vendor info، scope، terms references (templates only).",
    [("المحتوى", ["معلومات المورّد", "نطاق العمل", "مراجع شروط (قوالب تحتاج مراجعة قانونية)"])],
)
add(
    E,
    "06_EXECUTIVE_PROPOSAL_TEMPLATE.md",
    "Executive Proposal Template — قالب العرض التنفيذي",
    "عرض تنفيذي موجز للقرار، مبني على القيمة والبرهان القابل للمراجعة.",
    [("الأقسام", ["الملخّص التنفيذي", "النطاق والمخرجات", "الجدول والسعر", "الخطوة التالية"])],
)
add(
    E,
    "07_PILOT_GOVERNANCE_MODEL.md",
    "Pilot Governance Model — حوكمة التجربة",
    "كيف نحوكم pilot بمعايير نجاح واضحة وبوابة قبول.",
    [("العناصر", ["نطاق محدود", "معايير نجاح مقاسة", "بوابة قبول", "مسار التحول إلى retainer"])],
)
add(
    E,
    "08_ENTERPRISE_CLOSE_PLAN.md",
    "Enterprise Close Plan — خطة الإغلاق",
    "خطة إغلاق متبادلة (mutual close plan) بخطوات وتواريخ ومالكين.",
    [("العناصر", ["الخطوات المتبادلة", "التواريخ", "المالكون", "المخاطر"])],
)

# === 5. Customer Advisory Board OS ===
C = "customer-advisory-os"
add(
    C,
    "00_CUSTOMER_ADVISORY_OS.md",
    "Customer Advisory OS — نظام المجلس الاستشاري للعملاء",
    "كيف نستفيد من أول العملاء كحلقة feedback تتحول إلى roadmap دون تضخيم أو استخدام أسماء بدون إذن.",
    [
        (
            "المكوّنات",
            [
                "أطروحة المجلس",
                "المستشارون المثاليون",
                "قالب الدعوة",
                "أجندة ربعية",
                "حلقة feedback→product",
            ],
        )
    ],
)
add(
    C,
    "01_ADVISORY_BOARD_THESIS.md",
    "Advisory Board Thesis — أطروحة المجلس الاستشاري",
    "لماذا نبني مجلسًا استشاريًا من العملاء وكيف يضيف قيمة دون تعارض.",
    [
        (
            "الأطروحة",
            [
                "feedback مبكر يقلّل مخاطر المنتج",
                "بناء ثقة وعلاقة طويلة",
                "بدون تضخيم أو التزامات وهمية",
            ],
        )
    ],
)
add(
    C,
    "02_IDEAL_ADVISORS.md",
    "Ideal Advisors — المستشارون المثاليون",
    "معايير اختيار المستشارين من العملاء.",
    [("المعايير", ["تمثيل القطاع المستهدف", "صدق الملاحظات", "استعداد للمشاركة المنتظمة"])],
)
add(
    C,
    "03_ADVISOR_INVITE_TEMPLATE.md",
    "Advisor Invite Template — قالب دعوة المستشار",
    "قالب دعوة يُعتمد ويُرسل يدويًا من المؤسس.",
    [
        (
            "العناصر",
            [
                "الغرض",
                "الالتزام الزمني",
                "ما يحصل عليه المستشار",
                "بدون استخدام اسمه علنًا بدون إذن",
            ],
        )
    ],
)
add(
    C,
    "04_QUARTERLY_ADVISORY_AGENDA.md",
    "Quarterly Advisory Agenda — الأجندة الربعية",
    "هيكل اجتماع ربعي يحوّل الملاحظات إلى قرارات.",
    [("الأجندة", ["مراجعة roadmap", "أهم الملاحظات", "الأولويات القادمة"])],
)
add(
    C,
    "05_FEEDBACK_TO_PRODUCT_LOOP.md",
    "Feedback → Product Loop — حلقة الملاحظات إلى المنتج",
    "كيف نحوّل feedback وobjections إلى roadmap وproof assets.",
    [
        (
            "الحلقة",
            ["جمع الملاحظات", "ترتيبها وتقييمها", "تحويل objection إلى proof asset قابل للمراجعة"],
        )
    ],
)

# === 6. Commercial Legal Readiness OS ===
L = "commercial-legal-readiness-os"
_legal_note = "Templates only — ليست استشارة قانونية وتحتاج مراجعة قانونية قبل أي استخدام رسمي. لا لغة تدّعي امتثالًا كاملًا."
add(
    L,
    "00_COMMERCIAL_LEGAL_READINESS_OS.md",
    "Commercial Legal Readiness OS — الجاهزية القانونية التجارية",
    "قوالب تعاقد جاهزة للمراجعة: مسارات تعاقد، SOW، pilot، retainer، change request، acceptance، بوابة مراجعة قانونية.",
    [
        ("تنبيه", [_legal_note]),
        (
            "المكوّنات",
            [
                "contracting paths",
                "SOW playbook",
                "pilot/retainer/CR/acceptance templates",
                "legal review gate",
            ],
        ),
    ],
)
add(
    L,
    "01_CONTRACTING_PATHS.md",
    "Contracting Paths — مسارات التعاقد",
    "مسارات التعاقد حسب نوع العميل والصفقة.",
    [
        ("تنبيه", [_legal_note]),
        ("المسارات", ["pilot ثم retainer", "SOW لمشروع محدد", "اتفاقية إطارية للمؤسسات"]),
    ],
)
add(
    L,
    "02_SOW_PLAYBOOK.md",
    "SOW Playbook — دليل نطاق العمل",
    "كيف نكتب SOW واضح يحمي النطاق والربحية.",
    [
        ("تنبيه", [_legal_note]),
        ("العناصر", ["النطاق", "المخرجات", "المعايير", "الاستثناءات", "تغيير النطاق"]),
    ],
)
add(
    L,
    "03_PILOT_AGREEMENT_TEMPLATE.md",
    "Pilot Agreement Template — قالب اتفاقية التجربة",
    "قالب اتفاقية تجربة محدودة.",
    [("تنبيه", [_legal_note]), ("العناصر", ["النطاق المحدود", "المدة", "معايير النجاح", "السرية"])],
)
add(
    L,
    "04_RETAINER_AGREEMENT_TEMPLATE.md",
    "Retainer Agreement Template — قالب اتفاقية الاحتفاظ",
    "قالب اتفاقية retainer شهري.",
    [("تنبيه", [_legal_note]), ("العناصر", ["النطاق الشهري", "المخرجات", "الرسوم", "إنهاء"])],
)
add(
    L,
    "05_CHANGE_REQUEST_TEMPLATE.md",
    "Change Request Template — قالب طلب التغيير",
    "قالب موحّد لطلبات تغيير النطاق.",
    [("تنبيه", [_legal_note]), ("العناصر", ["وصف التغيير", "الأثر على الجدول والسعر", "الاعتماد"])],
)
add(
    L,
    "06_ACCEPTANCE_SIGNOFF_TEMPLATE.md",
    "Acceptance Sign-off Template — قالب قبول التسليم",
    "قالب توقيع قبول التسليم.",
    [("تنبيه", [_legal_note]), ("العناصر", ["المخرجات المقبولة", "المعايير المستوفاة", "التوقيع"])],
)
add(
    L,
    "07_LEGAL_REVIEW_GATE.md",
    "Legal Review Gate — بوابة المراجعة القانونية",
    "بوابة إلزامية قبل أي استخدام رسمي للقوالب.",
    [("القاعدة", ["كل قالب يمر بمراجعة قانونية قبل التوقيع.", "لا ادعاء امتثال كامل في النصوص."])],
)

# === 7. Profitability OS ===
P = "profitability-os"
add(
    P,
    "00_PROFITABILITY_OS.md",
    "Profitability OS — نظام الهامش والربحية",
    "نموذج هامش الخدمة وكلفة التسليم وحدود الهامش وأرضية السعر — بمدخلات example/manual فقط، وكل تقدير مُعلَّم كافتراض.",
    [
        (
            "المكوّنات",
            [
                "service margin model",
                "delivery cost model",
                "gross margin guardrails",
                "pricing floor",
                "discount rules",
                "scope creep cost",
                "monthly profit review",
            ],
        ),
        (
            "تنبيه",
            ["لا أرقام إيراد حقيقية؛ inputs من `data/profitability_inputs.example.jsonl` فقط."],
        ),
    ],
)
add(
    P,
    "01_SERVICE_MARGIN_MODEL.md",
    "Service Margin Model — نموذج هامش الخدمة",
    "كيف نحسب الهامش لكل عرض من العروض الخمسة.",
    [
        (
            "المنهج",
            [
                "سعر العرض − كلفة التسليم = هامش",
                "كل المدخلات example/assumption",
                "يُلخّصها `scripts/profitability_summary.py`",
            ],
        )
    ],
)
add(
    P,
    "02_DELIVERY_COST_MODEL.md",
    "Delivery Cost Model — نموذج كلفة التسليم",
    "مكوّنات كلفة التسليم وكيف نخفضها بالقوالب.",
    [("المكوّنات", ["وقت المؤسس/الفريق", "وقت المقاول", "أدوات", "إعادة العمل (rework)"])],
)
add(
    P,
    "03_GROSS_MARGIN_GUARDRAILS.md",
    "Gross Margin Guardrails — حدود الهامش الإجمالي",
    "حدود دنيا للهامش توقف الصفقة دون مراجعة.",
    [
        (
            "الحدود",
            [
                "هامش أدنى مستهدف لكل عرض",
                "تنبيه عند الاقتراب من الحد",
                "مراجعة المؤسس قبل القبول دون الحد",
            ],
        )
    ],
)
add(
    P,
    "04_PRICING_FLOOR_POLICY.md",
    "Pricing Floor Policy — سياسة أرضية السعر",
    "أرضية سعر لكل عرض لا يُنزل تحتها دون اعتماد.",
    [
        (
            "السلم",
            [
                "Free Diagnostic",
                "499 SAR Sprint",
                "1,500 SAR Data Pack",
                "2,999–4,999 SAR/mo Managed Ops",
                "5K–25K SAR Custom AI",
            ],
        )
    ],
)
add(
    P,
    "05_DISCOUNT_APPROVAL_RULES.md",
    "Discount Approval Rules — قواعد اعتماد الخصم",
    "متى وكيف يُعتمد الخصم.",
    [("القواعد", ["خصم محدود ضمن صلاحية", "ما يتجاوزها يتطلب اعتماد المؤسس", "توثيق سبب الخصم"])],
)
add(
    P,
    "06_SCOPE_CREEP_COST_CONTROL.md",
    "Scope Creep Cost Control — ضبط كلفة تمدد النطاق",
    "كيف نمنع scope creep من تآكل الهامش.",
    [("الضبط", ["كل خارج النطاق = change request", "تسعير التغيير", "حماية الهامش والثقة معًا"])],
)
add(
    P,
    "07_MONTHLY_PROFIT_REVIEW.md",
    "Monthly Profit Review — المراجعة الشهرية للربح",
    "إيقاع شهري لمراجعة الهامش الفعلي مقابل المستهدف.",
    [("الأجندة", ["هامش كل عرض", "أكبر مصادر تآكل الهامش", "قرارات التسعير/النطاق"])],
)

# === 8. Scope Control OS ===
SC = "scope-control-os"
add(
    SC,
    "00_SCOPE_CONTROL_OS.md",
    "Scope Control OS — نظام ضبط النطاق",
    "كيف نمنع scope creep ونحمي الربحية والثقة عبر حدود نطاق واضحة وبوابات قبول.",
    [
        (
            "المكوّنات",
            [
                "scope boundary policy",
                "change request process",
                "out-of-scope library",
                "client request triage",
                "delivery acceptance gates",
            ],
        )
    ],
)
add(
    SC,
    "01_SCOPE_BOUNDARY_POLICY.md",
    "Scope Boundary Policy — سياسة حدود النطاق",
    "ما الذي يدخل في كل عرض وما لا يدخل.",
    [("الحدود", ["ما يدخل في diagnostic", "ما يدخل في pilot", "ما لا يدخل في أي منهما"])],
)
add(
    SC,
    "02_CHANGE_REQUEST_PROCESS.md",
    "Change Request Process — عملية طلب التغيير",
    "كيف يُطلب ويُعتمد تغيير النطاق.",
    [("الخطوات", ["توثيق الطلب", "تقدير الأثر", "اعتماد قبل التنفيذ"])],
)
add(
    SC,
    "03_OUT_OF_SCOPE_LIBRARY.md",
    "Out-of-Scope Library — مكتبة خارج النطاق",
    "أمثلة شائعة لما هو خارج النطاق لتسريع الفرز.",
    [
        (
            "أمثلة",
            [
                "تكاملات غير متفق عليها",
                "تقارير إضافية",
                "تدريب موسّع",
                "دعم خارج الساعات المتفق عليها",
            ],
        )
    ],
)
add(
    SC,
    "04_CLIENT_REQUEST_TRIAGE.md",
    "Client Request Triage — فرز طلبات العميل",
    "كيف نفرز كل طلب: داخل النطاق، تغيير، أو لاحقًا.",
    [
        (
            "الفرز",
            ["داخل النطاق → تنفيذ", "خارج النطاق → change request", "غير ضروري الآن → backlog"],
        )
    ],
)
add(
    SC,
    "05_DELIVERY_ACCEPTANCE_GATES.md",
    "Delivery Acceptance Gates — بوابات قبول التسليم",
    "معايير قبول كل تسليم قبل اعتماده.",
    [("البوابات", ["استيفاء معايير DoD", "QA داخلي", "اعتماد المؤسس قبل الإرسال"])],
)

# === 9. Case Study Governance OS ===
CS = "case-study-governance-os"
add(
    CS,
    "00_CASE_STUDY_GOVERNANCE_OS.md",
    "Case Study Governance OS — حوكمة دراسات الحالة",
    "كيف ننتج proof assets ودراسات حالة بصدق: إذن العميل، أرقام مدعومة بـ evidence، لا حالات مزيّفة.",
    [
        (
            "المكوّنات",
            [
                "eligibility",
                "client permission",
                "anonymized process",
                "metric claim rules",
                "proof asset review gate",
            ],
        )
    ],
)
add(
    CS,
    "01_CASE_STUDY_ELIGIBILITY.md",
    "Case Study Eligibility — أهلية دراسة الحالة",
    "متى يكون العميل مؤهلًا لدراسة حالة.",
    [("المعايير", ["نتيجة قابلة للقياس", "evidence موثّق", "إذن العميل"])],
)
add(
    CS,
    "02_CLIENT_PERMISSION_PROCESS.md",
    "Client Permission Process — عملية إذن العميل",
    "كيف نحصل على إذن موثّق قبل استخدام اسم العميل.",
    [("الخطوات", ["طلب إذن مكتوب", "تحديد ما يُنشر", "حق السحب"])],
)
add(
    CS,
    "03_ANONYMIZED_CASE_PROCESS.md",
    "Anonymized Case Process — الحالات المجهّلة",
    "كيف ننتج حالة مجهّلة عند غياب الإذن للاسم.",
    [("القواعد", ["إخفاء الهوية", "أرقام مدعومة فقط", "وصف القطاع دون كشف العميل"])],
)
add(
    CS,
    "04_METRIC_CLAIM_RULES.md",
    "Metric Claim Rules — قواعد ادعاء الأرقام",
    "لا رقم نتيجة بدون evidence ولا مبالغة.",
    [("القواعد", ["كل رقم له مصدر", "لا ROI مضمون", "وسم الافتراضات"])],
)
add(
    CS,
    "05_PROOF_ASSET_REVIEW_GATE.md",
    "Proof Asset Review Gate — بوابة مراجعة أصول البرهان",
    "بوابة مراجعة قبل نشر أي proof asset.",
    [("البوابة", ["مراجعة الادعاءات", "تأكيد الإذن", "اعتماد المؤسس"])],
)

# === 10. Competitive Win Room OS ===
W = "competitive-win-room-os"
_battle_note = "موضوعي ومحترم — لا تشهير ولا ادعاءات غير مثبتة. التركيز على positioning."
add(
    W,
    "00_COMPETITIVE_WIN_ROOM_OS.md",
    "Competitive Win Room OS — غرفة الفوز التنافسي",
    "بطاقات معركة موضوعية مقابل البدائل، مع مراجعة win/loss.",
    [
        ("تنبيه", [_battle_note]),
        (
            "المكوّنات",
            [
                "battlecard index",
                "vs CRM/agency/software house/internal IT/generic AI chatbot",
                "win-loss review",
            ],
        ),
    ],
)
add(
    W,
    "01_BATTLECARD_INDEX.md",
    "Battlecard Index — فهرس بطاقات المعركة",
    "فهرس البطاقات ومتى تُستخدم.",
    [
        ("تنبيه", [_battle_note]),
        (
            "الفهرس",
            ["vs CRM", "vs Agency", "vs Software House", "vs Internal IT", "vs Generic AI Chatbot"],
        ),
    ],
)
add(
    W,
    "02_VS_CRM_BATTLECARD.md",
    "vs CRM — بطاقة مقابل CRM",
    "متى يكون Dealix مكمّلًا لا بديلًا لـ CRM.",
    [
        ("تنبيه", [_battle_note]),
        (
            "Positioning",
            ["Dealix يحوّل بيانات CRM إلى قرارات إيراد مع موافقة بشرية", "ليس CRM بديلًا"],
        ),
    ],
)
add(
    W,
    "03_VS_AGENCY_BATTLECARD.md",
    "vs Agency — بطاقة مقابل الوكالة",
    "الفرق عن وكالة تسويق/مبيعات تقليدية.",
    [
        ("تنبيه", [_battle_note]),
        ("Positioning", ["نظام تشغيل مدعوم AI لا ساعات عمل", "قابلية تكرار وقوالب"]),
    ],
)
add(
    W,
    "04_VS_CUSTOM_SOFTWARE_HOUSE.md",
    "vs Custom Software House — بطاقة مقابل بيت برمجة",
    "الفرق عن مشروع برمجي مخصص طويل.",
    [
        ("تنبيه", [_battle_note]),
        ("Positioning", ["قيمة أسرع عبر modules جاهزة", "بدون مشروع طويل المخاطر"]),
    ],
)
add(
    W,
    "05_VS_INTERNAL_IT.md",
    "vs Internal IT — بطاقة مقابل تقنية داخلية",
    "الفرق عن بناء داخلي.",
    [
        ("تنبيه", [_battle_note]),
        ("Positioning", ["خبرة قطاعية وقوالب جاهزة", "تركيز IT الداخلي على أولوياته"]),
    ],
)
add(
    W,
    "06_VS_GENERIC_AI_CHATBOT.md",
    "vs Generic AI Chatbot — بطاقة مقابل شات بوت عام",
    "الفرق عن chatbot عام.",
    [
        ("تنبيه", [_battle_note]),
        ("Positioning", ["نظام تشغيل إيراد محكوم بموافقة لا مجرد محادثة", "evidence وحوكمة"]),
    ],
)
add(
    W,
    "07_WIN_LOSS_REVIEW.md",
    "Win/Loss Review — مراجعة الفوز والخسارة",
    "كيف نتعلّم من كل صفقة.",
    [
        ("تنبيه", [_battle_note]),
        ("المراجعة", ["سبب الفوز/الخسارة", "اعتراضات متكررة", "تحسينات positioning"]),
    ],
)

# === 11. Saudi/GCC Localization OS ===
LO = "localization-os"
add(
    LO,
    "00_SAUDI_GCC_LOCALIZATION_OS.md",
    "Saudi/GCC Localization OS — نظام التوطين السعودي الخليجي",
    "لغة عربية تنفيذية غير مترجمة حرفيًا، بسياق سعودي/خليجي، وإشارات ثقة محلية.",
    [
        (
            "المكوّنات",
            [
                "arabic business language",
                "saudi buyer context",
                "gcc expansion",
                "sector language",
                "local trust signals",
                "cultural tone",
            ],
        )
    ],
)
add(
    LO,
    "01_ARABIC_BUSINESS_LANGUAGE_GUIDE.md",
    "Arabic Business Language Guide — دليل اللغة التجارية العربية",
    "كيف نكتب عربية تنفيذية قوية ومحترمة غير مترجمة حرفيًا.",
    [
        ("مبادئ", ["جُمل قصيرة واضحة", "أفعال قوية", "بدون حشو إنجليزي غير ضروري"]),
        ("كلمات ضعيفة/ممنوعة", ["نضمن لك", "الأفضل في العالم", "ثوري", "بدون مجهود"]),
        (
            "صياغات قوية",
            ["نُجهّز ونرتّب القرار، وأنت تعتمد", "نتائج مدعومة بـ evidence", "منهج قابل للتكرار"],
        ),
    ],
)
add(
    LO,
    "02_SAUDI_BUYER_CONTEXT.md",
    "Saudi Buyer Context — سياق المشتري السعودي",
    "كيف نخاطب المدير والمالك والشريك ورئيس العمليات.",
    [
        (
            "المخاطبة",
            [
                "المالك: نمو وربحية",
                "المدير: سيطرة وتقارير",
                "رئيس العمليات: كفاءة وتقليل عمل يدوي",
                "الشريك: مخاطرة محسوبة وبرهان",
            ],
        )
    ],
)
add(
    LO,
    "03_GCC_EXPANSION_NOTES.md",
    "GCC Expansion Notes — ملاحظات التوسع الخليجي",
    "اعتبارات التوسع للخليج بعد ترسيخ السعودية.",
    [("اعتبارات", ["اختلافات تنظيمية", "تكييف اللغة لكل سوق", "شركاء توزيع محليون"])],
)
add(
    LO,
    "04_SECTOR_LANGUAGE_GUIDE.md",
    "Sector Language Guide — دليل لغة القطاعات",
    "أمثلة صياغة لكل قطاع مستهدف.",
    [
        (
            "أمثلة قطاعية",
            [
                "تجزئة/تجارة: دورة الشراء والمخزون",
                "عقارات: دورة الليد الطويلة",
                "خدمات B2B: العروض والعقود",
                "صحة/تعليم: الثقة والامتثال",
            ],
        )
    ],
)
add(
    LO,
    "05_LOCAL_TRUST_SIGNALS.md",
    "Local Trust Signals — إشارات الثقة المحلية",
    "ما يبني الثقة في السوق المحلي دون ادعاءات.",
    [
        (
            "الإشارات",
            [
                "لغة ومحتوى عربي رصين",
                "وعي PDPL/ZATCA دون ادعاء امتثال كامل",
                "برهان قابل للمراجعة",
                "حضور محلي",
            ],
        )
    ],
)
add(
    LO,
    "06_CULTURAL_TONE_RULES.md",
    "Cultural Tone Rules — قواعد النبرة الثقافية",
    "نبرة محترمة ومهنية تناسب السوق.",
    [("القواعد", ["احترام ورسمية مناسبة", "بدون مبالغة أو ضغط", "وضوح والتزام بالوعود"])],
)

# === 12. Talent Bench & Contractor Marketplace OS ===
T = "talent-bench-os"
add(
    T,
    "00_TALENT_BENCH_OS.md",
    "Talent Bench OS — نظام مقاعد المواهب والمقاولين",
    "كيف نضيف مقاولين بأمان: task packs من الريبو، QA، حماية الأسرار، ومنع كشف العملاء بدون إذن.",
    [
        (
            "المكوّنات",
            [
                "contractor bench strategy",
                "role-based task packs",
                "contractor QA",
                "delivery partner scorecard",
                "on-demand capacity",
            ],
        )
    ],
)
add(
    T,
    "01_CONTRACTOR_BENCH_STRATEGY.md",
    "Contractor Bench Strategy — استراتيجية المقاعد",
    "كيف نبني bench مرنًا دون فوضى.",
    [("المبادئ", ["إضافة عند الحاجة فقط", "أدوار محددة", "عقود وسرية واضحة"])],
)
add(
    T,
    "02_ROLE_BASED_TASK_PACKS.md",
    "Role-Based Task Packs — حزم مهام حسب الدور",
    "كيف نعطي المقاولين مهامًا من الريبو بحدود واضحة.",
    [("الحزم", ["مهمة محددة المخرجات", "وصول محدود", "بدون أسرار العميل ما لم يُصرّح"])],
)
add(
    T,
    "03_CONTRACTOR_QA.md",
    "Contractor QA — ضمان جودة المقاول",
    "كيف نراجع جودة عمل المقاول قبل الاعتماد.",
    [("الآلية", ["مراجعة مقابل DoD", "تغذية راجعة", "بوابة قبول قبل التسليم للعميل"])],
)
add(
    T,
    "04_DELIVERY_PARTNER_SCORECARD.md",
    "Delivery Partner Scorecard — بطاقة أداء شريك التسليم",
    "تقييم المقاولين بمؤشرات.",
    [("المؤشرات", ["الجودة", "الالتزام بالموعد", "إعادة العمل", "التواصل"])],
)
add(
    T,
    "05_ON_DEMAND_CAPACITY_PLAN.md",
    "On-Demand Capacity Plan — خطة الطاقة عند الطلب",
    "كيف نوسّع الطاقة عند ذروة الطلب.",
    [("الخطة", ["bench جاهز", "task packs معدّة مسبقًا", "تفعيل سريع بحوكمة"])],
)

# === 13. Productization OS ===
PR2 = "productization-os"
add(
    PR2,
    "00_PRODUCTIZATION_OS.md",
    "Productization OS — نظام تحويل الخدمة إلى منتج",
    "كيف يتحول كل delivery إلى module قابل لإعادة الاستخدام يخفض وقت التسليم ويرفع الهامش.",
    [
        (
            "المكوّنات",
            [
                "from service to product",
                "repeatable modules",
                "template library",
                "client portal roadmap",
                "internal tooling roadmap",
                "productized delivery checklist",
            ],
        )
    ],
)
add(
    PR2,
    "01_FROM_SERVICE_TO_PRODUCT.md",
    "From Service to Product — من خدمة إلى منتج",
    "كيف نعرف أن workflow يستحق productization.",
    [("الإشارات", ["تكرار ≥ 3 مرات", "نفس المخرجات", "إمكانية القولبة"])],
)
add(
    PR2,
    "02_REPEATABLE_MODULES.md",
    "Repeatable Modules — الوحدات القابلة للتكرار",
    "كيف نبني modules من عمليات التسليم المتكررة.",
    [("البناء", ["مدخلات/مخرجات واضحة", "قالب + checklist", "نقاط QA"])],
)
add(
    PR2,
    "03_TEMPLATE_LIBRARY.md",
    "Template Library — مكتبة القوالب",
    "كيف ننظّم القوالب لإعادة الاستخدام.",
    [("التنظيم", ["تصنيف حسب العرض/القطاع", "نسخ محدّثة", "ربط بـ Operating Leverage OS"])],
)
add(
    PR2,
    "04_CLIENT_PORTAL_ROADMAP.md",
    "Client Portal Roadmap — خارطة بوابة العميل",
    "خطة بوابة للقراءة والاعتماد دون إرسال خارجي.",
    [("المراحل", ["عرض المخرجات", "اعتماد العميل داخليًا", "بدون أي إرسال خارجي تلقائي"])],
)
add(
    PR2,
    "05_INTERNAL_TOOLING_ROADMAP.md",
    "Internal Tooling Roadmap — خارطة الأدوات الداخلية",
    "أدوات داخلية generate/score/report فقط.",
    [("الأدوات", ["مولّدات حزم", "مقيّمات", "مولّدات تقارير", "بدون send/submit"])],
)
add(
    PR2,
    "06_PRODUCTIZED_DELIVERY_CHECKLIST.md",
    "Productized Delivery Checklist — قائمة التسليم المُمنتَج",
    "checklist لكل تسليم مُمنتَج.",
    [("القائمة", ["استخدام القالب", "تخصيص محدود", "QA", "اعتماد المؤسس"])],
)

# === 14. Operating Leverage OS ===
OL = "operating-leverage-os"
add(
    OL,
    "00_OPERATING_LEVERAGE_OS.md",
    "Operating Leverage OS — نظام الرافعة التشغيلية",
    "أين يستخدم AI لتوفير وقت المؤسس، وأين تُمنع الأتمتة، وأفضل القوالب القابلة لإعادة الاستخدام.",
    [
        (
            "المكوّنات",
            [
                "leverage map",
                "automation with boundaries",
                "template reuse",
                "agent-assisted workflows",
                "founder time multiplier",
            ],
        )
    ],
)
add(
    OL,
    "01_LEVERAGE_MAP.md",
    "Leverage Map — خريطة الرافعة",
    "أين تُحقّق الرافعة أعلى أثر.",
    [("المناطق", ["تجهيز الحزم", "التقييم والترتيب", "التقارير", "المسودّات (drafts) للاعتماد"])],
)
add(
    OL,
    "02_AUTOMATION_WITH_BOUNDARIES.md",
    "Automation with Boundaries — أتمتة بحدود",
    "ما يُسمح وما يُمنع من الأتمتة.",
    [
        ("مسموح", ["generate/rank/score/validate/summarize/report/package/verify"]),
        (
            "ممنوع",
            ["send/submit/scrape/impersonate/publish/launch ads/modify production بدون اعتماد"],
        ),
    ],
)
add(
    OL,
    "03_TEMPLATE_REUSE_SYSTEM.md",
    "Template Reuse System — نظام إعادة استخدام القوالب",
    "كيف نعظّم إعادة استخدام القوالب.",
    [("النظام", ["مكتبة مركزية", "إصدارات", "قياس reuse rate"])],
)
add(
    OL,
    "04_AGENT_ASSISTED_WORKFLOWS.md",
    "Agent-Assisted Workflows — تدفقات بمساعدة الوكيل",
    "كيف تساعد الوكلاء دون كسر قاعدة الإرسال.",
    [("التدفقات", ["الوكيل يجهّز ويقترح", "المؤسس يعتمد ويرسل", "audit trail لكل خطوة"])],
)
add(
    OL,
    "05_FOUNDER_TIME_MULTIPLIER.md",
    "Founder Time Multiplier — مضاعِف وقت المؤسس",
    "كيف نضاعف إنتاج المؤسس دون زيادة المخاطر.",
    [("الأساليب", ["قوالب جاهزة", "حزم مولّدة", "تقارير cockpit", "قرارات مركّزة"])],
)

# === 15. Safe Lifecycle Automation OS ===
SA = "safe-lifecycle-automation-os"
add(
    SA,
    "00_SAFE_LIFECYCLE_AUTOMATION_OS.md",
    "Safe Lifecycle Automation OS — أتمتة دورة الحياة الآمنة",
    "ما يُسمح أتمتته داخليًا وما يُمنع خارجيًا، مع approval workflows وaudit trails.",
    [
        (
            "مسموح",
            ["generate", "rank", "score", "validate", "summarize", "report", "package", "verify"],
        ),
        (
            "ممنوع",
            [
                "send",
                "submit",
                "scrape",
                "impersonate",
                "publish",
                "launch ads",
                "modify production بدون اعتماد",
            ],
        ),
    ],
)
add(
    SA,
    "01_ALLOWED_INTERNAL_AUTOMATIONS.md",
    "Allowed Internal Automations — الأتمتة الداخلية المسموحة",
    "قائمة الأتمتة الداخلية الآمنة.",
    [("القائمة", ["توليد الحزم والتقارير", "التقييم والترتيب", "التحقق والتغليف"])],
)
add(
    SA,
    "02_REVIEW_ONLY_AUTOMATIONS.md",
    "Review-Only Automations — أتمتة للمراجعة فقط",
    "أتمتة تنتج drafts للمراجعة لا للإرسال.",
    [("القاعدة", ["كل مخرج draft", "اعتماد المؤسس قبل أي استخدام خارجي"])],
)
add(
    SA,
    "03_FORBIDDEN_EXTERNAL_AUTOMATIONS.md",
    "Forbidden External Automations — الأتمتة الخارجية الممنوعة",
    "ما يُمنع منعًا باتًا.",
    [
        (
            "الممنوع",
            ["إرسال Email/WhatsApp", "أتمتة LinkedIn", "scraping", "auto-submit", "إعلانات حيّة"],
        )
    ],
)
add(
    SA,
    "04_APPROVAL_WORKFLOWS.md",
    "Approval Workflows — تدفقات الاعتماد",
    "كيف يعتمد المؤسس قبل أي فعل خارجي.",
    [("التدفق", ["النظام يجهّز", "المؤسس يراجع", "اعتماد موثّق", "تنفيذ يدوي خارجي"])],
)
add(
    SA,
    "05_AUDIT_TRAILS.md",
    "Audit Trails — سجلّات التدقيق",
    "كيف نسجّل كل خطوة للمراجعة.",
    [("السجلّات", ["من جهّز", "من اعتمد", "متى", "ماذا"])],
)

# === 16. Moat Metrics OS ===
MO = "moat-metrics-os"
add(
    MO,
    "00_MOAT_METRICS_OS.md",
    "Moat Metrics OS — نظام مؤشرات الموات",
    "قياس عمق الموات: أصول التعلّم، القوالب القابلة لإعادة الاستخدام، عمق القطاع، معدّل إعادة التسليم، أصول الثقة، سلطة الفئة.",
    [
        (
            "المؤشرات",
            [
                "learning asset count",
                "reusable template count",
                "sector depth score",
                "delivery reuse rate",
                "trust asset score",
                "category authority score",
            ],
        ),
        ("الحساب", ["يلخّصها `scripts/moat_metrics_summary.py` من مدخلات example/manual."]),
    ],
)
for fn, tt, pp in [
    (
        "01_LEARNING_ASSET_COUNT.md",
        "Learning Asset Count — عدد أصول التعلّم",
        "عدّ الأصول المعرفية المتراكمة من كل تسليم.",
    ),
    (
        "02_REUSABLE_TEMPLATE_COUNT.md",
        "Reusable Template Count — عدد القوالب القابلة لإعادة الاستخدام",
        "عدّ القوالب الجاهزة لإعادة الاستخدام.",
    ),
    (
        "03_SECTOR_DEPTH_SCORE.md",
        "Sector Depth Score — درجة عمق القطاع",
        "قياس عمق الخبرة في كل قطاع.",
    ),
    (
        "04_DELIVERY_REUSE_RATE.md",
        "Delivery Reuse Rate — معدّل إعادة استخدام التسليم",
        "نسبة التسليم المعتمد على modules/templates جاهزة.",
    ),
    (
        "05_TRUST_ASSET_SCORE.md",
        "Trust Asset Score — درجة أصول الثقة",
        "قياس أصول الثقة (proof معتمد، إشارات محلية).",
    ),
    (
        "06_CATEGORY_AUTHORITY_SCORE.md",
        "Category Authority Score — درجة سلطة الفئة",
        "قياس الحضور كمرجع في فئة AI Revenue & Operations OS.",
    ),
]:
    add(
        MO,
        fn,
        tt,
        pp,
        [("المنهج", ["مدخلات example/manual", "تقدير مُعلَّم كافتراض", "يُجمع في تقرير moat"])],
    )

# === 17. Executive Demo Day OS ===
D = "executive-demo-day-os"
add(
    D,
    "00_EXECUTIVE_DEMO_DAY_OS.md",
    "Executive Demo Day OS — نظام يوم العرض التنفيذي",
    "كيف نجهّز يوم عرض تنفيذي يحوّل العرض إلى صفقة، مع script وassets وQA وخطة تحويل.",
    [
        (
            "المخرجات",
            ["demo_day_script", "demo_assets_checklist", "executive_followup", "conversion_plan"],
        ),
        ("التوليد", ["يولّدها `scripts/executive_demo_day_pack_generate.py`."]),
    ],
)
add(
    D,
    "01_DEMO_DAY_SCRIPT.md",
    "Demo Day Script — سيناريو يوم العرض",
    "هيكل عرض تنفيذي مركّز على القيمة والبرهان.",
    [("الهيكل", ["المشكلة", "المنهج", "البرهان القابل للمراجعة", "الخطوة التالية"])],
)
add(
    D,
    "02_DEMO_DAY_ASSETS.md",
    "Demo Day Assets — أصول يوم العرض",
    "قائمة الأصول المطلوبة للعرض.",
    [("الأصول", ["شرائح موجزة", "حالة برهان معتمدة", "عرض تنفيذي"])],
)
add(
    D,
    "03_DEMO_DAY_QA.md",
    "Demo Day Q&A — أسئلة وأجوبة العرض",
    "تجهيز إجابات للأسئلة المتوقعة بصدق.",
    [("التجهيز", ["اعتراضات متكررة", "إجابات مدعومة بـ evidence", "بدون وعود مضمونة"])],
)
add(
    D,
    "04_DEMO_TO_DEAL_CONVERSION.md",
    "Demo to Deal Conversion — تحويل العرض إلى صفقة",
    "كيف نحوّل العرض إلى خطوة بيع واضحة.",
    [("التحويل", ["خطوة تالية محددة", "close plan", "متابعة يعتمدها المؤسس ويرسلها يدويًا"])],
)

# === 18. CEO Cockpit OS ===
CC = "ceo-cockpit-os"
add(
    CC,
    "00_CEO_COCKPIT_OS.md",
    "CEO Cockpit OS — قمرة قيادة الرئيس التنفيذي",
    "لوحة واحدة تجمع revenue وpipeline وdelivery وsite وmedia وsafety وfinance assumptions والمخاطر والقرارات والإجراءات وتحذيرات no-go.",
    [
        (
            "الواجهات",
            [
                "daily view",
                "weekly view",
                "monthly view",
                "decision queue",
                "risk queue",
                "opportunity queue",
            ],
        ),
        (
            "التوليد",
            [
                "يولّدها `scripts/ceo_cockpit_generate.py` إلى `outputs/ceo_cockpit/latest/CEO_COCKPIT.md`."
            ],
        ),
    ],
)
add(
    CC,
    "01_CEO_DAILY_VIEW.md",
    "CEO Daily View — العرض اليومي",
    "ما يراجعه المؤسس يوميًا.",
    [("العناصر", ["قرارات اليوم", "مخاطر عاجلة", "أهم 3 إجراءات"])],
)
add(
    CC,
    "02_CEO_WEEKLY_VIEW.md",
    "CEO Weekly View — العرض الأسبوعي",
    "مراجعة أسبوعية للأداء.",
    [("العناصر", ["pipeline", "delivery", "محتوى/موقع", "مؤشرات الأمان"])],
)
add(
    CC,
    "03_CEO_MONTHLY_VIEW.md",
    "CEO Monthly View — العرض الشهري",
    "مراجعة شهرية مرتبطة بالمجلس.",
    [("العناصر", ["unit economics (assumptions)", "moat metrics", "قرارات المجلس"])],
)
add(
    CC,
    "04_DECISION_QUEUE.md",
    "Decision Queue — طابور القرارات",
    "القرارات المطلوبة بترتيب الأولوية.",
    [("الحقول", ["القرار", "السياق", "التوصية", "الموعد"])],
)
add(
    CC,
    "05_RISK_QUEUE.md",
    "Risk Queue — طابور المخاطر",
    "المخاطر المفتوحة بترتيب الشدّة.",
    [("الحقول", ["الخطر", "الشدّة", "المعالجة", "المالك"])],
)
add(
    CC,
    "06_OPPORTUNITY_QUEUE.md",
    "Opportunity Queue — طابور الفرص",
    "الفرص المؤهَّلة بترتيب القيمة.",
    [("الحقول", ["الفرصة", "القيمة المقدّرة (assumption)", "الخطوة التالية"])],
)


# ---------------------------------------------------------------------------
# Reports (99_*)
# ---------------------------------------------------------------------------

REPORTS: list[tuple[str, str, str, list[str], list[str]]] = [
    (
        "institutional-scale-os",
        "99_INSTITUTIONAL_SCALE_REPORT.md",
        "Institutional Scale Report — تقرير التوسع المؤسسي",
        ["نموذج تشغيل مرحلي + playbooks للنمو + سجل مخاطر التوسع."],
        ["التوسع المرحلي المبني على البرهان والمؤشرات."],
    ),
    (
        "board-governance-os",
        "99_BOARD_GOVERNANCE_REPORT.md",
        "Board Governance Report — تقرير حوكمة المجلس",
        ["قوالب حزمة المجلس + مولّد + سياسة نزاهة المؤشرات."],
        ["توليد board packet ومراجعة شهرية محكومة."],
    ),
    (
        "market-domination-os",
        "99_MARKET_DOMINATION_REPORT.md",
        "Market Domination Report — تقرير السيطرة على السوق",
        ["beachhead + vertical domination + thought leadership + distribution."],
        ["تخطيط السيطرة القطاعية وتعليم الفئة."],
    ),
    (
        "enterprise-sales-room-os",
        "99_ENTERPRISE_SALES_ROOM_REPORT.md",
        "Enterprise Sales Room Report — تقرير غرفة المبيعات المؤسسية",
        ["مولّد غرفة مبيعات مؤسسية ينتج 7 مخرجات draft."],
        ["إعداد صفقات مؤسسية كمسودّات للمراجعة."],
    ),
    (
        "customer-advisory-os",
        "99_CUSTOMER_ADVISORY_REPORT.md",
        "Customer Advisory Report — تقرير المجلس الاستشاري",
        ["أطروحة + قالب دعوة + أجندة + حلقة feedback→product."],
        ["تشغيل مجلس استشاري بدون تضخيم أو استخدام أسماء بدون إذن."],
    ),
    (
        "commercial-legal-readiness-os",
        "99_COMMERCIAL_LEGAL_READINESS_REPORT.md",
        "Commercial Legal Readiness Report — تقرير الجاهزية القانونية",
        ["قوالب تعاقد للمراجعة + بوابة مراجعة قانونية."],
        ["تجهيز قوالب تعاقد (تحتاج مراجعة قانونية قبل الاستخدام)."],
    ),
    (
        "profitability-os",
        "99_PROFITABILITY_REPORT.md",
        "Profitability Report — تقرير الربحية",
        ["نماذج هامش/كلفة + guardrails + مولّد ملخّص ربحية (example inputs)."],
        ["مراجعة ربحية بمدخلات example/assumption فقط."],
    ),
    (
        "scope-control-os",
        "99_SCOPE_CONTROL_REPORT.md",
        "Scope Control Report — تقرير ضبط النطاق",
        ["سياسة حدود + change request + out-of-scope library + acceptance gates."],
        ["منع scope creep وحماية الهامش والثقة."],
    ),
    (
        "case-study-governance-os",
        "99_CASE_STUDY_GOVERNANCE_REPORT.md",
        "Case Study Governance Report — تقرير حوكمة دراسات الحالة",
        ["أهلية + إذن + حالات مجهّلة + قواعد ادعاء الأرقام + بوابة مراجعة."],
        ["إنتاج proof بصدق وبإذن وبـ evidence."],
    ),
    (
        "competitive-win-room-os",
        "99_COMPETITIVE_WIN_ROOM_REPORT.md",
        "Competitive Win Room Report — تقرير الفوز التنافسي",
        ["بطاقات معركة موضوعية + مراجعة win/loss."],
        ["positioning موضوعي بدون تشهير أو ادعاءات."],
    ),
    (
        "localization-os",
        "99_LOCALIZATION_REPORT.md",
        "Localization Report — تقرير التوطين",
        ["دليل لغة عربية تنفيذية + سياق المشتري + إشارات ثقة محلية."],
        ["توطين سعودي/خليجي للغة والمحتوى."],
    ),
    (
        "talent-bench-os",
        "99_TALENT_BENCH_REPORT.md",
        "Talent Bench Report — تقرير مقاعد المواهب",
        ["استراتيجية bench + task packs + QA + scorecard + capacity."],
        ["إضافة مقاولين بأمان وحماية الأسرار."],
    ),
    (
        "productization-os",
        "99_PRODUCTIZATION_REPORT.md",
        "Productization Report — تقرير التحويل إلى منتج",
        ["تحويل الخدمة إلى modules + مكتبة قوالب + خرائط portal/tooling."],
        ["تحويل التسليم المتكرر إلى modules لرفع الهامش."],
    ),
    (
        "operating-leverage-os",
        "99_OPERATING_LEVERAGE_REPORT.md",
        "Operating Leverage Report — تقرير الرافعة التشغيلية",
        ["خريطة رافعة + أتمتة بحدود + إعادة استخدام قوالب + مضاعِف وقت المؤسس."],
        ["مضاعفة الإنتاج دون زيادة المخاطر."],
    ),
    (
        "safe-lifecycle-automation-os",
        "99_SAFE_LIFECYCLE_AUTOMATION_REPORT.md",
        "Safe Lifecycle Automation Report — تقرير الأتمتة الآمنة",
        ["قوائم مسموح/ممنوع + approval workflows + audit trails."],
        ["أتمتة داخلية آمنة فقط (generate/score/report)."],
    ),
    (
        "moat-metrics-os",
        "99_MOAT_METRICS_REPORT.md",
        "Moat Metrics Report — تقرير مؤشرات الموات",
        ["6 مؤشرات موات + مولّد ملخّص (example inputs)."],
        ["قياس عمق الموات بمدخلات example/assumption."],
    ),
    (
        "executive-demo-day-os",
        "99_EXECUTIVE_DEMO_DAY_REPORT.md",
        "Executive Demo Day Report — تقرير يوم العرض التنفيذي",
        ["script + assets + followup + conversion + مولّد حزمة."],
        ["تجهيز يوم عرض تنفيذي يحوّل العرض إلى صفقة."],
    ),
    (
        "ceo-cockpit-os",
        "99_CEO_COCKPIT_REPORT.md",
        "CEO Cockpit Report — تقرير قمرة القيادة",
        ["6 واجهات + مولّد cockpit يجمع كل المؤشرات والقرارات والمخاطر."],
        ["قمرة قيادة واحدة لقرارات يومية/أسبوعية/شهرية."],
    ),
]


def main() -> int:
    written = 0
    for dir_, fname, title, purpose, sections in DOCS:
        out = REPO / "docs" / dir_ / fname
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_doc(title, purpose, sections), encoding="utf-8")
        written += 1
    for dir_, fname, title, what, _why in REPORTS:
        out = REPO / "docs" / dir_ / fname
        out.parent.mkdir(parents=True, exist_ok=True)
        go = ["مراجعة واعتماد المؤسس", "توليد المخرجات الداخلية (drafts/reports)"]
        out.write_text(_std_report(title, what[0], go, DEFAULT_NO_GO), encoding="utf-8")
        written += 1
    print(f"v10_build_docs: wrote {written} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
