#!/usr/bin/env python3
"""Generate the Dealix V9 Strategic Moat & Enterprise Readiness OS documentation.

Data-driven: every operating file is defined as (title, purpose, sections) and
rendered as bilingual (EN + AR) markdown with the shared non-negotiables footer.
Run once to (re)materialise docs; safe to re-run (idempotent overwrite).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SAFETY_FOOTER = """
---

## Operating Boundaries / حدود التشغيل

**AI prepares, analyzes, drafts, ranks, and recommends. The founder reviews,
approves, sends manually, sells, signs, and decides. The system never sends
externally.**

الذكاء الاصطناعي يجهّز ويحلّل ويصيغ ويرتّب ويوصي. المؤسس يراجع ويعتمد ويرسل يدويًا
ويبيع ويوقّع ويقرّر. النظام لا يرسل خارجيًا أبدًا.

Non-negotiables enforced across this OS:

- No secrets, API keys, SMTP, or credentials committed.
- No email / WhatsApp / LinkedIn outbound, no platform automation.
- No scraping, no auto-submit, no live paid-ads launch.
- No fake traction, no guaranteed ROI, no unverified claims or certifications.
- No external sending from GitHub Actions; verification is artifact-only.
- Founder approval remains required before anything leaves the building.
"""


def render(title_en: str, title_ar: str, purpose_en: str, purpose_ar: str,
           sections: list[tuple[str, list[str]]]) -> str:
    """Render one operating doc as bilingual markdown."""
    lines: list[str] = []
    lines.append(f"# {title_en} / {title_ar}")
    lines.append("")
    lines.append(f"> **Purpose (EN):** {purpose_en}")
    lines.append(">")
    lines.append(f"> **الغرض (AR):** {purpose_ar}")
    lines.append("")
    lines.append(f"_Layer: V9 — Strategic Moat & Enterprise Readiness OS · "
                 f"Generated: {date.today().isoformat()}_")
    lines.append("")
    for heading, bullets in sections:
        lines.append(f"## {heading}")
        lines.append("")
        for b in bullets:
            lines.append(f"- {b}")
        lines.append("")
    lines.append(SAFETY_FOOTER.strip())
    lines.append("")
    return "\n".join(lines)


def report_sections(system: str, added: list[str], why: list[str],
                    risks: list[str], next_actions: list[str]) -> list[tuple[str, list[str]]]:
    """Standard 99_*_REPORT section set."""
    return [
        ("What Was Added / ما الذي أُضيف", added),
        ("Why It Matters / لماذا يهم", why),
        ("Verification Status / حالة التحقق", [
            f"Run `python scripts/{system}_verify.py` for the machine-readable result.",
            "JSON report is written to `outputs/v9_verification/`.",
            "Verdict is PASS when all required files exist, are substantive, and carry no forbidden claims.",
        ]),
        ("Risks / المخاطر", risks),
        ("Blockers / المعوقات", [
            "Legal and security templates remain pending external review before customer use.",
            "No external certifications are claimed; statements are marked as pending verification.",
        ]),
        ("Next Actions / الخطوات التالية", next_actions),
        ("GO / NO-GO", [
            "GO: internal preparation, drafting, ranking, and founder-reviewed packets.",
            "NO-GO: external sending, platform automation, fake traction, unreviewed legal/security claims.",
        ]),
    ]


# ---------------------------------------------------------------------------
# System definitions. Each entry: folder -> list of (filename, doc-spec)
# doc-spec = (title_en, title_ar, purpose_en, purpose_ar, sections)
# ---------------------------------------------------------------------------

def S(h: str, *bullets: str) -> tuple[str, list[str]]:
    return (h, list(bullets))


SYSTEMS: dict[str, list[tuple[str, tuple]]] = {}


# 1. Strategic Moat OS -------------------------------------------------------
SYSTEMS["docs/strategic-moat-os"] = [
    ("00_STRATEGIC_MOAT_OS.md", (
        "Strategic Moat OS", "نظام الميزة التنافسية",
        "How Dealix builds advantages that are hard to copy and compound over time.",
        "كيف يبني Dealix ميزات يصعب نسخها وتتراكم مع الوقت.",
        [
            S("Overview / نظرة عامة",
              "Five reinforcing moats: data, workflow IP, trust, distribution, delivery.",
              "Each daily output is captured as reusable knowledge, not thrown away.",
              "The repository itself is the company's operating memory."),
            S("How To Use / كيفية الاستخدام",
              "Read the thesis (01), then the compounding map (02).",
              "Every engagement feeds one or more moats; record the asset in the relevant ledger."),
        ],
    )),
    ("01_MOAT_THESIS.md", (
        "Moat Thesis", "أطروحة الميزة",
        "The core argument for why Dealix's advantage widens with usage.",
        "الحجة الأساسية لاتساع ميزة Dealix مع الاستخدام.",
        [
            S("Thesis / الأطروحة",
              "Advantage = accumulated workflows × verified proof × trusted relationships.",
              "Competitors can copy a feature but not the accumulated operating memory.",
              "Approval-first delivery is a trust advantage in regulated Saudi sectors."),
            S("What Compounds / ما الذي يتراكم",
              "Sector-specific playbooks, objection libraries, and proof packs.",
              "Founder relationships and reference customers."),
        ],
    )),
    ("02_COMPOUNDING_ADVANTAGES.md", (
        "Compounding Advantages", "الميزات المتراكمة",
        "The loops that turn daily work into durable advantage.",
        "الحلقات التي تحوّل العمل اليومي إلى ميزة دائمة.",
        [
            S("Loops / الحلقات",
              "Delivery → playbook → faster next delivery.",
              "Objection → asset → higher next close rate.",
              "Proof → reference → easier next sale."),
            S("Measurement / القياس",
              "Track assets created per engagement.",
              "Track reuse rate of playbooks and templates."),
        ],
    )),
    ("03_DATA_ASSET_STRATEGY.md", (
        "Data Asset Strategy", "استراتيجية أصول البيانات",
        "How Dealix turns operating data into a durable, privacy-safe asset.",
        "كيف يحوّل Dealix بيانات التشغيل إلى أصل دائم وآمن للخصوصية.",
        [
            S("Principles / المبادئ",
              "Data minimization: collect only what the engagement requires.",
              "No customer-sensitive data without a signed agreement.",
              "Aggregated, anonymized patterns are the reusable asset — not raw records."),
            S("What We Keep / ما نحتفظ به",
              "Sector benchmarks, scoring heuristics, and workflow templates.",
              "We do not keep or claim any data we are not authorized to hold."),
        ],
    )),
    ("04_WORKFLOW_IP_STRATEGY.md", (
        "Workflow IP Strategy", "استراتيجية ملكية سير العمل",
        "How delivery playbooks become defensible intellectual property.",
        "كيف تتحول أدلة التسليم إلى ملكية فكرية قابلة للدفاع.",
        [
            S("IP Capture / التقاط الملكية",
              "Every repeatable delivery step is documented as a playbook.",
              "Playbooks are versioned and owned in the repository.",
              "Naming, scoring, and sequencing of steps form the proprietary method."),
            S("Protection / الحماية",
              "Internal-only playbooks are not published.",
              "Customer-facing summaries omit the proprietary mechanics."),
        ],
    )),
    ("05_TRUST_MOAT.md", (
        "Trust Moat", "ميزة الثقة",
        "How approval-first governance and compliance posture become a moat.",
        "كيف تصبح الحوكمة القائمة على الاعتماد والامتثال ميزة تنافسية.",
        [
            S("Trust Levers / روافع الثقة",
              "Approval-first: nothing is sent without founder review.",
              "No blind automation; auditable human-in-the-loop decisions.",
              "Data minimization and clear boundaries reassure regulated buyers."),
            S("Why It Defends / لماذا تحمي",
              "Trust is earned over time and cannot be cloned by a competitor overnight."),
        ],
    )),
    ("06_DISTRIBUTION_MOAT.md", (
        "Distribution Moat", "ميزة التوزيع",
        "How founder-led, referral, and partner channels compound reach.",
        "كيف تتراكم قنوات المؤسس والإحالة والشركاء.",
        [
            S("Channels / القنوات",
              "Founder-led warm relationships (manual, approval-first).",
              "Referral loops from satisfied reference customers.",
              "Partner motion with aligned service providers."),
            S("Boundaries / الحدود",
              "No cold automation, no scraping, no platform automation."),
        ],
    )),
    ("07_DELIVERY_MOAT.md", (
        "Delivery Moat", "ميزة التسليم",
        "How consistent, fast, high-quality delivery widens the lead.",
        "كيف يوسّع التسليم المتسق السريع عالي الجودة الفجوة.",
        [
            S("Delivery Levers / روافع التسليم",
              "Productized 7-day sprint with a fixed, proven sequence.",
              "QMS checklists guarantee a consistent quality bar.",
              "Each delivery improves the next via captured learnings."),
        ],
    )),
    ("08_CATEGORY_MOAT.md", (
        "Category Moat", "ميزة الفئة",
        "How owning the first five sectors deeply creates category leadership.",
        "كيف يخلق التعمق في أول خمسة قطاعات ريادة في الفئة.",
        [
            S("Category Strategy / استراتيجية الفئة",
              "Go deep in five sectors before going wide.",
              "Sector depth produces language, benchmarks, and references competitors lack.",
              "Define the category vocabulary so buyers evaluate on our terms."),
        ],
    )),
]

# 2. Enterprise Readiness OS -------------------------------------------------
SYSTEMS["docs/enterprise-readiness-os"] = [
    ("00_ENTERPRISE_READINESS_OS.md", (
        "Enterprise Readiness OS", "نظام الجاهزية المؤسسية",
        "How Dealix prepares to sell to large organizations without overclaiming.",
        "كيف يستعد Dealix للبيع للمؤسسات الكبيرة دون مبالغة.",
        [
            S("Overview / نظرة عامة",
              "Maps the enterprise buyer, procurement, security, and legal paths.",
              "Provides ready answers marked 'pending legal/security review'.",
              "Protects price and prevents scope creep."),
        ],
    )),
    ("01_ENTERPRISE_BUYER_MAP.md", (
        "Enterprise Buyer Map", "خريطة المشتري المؤسسي",
        "Who decides, who blocks, and who champions inside a large account.",
        "من يقرر ومن يعطّل ومن يدعم داخل الحساب الكبير.",
        [
            S("Roles / الأدوار",
              "Economic buyer: owns the budget and the business outcome.",
              "Technical evaluator: security, data, and integration concerns.",
              "Procurement: vendor registration, terms, and pricing.",
              "Champion: internal advocate who navigates the org."),
            S("Blockers / المعطّلون",
              "Security review, legal/DPA, and procurement are the common gates."),
        ],
    )),
    ("02_PROCUREMENT_READINESS.md", (
        "Procurement Readiness", "جاهزية المشتريات",
        "What a large buyer's procurement function will ask, and our prepared posture.",
        "ما ستطلبه إدارة المشتريات وموقفنا المُجهّز.",
        [
            S("Readiness Items / عناصر الجاهزية",
              "Company registration and basic legal documents (founder-maintained).",
              "Standard SOW, payment terms, and acceptance criteria templates.",
              "All commercial terms remain pending founder sign-off."),
        ],
    )),
    ("03_VENDOR_ONBOARDING_ANSWERS.md", (
        "Vendor Onboarding Answers", "إجابات تأهيل المورّد",
        "Prepared answers to common vendor-onboarding questionnaires.",
        "إجابات مُجهّزة لاستبيانات تأهيل المورّد الشائعة.",
        [
            S("Prepared Answers / إجابات مُجهّزة",
              "Company description, services, and engagement model.",
              "Data handling summary (see Data Processing Answers).",
              "Answers are templates pending legal/security review before submission."),
        ],
    )),
    ("04_SECURITY_QUESTIONNAIRE_ANSWERS.md", (
        "Security Questionnaire Answers", "إجابات استبيان الأمن",
        "Prepared, honest answers to security questionnaires — no false certifications.",
        "إجابات أمنية صادقة مُجهّزة دون ادعاء شهادات.",
        [
            S("Posture / الموقف",
              "Approval-first; no blind automation; human-in-the-loop.",
              "Secrets are never committed; least-privilege access.",
              "We do NOT claim SOC 2 / ISO 27001 certification; status is pending and disclosed honestly."),
            S("Review / المراجعة",
              "Answers are templates pending security review before sending."),
        ],
    )),
    ("05_DATA_PROCESSING_ANSWERS.md", (
        "Data Processing Answers", "إجابات معالجة البيانات",
        "How we describe data boundaries, residency, and minimization to buyers.",
        "كيف نصف حدود البيانات والإقامة والتقليل للمشترين.",
        [
            S("Data Boundaries / حدود البيانات",
              "Data minimization: only what the engagement requires.",
              "No customer-sensitive data processed without a signed DPA.",
              "Clear separation between demo/sandbox data and any customer data."),
        ],
    )),
    ("06_IMPLEMENTATION_GOVERNANCE.md", (
        "Implementation Governance", "حوكمة التنفيذ",
        "How an enterprise implementation is governed to stay on scope and on quality.",
        "كيف تُحكم عملية التنفيذ المؤسسي للبقاء ضمن النطاق والجودة.",
        [
            S("Governance / الحوكمة",
              "Defined milestones, acceptance criteria, and change-request process.",
              "Weekly review against the agreed scope.",
              "Escalation path for risks and blockers."),
        ],
    )),
    ("07_ENTERPRISE_PILOT_STRUCTURE.md", (
        "Enterprise Pilot Structure", "هيكل التجربة المؤسسية",
        "A low-risk, time-boxed pilot structure that proves value before scale.",
        "هيكل تجربة محدد بوقت ومنخفض المخاطر يثبت القيمة قبل التوسع.",
        [
            S("Pilot Design / تصميم التجربة",
              "Fixed scope, fixed duration, clear success metrics.",
              "Sandbox/sample data first; customer data only after agreement.",
              "Explicit go/no-go criteria for converting to a retainer."),
        ],
    )),
    ("08_ENTERPRISE_PRICING_GUARDRAILS.md", (
        "Enterprise Pricing Guardrails", "ضوابط التسعير المؤسسي",
        "How to protect price and value in enterprise negotiations.",
        "كيف نحمي السعر والقيمة في مفاوضات المؤسسات.",
        [
            S("Guardrails / الضوابط",
              "Anchor on outcome value, not hourly cost.",
              "Floor prices below which we walk; discounts trade for scope, not free.",
              "No guaranteed ROI; value framed as expected and measured, not promised."),
        ],
    )),
]

# 3. Trust Center OS ---------------------------------------------------------
SYSTEMS["docs/trust-center-os"] = [
    ("00_TRUST_CENTER_OS.md", (
        "Trust Center OS", "نظام مركز الثقة",
        "The public-facing and internal trust posture of Dealix.",
        "موقف الثقة العام والداخلي لـ Dealix.",
        [
            S("Overview / نظرة عامة",
              "Public trust page communicates approval-first and no blind automation.",
              "Internal policies back every public statement.",
              "No unverified claims; certifications shown only when real."),
        ],
    )),
    ("01_PUBLIC_TRUST_PAGE_SPEC.md", (
        "Public Trust Page Spec", "مواصفات صفحة الثقة العامة",
        "Specification for the /trust, /security, and /privacy pages.",
        "مواصفات صفحات /trust و/security و/privacy.",
        [
            S("Page Content / محتوى الصفحة",
              "Approval-first commitment and human review statement.",
              "Data minimization and founder-approval messaging.",
              "Auditability and no-external-sending-from-actions statement.",
              "Only verifiable claims; pending items labeled as such."),
        ],
    )),
    ("02_SECURITY_OVERVIEW.md", (
        "Security Overview", "نظرة أمنية عامة",
        "A plain-language description of our security posture.",
        "وصف بلغة واضحة لموقفنا الأمني.",
        [
            S("Security Posture / الموقف الأمني",
              "Secrets never committed; least privilege; audited access.",
              "Human-in-the-loop for any external-facing action.",
              "We do not claim formal certification we do not hold."),
        ],
    )),
    ("03_PRIVACY_OVERVIEW.md", (
        "Privacy Overview", "نظرة عامة على الخصوصية",
        "How we handle personal and customer data responsibly.",
        "كيف نتعامل مع البيانات الشخصية وبيانات العملاء بمسؤولية.",
        [
            S("Privacy Posture / موقف الخصوصية",
              "Data minimization by default.",
              "No customer-sensitive data without a signed agreement.",
              "Clear retention and deletion expectations."),
        ],
    )),
    ("04_HUMAN_APPROVAL_POLICY.md", (
        "Human Approval Policy", "سياسة الاعتماد البشري",
        "The policy that the founder approves anything before it leaves the building.",
        "السياسة التي توجب اعتماد المؤسس لأي شيء قبل خروجه.",
        [
            S("Policy / السياسة",
              "AI drafts and recommends; the founder approves and sends manually.",
              "No autonomous external action under any circumstance.",
              "Every approval is auditable."),
        ],
    )),
    ("05_NO_BLIND_AUTOMATION_POLICY.md", (
        "No Blind Automation Policy", "سياسة منع الأتمتة العمياء",
        "We never run unattended automation that contacts people externally.",
        "لا نشغّل أتمتة غير مراقَبة تتواصل مع الناس خارجيًا.",
        [
            S("Policy / السياسة",
              "No outbound email, WhatsApp, or LinkedIn automation.",
              "No scraping and no auto-submit of forms.",
              "GitHub Actions are artifact-only and never send externally."),
        ],
    )),
    ("06_DATA_MINIMIZATION_POLICY.md", (
        "Data Minimization Policy", "سياسة تقليل البيانات",
        "We collect and retain the minimum data necessary.",
        "نجمع ونحتفظ بالحد الأدنى الضروري من البيانات.",
        [
            S("Policy / السياسة",
              "Collect only what the engagement requires.",
              "Prefer aggregated/anonymized data for reusable assets.",
              "Delete on request and on retention expiry."),
        ],
    )),
    ("07_INCIDENT_DISCLOSURE_PROCESS.md", (
        "Incident Disclosure Process", "عملية الإفصاح عن الحوادث",
        "How we would detect, contain, and disclose a security incident.",
        "كيف نكتشف ونحتوي ونفصح عن حادث أمني.",
        [
            S("Process / العملية",
              "Detect and contain; preserve evidence.",
              "Assess impact and notify affected parties honestly and promptly.",
              "Document root cause and remediation."),
        ],
    )),
    ("08_CUSTOMER_SECURITY_FAQ.md", (
        "Customer Security FAQ", "الأسئلة الأمنية للعملاء",
        "Common customer security questions and our honest answers.",
        "أسئلة العملاء الأمنية الشائعة وإجاباتنا الصادقة.",
        [
            S("FAQ / الأسئلة",
              "Where is data stored? — disclosed per engagement, minimized by default.",
              "Do you auto-send to my contacts? — No, never; approval-first.",
              "Are you certified? — We disclose actual status; no false certification claims."),
        ],
    )),
]

# 4. Demo & Sandbox OS -------------------------------------------------------
SYSTEMS["docs/demo-os"] = [
    ("00_DEMO_OS.md", (
        "Demo OS", "نظام العرض التوضيحي",
        "How Dealix runs safe, sandbox-only demos that convert to diagnostics.",
        "كيف يشغّل Dealix عروضًا آمنة على بيئة تجريبية تتحول إلى تشخيص.",
        [
            S("Overview / نظرة عامة",
              "All demos use sample/sandbox data only — never real customer data.",
              "A clear narrative leads from problem to value to next step.",
              "Demo never claims to be connected to a customer's live data."),
        ],
    )),
    ("01_DEMO_NARRATIVE.md", (
        "Demo Narrative", "سردية العرض",
        "The story arc that frames every demo.",
        "القوس السردي الذي يؤطّر كل عرض.",
        [
            S("Narrative / السردية",
              "Problem the buyer feels → how Dealix approaches it → visible value.",
              "End on a concrete next step: the paid diagnostic.",
              "Honest framing: sample data, expected value, no guarantees."),
        ],
    )),
    ("02_VERTICAL_DEMO_SCENARIOS.md", (
        "Vertical Demo Scenarios", "سيناريوهات العرض القطاعية",
        "Tailored demo scenarios per priority sector.",
        "سيناريوهات عرض مخصصة لكل قطاع أولوية.",
        [
            S("Scenarios / السيناريوهات",
              "One scenario per priority sector, driven by config/demo_scenarios.json.",
              "Each scenario maps a pain point to a demonstrable workflow.",
              "Sample companies come from data/demo_companies.example.jsonl."),
        ],
    )),
    ("03_SAFE_SAMPLE_DATA_POLICY.md", (
        "Safe Sample Data Policy", "سياسة بيانات العينة الآمنة",
        "Rules ensuring demo data is synthetic and safe.",
        "قواعد تضمن أن بيانات العرض اصطناعية وآمنة.",
        [
            S("Policy / السياسة",
              "Only synthetic/sample data; clearly labeled as example.",
              "No real customer data and no secrets in demo assets.",
              "Demo data never implies a live customer integration."),
        ],
    )),
    ("04_DEMO_SCRIPT_AR_EN.md", (
        "Demo Script (AR/EN)", "سكربت العرض (عربي/إنجليزي)",
        "A bilingual run-of-show the founder can deliver.",
        "سكربت ثنائي اللغة يمكن للمؤسس تقديمه.",
        [
            S("Run of Show / تسلسل العرض",
              "Open with the buyer's problem in their language.",
              "Walk the sandbox workflow; narrate the value at each step.",
              "Close on the paid diagnostic as the next step.",
              "Generated packs include a fresh demo_script.md per run."),
        ],
    )),
    ("05_DEMO_TO_DIAGNOSTIC_CONVERSION.md", (
        "Demo To Diagnostic Conversion", "تحويل العرض إلى تشخيص",
        "How a demo converts into a paid diagnostic engagement.",
        "كيف يتحول العرض إلى تشخيص مدفوع.",
        [
            S("Conversion / التحويل",
              "Ask for the diagnostic at the moment of demonstrated value.",
              "Set scope, price, and timeline clearly.",
              "Founder confirms next step manually; no auto-booking."),
        ],
    )),
    ("06_DEMO_QA_CHECKLIST.md", (
        "Demo QA Checklist", "قائمة فحص جودة العرض",
        "Pre-demo checklist to ensure quality and safety.",
        "قائمة فحص قبل العرض لضمان الجودة والسلامة.",
        [
            S("Checklist / القائمة",
              "Confirm sample data only; no secrets present.",
              "Confirm narrative matches the buyer's sector.",
              "Confirm the next-step ask is clear and honest."),
        ],
    )),
]

# 5. Customer Lifecycle OS ---------------------------------------------------
SYSTEMS["docs/customer-lifecycle-os"] = [
    ("00_CUSTOMER_LIFECYCLE_OS.md", (
        "Customer Lifecycle OS", "نظام دورة حياة العميل",
        "The full journey from first touch to expansion, with measures and triggers.",
        "الرحلة الكاملة من أول تواصل إلى التوسع مع القياسات والمحفزات.",
        [
            S("Stages / المراحل",
              "First touch → diagnostic → pilot → retainer → expansion.",
              "Each stage has outputs, a measure, a next action, and risk signals.",
              "Stages are defined in config/customer_lifecycle_stages.json."),
        ],
    )),
    ("01_FIRST_TOUCH_TO_DIAGNOSTIC.md", (
        "First Touch To Diagnostic", "من أول تواصل إلى التشخيص",
        "Converting an initial warm contact into a paid diagnostic.",
        "تحويل التواصل الدافئ الأولي إلى تشخيص مدفوع.",
        [
            S("Stage / المرحلة",
              "Output: qualified opportunity and agreed diagnostic scope.",
              "Measure: time-to-diagnostic and qualification quality.",
              "Risk: vague pain, no budget owner, no timeline."),
        ],
    )),
    ("02_DIAGNOSTIC_TO_PILOT.md", (
        "Diagnostic To Pilot", "من التشخيص إلى التجربة",
        "Converting a diagnostic into a structured pilot.",
        "تحويل التشخيص إلى تجربة منظمة.",
        [
            S("Stage / المرحلة",
              "Output: diagnostic findings and a proposed pilot scope.",
              "Measure: diagnostic-to-pilot conversion rate.",
              "Risk: findings not tied to a measurable outcome."),
        ],
    )),
    ("03_PILOT_TO_RETAINER.md", (
        "Pilot To Retainer", "من التجربة إلى التعاقد الشهري",
        "Converting a successful pilot into a recurring retainer.",
        "تحويل التجربة الناجحة إلى تعاقد شهري متكرر.",
        [
            S("Stage / المرحلة",
              "Output: proof pack and a retainer proposal.",
              "Measure: pilot-to-retainer conversion and time-to-value.",
              "Risk: value not documented; champion left."),
        ],
    )),
    ("04_RETAINER_TO_EXPANSION.md", (
        "Retainer To Expansion", "من التعاقد إلى التوسع",
        "Growing a retainer into additional scope and value.",
        "تنمية التعاقد إلى نطاق وقيمة إضافية.",
        [
            S("Stage / المرحلة",
              "Output: expansion proposal grounded in delivered value.",
              "Measure: net revenue retention and expansion rate.",
              "Trigger: new use case, new department, or new sector."),
        ],
    )),
    ("05_CUSTOMER_HEALTH_REVIEW.md", (
        "Customer Health Review", "مراجعة صحة العميل",
        "A recurring review of customer health signals.",
        "مراجعة دورية لإشارات صحة العميل.",
        [
            S("Health Signals / إشارات الصحة",
              "Usage, value realized, sentiment, and champion stability.",
              "Green/amber/red status with a clear next action.",
              "Reviewed on a fixed cadence."),
        ],
    )),
    ("06_RENEWAL_PLAYBOOK.md", (
        "Renewal Playbook", "دليل التجديد",
        "How to secure renewals before they lapse.",
        "كيف نؤمّن التجديدات قبل انتهائها.",
        [
            S("Renewal / التجديد",
              "Start the renewal conversation well before term end.",
              "Re-quantify delivered value; present a clear renewal proposal.",
              "Trigger: term end approaching, value confirmed."),
        ],
    )),
    ("07_CHURN_PREVENTION.md", (
        "Churn Prevention", "منع التسرب",
        "Detecting and acting on churn risk early.",
        "اكتشاف خطر التسرب والتصرف مبكرًا.",
        [
            S("Churn Signals / إشارات التسرب",
              "Declining usage, unaddressed issues, champion departure.",
              "Escalation and recovery plan for red accounts.",
              "Document learnings to prevent recurrence."),
        ],
    )),
    ("08_EXPANSION_PLAYBOOK.md", (
        "Expansion Playbook", "دليل التوسع",
        "How to grow within an account responsibly.",
        "كيف ننمو داخل الحساب بمسؤولية.",
        [
            S("Expansion / التوسع",
              "Expansion is earned by delivered, documented value.",
              "Triggers: new use case, department, or success milestone.",
              "Proposals remain founder-approved before sending."),
        ],
    )),
]

# 6. Founder Delegation OS ---------------------------------------------------
SYSTEMS["docs/delegation-os"] = [
    ("00_DELEGATION_OS.md", (
        "Delegation OS", "نظام التفويض",
        "What stays with the founder and what an operator can safely take on.",
        "ما يبقى مع المؤسس وما يمكن أن يتسلمه المشغّل بأمان.",
        [
            S("Overview / نظرة عامة",
              "Clear split between founder-only and delegable work.",
              "The repository is the operating manual for any operator.",
              "Quality is reviewed; context is preserved in writing."),
        ],
    )),
    ("01_WHAT_ONLY_FOUNDER_DOES.md", (
        "What Only Founder Does", "ما يقوم به المؤسس فقط",
        "The irreducible founder responsibilities.",
        "مسؤوليات المؤسس غير القابلة للتفويض.",
        [
            S("Founder-Only / للمؤسس فقط",
              "Final approval of anything sent externally.",
              "Selling, signing contracts, and pricing decisions.",
              "Strategic direction and key relationships."),
        ],
    )),
    ("02_WHAT_CAN_BE_DELEGATED.md", (
        "What Can Be Delegated", "ما يمكن تفويضه",
        "Work an operator can own with review.",
        "العمل الذي يمكن للمشغّل امتلاكه مع المراجعة.",
        [
            S("Delegable / قابل للتفويض",
              "Drafting, research, scheduling preparation, and asset assembly.",
              "Pack preparation and ledger updates.",
              "All outputs remain founder-reviewed before external use."),
        ],
    )),
    ("03_FIRST_OPERATOR_PLAYBOOK.md", (
        "First Operator Playbook", "دليل أول مشغّل",
        "Onboarding the first operator using the repository as the manual.",
        "تأهيل أول مشغّل باستخدام الريبو كدليل.",
        [
            S("Playbook / الدليل",
              "Start with the Master Index and Daily Operating Guide.",
              "Use checklists to prevent errors.",
              "Escalate anything ambiguous to the founder."),
        ],
    )),
    ("04_GROWTH_OPERATOR_PLAYBOOK.md", (
        "Growth Operator Playbook", "دليل مشغّل النمو",
        "Delegable growth-support tasks, approval-first.",
        "مهام دعم النمو القابلة للتفويض مع الاعتماد أولًا.",
        [
            S("Playbook / الدليل",
              "Prepare warm-list drafts for founder approval.",
              "Maintain pipeline hygiene and follow-up reminders.",
              "No external sending; no automation; no scraping."),
        ],
    )),
    ("05_DELIVERY_OPERATOR_PLAYBOOK.md", (
        "Delivery Operator Playbook", "دليل مشغّل التسليم",
        "Delegable delivery-support tasks under QMS.",
        "مهام دعم التسليم القابلة للتفويض ضمن نظام الجودة.",
        [
            S("Playbook / الدليل",
              "Assemble proof packs using QMS checklists.",
              "Track milestones and acceptance criteria.",
              "Surface risks early; keep written context."),
        ],
    )),
    ("06_WEEKLY_DELEGATION_REVIEW.md", (
        "Weekly Delegation Review", "المراجعة الأسبوعية للتفويض",
        "A weekly cadence to review delegated work quality.",
        "إيقاع أسبوعي لمراجعة جودة العمل المفوَّض.",
        [
            S("Review / المراجعة",
              "Review delegated outputs against checklists.",
              "Capture errors as prevention items.",
              "Confirm context is preserved for continuity."),
        ],
    )),
]

# 7. Agent Governance OS -----------------------------------------------------
SYSTEMS["docs/agent-governance-os"] = [
    ("00_AGENT_GOVERNANCE_OS.md", (
        "Agent Governance OS", "نظام حوكمة الوكلاء",
        "Roles, boundaries, QA, cost control, and audit for AI agents.",
        "الأدوار والحدود وضمان الجودة وضبط التكلفة والتدقيق للوكلاء.",
        [
            S("Overview / نظرة عامة",
              "Every agent has a defined role and explicit boundaries.",
              "Agents prepare and recommend; they never act autonomously externally.",
              "Defined in config/agent_registry.json and config/agent_prompt_library.json."),
        ],
    )),
    ("01_AGENT_ROLES.md", (
        "Agent Roles", "أدوار الوكلاء",
        "The defined agent roles and their responsibilities.",
        "أدوار الوكلاء المحددة ومسؤولياتها.",
        [
            S("Roles / الأدوار",
              "founder_brief_agent: synthesizes daily briefs for the founder.",
              "commercial_draft_agent: drafts commercial copy for approval.",
              "safety_audit_agent: scans outputs for boundary violations.",
              "message_quality_agent: checks message clarity and tone.",
              "market_intelligence_agent: compiles market signals from allowed sources.",
              "proposal_agent: assembles proposals for founder review.",
              "delivery_agent: prepares delivery artifacts under QMS.",
              "media_social_agent: drafts social content for approval.",
              "investor_readiness_agent: prepares investor materials."),
        ],
    )),
    ("02_AGENT_BOUNDARIES.md", (
        "Agent Boundaries", "حدود الوكلاء",
        "Hard boundaries every agent must respect.",
        "الحدود الصارمة التي يجب على كل وكيل احترامها.",
        [
            S("Boundaries / الحدود",
              "No external sending under any circumstance.",
              "No secrets and no customer-sensitive data without agreement.",
              "No unverified claims and no autonomous decisions.",
              "Founder approval is required before any external use."),
        ],
    )),
    ("03_AGENT_PROMPT_LIBRARY.md", (
        "Agent Prompt Library", "مكتبة موجهات الوكلاء",
        "Reusable, governed prompts mapped to agent roles.",
        "موجهات قابلة لإعادة الاستخدام ومحكومة ومرتبطة بأدوار الوكلاء.",
        [
            S("Library / المكتبة",
              "Each role maps to a vetted prompt in config/agent_prompt_library.json.",
              "Prompts embed the boundaries and the approval-first rule.",
              "Prompts are versioned and reviewed."),
        ],
    )),
    ("04_AGENT_OUTPUT_QA.md", (
        "Agent Output QA", "ضمان جودة مخرجات الوكلاء",
        "How agent outputs are checked before use.",
        "كيف تُفحص مخرجات الوكلاء قبل الاستخدام.",
        [
            S("QA / ضمان الجودة",
              "Safety scan for boundary and claim violations.",
              "Quality scan for clarity, accuracy, and tone.",
              "Founder review before anything external."),
        ],
    )),
    ("05_AGENT_COST_CONTROL.md", (
        "Agent Cost Control", "ضبط تكلفة الوكلاء",
        "How agent usage is kept cost-efficient.",
        "كيف يبقى استخدام الوكلاء فعّالًا من حيث التكلفة.",
        [
            S("Cost Control / ضبط التكلفة",
              "Cheap-model-first; escalate to strong models only when justified.",
              "Token budgets per task tier (see Cost Control OS).",
              "No API keys stored; cost assumptions documented in config."),
        ],
    )),
    ("06_AGENT_FAILURE_MODES.md", (
        "Agent Failure Modes", "أنماط فشل الوكلاء",
        "Known failure modes and mitigations.",
        "أنماط الفشل المعروفة وإجراءات التخفيف.",
        [
            S("Failure Modes / أنماط الفشل",
              "Hallucinated claims → safety/quality QA gates.",
              "Boundary drift → explicit boundary prompts and audit log.",
              "Cost overrun → budgets and cheap-model-first routing."),
        ],
    )),
    ("07_AGENT_AUDIT_LOG_POLICY.md", (
        "Agent Audit Log Policy", "سياسة سجل تدقيق الوكلاء",
        "What agent activity is logged for auditability.",
        "ما يُسجَّل من نشاط الوكلاء لأغراض التدقيق.",
        [
            S("Audit Log / سجل التدقيق",
              "Record role, task, model tier, and approval status.",
              "No secrets or customer-sensitive data in logs.",
              "Logs support founder review and accountability."),
        ],
    )),
]

# 8. Cost Control OS ---------------------------------------------------------
SYSTEMS["docs/cost-control-os"] = [
    ("00_COST_CONTROL_OS.md", (
        "Cost Control OS", "نظام ضبط التكاليف",
        "Model routing and token budgets to keep AI usage affordable.",
        "توجيه النماذج وميزانيات التوكنز لإبقاء استخدام الذكاء الاصطناعي ميسورًا.",
        [
            S("Overview / نظرة عامة",
              "Cheap-model-first; strong models only with justification.",
              "Token budgets per task tier; manual cost alerts.",
              "Defined in config/model_routing_policy.json and config/token_budgets.json."),
        ],
    )),
    ("01_MODEL_ROUTING_POLICY.md", (
        "Model Routing Policy", "سياسة توجيه النماذج",
        "Which tasks use light vs strong models.",
        "أي المهام تستخدم نماذج خفيفة مقابل قوية.",
        [
            S("Routing / التوجيه",
              "Light model: drafting, summarization, classification.",
              "Strong model: complex reasoning, high-stakes proposals.",
              "Founder approval required to escalate to the most expensive tier."),
        ],
    )),
    ("02_TOKEN_BUDGETS.md", (
        "Token Budgets", "ميزانيات التوكنز",
        "Budget ceilings per task tier.",
        "سقوف الميزانية لكل فئة مهمة.",
        [
            S("Budgets / الميزانيات",
              "Each tier has a soft and hard token ceiling.",
              "Exceeding the soft ceiling triggers a manual review.",
              "Budgets are assumptions documented in config, not live billing."),
        ],
    )),
    ("03_TASK_TIERING.md", (
        "Task Tiering", "تصنيف المهام",
        "How tasks are tiered by complexity and stakes.",
        "كيف تُصنّف المهام حسب التعقيد والأهمية.",
        [
            S("Tiers / الفئات",
              "Tier 1 (light): routine drafting and formatting.",
              "Tier 2 (standard): analysis and ranking.",
              "Tier 3 (high): strategic reasoning and high-stakes outputs."),
        ],
    )),
    ("04_COST_ALERTS_MANUAL_PROCESS.md", (
        "Cost Alerts Manual Process", "عملية تنبيهات التكلفة اليدوية",
        "A manual process for monitoring and reacting to cost.",
        "عملية يدوية لمراقبة التكلفة والتفاعل معها.",
        [
            S("Process / العملية",
              "Review usage assumptions on a fixed cadence.",
              "Flag tasks exceeding their tier budget.",
              "No automated billing access; founder reviews assumptions."),
        ],
    )),
    ("05_CHEAP_MODEL_FIRST_POLICY.md", (
        "Cheap Model First Policy", "سياسة النموذج الأرخص أولًا",
        "Default to the cheapest model that meets the quality bar.",
        "الافتراضي هو أرخص نموذج يحقق مستوى الجودة.",
        [
            S("Policy / السياسة",
              "Start with the light model; escalate only on measured need.",
              "Document the reason for any escalation.",
              "Re-test downgrades periodically."),
        ],
    )),
    ("06_EXPENSIVE_MODEL_APPROVAL_RULES.md", (
        "Expensive Model Approval Rules", "قواعد اعتماد النموذج المكلف",
        "When the most expensive model requires founder approval.",
        "متى يتطلب النموذج الأغلى اعتماد المؤسس.",
        [
            S("Rules / القواعد",
              "Tier 3 high-stakes outputs may use the strongest model.",
              "Founder approval required when exceeding hard token ceilings.",
              "Every escalation is recorded for cost auditability."),
        ],
    )),
]

# 9. Data Room OS ------------------------------------------------------------
SYSTEMS["docs/data-room-os"] = [
    ("00_DATA_ROOM_OS.md", (
        "Data Room OS", "نظام غرفة البيانات",
        "What goes to investors, enterprise clients, and partners — evidence-first.",
        "ما يُقدّم للمستثمرين وعملاء المؤسسات والشركاء — بالدليل أولًا.",
        [
            S("Overview / نظرة عامة",
              "Separate packets for investors, enterprise clients, and partners.",
              "Only sourced evidence; no fake traction and no numbers without a source.",
              "Indexed for fast, controlled access."),
        ],
    )),
    ("01_DATA_ROOM_INDEX.md", (
        "Data Room Index", "فهرس غرفة البيانات",
        "The master index of data-room contents.",
        "الفهرس الرئيسي لمحتويات غرفة البيانات.",
        [
            S("Index / الفهرس",
              "Company overview, evidence policy, and packet folders.",
              "Each item links to a verifiable source.",
              "Access is controlled and logged by the founder."),
        ],
    )),
    ("02_COMPANY_FOLDER_STRUCTURE.md", (
        "Company Folder Structure", "هيكل مجلدات الشركة",
        "How company documents are organized.",
        "كيف تُنظّم وثائق الشركة.",
        [
            S("Structure / الهيكل",
              "Legal, financial, product, and proof folders.",
              "Consistent naming and versioning.",
              "Sensitive items gated behind agreements."),
        ],
    )),
    ("03_INVESTOR_PACKET.md", (
        "Investor Packet", "حزمة المستثمر",
        "What an investor sees, evidence-first.",
        "ما يراه المستثمر بالدليل أولًا.",
        [
            S("Contents / المحتويات",
              "Company narrative, market, and traction with sources.",
              "Unit-economics assumptions clearly labeled as assumptions.",
              "No fabricated metrics; gaps disclosed honestly."),
        ],
    )),
    ("04_ENTERPRISE_CLIENT_PACKET.md", (
        "Enterprise Client Packet", "حزمة العميل المؤسسي",
        "What an enterprise client receives for evaluation.",
        "ما يتلقاه العميل المؤسسي للتقييم.",
        [
            S("Contents / المحتويات",
              "Security and privacy overviews, service catalog, and pilot structure.",
              "Honest certification status; pending items disclosed.",
              "Reference proof where verifiable."),
        ],
    )),
    ("05_PARTNER_PACKET.md", (
        "Partner Packet", "حزمة الشريك",
        "What a partner receives to evaluate collaboration.",
        "ما يتلقاه الشريك لتقييم التعاون.",
        [
            S("Contents / المحتويات",
              "Partnership model, responsibilities, and economics.",
              "Boundaries: no scraping, no automation, approval-first.",
              "Mutual evidence and expectations."),
        ],
    )),
    ("06_DUE_DILIGENCE_QA.md", (
        "Due Diligence Q&A", "أسئلة وأجوبة العناية الواجبة",
        "Prepared answers to common due-diligence questions.",
        "إجابات مُجهّزة لأسئلة العناية الواجبة الشائعة.",
        [
            S("Q&A / أسئلة وأجوبة",
              "Legal, security, data, and commercial questions.",
              "Honest answers; pending items marked as such.",
              "No unverified claims."),
        ],
    )),
    ("07_EVIDENCE_POLICY.md", (
        "Evidence Policy", "سياسة الأدلة",
        "What evidence is allowed and what is forbidden.",
        "ما الأدلة المسموحة وما الممنوعة.",
        [
            S("Policy / السياسة",
              "Allowed: sourced, verifiable evidence.",
              "Forbidden: fake traction, numbers without a source, unverified claims.",
              "Every claim links to its source."),
        ],
    )),
]

# 10. Procurement OS ---------------------------------------------------------
SYSTEMS["docs/procurement-os"] = [
    ("00_PROCUREMENT_OS.md", (
        "Procurement OS", "نظام المشتريات والتعاقد",
        "How Dealix navigates vendor registration, POs, SOWs, and change requests.",
        "كيف يتعامل Dealix مع تسجيل المورّد وأوامر الشراء وبيانات العمل وطلبات التغيير.",
        [
            S("Overview / نظرة عامة",
              "Standardized vendor registration and contracting posture.",
              "SOW acceptance criteria and change-request control prevent scope creep.",
              "All terms remain founder-approved."),
        ],
    )),
    ("01_VENDOR_REGISTRATION_PACKET.md", (
        "Vendor Registration Packet", "حزمة تسجيل المورّد",
        "What large buyers need to register Dealix as a vendor.",
        "ما يحتاجه المشترون الكبار لتسجيل Dealix كمورّد.",
        [
            S("Packet / الحزمة",
              "Company registration, banking, and contact details (founder-maintained).",
              "Standard answers to vendor forms (pending legal review).",
              "No secrets included."),
        ],
    )),
    ("02_PURCHASE_ORDER_PROCESS.md", (
        "Purchase Order Process", "عملية أمر الشراء",
        "How POs are received and fulfilled.",
        "كيف تُستلم أوامر الشراء وتُنفّذ.",
        [
            S("Process / العملية",
              "Match PO to the agreed SOW and price.",
              "Confirm acceptance criteria before starting work.",
              "Founder confirms commercial terms."),
        ],
    )),
    ("03_CONTRACT_NEGOTIATION_RULES.md", (
        "Contract Negotiation Rules", "قواعد التفاوض على العقود",
        "Guardrails for negotiating contracts.",
        "ضوابط التفاوض على العقود.",
        [
            S("Rules / القواعد",
              "Protect scope, price, and timeline.",
              "Trade concessions for scope, not for free value.",
              "No guaranteed-outcome clauses."),
        ],
    )),
    ("04_PAYMENT_TERMS_POLICY.md", (
        "Payment Terms Policy", "سياسة شروط الدفع",
        "Standard payment-terms posture.",
        "الموقف القياسي لشروط الدفع.",
        [
            S("Policy / السياسة",
              "Prefer upfront or milestone-based payment.",
              "Define late-payment handling.",
              "Terms remain founder-approved per deal."),
        ],
    )),
    ("05_SOW_ACCEPTANCE_CRITERIA.md", (
        "SOW Acceptance Criteria", "معايير قبول بيان العمل",
        "How deliverables are accepted.",
        "كيف تُقبل المخرجات.",
        [
            S("Criteria / المعايير",
              "Define done before work starts.",
              "Acceptance tied to measurable deliverables.",
              "Sign-off recorded."),
        ],
    )),
    ("06_CHANGE_REQUEST_PROCESS.md", (
        "Change Request Process", "عملية طلب التغيير",
        "How scope changes are controlled and priced.",
        "كيف تُضبط تغييرات النطاق وتُسعّر.",
        [
            S("Process / العملية",
              "All changes go through a written change request.",
              "Each change is scoped, priced, and approved before work.",
              "Prevents uncompensated scope creep."),
        ],
    )),
]

# 11. QMS OS -----------------------------------------------------------------
SYSTEMS["docs/qms-os"] = [
    ("00_QUALITY_MANAGEMENT_SYSTEM.md", (
        "Quality Management System", "نظام إدارة الجودة",
        "The quality system governing delivery, sales, messaging, and security.",
        "نظام الجودة الذي يحكم التسليم والمبيعات والرسائل والأمن.",
        [
            S("Overview / نظرة عامة",
              "Quality policy, document control, and continuous improvement.",
              "Checklists per function (config/qms_checklists.json).",
              "Quality bar is consistent and auditable."),
        ],
    )),
    ("01_QUALITY_POLICY.md", (
        "Quality Policy", "سياسة الجودة",
        "Our commitment to a consistent quality standard.",
        "التزامنا بمعيار جودة متسق.",
        [
            S("Policy / السياسة",
              "Every external artifact meets a defined quality bar.",
              "Quality is reviewed, not assumed.",
              "Defects feed continuous improvement."),
        ],
    )),
    ("02_DOCUMENT_CONTROL.md", (
        "Document Control", "ضبط الوثائق",
        "How documents are owned, versioned, and kept current.",
        "كيف تُملك الوثائق وتُؤرشف وتبقى محدثة.",
        [
            S("Control / الضبط",
              "Each document has an owner and a version.",
              "Deprecated docs are clearly marked.",
              "Source-of-truth rules prevent drift."),
        ],
    )),
    ("03_DELIVERY_QA.md", (
        "Delivery QA", "ضمان جودة التسليم",
        "Quality checks for delivery artifacts.",
        "فحوص الجودة لمخرجات التسليم.",
        [
            S("Delivery QA / ضمان جودة التسليم",
              "Proof packs meet the QMS checklist.",
              "Acceptance criteria verified before handoff.",
              "Learnings captured per delivery."),
        ],
    )),
    ("04_SALES_QA.md", (
        "Sales QA", "ضمان جودة المبيعات",
        "Quality checks for sales artifacts.",
        "فحوص الجودة لمخرجات المبيعات.",
        [
            S("Sales QA / ضمان جودة المبيعات",
              "Proposals are accurate and free of unverified claims.",
              "Pricing follows the guardrails.",
              "Founder-approved before sending."),
        ],
    )),
    ("05_MESSAGE_QA.md", (
        "Message QA", "ضمان جودة الرسائل",
        "Quality checks for outbound-draft messages.",
        "فحوص الجودة لمسودات الرسائل.",
        [
            S("Message QA / ضمان جودة الرسائل",
              "Clarity, tone, and accuracy checked.",
              "No promises that cannot be kept.",
              "Drafts queued for founder approval; never auto-sent."),
        ],
    )),
    ("06_SECURITY_QA.md", (
        "Security QA", "ضمان الجودة الأمنية",
        "Quality checks for security posture.",
        "فحوص الجودة للموقف الأمني.",
        [
            S("Security QA / ضمان الجودة الأمنية",
              "No secrets in artifacts.",
              "Boundaries respected; no external sending.",
              "Honest certification status."),
        ],
    )),
    ("07_CONTINUOUS_IMPROVEMENT.md", (
        "Continuous Improvement", "التحسين المستمر",
        "How defects and learnings improve the system.",
        "كيف تحسّن العيوب والدروس النظام.",
        [
            S("Improvement / التحسين",
              "Capture defects and root causes.",
              "Update checklists and playbooks.",
              "Review improvement actions on a cadence."),
        ],
    )),
]

# 12. Documentation Governance OS -------------------------------------------
SYSTEMS["docs/docs-governance-os"] = [
    ("00_DOCS_GOVERNANCE_OS.md", (
        "Documentation Governance OS", "نظام حوكمة الوثائق",
        "Source-of-truth, ownership, versioning, and link-health rules.",
        "قواعد مصدر الحقيقة والملكية والإصدارات وصحة الروابط.",
        [
            S("Overview / نظرة عامة",
              "One source of truth per topic.",
              "Owners, versions, and deprecation rules.",
              "Automated checks via scripts/docs_governance_verify.py."),
        ],
    )),
    ("01_SOURCE_OF_TRUTH_RULES.md", (
        "Source Of Truth Rules", "قواعد مصدر الحقيقة",
        "How we avoid conflicting documents.",
        "كيف نتجنب الوثائق المتعارضة.",
        [
            S("Rules / القواعد",
              "One canonical doc per topic; others link to it.",
              "Conflicts are resolved by the owner.",
              "Master Index points to canonical systems."),
        ],
    )),
    ("02_DOC_OWNERSHIP.md", (
        "Doc Ownership", "ملكية الوثائق",
        "Every document has an accountable owner.",
        "لكل وثيقة مالك مسؤول.",
        [
            S("Ownership / الملكية",
              "Owner maintains accuracy and currency.",
              "Ownership recorded and reviewed.",
              "Founder owns boundary-critical policies."),
        ],
    )),
    ("03_VERSIONING_POLICY.md", (
        "Versioning Policy", "سياسة الإصدارات",
        "How document versions are tracked.",
        "كيف تُتابع إصدارات الوثائق.",
        [
            S("Policy / السياسة",
              "Material changes bump the version.",
              "History preserved in git.",
              "Layer labels (e.g. V9) indicate provenance."),
        ],
    )),
    ("04_DEPRECATION_POLICY.md", (
        "Deprecation Policy", "سياسة الإيقاف",
        "How obsolete docs are retired safely.",
        "كيف تُتقاعد الوثائق القديمة بأمان.",
        [
            S("Policy / السياسة",
              "Deprecated docs are clearly labeled.",
              "Replacement is linked.",
              "No silent deletion of referenced docs."),
        ],
    )),
    ("05_LINK_CHECK_POLICY.md", (
        "Link Check Policy", "سياسة فحص الروابط",
        "How we keep internal references healthy.",
        "كيف نحافظ على صحة المراجع الداخلية.",
        [
            S("Policy / السياسة",
              "No stale legacy brand references; retired product codenames are purged.",
              "Key reports must exist and be referenced.",
              "README points to the most important systems."),
        ],
    )),
]

# 14. Deployment Verification OS --------------------------------------------
SYSTEMS["docs/deployment-verification-os"] = [
    ("00_DEPLOYMENT_VERIFICATION_OS.md", (
        "Deployment Verification OS", "نظام التحقق من النشر",
        "Static, non-destructive checks for safe deployment posture.",
        "فحوص ثابتة وغير مدمّرة لموقف نشر آمن.",
        [
            S("Overview / نظرة عامة",
              "Static verification only; no risky deploys triggered.",
              "Documented commands for main server, frontend, and backend.",
              "Rollback and smoke-test checklists."),
        ],
    )),
    ("01_MAIN_SERVER_CHECKLIST.md", (
        "Main Server Checklist", "قائمة فحص الخادم الرئيسي",
        "Pre/post checks for the main server.",
        "فحوص قبل/بعد للخادم الرئيسي.",
        [
            S("Checklist / القائمة",
              "Confirm health endpoint responds.",
              "Confirm environment configuration is present (no secrets in repo).",
              "Confirm no destructive migrations queued."),
        ],
    )),
    ("02_HEALTHCHECK_POLICY.md", (
        "Healthcheck Policy", "سياسة فحص الصحة",
        "How service health is verified.",
        "كيف تُتحقق صحة الخدمة.",
        [
            S("Policy / السياسة",
              "Health endpoints return a clear status.",
              "Checks are read-only.",
              "Failures escalate to the founder."),
        ],
    )),
    ("03_FRONTEND_DEPLOY_CHECK.md", (
        "Frontend Deploy Check", "فحص نشر الواجهة",
        "Static checks for the frontend deployment.",
        "فحوص ثابتة لنشر الواجهة.",
        [
            S("Checks / الفحوص",
              "Build configuration present and valid.",
              "Trust/security/privacy pages referenced where applicable.",
              "No secrets embedded in the build."),
        ],
    )),
    ("04_BACKEND_DEPLOY_CHECK.md", (
        "Backend Deploy Check", "فحص نشر الخادم الخلفي",
        "Static checks for the backend deployment.",
        "فحوص ثابتة لنشر الخادم الخلفي.",
        [
            S("Checks / الفحوص",
              "Required config files present.",
              "No destructive migration on deploy.",
              "Health and readiness documented."),
        ],
    )),
    ("05_ROLLBACK_CHECKLIST.md", (
        "Rollback Checklist", "قائمة فحص التراجع",
        "How to roll back safely.",
        "كيف نتراجع بأمان.",
        [
            S("Checklist / القائمة",
              "Identify last known-good release.",
              "Roll back without data loss.",
              "Verify health after rollback."),
        ],
    )),
    ("06_POST_DEPLOY_SMOKE_TEST.md", (
        "Post Deploy Smoke Test", "اختبار الدخان بعد النشر",
        "Minimal checks confirming a deploy is healthy.",
        "فحوص دنيا تؤكد سلامة النشر.",
        [
            S("Smoke Test / اختبار الدخان",
              "Core endpoints respond.",
              "No errors in startup logs.",
              "Trust pages reachable where present."),
        ],
    )),
]


def build_reports() -> None:
    """Write the 99_*_REPORT.md for each system folder."""
    report_specs = {
        "docs/strategic-moat-os/99_STRATEGIC_MOAT_REPORT.md": (
            "Strategic Moat OS", "strategic_moat",
            ["Five-moat operating docs (data, workflow IP, trust, distribution, delivery, category)."],
            ["Defines durable, compounding advantages that are hard to copy."],
            ["Moats compound slowly; require disciplined asset capture each engagement."],
            ["Capture one reusable asset per engagement; review moat metrics monthly."]),
        "docs/enterprise-readiness-os/99_ENTERPRISE_READINESS_REPORT.md": (
            "Enterprise Readiness OS", "enterprise_readiness",
            ["Buyer map, procurement, security/data answers, pilot, and pricing guardrails."],
            ["Prepares Dealix to sell to large organizations without overclaiming."],
            ["Security/legal answers are templates pending external review."],
            ["Route security and legal templates through review before customer use."]),
        "docs/trust-center-os/99_TRUST_CENTER_REPORT.md": (
            "Trust Center OS", "trust_center",
            ["Public trust page spec plus security, privacy, and approval policies."],
            ["Trust is a moat in regulated Saudi sectors."],
            ["Public claims must stay strictly verifiable."],
            ["Publish /trust, /security, /privacy aligned to these policies."]),
        "docs/demo-os/99_DEMO_OS_REPORT.md": (
            "Demo OS", "demo_os",
            ["Demo narrative, vertical scenarios, sample-data policy, script, and QA.",
             "Demo pack generator and sample data/config."],
            ["Safe, sandbox-only demos that convert to paid diagnostics."],
            ["Demo must never imply a live customer integration."],
            ["Run scripts/demo_pack_generate.py before each founder demo."]),
        "docs/customer-lifecycle-os/99_CUSTOMER_LIFECYCLE_REPORT.md": (
            "Customer Lifecycle OS", "customer_lifecycle",
            ["Full lifecycle stages with outputs, measures, triggers, and risks.",
             "Lifecycle stage config and verifier."],
            ["Drives conversion, retention, and expansion systematically."],
            ["Health signals require disciplined, regular review."],
            ["Run health reviews on cadence; act on amber/red early."]),
        "docs/delegation-os/99_DELEGATION_OS_REPORT.md": (
            "Delegation OS", "delegation",
            ["Founder-only vs delegable split and operator playbooks."],
            ["Lets the founder scale without losing context or quality."],
            ["Delegated work needs review to maintain the quality bar."],
            ["Onboard first operator using the Master Index and checklists."]),
        "docs/agent-governance-os/99_AGENT_GOVERNANCE_REPORT.md": (
            "Agent Governance OS", "agent_governance",
            ["Agent roles, boundaries, prompt library, QA, cost, and audit.",
             "Agent registry and prompt-library configs."],
            ["Keeps AI agents safe, bounded, and approval-first."],
            ["Boundary drift if prompts are edited without review."],
            ["Review agent registry and prompts on each change."]),
        "docs/cost-control-os/99_COST_CONTROL_REPORT.md": (
            "Cost Control OS", "cost_control",
            ["Model routing, token budgets, tiering, and approval rules.",
             "Routing and budget configs (no API keys)."],
            ["Keeps AI usage affordable and predictable."],
            ["Budgets are assumptions, not live billing."],
            ["Review usage assumptions on cadence; tune tiers."]),
        "docs/data-room-os/99_DATA_ROOM_REPORT.md": (
            "Data Room OS", "data_room",
            ["Index, packets for investor/enterprise/partner, and evidence policy."],
            ["Controlled, evidence-first sharing with stakeholders."],
            ["Any unsourced number would undermine credibility."],
            ["Keep every claim sourced; refuse fake traction."]),
        "docs/procurement-os/99_PROCUREMENT_OS_REPORT.md": (
            "Procurement OS", "procurement",
            ["Vendor registration, PO, SOW, payment, and change-request processes."],
            ["Lets Dealix transact cleanly with large buyers."],
            ["Scope creep without disciplined change control."],
            ["Use change requests for every scope change."]),
        "docs/qms-os/99_QMS_REPORT.md": (
            "Quality Management System", "qms",
            ["Quality policy, document control, and per-function QA checklists.",
             "QMS checklist config and verifier."],
            ["Guarantees a consistent quality bar across functions."],
            ["Checklists must be kept current."],
            ["Run QMS checks before external artifacts ship."]),
        "docs/docs-governance-os/99_DOCS_GOVERNANCE_REPORT.md": (
            "Documentation Governance OS", "docs_governance",
            ["Source-of-truth, ownership, versioning, deprecation, link-health.",
             "Docs governance verifier."],
            ["Prevents conflicting or stale documentation."],
            ["Stale brand references must be caught."],
            ["Run docs_governance_verify.py in CI."]),
        "docs/deployment-verification-os/99_DEPLOYMENT_VERIFICATION_REPORT.md": (
            "Deployment Verification OS", "deployment_static",
            ["Server/frontend/backend checklists, rollback, and smoke tests.",
             "Static deployment verifier (non-destructive)."],
            ["Confirms safe deploy posture without risky actions."],
            ["Static checks do not replace live monitoring."],
            ["Run static verification before and after deploys."]),
    }
    for path, (system, slug, added, why, risks, nexts) in report_specs.items():
        body = render(
            f"{system} — Report", f"{system} — تقرير",
            f"Status report for {system}.", f"تقرير حالة لـ {system}.",
            report_sections(slug, added, why, risks, nexts),
        )
        out = REPO / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8")


def main() -> int:
    count = 0
    for folder, files in SYSTEMS.items():
        for filename, spec in files:
            out = REPO / folder / filename
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(*spec), encoding="utf-8")
            count += 1
    build_reports()
    count += 13
    print(f"generated {count} V9 docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
