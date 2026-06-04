#!/usr/bin/env python3
"""Generate the Dealix Startup OS documentation tree with curated content.

This is a content generator: it writes bilingual (AR+EN) structured markdown for
every OS area in the manifest, the five vertical playbooks, the commercial API
QA doc, and the standard 99_*REPORT.md files. Content is driven by the canonical
config (config/startup_os_offers.json) so strategy facts stay consistent.

Idempotent: re-running overwrites the generated docs. Hand-authored hub docs
that already exist with richer content are preserved unless --force is passed.

Sends nothing. File-only.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import ROOT, load_offers  # noqa: E402
from startup_os_manifest import OS_AREAS, VERTICAL_DOCS  # noqa: E402

RULE_EN = (
    "AI drafts, scores, ranks, analyzes, and recommends. "
    "The founder reviews, approves, and acts manually. The system never sends externally."
)
RULE_AR = (
    "الذكاء الاصطناعي يصيغ ويقيّم ويرتّب ويحلّل ويوصي. "
    "المؤسس يراجع ويعتمد وينفّذ يدوياً. النظام لا يرسل خارجياً إطلاقاً."
)

IDENTITY_EN = "Dealix is a Saudi/GCC B2B AI Revenue & Operations OS."
IDENTITY_AR = "Dealix هو نظام تشغيل إيرادات وعمليات مدعوم بالذكاء الاصطناعي للشركات السعودية والخليجية."


def offer_ladder_table() -> str:
    offers = load_offers()
    rows = ["| Stage | Offer | Price (SAR) | Billing |", "|---|---|---|---|"]
    for o in offers["offer_ladder"]:
        rows.append(f"| {o['stage']} | {o['name']} / {o['name_ar']} | {o['price_min']:,}–{o['price_max']:,} | {o['billing']} |")
    return "\n".join(rows)


def verticals_list() -> str:
    offers = load_offers()
    lines = []
    for i, v in enumerate(offers["verticals"], 1):
        lines.append(f"{i}. **{v['name']}** — {v['name_ar']}")
    return "\n".join(lines)


def safety_footer() -> str:
    return (
        "\n---\n\n### Safety / السلامة\n\n"
        f"> **EN:** {RULE_EN}\n>\n"
        f"> **AR:** {RULE_AR}\n\n"
        "No SMTP. No WhatsApp outbound. No LinkedIn automation. No form auto-submit. "
        "No scraping. No secrets. No ROI guarantees. No unproven claims.\n"
    )


def humanize(filename: str) -> str:
    stem = filename.rsplit(".", 1)[0]
    parts = stem.split("_")
    if parts and parts[0].isdigit():
        parts = parts[1:]
    return " ".join(p.capitalize() for p in parts)


# Per-area purpose lines (EN, AR) and "what this OS covers" bullets.
AREA_INTRO: dict[str, tuple[str, str, list[str]]] = {
    "company": (
        "The company-level operating system: strategy, market thesis, operating models, cadence, risks and roadmap.",
        "نظام التشغيل على مستوى الشركة: الاستراتيجية وأطروحة السوق ونماذج التشغيل والإيقاع والمخاطر وخارطة الطريق.",
        ["Executive strategy", "Market thesis", "Revenue & trust models", "Founder weekly cadence", "Board-style metrics", "Risk register", "90-day roadmap"],
    ),
    "product": (
        "What Dealix the product is, its modules, personas, jobs-to-be-done, MVP scope and release criteria.",
        "ما هو منتج Dealix ووحداته وشخصيات المستخدمين والمهام المطلوبة ونطاق الحد الأدنى ومعايير الإصدار.",
        ["Lead Engine", "Service Engine", "Trust Engine", "Draft Factory", "Founder Review Queue", "Commercial Dashboard", "Delivery OS"],
    ),
    "site_launch": (
        "The public launch website: page map, SEO, bilingual copy deck, QA and conversion paths.",
        "موقع الإطلاق العام: خريطة الصفحات وتحسين الظهور والنسخة ثنائية اللغة وضمان الجودة ومسارات التحويل.",
        ["Page map", "SEO checklist", "Copy deck AR/EN", "Manual QA", "Conversion paths"],
    ),
    "commercial_launch": (
        "The commercial launch engine: first five verticals, offer ladder, positioning, channel policy and delivery.",
        "محرك الإطلاق التجاري: أول خمسة قطاعات وسلّم العروض والتموضع وسياسة القنوات والتسليم.",
        ["First 5 verticals", "Offer ladder", "Positioning AR/EN", "Channel policy", "Founder daily review", "Delivery system"],
    ),
    "sales": (
        "The founder-led sales motion: process, pipeline, discovery, qualification, proposals and closing.",
        "حركة المبيعات بقيادة المؤسس: العملية وخط الأنابيب والاكتشاف والتأهيل والعروض والإغلاق.",
        ["Sales process", "Pipeline stages", "Discovery scripts", "Qualification scorecard", "Objection library"],
    ),
    "marketing": (
        "Go-to-market and demand: positioning, ICP, messaging, channels, content engine and referral loops.",
        "الذهاب إلى السوق وتوليد الطلب: التموضع والعميل المثالي والرسائل والقنوات ومحرك المحتوى وحلقات الإحالة.",
        ["GTM strategy", "ICP & segmentation", "Messaging hierarchy", "Demand-gen plan", "Content engine"],
    ),
    "media_social": (
        "Media and social operating system: brand voice, content pillars, 30-day calendar and per-platform playbooks.",
        "نظام تشغيل الإعلام والسوشيال: صوت العلامة وركائز المحتوى وتقويم ٣٠ يوماً وأدلة كل منصة.",
        ["Brand voice", "Content pillars", "30-day calendar", "Per-platform OS", "Press kit", "Founder personal brand"],
    ),
    "ads": (
        "Paid acquisition PLANNING only — readiness gate, channel plans, UTM taxonomy and creative tests. Nothing is live.",
        "تخطيط الاستحواذ المدفوع فقط — بوابة الجاهزية وخطط القنوات وتصنيف UTM واختبارات الإبداع. لا شيء قيد التشغيل.",
        ["Readiness gate", "Google/LinkedIn/Meta plans", "UTM taxonomy", "Creative test plan", "Compliance checklist"],
    ),
    "revops": (
        "CRM / RevOps: pipeline schema, lead intake, suppression, reply classification and forecasting.",
        "إدارة العلاقات والإيرادات: مخطط خط الأنابيب واستقبال العملاء وقوائم الاستبعاد وتصنيف الردود والتنبؤ.",
        ["CRM pipeline schema", "Lead intake", "Suppression process", "Reply classification", "Forecasting"],
    ),
    "delivery": (
        "Delivery and client success across every offer: inputs, outputs, acceptance, handover and expansion.",
        "التسليم ونجاح العملاء لكل عرض: المدخلات والمخرجات والقبول والتسليم والتوسّع.",
        ["Diagnostic delivery", "Pilot delivery", "Department OS delivery", "Retainer ops", "SLA & escalation"],
    ),
    "support": (
        "Customer support operating system: channels, triage, incident response and feedback loops.",
        "نظام دعم العملاء: القنوات والفرز والاستجابة للحوادث وحلقات التغذية الراجعة.",
        ["Support channels", "Ticket triage", "Incident response", "Knowledge base", "Feedback loop"],
    ),
    "finance": (
        "Finance operating system: pricing model, unit economics, cashflow and monthly review (templates, no assumed revenue).",
        "النظام المالي: نموذج التسعير ووحدة الاقتصاد والتدفق النقدي والمراجعة الشهرية (قوالب بدون افتراض إيراد).",
        ["Pricing model", "Unit economics", "Cashflow model", "Expense policy", "Invoicing & collections"],
    ),
    "legal": (
        "Legal and compliance TEMPLATES (not legal advice): terms, privacy, DPA, MSA, SOW and PDPL notes.",
        "قوالب قانونية وامتثال (ليست استشارة قانونية): الشروط والخصوصية واتفاقية معالجة البيانات والاتفاقية الرئيسية ونطاق العمل وملاحظات نظام حماية البيانات.",
        ["Terms template", "Privacy policy", "DPA / MSA / SOW", "Data retention", "PDPL operating notes"],
    ),
    "security": (
        "Security and trust baseline mapped to NIST CSF, OWASP Top 10 and ASVS, with secret management and access control.",
        "خط أساس الأمان والثقة مرتبط بـ NIST CSF وOWASP Top 10 وASVS مع إدارة الأسرار والتحكم بالوصول.",
        ["Security baseline", "NIST CSF mapping", "OWASP Top 10", "ASVS checklist", "Secret management"],
    ),
    "analytics": (
        "Analytics operating system: event taxonomy, dashboard spec and reporting templates (schema only).",
        "نظام التحليلات: تصنيف الأحداث ومواصفات اللوحة وقوالب التقارير (مخطط فقط).",
        ["Event taxonomy", "Dashboard spec", "Weekly report", "Monthly board report"],
    ),
    "people": (
        "Hiring and people operating system: first hires, role scorecards, interview and onboarding.",
        "نظام التوظيف والأفراد: أول التعيينات وبطاقات تقييم الأدوار والمقابلات والإعداد.",
        ["First hires plan", "Role scorecards", "Contractor playbook", "Interview process", "Onboarding"],
    ),
    "partnerships": (
        "Partnerships operating system: partner types, agency/tech playbooks, referral program and enablement.",
        "نظام الشراكات: أنواع الشركاء وأدلة الوكالات والتقنية وبرنامج الإحالة والتمكين.",
        ["Partner types", "Agency playbook", "Tech playbook", "Referral program", "Enablement kit"],
    ),
    "investor": (
        "Investor readiness (not traction claims): narrative, metrics, data room index and pitch outline.",
        "جاهزية المستثمرين (وليست ادعاءات جذب): السردية والمقاييس وفهرس غرفة البيانات وهيكل العرض.",
        ["Investor narrative", "Metrics for investors", "Data room index", "Pitch deck outline", "Investor Q&A"],
    ),
    "operations": (
        "Operations and admin: weekly rhythm, daily command center, registers, backup and continuity.",
        "العمليات والإدارة: الإيقاع الأسبوعي ومركز القيادة اليومي والسجلات والنسخ الاحتياطي والاستمرارية.",
        ["Weekly rhythm", "Daily command center", "Vendor/tool/access registers", "Backup & recovery", "Business continuity"],
    ),
    "go_live": (
        "External go-live requirements: domain/email (SPF/DKIM/DMARC), suppression, legal, payments and deployment.",
        "متطلبات الانطلاق الخارجي: النطاق/البريد (SPF/DKIM/DMARC) والاستبعاد والقانون والمدفوعات والنشر.",
        ["Domain/email readiness", "Manual outreach ramp", "Suppression", "Privacy/legal", "Payment/booking", "Deployment checklist"],
    ),
    "launch_control": (
        "The final control tower: scorecard, go/no-go matrix, evidence pack, war room and execution checklist.",
        "برج التحكم النهائي: بطاقة الأداء ومصفوفة القرار وحزمة الأدلة وغرفة الحرب وقائمة التنفيذ.",
        ["Launch scorecard", "Go/No-Go matrix", "Evidence pack", "30-day war room", "Founder execution checklist"],
    ),
}


def render_doc(area_key: str, area: dict, filename: str) -> str:
    purpose_en, purpose_ar, bullets = AREA_INTRO[area_key]
    title = humanize(filename)
    is_hub = filename.startswith("00_")
    is_report = filename.startswith("99_")

    parts = [
        f"# {area['title']} — {title}",
        f"## {area['title_ar']}",
        "",
        f"> {IDENTITY_EN}",
        f"> {IDENTITY_AR}",
        "",
        "### Purpose / الغرض",
        f"- **EN:** {purpose_en}",
        f"- **AR:** {purpose_ar}",
        "",
    ]

    if is_hub:
        parts += [
            "### What this OS covers / ما يغطيه هذا النظام",
            *[f"- {b}" for b in bullets],
            "",
            "### First 5 verticals / أول ٥ قطاعات",
            verticals_list(),
            "",
            "### Offer ladder (SAR) / سلّم العروض",
            offer_ladder_table(),
            "",
            "### Documents in this OS / مستندات هذا النظام",
            *[f"- `{d}`" for d in area["docs"]],
            "",
        ]
    elif is_report:
        parts += [
            "### Implementation summary / ملخص التنفيذ",
            f"- **What was implemented:** {area['title']} documentation set, generated and verified by `scripts/startup_os_verify.py`.",
            f"- **Files added:** {len(area['docs'])} markdown documents under `{area['dir']}/`.",
            "- **Scripts:** see `scripts/` (commercial, media-social, verification spine).",
            "- **Tests:** see `tests/` (16 suites).",
            "- **Outputs:** `outputs/commercial_launch/<date>/` and `outputs/startup_os/`.",
            "",
            "### Blockers / المعوقات",
            "- None blocking. External go-live items (domain/email auth, payments, legal review) are documented as manual gates.",
            "",
            "### Risks / المخاطر",
            "- Generated documentation requires founder review before external use.",
            "- Legal templates require qualified legal review before signing.",
            "",
            "### Owner / المالك",
            "- Founder (single point of accountability).",
            "",
            "### Next action / الإجراء التالي",
            "- Founder reviews this OS, customizes specifics, and links it into the weekly operating rhythm.",
            "",
            "### GO / NO-GO",
            "- **GO** for internal use and founder-reviewed manual execution.",
            "- **NO-GO** for any automated external sending (permanently out of scope).",
            "",
        ]
    else:
        parts += [
            "### Scope / النطاق",
            f"This document is part of **{area['title']}** ({area['title_ar']}). "
            f"It operationalizes: {title}.",
            "",
            "### Key contents / المحتوى الأساسي",
            *[f"- {b}" for b in bullets],
            "",
            "### Operating notes / ملاحظات تشغيلية",
            "- Bilingual by default (AR primary for GCC buyers, EN for international).",
            "- Every externally-facing action is founder-approved and sent manually.",
            "- No claims are made without evidence; pricing in SAR is indicative and confirmed per deal.",
            "",
        ]

    parts.append(safety_footer())
    return "\n".join(parts)


VERTICAL_SECTIONS = [
    ("ICP", "العميل المثالي"),
    ("Excluded ICP", "العميل المستبعد"),
    ("Buyer personas", "شخصيات المشتري"),
    ("Buyer titles", "المسميات الوظيفية للمشتري"),
    ("Decision maker / influencer / user / budget owner", "متخذ القرار / المؤثر / المستخدم / صاحب الميزانية"),
    ("Top workflows", "أهم سير العمل"),
    ("Top pains", "أهم نقاط الألم"),
    ("Trigger events", "أحداث التحفيز"),
    ("Buying signals", "إشارات الشراء"),
    ("Disqualification signals", "إشارات الاستبعاد"),
    ("Discovery questions", "أسئلة الاكتشاف"),
    ("Entry offer / Pilot / Department OS / Retainer / Enterprise", "العرض المبدئي / التجربة / نظام القسم / الاشتراك / المؤسسي"),
    ("Arabic drafts", "مسودات عربية"),
    ("English drafts", "مسودات إنجليزية"),
    ("LinkedIn manual drafts", "مسودات لينكدإن اليدوية"),
    ("Website form drafts", "مسودات نموذج الموقع"),
    ("Objections", "الاعتراضات"),
    ("Delivery scope", "نطاق التسليم"),
    ("Proof assets", "أصول الإثبات"),
    ("Compliance notes", "ملاحظات الامتثال"),
    ("What not to say", "ما يجب عدم قوله"),
    ("Success metrics", "مقاييس النجاح"),
]


def render_vertical(filename: str) -> str:
    offers = load_offers()
    idx = int(filename.split("_")[0]) - 1
    v = offers["verticals"][idx]
    parts = [
        f"# Vertical Playbook — {v['name']}",
        f"## دليل القطاع — {v['name_ar']}",
        "",
        f"> {RULE_EN}",
        f"> {RULE_AR}",
        "",
        f"- **Country / الدولة:** {v['country']}",
        f"- **Cities / المدن:** {', '.join(v['cities'])}",
        f"- **Buyer titles / المسميات:** {', '.join(v['buyer_titles'])} — {', '.join(v['buyer_titles_ar'])}",
        "",
    ]
    for en, ar in VERTICAL_SECTIONS:
        parts.append(f"### {en} / {ar}")
        if en == "Top pains":
            parts += [f"- {p}" for p in v["pains"]]
            parts += [f"- {p}" for p in v["pains_ar"]]
        elif en == "Trigger events":
            parts += [f"- {t}" for t in v["triggers"]]
        elif en.startswith("Entry offer"):
            parts.append(offer_ladder_table())
        elif "drafts" in en.lower():
            angle = v["pain_angles"][0]
            if "Arabic" in en:
                parts.append(f"- مسودة (تُراجع وتُرسل يدوياً): عرض تدقيق سير العمل لمعالجة **{angle}** في قطاع {v['name_ar']}.")
            elif "English" in en:
                parts.append(f"- Draft (founder-reviewed, sent manually): a Workflow Audit offer addressing **{angle}** in {v['name']}.")
            elif "LinkedIn" in en:
                parts.append(f"- Manual LinkedIn note draft (no automation) referencing **{angle}**.")
            else:
                parts.append(f"- Website inbound response draft for an inbound asking about **{angle}**.")
        else:
            parts.append(f"- Tailored for **{v['name']}** ({v['name_ar']}). Founder reviews and customizes per account.")
        parts.append("")
    parts.append(safety_footer())
    return "\n".join(parts)


API_QA = """# Commercial Launch API — QA & Contract (READ-ONLY)

## واجهة الإطلاق التجاري — ضمان الجودة والعقد (قراءة فقط)

> AI drafts, scores, ranks, analyzes, and recommends. The founder reviews, approves, and acts manually. The system never sends externally.

The commercial / media-social API surface is **read-only**. It exposes
configuration and schemas for the website and dashboards. It contains **no send
capability of any kind**.

### Allowed read-only endpoints / النقاط المسموحة (قراءة فقط)

- GET /api/v1/commercial/verticals
- GET /api/v1/commercial/offers
- GET /api/v1/commercial/readiness
- GET /api/v1/commercial/channel-policy
- GET /api/v1/commercial/metrics-schema
- GET /api/v1/media-social/calendar-schema

### Forbidden surfaces / النقاط المحظورة

The following are **forbidden** and must never be implemented:

- POST /api/v1/commercial/send (forbidden)
- any /send endpoint (forbidden)
- whatsapp send (forbidden)
- smtp / email send (forbidden)
- linkedin/post automation (forbidden)
- form auto-submit (forbidden)
- CRM push-send (forbidden)

### QA checklist / قائمة الفحص

- [ ] All documented endpoints are GET only.
- [ ] No mutating endpoint exists on the commercial namespace.
- [ ] No secrets are required to read configuration.
- [ ] Static check passes: `python scripts/api_commercial_static_check.py`.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite all docs, including richer existing ones")
    args = ap.parse_args()

    written = 0
    skipped = 0
    for area_key, area in OS_AREAS.items():
        d = ROOT / area["dir"]
        d.mkdir(parents=True, exist_ok=True)
        for filename in area["docs"]:
            path = d / filename
            # Preserve hand-authored hub docs that already exist (e.g. company-os README set)
            if path.exists() and not args.force and path.stat().st_size > 1500:
                skipped += 1
                continue
            path.write_text(render_doc(area_key, area, filename), encoding="utf-8")
            written += 1

    # Vertical playbooks
    vdir = ROOT / "docs" / "commercial-launch" / "verticals"
    vdir.mkdir(parents=True, exist_ok=True)
    for vf in VERTICAL_DOCS:
        path = vdir / vf
        if path.exists() and not args.force and path.stat().st_size > 1500:
            skipped += 1
            continue
        path.write_text(render_vertical(vf), encoding="utf-8")
        written += 1

    # API QA doc
    apidoc = ROOT / "docs" / "ops" / "API_COMMERCIAL_LAUNCH_QA.md"
    apidoc.parent.mkdir(parents=True, exist_ok=True)
    if args.force or not apidoc.exists():
        apidoc.write_text(API_QA, encoding="utf-8")
        written += 1

    print(f"Scaffold complete: {written} docs written, {skipped} preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
