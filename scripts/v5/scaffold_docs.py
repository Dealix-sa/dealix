#!/usr/bin/env python3
"""
Dealix Full Startup Company OS V5 — documentation tree generator.

Reproducibly emits the V5 company-OS markdown tree under docs/. Content is
doctrine-consistent (the non-negotiable review-only rule), bilingual-aware
(AR + EN), and area-specific — NOT empty stubs.

Re-running is idempotent: it overwrites generated files in place. Hand-authored
files are NOT listed here (the generator never touches them).

Usage:
    python scripts/v5/scaffold_docs.py [--check]

    --check  Do not write; exit 1 if any expected file is missing.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

NON_NEGOTIABLE = (
    "**Non-negotiable:** AI drafts, analyzes, scores, ranks, recommends, and prepares. "
    "The founder reviews, approves, sells, sends manually, and signs off. "
    "**The system never sends externally.**"
)

SAFETY = (
    "**Safety boundary:** No automated email/WhatsApp/LinkedIn sending, no scraping, "
    "no form auto-submit, no live paid ads, no secrets. All outputs are local, "
    "review-only artifacts requiring founder approval before any external action."
)

DEALIX_DEF = (
    "Dealix is a Saudi/GCC B2B AI Revenue & Operations OS "
    "(نظام تشغيل إيرادات وعمليات مدعوم بالذكاء الاصطناعي للشركات السعودية والخليجية). "
    "It is **not** a generic CRM, chatbot, marketing agency, mass-sender, or blind-automation tool."
)

VERTICALS = [
    "Facilities Management & Maintenance",
    "Contracting & Project Controls",
    "Real Estate & Property Operations",
    "Legal & Professional Services",
    "Consulting, Training & B2B Services",
]

OFFER_LADDER = [
    ("AI Workflow Audit", "499–2,500 SAR", "Entry diagnostic — review-only findings + prioritized fixes."),
    ("Paid Pilot", "5,000–25,000 SAR", "Scoped, time-boxed proof on one workflow."),
    ("Department OS", "25,000–150,000 SAR", "Operating system for one department."),
    ("Monthly Retainer", "3,000–25,000 SAR/month", "Ongoing draft + review + delivery ops."),
    ("Enterprise Custom OS", "150,000+ SAR", "Multi-department, custom integrations."),
]


def footer(owner: str = "Founder", next_action: str = "Review and approve", go: str = "GO (internal asset) — external actions remain founder-gated") -> str:
    return (
        "\n---\n\n"
        "### Operating footer\n"
        f"- **Owner:** {owner}\n"
        f"- **Next action:** {next_action}\n"
        f"- **GO/NO-GO:** {go}\n\n"
        f"> {NON_NEGOTIABLE}\n>\n> {SAFETY}\n"
    )


def render(title: str, purpose_en: str, purpose_ar: str, sections: list[tuple[str, list[str]]],
           owner: str = "Founder", next_action: str = "Review and approve") -> str:
    out = [f"# {title}\n"]
    out.append(f"> **Purpose (EN):** {purpose_en}\n>\n> **الغرض (AR):** {purpose_ar}\n")
    for heading, bullets in sections:
        out.append(f"\n## {heading}\n")
        for b in bullets:
            out.append(f"- {b}")
        out.append("")
    out.append(footer(owner, next_action))
    return "\n".join(out)


def report(area_title: str, files_added: list[str], scripts: list[str], tests: list[str],
           outputs: list[str], go_items: list[str], nogo_items: list[str]) -> str:
    def bl(items):
        return "\n".join(f"- {i}" for i in items) if items else "- _none_"
    return f"""# {area_title} — Implementation Report

> {NON_NEGOTIABLE}

## What was implemented
{bl([f"Documentation and operating playbooks for **{area_title}**, doctrine-aligned and bilingual-aware."])}

## Files added
{bl(files_added)}

## Scripts
{bl(scripts)}

## Tests
{bl(tests)}

## Outputs / artifacts
{bl(outputs)}

## Blockers
- None blocking internal use. External actions remain founder-gated by design.

## Risks
- Templates are starting points, not legal/financial advice; require human review before formal use.

## Owner
- Founder (single point of accountability), with sub-agents drafting under review.

## Next action
- Founder review → approve → operate the weekly cadence.

## GO / NO-GO

**GO (ready):**
{bl(go_items)}

**NO-GO (forbidden / blocked):**
{bl(nogo_items)}

{SAFETY}
"""


# ---------------------------------------------------------------------------
# Registry: directory -> list of (filename, builder)
# Builders are callables returning markdown. Kept compact via helpers.
# ---------------------------------------------------------------------------

def files_for_area(area_dir: str, area_title_en: str, area_title_ar: str,
                   specs: list[tuple[str, str, str, str, list[tuple[str, list[str]]]]],
                   report_meta: dict) -> dict[str, str]:
    """specs: list of (filename, title, purpose_en, purpose_ar, sections)."""
    out: dict[str, str] = {}
    for filename, title, pe, pa, sections in specs:
        out[f"{area_dir}/{filename}"] = render(title, pe, pa, sections)
    # report
    rfile = report_meta["filename"]
    out[f"{area_dir}/{rfile}"] = report(
        area_title_en,
        report_meta.get("files", [f"`docs/{area_dir}/`"]),
        report_meta.get("scripts", []),
        report_meta.get("tests", []),
        report_meta.get("outputs", []),
        report_meta.get("go", ["Internal operating asset ready for founder use."]),
        report_meta.get("nogo", ["Any external sending or live paid launch without founder sign-off."]),
    )
    return out


def s(*pairs: tuple[str, list[str]]) -> list[tuple[str, list[str]]]:
    return list(pairs)


REGISTRY: dict[str, str] = {}


def add(area_dir, area_title_en, area_title_ar, specs, report_meta):
    REGISTRY.update(files_for_area(area_dir, area_title_en, area_title_ar, specs, report_meta))


# ===== 2. Company OS =====
add("company-os", "Company OS", "نظام تشغيل الشركة", [
    ("00_DEALIX_COMPANY_OS.md", "Dealix Company OS", "The master index of how Dealix operates as a company.",
     "الفهرس الرئيسي لكيفية تشغيل Dealix كشركة.",
     s(("What is Dealix", [DEALIX_DEF,
        "Lead Engine · Service Engine · Trust Engine · Commercial Launch OS · Founder Review OS · Media & Social OS · Delivery OS · Expansion OS."]),
       ("Why now", ["Saudi/GCC B2B operators face manual revenue ops and low trust in blind automation.",
                    "Dealix wins on trust-first, human-in-the-loop, review-before-send."]),
       ("What we sell / do not sell", ["Sell: diagnostics, pilots, department OS, retainers, enterprise OS.",
                                       "Do not sell: blind mass-sending, scraping, unverified ROI guarantees."]),
       ("Operating index", ["Company / Product / Engineering / Site / Commercial / Sales / Marketing / Media / Ads.",
                            "RevOps / Delivery / Support / Finance / Legal / Security / Analytics / AI-Evals.",
                            "People / Partnerships / Investor / Operations / Go-Live / Launch Control."]))),
    ("01_EXECUTIVE_STRATEGY.md", "Executive Strategy", "The one-page strategic spine.", "العمود الاستراتيجي في صفحة واحدة.",
     s(("Mission", ["Give Saudi/GCC operators an AI revenue & ops OS they can trust."]),
       ("3 bets", ["Trust-first beats automation-first in GCC B2B.",
                   "Founder-led, review-only motion compounds a defensible asset in the repo.",
                   "Vertical depth (first 5 sectors) beats horizontal breadth early."]),
       ("Guardrails", ["Never send externally from the system.", "Never claim unproven ROI."]))),
    ("02_MARKET_THESIS.md", "Market Thesis", "Why this market, why this wedge.", "لماذا هذا السوق وهذه الزاوية.",
     s(("The problem", ["Revenue & ops work in GCC SMBs is manual, fragmented, and trust-sensitive."]),
       ("The wedge", ["Review-only AI draft factory + founder approval + delivery."]),
       ("First market", ["Saudi Arabia, then GCC.", "First 5 verticals: " + "; ".join(VERTICALS) + "."]))),
    ("03_BUSINESS_MODEL.md", "Business Model", "How Dealix makes money.", "كيف تحقق Dealix الإيراد.",
     s(("Offer ladder (SAR)", [f"**{n}** — {p}: {d}" for n, p, d in OFFER_LADDER]),
       ("Motion", ["Diagnostic → Pilot → Department OS / Retainer → Enterprise."]),
       ("Unit logic", ["Land with low-risk diagnostic; expand via proof; retain via delivery."]))),
    ("04_PRODUCT_OPERATING_MODEL.md", "Product Operating Model", "How product is built and shipped.", "كيف يُبنى المنتج ويُشحن.",
     s(("Modules", ["Lead Engine, Draft Factory, Founder Review Queue, Service Engine, Trust Engine, Commercial Dashboard, Delivery OS, Client Success OS, Analytics, Audit/Evidence Pack."]),
       ("Approval gates", ["Every external-facing artifact passes a founder approval gate."]))),
    ("05_REVENUE_OPERATING_MODEL.md", "Revenue Operating Model", "How revenue is generated and reviewed.", "كيف تتولد الإيرادات وتُراجَع.",
     s(("Pipeline", ["raw → researched → draft → founder review → manual contact → reply → discovery → diagnostic → pilot → retainer → expansion."]),
       ("Cadence", ["Daily founder review; weekly revenue review."]))),
    ("06_TRUST_OPERATING_MODEL.md", "Trust Operating Model", "How trust is engineered and proven.", "كيف تُهندَس الثقة وتُثبَت.",
     s(("Trust primitives", ["Human-in-the-loop, evidence packs, no blind automation, PDPL-aware data handling."]),
       ("Proof", ["Every claim is backed by an artifact or marked as a template/estimate."]))),
    ("07_COMPETITIVE_POSITIONING.md", "Competitive Positioning", "Where Dealix sits vs alternatives.", "موقع Dealix مقابل البدائل.",
     s(("vs CRM", ["CRM stores; Dealix drafts, scores, and prepares revenue actions for review."]),
       ("vs agencies / mass-senders", ["No spray-and-pray; trust-first, review-only."]))),
    ("08_FOUNDER_WEEKLY_CADENCE.md", "Founder Weekly Cadence", "The founder's operating week.", "أسبوع تشغيل المؤسس.",
     s(("Weekly rhythm", ["Mon: pipeline + drafts review.", "Wed: delivery + client success.", "Fri: metrics + decisions + risk."]),
       ("Daily", ["Review draft queue, approve manual sends, log decisions."]))),
    ("09_BOARD_STYLE_METRICS.md", "Board-Style Metrics", "What a board would track.", "ما يتابعه المجلس.",
     s(("North-star", ["Realized revenue (SAR) and qualified pipeline (SAR)."]),
       ("Leading", ["Drafts generated, founder-approved sends, positive replies, diagnostics sold."]))),
    ("10_RISK_REGISTER.md", "Company Risk Register", "Top company risks and mitigations.", "أهم مخاطر الشركة والتخفيف.",
     s(("Risks", ["Trust/compliance breach (high impact) — mitigate via review-only doctrine.",
                  "Over-promising ROI — mitigate via evidence-only claims.",
                  "Single-founder bandwidth — mitigate via sub-agent drafting + cadence."]))),
    ("11_DECISION_LOG.md", "Decision Log", "Append-only record of company decisions.", "سجل القرارات (إضافة فقط).",
     s(("Format", ["Date · Decision · Context · Owner · Reversible? · Outcome."]),
       ("Seed entry", ["2026-06-04 · Adopt V5 review-only company OS · Founder · reversible · in progress."]))),
    ("12_OPERATING_PRINCIPLES.md", "Operating Principles", "How we behave.", "كيف نتصرف.",
     s(("Principles", ["Trust over speed.", "Evidence over claims.", "Review before send.", "Small safe changes.", "Founder signs off."]))),
    ("13_90_DAY_COMPANY_ROADMAP.md", "90-Day Company Roadmap", "30/60/90 milestones.", "مسار 30/60/90 يوم.",
     s(("0–30", ["Launch site, run draft factory, founder review, first diagnostics."]),
       ("31–60", ["Convert diagnostics → pilots; publish proof; partner outreach (manual)."]),
       ("61–90", ["Retainers; expansion; investor readiness; hiring first roles."]))),
    ("14_COMPANY_SCORECARD.md", "Company Scorecard", "Single-screen company health.", "صحة الشركة في شاشة واحدة.",
     s(("Sections", ["Revenue · Pipeline · Delivery · Trust/Safety · Content · People."]),
       ("Rule", ["No fabricated numbers — manual inputs only until real data exists."]))),
], {"filename": "99_COMPANY_OS_REPORT.md", "files": ["`docs/company-os/*` (15 docs)"],
    "go": ["Company OS index ready; cadence and scorecard operable."],
    "nogo": ["Reporting fabricated metrics; external sending."]})


# ===== 3. Product OS =====
add("product-os", "Product OS", "نظام تشغيل المنتج", [
    ("00_PRODUCT_OS.md", "Product OS", "Master index for product.", "الفهرس الرئيسي للمنتج.",
     s(("Modules", ["Lead Engine, Draft Factory, Founder Review Queue, Service Engine, Trust Engine, Commercial Dashboard, Delivery OS, Client Success OS, Analytics, Audit/Evidence Pack."]),
       ("Boundaries", ["AI prepares; humans approve; system never sends."]))),
    ("01_PRODUCT_STRATEGY.md", "Product Strategy", "What we build and why.", "ماذا نبني ولماذا.",
     s(("Strategy", ["Depth in review-only revenue ops for the first 5 verticals."]))),
    ("02_PRODUCT_REQUIREMENTS.md", "Product Requirements", "Core PRD.", "متطلبات المنتج.",
     s(("Must", ["Draft factory ≥400/day, founder review queue, safety flags on every record."]),
       ("Must not", ["No external send endpoints, no auto-submit."]))),
    ("03_MODULE_MAP.md", "Module Map", "How modules connect.", "خريطة الوحدات.",
     s(("Flow", ["Leads → Draft Factory → Review Queue → (manual) Send → CRM → Delivery → Evidence."]))),
    ("04_USER_PERSONAS.md", "User Personas", "Who uses Dealix.", "من يستخدم Dealix.",
     s(("Personas", ["Founder/operator, delivery consultant, client admin, buyer (sector DM)."]))),
    ("05_JOBS_TO_BE_DONE.md", "Jobs To Be Done", "Outcomes customers hire us for.", "المهام المطلوبة.",
     s(("JTBD", ["Find qualified buyers, prepare trustworthy outreach, deliver proof, retain & expand."]))),
    ("06_PRODUCT_ROADMAP.md", "Product Roadmap", "MVP and later.", "خارطة المنتج.",
     s(("MVP", ["Draft Factory + Review Queue + Site + Analytics schema."]),
       ("Later", ["Service Engine depth, expansion automation (still review-gated)."]))),
    ("07_MVP_SCOPE.md", "MVP Scope", "What is in/out for MVP.", "نطاق الحد الأدنى.",
     s(("In", ["Review-only drafts, founder queue, vertical playbooks, site, analytics schema."]),
       ("Out", ["Any external auto-send, paid ads, scraping."]))),
    ("08_RELEASE_CRITERIA.md", "Release Criteria", "Gate to ship.", "معايير الإصدار.",
     s(("Gates", ["Verifiers PASS, tests green, safety audit clean, secret scan clean."]))),
    ("09_PRODUCT_RISK_REGISTER.md", "Product Risk Register", "Product risks.", "مخاطر المنتج.",
     s(("Risks", ["Draft quality drift — mitigate via evals; safety bypass — mitigate via tests."]))),
    ("10_PRODUCT_TELEMETRY.md", "Product Telemetry", "What we measure.", "ما نقيسه.",
     s(("Events", ["draft_generated, review_opened, approved_send, reply_logged. No PII beyond consent."]))),
    ("11_AI_FEATURE_BOUNDARIES.md", "AI Feature Boundaries", "What AI may and may not do.", "حدود ميزات الذكاء.",
     s(("May", ["Draft, score, rank, recommend, prepare."]),
       ("May not", ["Send, submit, scrape, launch paid ads, or act without founder approval."]))),
], {"filename": "99_PRODUCT_OS_REPORT.md", "files": ["`docs/product-os/*` (12 docs)"],
    "go": ["MVP scope and boundaries defined; release gates wired to verifiers."],
    "nogo": ["Shipping without verifier PASS."]})


# ===== 4. Engineering OS =====
add("engineering-os", "Engineering OS", "نظام تشغيل الهندسة", [
    ("00_ENGINEERING_OS.md", "Engineering OS", "Engineering operating index.", "فهرس تشغيل الهندسة.",
     s(("Stack", ["FastAPI backend, Next.js 15 web, pytest, GitHub Actions, Railway/Vercel deploy."]),
       ("Rule", ["No secret commits; no external sending from CI."]))),
    ("01_ARCHITECTURE_OVERVIEW.md", "Architecture Overview", "High-level architecture.", "نظرة عامة على المعمارية.",
     s(("Components", ["api/ (FastAPI), apps/web (Next.js), scripts/ (ops & verify), docs/ (OS)."]))),
    ("02_REPO_STRUCTURE.md", "Repo Structure", "Where things live.", "أين توجد الأشياء.",
     s(("Map", ["api/, apps/web/, dealix/, scripts/, tests/, docs/, config/, data/, outputs/."]))),
    ("03_LOCAL_DEVELOPMENT.md", "Local Development", "Terminal-first setup.", "إعداد محلي.",
     s(("Commands", ["`make setup`, `make run`, `make test`, `python scripts/startup_os_verify.py`."]))),
    ("04_CI_CD_POLICY.md", "CI/CD Policy", "What CI must enforce.", "سياسة CI/CD.",
     s(("Enforce", ["lint, type-check, tests, security-smoke, secret scan, V5 verifiers."]),
       ("Forbid", ["secrets in CI, external network sends, committing daily outputs."]))),
    ("05_TEST_STRATEGY.md", "Test Strategy", "How we test.", "استراتيجية الاختبار.",
     s(("Layers", ["unit, integration, regression; V5 adds safety/no-external-send tests."]))),
    ("06_RELEASE_PROCESS.md", "Release Process", "How we release.", "عملية الإصدار.",
     s(("Steps", ["green CI → verifiers PASS → evidence pack → PR → review → merge."]))),
    ("07_DEPLOYMENT_POLICY.md", "Deployment Policy", "How we deploy.", "سياسة النشر.",
     s(("Policy", ["Railway/Vercel; sandbox payments by default; no destructive migrations."]))),
    ("08_ROLLBACK_PROCESS.md", "Rollback Process", "How we revert.", "عملية التراجع.",
     s(("Steps", ["Revert PR, redeploy previous tag, verify smoke, log decision."]))),
    ("09_CODE_OWNERSHIP.md", "Code Ownership", "Who owns what.", "ملكية الكود.",
     s(("Owners", ["Founder owns all; sub-agents draft under review (see CODEOWNERS)."]))),
    ("10_TECH_DEBT_REGISTER.md", "Tech Debt Register", "Known debt.", "سجل الدين التقني.",
     s(("Debt", ["Duplicate legacy docs dirs (company_os/company); consolidate over time."]))),
], {"filename": "99_ENGINEERING_OS_REPORT.md", "files": ["`docs/engineering-os/*` (11 docs)"],
    "scripts": ["`scripts/startup_os_verify.py`", "`scripts/final_launch_control_verify.py`"],
    "go": ["Engineering policy documented; CI gates additive and non-destructive."],
    "nogo": ["Committing secrets; external sends from CI."]})


# ===== 6. Commercial Launch OS (index docs; verticals handled separately) =====
add("commercial-launch", "Commercial Launch OS", "نظام التدشين التجاري", [
    ("00_COMMERCIAL_LAUNCH_OS.md", "Commercial Launch OS", "Master commercial launch index.", "فهرس التدشين التجاري.",
     s(("Scope", ["First 5 verticals, offer ladder (SAR), channel policy, founder daily review, compliance gates."]),
       ("Rule", [NON_NEGOTIABLE]))),
    ("01_FIRST_5_VERTICALS_STRATEGY.md", "First 5 Verticals Strategy", "Why these five.", "لماذا هذه الخمسة.",
     s(("Verticals", VERTICALS), ("Why", ["High manual-ops pain, clear DMs, GCC density, proof-friendly."]))),
    ("02_OFFER_LADDER_SAR.md", "Offer Ladder (SAR)", "The five rungs.", "سلّم العروض بالريال.",
     s(("Ladder", [f"**{n}** — {p}: {d}" for n, p, d in OFFER_LADDER]))),
    ("03_PRICING_AND_PACKAGING.md", "Pricing & Packaging", "How offers are packaged.", "التسعير والتغليف.",
     s(("Packaging", ["Fixed-scope diagnostic, time-boxed pilot, monthly retainer, custom enterprise."]),
       ("Note", ["All SAR; no ROI guarantees; value framed as time/quality, evidence-backed."]))),
    ("04_POSITIONING_AR_EN.md", "Positioning (AR/EN)", "Bilingual positioning.", "التموضع بالعربية والإنجليزية.",
     s(("EN", ["The trust-first AI revenue & ops OS for Saudi/GCC B2B."]),
       ("AR", ["نظام تشغيل الإيرادات والعمليات المبني على الثقة للشركات السعودية والخليجية."]))),
    ("05_CHANNEL_POLICY.md", "Channel Policy", "Allowed vs forbidden channels.", "سياسة القنوات.",
     s(("Allowed", ["Manual founder outreach, warm intros, opt-in forms, founder-posted social."]),
       ("Forbidden", ["Cold automation, scraping, bulk send, LinkedIn automation, auto-submit."]))),
    ("06_FOUNDER_DAILY_REVIEW.md", "Founder Daily Review", "The daily review loop.", "المراجعة اليومية للمؤسس.",
     s(("Loop", ["Open draft queue → score-sort → approve/reject → export approved manual sends → log."]))),
    ("07_COMPLIANCE_AND_SAFETY_GATES.md", "Compliance & Safety Gates", "Gates before any send.", "بوابات الامتثال.",
     s(("Gates", ["opt-out present, no unverified claims, PDPL-aware, founder-approved, manual send only."]))),
    ("08_SALES_MESSAGING_AR_EN.md", "Sales Messaging (AR/EN)", "Approved message angles.", "رسائل البيع.",
     s(("Angles", ["Time saved, error reduction, trust, proof — never guaranteed ROI."]))),
    ("09_OBJECTION_HANDLING.md", "Objection Handling", "Common objections.", "معالجة الاعتراضات.",
     s(("Objections", ["'Is this spam?' → review-only, opt-in. 'ROI?' → evidence, not guarantees."]))),
    ("10_DISCOVERY_CALL_SCRIPT.md", "Discovery Call Script", "Discovery structure.", "نص مكالمة الاستكشاف.",
     s(("Structure", ["Context → pains → workflow → fit → diagnostic offer → next step."]))),
    ("11_PROPOSAL_TEMPLATE_AR_EN.md", "Proposal Template (AR/EN)", "Reusable proposal.", "قالب العرض.",
     s(("Sections", ["Problem, scope, deliverables, timeline, SAR price, acceptance, safety boundary."]))),
    ("12_ONE_PAGE_OFFER_AR_EN.md", "One-Page Offer (AR/EN)", "Single-page offer.", "عرض في صفحة.",
     s(("Content", ["Outcome, scope, price (SAR), proof, CTA — bilingual."]))),
    ("13_DELIVERY_OPERATING_SYSTEM.md", "Delivery Operating System", "How we deliver commercially.", "نظام التسليم.",
     s(("Per offer", ["inputs, outputs, timeline, acceptance, security boundary, handover, upsell."]))),
    ("14_CLIENT_ONBOARDING.md", "Client Onboarding", "First 14 days.", "إعداد العميل.",
     s(("Steps", ["Agreement → data boundary → kickoff → diagnostic → review → plan."]))),
    ("15_PILOT_DELIVERY_CHECKLIST.md", "Pilot Delivery Checklist", "Pilot QA.", "قائمة تسليم التجربة.",
     s(("Checklist", ["scope locked, data minimal, weekly review, evidence captured, handover ready."]))),
    ("16_HANDOVER_SUCCESS_REPORT.md", "Handover Success Report", "Closing a pilot.", "تقرير التسليم.",
     s(("Report", ["What was done, evidence, outcomes (measured/estimated labeled), next offer."]))),
    ("17_RETENTION_EXPANSION.md", "Retention & Expansion", "Grow accounts.", "الاحتفاظ والتوسع.",
     s(("Plays", ["QBR, health score, expand to new dept, retainer upgrade."]))),
    ("18_EXTERNAL_GO_LIVE_REQUIREMENTS.md", "External Go-Live Requirements", "What must be true to go live.", "متطلبات الإطلاق.",
     s(("Reqs", ["DNS/SPF/DKIM/DMARC, privacy+terms, suppression, booking, manual-ramp plan."]))),
    ("19_GTM_30_DAY_PLAN.md", "GTM 30-Day Plan", "First month motion.", "خطة 30 يوم.",
     s(("Weeks", ["W1 site+drafts, W2 manual outreach, W3 discovery, W4 diagnostics."]))),
    ("20_MANUAL_OUTREACH_RAMP.md", "Manual Outreach Ramp", "Safe ramp curve.", "تصعيد التواصل اليدوي.",
     s(("Ramp", ["Small daily volumes, warm-first, monitor replies/complaints, never bulk."]))),
    ("21_SUPPRESSION_PROCESS.md", "Suppression Process", "Honor opt-outs.", "عملية الاستبعاد.",
     s(("Process", ["Maintain suppression list; never contact suppressed; review before each send."]))),
    ("22_LEAD_INTAKE_AND_CRM_OS.md", "Lead Intake & CRM OS", "How leads enter.", "استقبال العملاء المحتملين.",
     s(("Intake", ["Opt-in forms + warm intros → validate → CRM schema → review queue."]))),
    ("23_LEAD_OPS_FINAL_QA.md", "Lead Ops Final QA", "QA before review.", "ضبط جودة العمليات.",
     s(("QA", ["fields valid, vertical tagged, suppression checked, safety flags set."]))),
], {"filename": "99_FINAL_COMMERCIAL_LAUNCH_REPORT.md",
    "files": ["`docs/commercial-launch/*` (24 docs)", "`docs/commercial-launch/verticals/*` (5 playbooks)"],
    "scripts": ["`scripts/commercial_generate_400_drafts.py`", "`scripts/commercial_safety_audit.py`",
                "`scripts/commercial_launch_readiness.py`", "`scripts/commercial_founder_review_report.py`"],
    "outputs": ["`outputs/commercial_launch/<date>/*`"],
    "go": ["Public commercial positioning, 400+ review-only drafts, founder manual review, paid diagnostics."],
    "nogo": ["Automated sending, bulk outreach, paid ads live without tracking/compliance."]})


# ===== 7. Sales OS =====
add("sales-os", "Sales OS", "نظام المبيعات", [
    ("00_SALES_OS.md", "Sales OS", "Sales operating index.", "فهرس المبيعات.",
     s(("Motion", ["Founder-led, review-only, evidence-based."]), ("Rule", [NON_NEGOTIABLE]))),
    ("01_SALES_PROCESS.md", "Sales Process", "End-to-end process.", "العملية البيعية.",
     s(("Stages", ["See pipeline stages doc."]))),
    ("02_PIPELINE_STAGES.md", "Pipeline Stages", "Canonical stages.", "مراحل خط الأنابيب.",
     s(("Stages", ["raw lead, researched, draft generated, founder review, manually contacted, replied positive, discovery booked, diagnostic proposed, diagnostic sold, pilot proposed, pilot sold, retainer, expansion, disqualified, suppressed."]))),
    ("03_DISCOVERY_CALL_SCRIPT_AR_EN.md", "Discovery Call Script (AR/EN)", "Bilingual script.", "نص الاستكشاف.",
     s(("Flow", ["Rapport → context → pains → fit → offer → next step."]))),
    ("04_QUALIFICATION_SCORECARD.md", "Qualification Scorecard", "Score fit.", "بطاقة التأهيل.",
     s(("Dimensions", ["Pain, budget, authority, timing, sector fit, trust signals."]))),
    ("05_PROPOSAL_PROCESS.md", "Proposal Process", "From fit to proposal.", "عملية العرض.",
     s(("Steps", ["Confirm scope → render proposal → founder review → manual send."]))),
    ("06_CLOSING_PLAYBOOK.md", "Closing Playbook", "How to close.", "دليل الإغلاق.",
     s(("Tactics", ["Low-risk diagnostic close; proof-led pilot close; never pressure."]))),
    ("07_FOLLOW_UP_SEQUENCE.md", "Follow-up Sequence", "Manual follow-ups.", "تسلسل المتابعة.",
     s(("Cadence", ["Spaced, value-add, manual, opt-out honored."]))),
    ("08_OBJECTION_LIBRARY.md", "Objection Library", "Reusable answers.", "مكتبة الاعتراضات.",
     s(("Library", ["Price, trust, timing, 'we do it manually', spam concern."]))),
    ("09_DEAL_DESK_RULES.md", "Deal Desk Rules", "Discount/scope rules.", "قواعد مكتب الصفقات.",
     s(("Rules", ["SAR floors per rung; scope creep guardrails; founder signs SOW."]))),
    ("10_SALES_DASHBOARD_SPEC.md", "Sales Dashboard Spec", "What to display.", "مواصفات لوحة المبيعات.",
     s(("Tiles", ["pipeline SAR, stage counts, win rate, approved sends, replies."]))),
    ("11_NEGOTIATION_RULES.md", "Negotiation Rules", "Boundaries.", "قواعد التفاوض.",
     s(("Rules", ["Protect value, avoid ROI guarantees, document concessions."]))),
    ("12_LOST_DEAL_REVIEW.md", "Lost Deal Review", "Learn from losses.", "مراجعة الصفقات الخاسرة.",
     s(("Review", ["Reason coded, lesson logged, follow-up scheduled if appropriate."]))),
], {"filename": "99_SALES_OS_REPORT.md", "files": ["`docs/sales-os/*` (13 docs)"],
    "go": ["Founder-led sales process and pipeline defined."],
    "nogo": ["Automated outreach or pressure tactics."]})


# ===== 8. Marketing OS =====
add("marketing-os", "Marketing OS", "نظام التسويق", [
    ("00_MARKETING_OS.md", "Marketing OS", "Marketing index.", "فهرس التسويق.",
     s(("Scope", ["GTM, ICP, messaging, channels, demand gen, content, proof."]), ("Rule", [NON_NEGOTIABLE]))),
    ("01_GTM_STRATEGY.md", "GTM Strategy", "Go-to-market.", "استراتيجية الدخول للسوق.",
     s(("Approach", ["Founder-led, vertical-first, proof-driven."]))),
    ("02_ICP_AND_SEGMENTATION.md", "ICP & Segmentation", "Who we target.", "العميل المثالي.",
     s(("ICP", ["GCC SMB/mid operators in the first 5 verticals with manual ops pain."]))),
    ("03_MESSAGING_HIERARCHY.md", "Messaging Hierarchy", "Message stack.", "هرم الرسائل.",
     s(("Stack", ["Promise → proof → mechanism → offer → CTA."]))),
    ("04_CHANNEL_STRATEGY.md", "Channel Strategy", "Where we show up.", "استراتيجية القنوات.",
     s(("Channels", ["Founder LinkedIn (manual), site/SEO, warm intros, partnerships."]))),
    ("05_DEMAND_GEN_PLAN.md", "Demand Gen Plan", "Generate demand.", "توليد الطلب.",
     s(("Plays", ["Founder content, sector insights, opt-in lead magnets."]))),
    ("06_CONTENT_ENGINE.md", "Content Engine", "How content is produced.", "محرك المحتوى.",
     s(("Engine", ["Draft (AI) → founder edit → manual post → measure."]))),
    ("07_LAUNCH_CAMPAIGN.md", "Launch Campaign", "Launch plan.", "حملة الإطلاق.",
     s(("Plan", ["Announce site, share thesis, sector proof, invite diagnostics."]))),
    ("08_REFERRAL_LOOP.md", "Referral Loop", "Word of mouth.", "حلقة الإحالة.",
     s(("Loop", ["Deliver proof → ask for intro → reward partners (manual)."]))),
    ("09_PARTNER_CHANNELS.md", "Partner Channels", "Partner-led demand.", "قنوات الشركاء.",
     s(("Partners", ["Agencies, consultants, ERP/CRM implementers."]))),
    ("10_MARKETING_METRICS.md", "Marketing Metrics", "What we track.", "مقاييس التسويق.",
     s(("Metrics", ["visitors, CTA clicks, audit requests, leads — manual until real data."]))),
    ("11_CASE_STUDY_ENGINE.md", "Case Study Engine", "Turn delivery into proof.", "محرك دراسات الحالة.",
     s(("Process", ["Capture evidence → draft → client approval → publish."]))),
    ("12_PROOF_ASSET_LIBRARY.md", "Proof Asset Library", "Reusable proof.", "مكتبة الأدلة.",
     s(("Assets", ["Anonymized outcomes, evidence packs, testimonials (with consent)."]))),
], {"filename": "99_MARKETING_OS_REPORT.md", "files": ["`docs/marketing-os/*` (13 docs)"],
    "go": ["Marketing strategy and content engine defined (manual posting)."],
    "nogo": ["Auto-posting, unverified claims."]})


# ===== 9. Media & Social OS =====
add("media-social-os", "Media & Social OS", "نظام الإعلام والسوشيال", [
    ("00_MEDIA_SOCIAL_OS.md", "Media & Social OS", "Media index.", "فهرس الإعلام.",
     s(("Scope", ["Brand voice, pillars, calendar, per-platform OS, ads readiness, PR."]),
       ("Forbidden", ["auto-post, platform API posting, secrets, live paid ads."]))),
    ("01_BRAND_VOICE.md", "Brand Voice", "How we sound.", "صوت العلامة.",
     s(("Voice", ["Trustworthy, precise, bilingual, evidence-led, never hypey."]))),
    ("02_CONTENT_PILLARS.md", "Content Pillars", "What we talk about.", "ركائز المحتوى.",
     s(("Pillars", ["Trust/AI safety, sector ops insight, proof/case, founder POV."]))),
    ("03_30_DAY_CONTENT_CALENDAR.md", "30-Day Content Calendar", "Calendar overview.", "تقويم 30 يوم.",
     s(("Source", ["Generated to `config/media_social_calendar.json` via `media_social_calendar_generate.py`."]))),
    ("04_LINKEDIN_OS.md", "LinkedIn OS", "Manual LinkedIn.", "نظام لينكدإن.",
     s(("Rule", ["Founder posts manually; no automation, no scraping, no auto-connect."]))),
    ("05_X_TWITTER_OS.md", "X/Twitter OS", "Manual X.", "نظام إكس.", s(("Rule", ["Manual posting only."]))),
    ("06_INSTAGRAM_OS.md", "Instagram OS", "Manual IG.", "نظام إنستغرام.", s(("Rule", ["Manual posting only."]))),
    ("07_TIKTOK_SHORTS_OS.md", "TikTok Shorts OS", "Manual TikTok.", "نظام تيك توك.", s(("Rule", ["Manual posting only."]))),
    ("08_YOUTUBE_SHORTS_OS.md", "YouTube Shorts OS", "Manual YouTube.", "نظام يوتيوب.", s(("Rule", ["Manual posting only."]))),
    ("09_PRESS_KIT.md", "Press Kit", "Media assets.", "حقيبة صحفية.",
     s(("Kit", ["Boilerplate, founder bio, logo usage, factual claims only."]))),
    ("10_ADS_OS.md", "Ads OS (overview)", "Ads planning only.", "الإعلانات (تخطيط فقط).",
     s(("Note", ["Planning only — see `docs/ads-os/`. No live launch."]))),
    ("11_CREATIVE_BRIEF_LIBRARY.md", "Creative Brief Library", "Briefs.", "مكتبة الموجزات.",
     s(("Briefs", ["Hook, message, proof, CTA, channel, language."]))),
    ("12_FOUNDER_PERSONAL_BRAND.md", "Founder Personal Brand", "Founder presence.", "العلامة الشخصية.",
     s(("Plan", ["Consistent POV, sector authority, manual cadence."]))),
    ("13_DAILY_MEDIA_ROUTINE.md", "Daily Media Routine", "Daily habit.", "روتين يومي.",
     s(("Routine", ["Draft → edit → post manually → engage → log."]))),
    ("14_SOCIAL_METRICS.md", "Social Metrics", "What we track.", "مقاييس السوشيال.",
     s(("Metrics", ["reach, engagement, profile visits, inbound — manual inputs."]))),
    ("15_ADS_READINESS_GATE.md", "Ads Readiness Gate", "Gate before any ad.", "بوابة جاهزية الإعلانات.",
     s(("Gate", ["tracking, legal, budget approval — all required before live."]))),
    ("16_PR_AND_MEDIA_RELATIONS.md", "PR & Media Relations", "Press approach.", "العلاقات الإعلامية.",
     s(("Approach", ["Factual story, sector angle, no inflated claims."]))),
    ("17_COMMUNITY_STRATEGY.md", "Community Strategy", "Build community.", "استراتيجية المجتمع.",
     s(("Plan", ["Sector operators community, value-first, opt-in."]))),
], {"filename": "99_MEDIA_SOCIAL_READY_REPORT.md",
    "files": ["`docs/media-social-os/*` (18 docs)", "`config/media_social_calendar.json`", "`config/ad_campaigns_seed.json`"],
    "scripts": ["`scripts/media_social_calendar_generate.py`", "`scripts/media_social_verify.py`", "`scripts/media_social_metrics_template.py`"],
    "tests": ["`tests/test_media_social_os.py`"],
    "go": ["Calendar + briefs ready for manual posting."],
    "nogo": ["Auto-post or platform API posting; live paid ads."]})


# ===== 10. Ads OS =====
add("ads-os", "Ads OS", "نظام الإعلانات", [
    ("00_ADS_OS.md", "Ads OS", "Ads planning index.", "فهرس تخطيط الإعلانات.",
     s(("Rule", ["Planning only. No live launch, no API, no secrets, no unverified claims."]))),
    ("01_ADS_READINESS_GATE.md", "Ads Readiness Gate", "Pre-launch gate.", "بوابة الجاهزية.",
     s(("Gate", ["tracking + legal + budget approval before any spend."]))),
    ("02_GOOGLE_SEARCH_PLAN.md", "Google Search Plan", "Search ads plan.", "خطة بحث جوجل.",
     s(("Plan", ["Intent keywords per vertical, landing mapping, conservative budgets."]))),
    ("03_LINKEDIN_ADS_PLAN.md", "LinkedIn Ads Plan", "LinkedIn plan.", "خطة لينكدإن.",
     s(("Plan", ["DM-title targeting, sector messaging — draft only."]))),
    ("04_META_ADS_PLAN.md", "Meta Ads Plan", "Meta plan.", "خطة ميتا.", s(("Plan", ["Awareness/retargeting concepts — draft only."]))),
    ("05_UTM_TAXONOMY.md", "UTM Taxonomy", "Tracking scheme.", "تصنيف UTM.",
     s(("Scheme", ["utm_source/medium/campaign/content per channel — consistent naming."]))),
    ("06_CREATIVE_TEST_PLAN.md", "Creative Test Plan", "How to test.", "خطة اختبار الإبداع.",
     s(("Plan", ["Hypothesis, variants, success metric — planning only."]))),
    ("07_ADS_COMPLIANCE_CHECKLIST.md", "Ads Compliance Checklist", "Stay compliant.", "قائمة الامتثال.",
     s(("Checklist", ["no false claims, clear disclosure, PDPL-aware data, opt-out."]))),
    ("08_LANDING_PAGE_MAPPING.md", "Landing Page Mapping", "Ad → page.", "ربط الصفحات.",
     s(("Mapping", ["Each campaign maps to a vertical landing page."]))),
    ("09_BUDGET_SCENARIOS.md", "Budget Scenarios", "Spend scenarios.", "سيناريوهات الميزانية.",
     s(("Scenarios", ["Low/Med/High — illustrative SAR, no commitment."]))),
], {"filename": "99_ADS_OS_REPORT.md", "files": ["`docs/ads-os/*` (10 docs)"],
    "go": ["Ads fully planned and gated."],
    "nogo": ["Any live paid ad before tracking/legal/budget approval."]})


# ===== 12. RevOps / CRM OS =====
add("revops-os", "RevOps / CRM OS", "نظام عمليات الإيراد", [
    ("00_REVOPS_OS.md", "RevOps / CRM OS", "RevOps index.", "فهرس عمليات الإيراد.",
     s(("Scope", ["CRM schema, intake, suppression, reply classification, metrics, forecasting."]),
       ("Rule", ["No CRM push-send."]))),
    ("01_CRM_PIPELINE_SCHEMA.md", "CRM Pipeline Schema", "Schema overview.", "مخطط خط الأنابيب.",
     s(("Source", ["`config/crm_pipeline_schema.json` (verified by `commercial_crm_schema_verify.py`)."]))),
    ("02_LEAD_INTAKE_PROCESS.md", "Lead Intake Process", "How leads enter.", "عملية الاستقبال.",
     s(("Process", ["opt-in/warm → validate → schema → review queue."]))),
    ("03_SUPPRESSION_PROCESS.md", "Suppression Process", "Honor opt-outs.", "عملية الاستبعاد.",
     s(("Process", ["maintain list, check before send, never contact suppressed."]))),
    ("04_REPLY_CLASSIFICATION.md", "Reply Classification", "Triage replies.", "تصنيف الردود.",
     s(("Classes", ["positive, neutral, negative, opt-out, OOO — manual tagging."]))),
    ("05_PIPELINE_METRICS.md", "Pipeline Metrics", "Pipeline health.", "مقاييس خط الأنابيب.",
     s(("Metrics", ["stage counts, conversion, velocity, SAR — manual inputs."]))),
    ("06_FORECASTING_MODEL.md", "Forecasting Model", "Forecast revenue.", "نموذج التنبؤ.",
     s(("Model", ["weighted pipeline by stage; conservative; no guarantees."]))),
    ("07_REVENUE_REVIEW_CADENCE.md", "Revenue Review Cadence", "Weekly review.", "إيقاع مراجعة الإيراد.",
     s(("Cadence", ["weekly pipeline + drafts + delivery review."]))),
    ("08_REVENUE_QUALITY_CONTROL.md", "Revenue Quality Control", "Keep data clean.", "ضبط جودة الإيراد.",
     s(("QC", ["dedupe, validate, suppression-respect, safety flags."]))),
], {"filename": "99_REVOPS_OS_REPORT.md", "files": ["`docs/revops-os/*` (9 docs)", "`config/crm_pipeline_schema.json`", "`data/commercial_seed_leads.example.jsonl`"],
    "scripts": ["`scripts/commercial_lead_intake_validate.py`", "`scripts/commercial_crm_schema_verify.py`"],
    "tests": ["`tests/test_crm_schema_verify.py`"],
    "go": ["CRM schema and intake validated; review-only."],
    "nogo": ["CRM push-send; contacting suppressed leads."]})


# ===== 13. Delivery OS =====
add("delivery-os", "Delivery OS", "نظام التسليم", [
    ("00_DELIVERY_OS.md", "Delivery OS", "Delivery index.", "فهرس التسليم.",
     s(("Per offer", ["inputs, outputs, timeline, acceptance, security boundary, approval boundary, handover, upsell, support, SLA, retention, expansion."]))),
    ("01_DIAGNOSTIC_DELIVERY.md", "Diagnostic Delivery", "Deliver the audit.", "تسليم التشخيص.",
     s(("Flow", ["intake → review workflow → findings → prioritized fixes → readout."]))),
    ("02_PILOT_DELIVERY.md", "Pilot Delivery", "Deliver the pilot.", "تسليم التجربة.",
     s(("Flow", ["scope lock → build (review-only) → weekly review → evidence → handover."]))),
    ("03_DEPARTMENT_OS_DELIVERY.md", "Department OS Delivery", "Deliver a dept OS.", "تسليم نظام القسم.",
     s(("Flow", ["map workflows → design OS → phased rollout → adoption → measure."]))),
    ("04_RETAINER_OPERATIONS.md", "Retainer Operations", "Run retainers.", "تشغيل الاشتراك.",
     s(("Ops", ["monthly plan, draft+review cadence, reporting, QBR."]))),
    ("05_CLIENT_SUCCESS_REPORTING.md", "Client Success Reporting", "Show value.", "تقارير نجاح العميل.",
     s(("Reports", ["outcomes (measured/estimated labeled), evidence, next steps."]))),
    ("06_HANDOVER_TEMPLATE.md", "Handover Template", "Close cleanly.", "قالب التسليم.",
     s(("Template", ["deliverables, evidence, access, training, support plan."]))),
    ("07_EXPANSION_PLAYBOOK.md", "Expansion Playbook", "Grow accounts.", "دليل التوسع.",
     s(("Plays", ["new dept, deeper workflows, retainer upgrade."]))),
    ("08_SUPPORT_PROCESS.md", "Support Process", "Support clients.", "عملية الدعم.",
     s(("Process", ["channels, triage, SLA, escalation."]))),
    ("09_SLA_AND_ESCALATION.md", "SLA & Escalation", "Response commitments.", "اتفاقية مستوى الخدمة.",
     s(("SLA", ["tiered response, escalation path, incident handling."]))),
    ("10_DELIVERY_QA_GATE.md", "Delivery QA Gate", "Quality before handover.", "بوابة جودة التسليم.",
     s(("Gate", ["acceptance met, evidence captured, client sign-off."]))),
], {"filename": "99_DELIVERY_READINESS_REPORT.md", "files": ["`docs/delivery-os/*` (11 docs)"],
    "go": ["Delivery playbooks ready per offer."],
    "nogo": ["Processing sensitive data before agreement."]})


# ===== 14. Support OS =====
add("support-os", "Support OS", "نظام الدعم", [
    ("00_SUPPORT_OS.md", "Support OS", "Support index.", "فهرس الدعم.",
     s(("Scope", ["channels, triage, incidents, KB, feedback, health, churn."]))),
    ("01_SUPPORT_CHANNELS.md", "Support Channels", "Where we help.", "قنوات الدعم.",
     s(("Channels", ["email/ticket (manual), scheduled calls — opt-in only."]))),
    ("02_TICKET_TRIAGE.md", "Ticket Triage", "Prioritize.", "فرز التذاكر.",
     s(("Triage", ["severity, impact, SLA mapping."]))),
    ("03_INCIDENT_RESPONSE.md", "Incident Response", "Handle incidents.", "الاستجابة للحوادث.",
     s(("Steps", ["detect, contain, communicate, resolve, post-mortem."]))),
    ("04_KNOWLEDGE_BASE.md", "Knowledge Base", "Self-serve help.", "قاعدة المعرفة.",
     s(("KB", ["FAQs, how-tos, safety boundaries."]))),
    ("05_CUSTOMER_FEEDBACK_LOOP.md", "Customer Feedback Loop", "Listen & improve.", "حلقة التغذية الراجعة.",
     s(("Loop", ["capture → categorize → roadmap → close loop."]))),
    ("06_HEALTH_SCORE.md", "Health Score", "Account health.", "مؤشر الصحة.",
     s(("Score", ["usage, outcomes, engagement, sentiment."]))),
    ("07_CHURN_RISK_PLAYBOOK.md", "Churn Risk Playbook", "Save accounts.", "دليل مخاطر الفقد.",
     s(("Plays", ["early signals, intervention, value re-prove."]))),
], {"filename": "99_SUPPORT_OS_REPORT.md", "files": ["`docs/support-os/*` (8 docs)"],
    "go": ["Support process defined."], "nogo": ["Unsolicited outreach."]})


# ===== 15. Finance OS =====
add("finance-os", "Finance OS", "النظام المالي", [
    ("00_FINANCE_OS.md", "Finance OS", "Finance index (templates only).", "فهرس المالية (قوالب فقط).",
     s(("Note", ["Templates and manual inputs only. No assumed real revenue. All SAR."]))),
    ("01_PRICING_MODEL.md", "Pricing Model", "How we price.", "نموذج التسعير.",
     s(("Model", ["Offer ladder SAR; value-based; no ROI guarantees."]))),
    ("02_UNIT_ECONOMICS.md", "Unit Economics", "Per-deal economics.", "اقتصاديات الوحدة.",
     s(("Template", ["CAC (manual), delivery cost, margin — inputs to fill."]))),
    ("03_CASHFLOW_MODEL.md", "Cashflow Model", "Cash in/out.", "نموذج التدفق النقدي.",
     s(("Template", ["monthly inflow/outflow, runway — manual."]))),
    ("04_REVENUE_FORECAST.md", "Revenue Forecast", "Forecast SAR.", "توقع الإيراد.",
     s(("Template", ["weighted pipeline; conservative; labeled estimates."]))),
    ("05_EXPENSE_POLICY.md", "Expense Policy", "Spend rules.", "سياسة المصروفات.",
     s(("Policy", ["approval thresholds, categories, receipts."]))),
    ("06_INVOICING_AND_COLLECTIONS.md", "Invoicing & Collections", "Get paid.", "الفوترة والتحصيل.",
     s(("Process", ["ZATCA-aware invoice (existing tooling), terms, follow-up."]))),
    ("07_MONTHLY_FINANCE_REVIEW.md", "Monthly Finance Review", "Monthly close.", "المراجعة الشهرية.",
     s(("Review", ["actuals vs plan, runway, decisions."]))),
    ("08_BUDGET_CONTROL.md", "Budget Control", "Stay in budget.", "ضبط الميزانية.",
     s(("Control", ["caps per area, approval gates."]))),
    ("09_PRICING_EXPERIMENTS.md", "Pricing Experiments", "Test pricing.", "تجارب التسعير.",
     s(("Experiments", ["hypothesis, control, measure — no manipulation."]))),
], {"filename": "99_FINANCE_OS_REPORT.md", "files": ["`docs/finance-os/*` (10 docs)"],
    "go": ["Finance templates ready (manual inputs)."],
    "nogo": ["Assuming/reporting fabricated revenue."]})


# ===== 16. Legal / Compliance OS =====
add("legal-os", "Legal / Compliance OS", "النظام القانوني والامتثال", [
    ("00_LEGAL_OS.md", "Legal / Compliance OS", "Legal index (templates only).", "فهرس قانوني (قوالب فقط).",
     s(("Disclaimer", ["Templates only — NOT legal advice. Require qualified legal review before formal use."]))),
    ("01_TERMS_TEMPLATE.md", "Terms Template", "Website/service terms.", "قالب الشروط.",
     s(("Template", ["scope, acceptable use, liability, governing law — review required."]))),
    ("02_PRIVACY_POLICY_TEMPLATE.md", "Privacy Policy Template", "Privacy.", "قالب الخصوصية.",
     s(("Template", ["data collected, purpose, retention, rights — PDPL-aware."]))),
    ("03_DPA_TEMPLATE.md", "DPA Template", "Data processing.", "قالب معالجة البيانات.",
     s(("Template", ["roles, security, sub-processors, breach — review required."]))),
    ("04_MSA_TEMPLATE.md", "MSA Template", "Master services.", "قالب الاتفاقية الرئيسية.",
     s(("Template", ["services, fees (SAR), IP, term, termination."]))),
    ("05_SOW_TEMPLATE.md", "SOW Template", "Statement of work.", "قالب نطاق العمل.",
     s(("Template", ["deliverables, timeline, acceptance, price (SAR)."]))),
    ("06_DATA_RETENTION_POLICY.md", "Data Retention Policy", "Retention rules.", "سياسة الاحتفاظ.",
     s(("Policy", ["minimize, retention periods, deletion."]))),
    ("07_MARKETING_COMPLIANCE.md", "Marketing Compliance", "Outreach rules.", "امتثال التسويق.",
     s(("Rules", ["opt-in/consent, opt-out, no false claims, platform ToS respected."]))),
    ("08_PDPL_OPERATING_NOTES.md", "PDPL Operating Notes", "Saudi PDPL notes.", "ملاحظات نظام حماية البيانات.",
     s(("Notes", ["lawful basis, data subject rights, cross-border care — review required."]))),
    ("09_CONTRACT_REVIEW_CHECKLIST.md", "Contract Review Checklist", "Before signing.", "قائمة مراجعة العقود.",
     s(("Checklist", ["scope, liability, data, payment, termination."]))),
    ("10_VENDOR_LEGAL_CHECKLIST.md", "Vendor Legal Checklist", "Vet vendors.", "قائمة الموردين.",
     s(("Checklist", ["DPA, security, ToS, data location."]))),
], {"filename": "99_LEGAL_OS_REPORT.md", "files": ["`docs/legal-os/*` (11 docs)"],
    "go": ["Legal templates available for legal review."],
    "nogo": ["Using templates as legal advice without qualified review."]})


# ===== 17. Security / Trust OS =====
add("security-os", "Security / Trust OS", "نظام الأمن والثقة", [
    ("00_SECURITY_TRUST_OS.md", "Security / Trust OS", "Security index.", "فهرس الأمن.",
     s(("Frameworks", ["NIST CSF 2.0, OWASP Top 10, OWASP ASVS."]),
       ("Rule", ["No secrets in repo; secret scan gates the build."]))),
    ("01_SECURITY_BASELINE.md", "Security Baseline", "Minimum bar.", "خط الأساس الأمني.",
     s(("Baseline", ["secret hygiene, least privilege, dependency scanning, CI checks."]))),
    ("02_NIST_CSF_MAPPING.md", "NIST CSF Mapping", "Map to CSF 2.0.", "ربط NIST CSF.",
     s(("Functions", ["Govern, Identify, Protect, Detect, Respond, Recover — mapped to controls."]))),
    ("03_OWASP_TOP_10_MAPPING.md", "OWASP Top 10 Mapping", "Web risks.", "ربط OWASP Top 10.",
     s(("Mapping", ["A01–A10 → controls in api/ and apps/web."]))),
    ("04_ASVS_CHECKLIST.md", "ASVS Checklist", "Verification standard.", "قائمة ASVS.",
     s(("Checklist", ["auth, session, access control, validation, logging."]))),
    ("05_SECRET_MANAGEMENT.md", "Secret Management", "Handle secrets.", "إدارة الأسرار.",
     s(("Rules", ["env/.env.example only; never commit real secrets; gitleaks + V5 scan."]))),
    ("06_ACCESS_CONTROL.md", "Access Control", "Who can do what.", "التحكم بالوصول.",
     s(("Model", ["least privilege, role-based, audited."]))),
    ("07_INCIDENT_RESPONSE.md", "Incident Response", "Security incidents.", "الاستجابة للحوادث الأمنية.",
     s(("Plan", ["detect, contain, eradicate, recover, learn."]))),
    ("08_VENDOR_RISK.md", "Vendor Risk", "Third-party risk.", "مخاطر الموردين.",
     s(("Assess", ["data access, security posture, DPA."]))),
    ("09_SECURITY_EVIDENCE_PACK.md", "Security Evidence Pack", "Prove security.", "حزمة أدلة الأمن.",
     s(("Pack", ["scan results, control mappings, policy docs."]))),
    ("10_PRODUCTION_SECURITY_GATE.md", "Production Security Gate", "Gate to prod.", "بوابة أمن الإنتاج.",
     s(("Gate", ["secret scan clean, deps clean, no external send paths added."]))),
], {"filename": "99_SECURITY_TRUST_REPORT.md", "files": ["`docs/security-os/*` (11 docs)"],
    "scripts": ["`scripts/final_secret_and_risk_scan.py`"], "tests": ["`tests/test_final_secret_and_risk_scan.py`"],
    "go": ["Security baseline and secret scan operational. Note: README/SECURITY VoXc2 org links flagged for a follow-up security PR."],
    "nogo": ["Committing secrets; adding external send endpoints."]})


# ===== 18. Analytics OS =====
add("analytics-os", "Data / Analytics OS", "نظام البيانات والتحليلات", [
    ("00_ANALYTICS_OS.md", "Data / Analytics OS", "Analytics index.", "فهرس التحليلات.",
     s(("Rule", ["No fabricated numbers — schema + manual inputs only."]),
       ("Source", ["`config/analytics_events.json`."]))),
    ("01_EVENT_TAXONOMY.md", "Event Taxonomy", "Named events.", "تصنيف الأحداث.",
     s(("Events", ["website_visit, cta_click, audit_request, lead_created, draft_generated, founder_review, manual_send, reply, positive_reply, diagnostic_booked, diagnostic_paid, pilot_proposed, pilot_sold, retainer_start, pipeline_sar, realized_revenue_sar, safety_violation, compliance_rejection."]))),
    ("02_DASHBOARD_SPEC.md", "Dashboard Spec", "What to show.", "مواصفات اللوحة.",
     s(("Tiles", ["funnel, pipeline SAR, drafts/review, safety, content."]))),
    ("03_WEEKLY_REPORT_TEMPLATE.md", "Weekly Report Template", "Weekly snapshot.", "تقرير أسبوعي.",
     s(("Sections", ["revenue, pipeline, delivery, content, safety."]))),
    ("04_MONTHLY_BOARD_REPORT.md", "Monthly Board Report", "Board view.", "تقرير المجلس الشهري.",
     s(("Sections", ["north-star, leading indicators, risks, decisions."]))),
    ("05_DATA_QUALITY_RULES.md", "Data Quality Rules", "Keep data clean.", "قواعد جودة البيانات.",
     s(("Rules", ["validation, dedupe, consent, labeled estimates."]))),
    ("06_METRIC_DEFINITIONS.md", "Metric Definitions", "Define every metric.", "تعريفات المقاييس.",
     s(("Defs", ["each event/metric with formula and source."]))),
], {"filename": "99_ANALYTICS_READY_REPORT.md", "files": ["`docs/analytics-os/*` (7 docs)", "`config/analytics_events.json`"],
    "go": ["Event taxonomy and report templates ready."],
    "nogo": ["Reporting fabricated numbers."]})


# ===== 19. AI Evals OS =====
add("ai-evals-os", "AI Quality / Evals OS", "نظام جودة الذكاء والتقييم", [
    ("00_AI_EVALS_OS.md", "AI Quality / Evals OS", "Evals index.", "فهرس التقييم.",
     s(("Scope", ["draft quality, compliance, sector relevance, AR/EN quality, regression."]),
       ("Source", ["`config/ai_eval_rubrics.json`."]))),
    ("01_DRAFT_QUALITY_RUBRIC.md", "Draft Quality Rubric", "Score drafts.", "معايير جودة المسودة.",
     s(("Dimensions", ["clarity, relevance, personalization, CTA, compliance, no-claims."]))),
    ("02_COMPLIANCE_EVALS.md", "Compliance Evals", "Safety/compliance checks.", "تقييم الامتثال.",
     s(("Checks", ["opt-out present, no unverified claims, PDPL-aware, no banned tactics."]))),
    ("03_SECTOR_RELEVANCE_EVALS.md", "Sector Relevance Evals", "Sector fit.", "تقييم ملاءمة القطاع.",
     s(("Checks", ["correct vertical pains, persona fit, trigger relevance."]))),
    ("04_ARABIC_QUALITY_EVALS.md", "Arabic Quality Evals", "AR quality.", "تقييم جودة العربية.",
     s(("Checks", ["grammar, tone, dialect-appropriateness, clarity."]))),
    ("05_ENGLISH_QUALITY_EVALS.md", "English Quality Evals", "EN quality.", "تقييم جودة الإنجليزية.",
     s(("Checks", ["grammar, tone, concision, clarity."]))),
    ("06_REGRESSION_EVAL_PROCESS.md", "Regression Eval Process", "Prevent drift.", "عملية اختبار الانحدار.",
     s(("Process", ["golden set, rubric scoring, threshold gating."]))),
], {"filename": "99_AI_EVALS_REPORT.md", "files": ["`docs/ai-evals-os/*` (7 docs)", "`config/ai_eval_rubrics.json`"],
    "scripts": ["`scripts/ai_eval_sample_drafts.py`"], "tests": ["`tests/test_ai_eval_rubrics.py`"],
    "go": ["Rubrics defined; sample eval runs over generated drafts."],
    "nogo": ["Shipping drafts that fail compliance evals."]})


# ===== 20. People OS =====
add("people-os", "People / Hiring OS", "نظام الأفراد والتوظيف", [
    ("00_PEOPLE_OS.md", "People / Hiring OS", "People index.", "فهرس الأفراد.",
     s(("Scope", ["first hires, scorecards, contractors, interviews, onboarding, performance, comp."]))),
    ("01_FIRST_HIRES_PLAN.md", "First Hires Plan", "Who to hire first.", "خطة أول التعيينات.",
     s(("Roles", ["Founder assistant/ops, full-stack engineer, growth operator, delivery consultant, designer/content editor, compliance advisor (contractor), SDR (contractor)."]))),
    ("02_ROLE_SCORECARDS.md", "Role Scorecards", "Define success per role.", "بطاقات الأدوار.",
     s(("Format", ["mission, outcomes, competencies."]))),
    ("03_CONTRACTOR_PLAYBOOK.md", "Contractor Playbook", "Work with contractors.", "دليل المتعاقدين.",
     s(("Playbook", ["scope, IP, NDA, payment, review."]))),
    ("04_INTERVIEW_PROCESS.md", "Interview Process", "Hire well.", "عملية المقابلات.",
     s(("Stages", ["screen, skills, values, references."]))),
    ("05_ONBOARDING_PROCESS.md", "Onboarding Process", "Ramp new people.", "عملية الإعداد.",
     s(("Steps", ["access (least privilege), doctrine, tools, first wins."]))),
    ("06_PERFORMANCE_CADENCE.md", "Performance Cadence", "Keep aligned.", "إيقاع الأداء.",
     s(("Cadence", ["weekly 1:1, monthly review, quarterly goals."]))),
    ("07_COMPENSATION_GUIDELINES.md", "Compensation Guidelines", "Pay fairly.", "إرشادات التعويض.",
     s(("Guidelines", ["bands (SAR), equity ranges, contractor rates — illustrative."]))),
], {"filename": "99_PEOPLE_OS_REPORT.md", "files": ["`docs/people-os/*` (8 docs)"],
    "go": ["Hiring plan and scorecards ready."], "nogo": ["Granting excess access."]})


# ===== 21. Partnerships OS =====
add("partnerships-os", "Partnerships OS", "نظام الشراكات", [
    ("00_PARTNERSHIPS_OS.md", "Partnerships OS", "Partnerships index.", "فهرس الشراكات.",
     s(("Types", ["agencies, consultants, IT providers, ERP/CRM implementers, sector experts, legal/compliance advisors, training companies."]))),
    ("01_PARTNER_TYPES.md", "Partner Types", "Who we partner with.", "أنواع الشركاء.",
     s(("Types", ["referral, delivery, tech, sector."]))),
    ("02_AGENCY_PARTNER_PLAYBOOK.md", "Agency Partner Playbook", "Work with agencies.", "دليل شراكة الوكالات.",
     s(("Playbook", ["enablement, co-delivery, referral terms."]))),
    ("03_TECH_PARTNER_PLAYBOOK.md", "Tech Partner Playbook", "Tech integrations.", "دليل الشركاء التقنيين.",
     s(("Playbook", ["integration scope, data boundaries, support."]))),
    ("04_REFERRAL_PROGRAM.md", "Referral Program", "Reward intros.", "برنامج الإحالة.",
     s(("Program", ["terms, tracking (manual), payout."]))),
    ("05_PARTNER_ENABLEMENT_KIT.md", "Partner Enablement Kit", "Equip partners.", "حقيبة تمكين الشركاء.",
     s(("Kit", ["one-pager, deck, proof, FAQs."]))),
    ("06_PARTNER_SCORECARD.md", "Partner Scorecard", "Measure partners.", "بطاقة الشركاء.",
     s(("Metrics", ["referrals, conversions, delivery quality."]))),
], {"filename": "99_PARTNERSHIPS_OS_REPORT.md", "files": ["`docs/partnerships-os/*` (7 docs)"],
    "go": ["Partner playbooks and enablement kit ready."], "nogo": ["Sharing client data without DPA."]})


# ===== 22. Investor OS =====
add("investor-os", "Investor / Data Room OS", "نظام المستثمرين وغرفة البيانات", [
    ("00_INVESTOR_OS.md", "Investor / Data Room OS", "Investor index (readiness only).", "فهرس المستثمرين (جاهزية فقط).",
     s(("Rule", ["No unproven traction claims. Readiness documentation only."]))),
    ("01_INVESTOR_NARRATIVE.md", "Investor Narrative", "The story.", "السردية.",
     s(("Narrative", ["problem, wedge, market, why-now, why-us — evidence-led."]))),
    ("02_METRICS_FOR_INVESTORS.md", "Metrics for Investors", "What to show.", "مقاييس المستثمرين.",
     s(("Metrics", ["pipeline SAR, diagnostics, pilots, retention — actuals only when real."]))),
    ("03_DATA_ROOM_INDEX.md", "Data Room Index", "What's in the room.", "فهرس غرفة البيانات.",
     s(("Index", ["company, product, security, legal templates, metrics, team."]))),
    ("04_PITCH_DECK_OUTLINE.md", "Pitch Deck Outline", "Deck structure.", "هيكل العرض التقديمي.",
     s(("Slides", ["problem, solution, market, product, traction (when real), team, ask."]))),
    ("05_INVESTOR_QA.md", "Investor Q&A", "Anticipated questions.", "أسئلة المستثمرين.",
     s(("Q&A", ["moat, GTM, unit economics, compliance, risks."]))),
    ("06_TRACTION_EVIDENCE_POLICY.md", "Traction Evidence Policy", "Honest claims.", "سياسة أدلة الجذب.",
     s(("Policy", ["every traction claim backed by evidence or omitted."]))),
], {"filename": "99_INVESTOR_OS_REPORT.md", "files": ["`docs/investor-os/*` (7 docs)"],
    "go": ["Investor readiness docs prepared (no unproven traction)."],
    "nogo": ["Claiming traction without evidence."]})


# ===== 23. Operations OS =====
add("operations-os", "Operations / Admin OS", "نظام العمليات والإدارة", [
    ("00_OPERATIONS_OS.md", "Operations / Admin OS", "Ops index.", "فهرس العمليات.",
     s(("Scope", ["operating rhythm, command center, registers, continuity, admin."]))),
    ("01_WEEKLY_OPERATING_RHYTHM.md", "Weekly Operating Rhythm", "The week.", "الإيقاع الأسبوعي.",
     s(("Rhythm", ["Mon plan, Wed delivery, Fri review."]))),
    ("02_DAILY_COMMAND_CENTER.md", "Daily Command Center", "Daily screen.", "مركز القيادة اليومي.",
     s(("Screen", ["draft queue, approvals, pipeline, safety."]))),
    ("03_VENDOR_REGISTER.md", "Vendor Register", "Track vendors.", "سجل الموردين.",
     s(("Fields", ["vendor, service, data access, DPA, renewal."]))),
    ("04_TOOL_STACK_REGISTER.md", "Tool Stack Register", "Track tools.", "سجل الأدوات.",
     s(("Fields", ["tool, purpose, owner, cost, access."]))),
    ("05_ACCOUNT_ACCESS_REGISTER.md", "Account Access Register", "Who has access.", "سجل الوصول.",
     s(("Fields", ["account, owner, role, MFA, review date — no secrets stored here."]))),
    ("06_BACKUP_AND_RECOVERY.md", "Backup & Recovery", "Don't lose data.", "النسخ والاسترداد.",
     s(("Plan", ["what, frequency, location, restore test."]))),
    ("07_BUSINESS_CONTINUITY.md", "Business Continuity", "Keep running.", "استمرارية الأعمال.",
     s(("Plan", ["key risks, fallbacks, single-founder mitigations."]))),
    ("08_ADMIN_CHECKLIST.md", "Admin Checklist", "Recurring admin.", "قائمة الإدارة.",
     s(("Checklist", ["invoices, renewals, compliance, backups."]))),
    ("09_MEETING_CADENCE.md", "Meeting Cadence", "Meetings.", "إيقاع الاجتماعات.",
     s(("Cadence", ["weekly review, client QBRs, partner syncs."]))),
], {"filename": "99_OPERATIONS_OS_REPORT.md", "files": ["`docs/operations-os/*` (10 docs)"],
    "go": ["Operating rhythm and registers ready."], "nogo": ["Storing secrets in registers."]})


# ===== 25. Go-Live OS =====
add("go-live", "Go-Live OS", "نظام الإطلاق", [
    ("00_EXTERNAL_GO_LIVE_REQUIREMENTS.md", "External Go-Live Requirements", "Must-haves to go live.", "متطلبات الإطلاق.",
     s(("Reqs", ["DNS, SPF, DKIM, DMARC, Google Postmaster, bounce tracking, suppression, Calendly, payments, privacy, terms, DPA, email ramp, sender reputation, complaint handling, production smoke."]))),
    ("01_DOMAIN_EMAIL_READINESS.md", "Domain & Email Readiness", "Email deliverability.", "جاهزية البريد.",
     s(("Setup", ["SPF/DKIM/DMARC records, Postmaster monitoring, warm-up plan."]),
       ("Rule", ["Configuration guidance only — no automated sending added."]))),
    ("02_MANUAL_OUTREACH_RAMP.md", "Manual Outreach Ramp", "Safe ramp.", "تصعيد يدوي.",
     s(("Ramp", ["small daily volumes, warm-first, monitor reputation."]))),
    ("03_SUPPRESSION_PROCESS.md", "Suppression Process", "Opt-outs.", "الاستبعاد.",
     s(("Process", ["maintain + honor suppression."]))),
    ("04_PRIVACY_LEGAL_READINESS.md", "Privacy & Legal Readiness", "Legal go-live.", "الجاهزية القانونية.",
     s(("Reqs", ["privacy + terms published, DPA ready, PDPL notes reviewed."]))),
    ("05_PAYMENT_BOOKING_READINESS.md", "Payment & Booking Readiness", "Get paid/booked.", "جاهزية الدفع والحجز.",
     s(("Reqs", ["payment link (sandbox→live gated), booking link, invoice."]))),
    ("06_INCIDENT_AND_COMPLAINT_PROCESS.md", "Incident & Complaint Process", "Handle issues.", "الحوادث والشكاوى.",
     s(("Process", ["intake, triage, resolve, suppress on complaint."]))),
    ("07_PRODUCTION_DEPLOYMENT_CHECKLIST.md", "Production Deployment Checklist", "Ship safely.", "قائمة النشر.",
     s(("Checklist", ["green CI, verifiers PASS, smoke, rollback ready."]))),
    ("08_LAUNCH_DAY_RUNBOOK.md", "Launch Day Runbook", "Launch day.", "كتيب يوم الإطلاق.",
     s(("Runbook", ["pre-checks, go, monitor, comms, rollback triggers."]))),
    ("09_POST_LAUNCH_REVIEW.md", "Post-Launch Review", "Learn after.", "مراجعة ما بعد الإطلاق.",
     s(("Review", ["what worked, issues, next actions."]))),
], {"filename": "99_GO_LIVE_REPORT.md", "files": ["`docs/go-live/*` (10 docs)"],
    "go": ["Go-live requirements documented; production checklist ready."],
    "nogo": ["Going live without DNS/legal/suppression/tracking in place."]})


# ===== 5. Site Launch OS =====
add("site-launch", "Website Launch OS", "نظام إطلاق الموقع", [
    ("00_SITE_LAUNCH_OS.md", "Website Launch OS", "Site launch index.", "فهرس إطلاق الموقع.",
     s(("Stack", ["Next.js 15 App Router under `apps/web/`. Checked by `scripts/site_launch_static_check.py`."]),
       ("Principles", ["trust-first, approval-first, human-in-the-loop, no blind automation, mobile-first, bilingual, SEO-ready, no exaggerated claims, no ROI guarantees."]))),
    ("01_PAGE_MAP.md", "Page Map", "Required routes.", "خريطة الصفحات.",
     s(("Routes", ["/ , /en, /commercial, /services, /pricing, /trust, /launch, /contact, /status, /verticals (+5 vertical pages), /case-method, /media, /faq, /privacy, /terms."]))),
    ("02_SEO_CHECKLIST.md", "SEO Checklist", "Make it findable.", "قائمة تحسين محركات البحث.",
     s(("Checklist", ["title/meta per page, OpenGraph, Twitter card, sitemap, robots, structured data, fast mobile, clear IA — per Google SEO basics."]))),
    ("03_COPY_DECK_AR_EN.md", "Copy Deck (AR/EN)", "Bilingual copy.", "نصوص الموقع.",
     s(("Hero EN", ["The trust-first AI revenue & ops OS for Saudi/GCC B2B. AI prepares; you approve; nothing sends without you."]),
       ("Hero AR", ["نظام تشغيل الإيرادات والعمليات المبني على الثقة. الذكاء يجهّز، وأنت تعتمد، ولا شيء يُرسل دون موافقتك."]),
       ("CTA", ["Request an AI Workflow Audit (from 499 SAR) — اطلب تشخيص سير العمل."]))),
    ("04_MANUAL_QA_CHECKLIST.md", "Manual QA Checklist", "Pre-launch QA.", "ضبط الجودة اليدوي.",
     s(("Checklist", ["all routes render, bilingual toggle, mobile, links, forms (no auto-submit), metadata, no broken claims."]))),
    ("05_CONVERSION_PATHS.md", "Conversion Paths", "How visitors convert.", "مسارات التحويل.",
     s(("Paths", ["Home → Vertical → Pricing → Contact (opt-in) → founder follow-up (manual)."]))),
    ("06_LANDING_PAGE_QA.md", "Landing Page QA", "Per-vertical QA.", "ضبط جودة صفحات الهبوط.",
     s(("QA", ["one clear promise, proof, offer (SAR), CTA, safety note."]))),
    ("07_SITE_CONTENT_GOVERNANCE.md", "Site Content Governance", "Keep copy honest.", "حوكمة المحتوى.",
     s(("Rules", ["no ROI guarantees, no unverified claims, founder approves copy changes."]))),
], {"filename": "99_SITE_LAUNCH_REPORT.md", "files": ["`docs/site-launch/*` (8 docs)", "new `apps/web/app/*` routes"],
    "scripts": ["`scripts/site_launch_static_check.py`"],
    "tests": ["`tests/test_site_launch_static_check.py`", "`tests/test_site_commercial_pages.py`"],
    "go": ["Public website launch with commercial positioning and vertical pages."],
    "nogo": ["Form auto-submit; exaggerated claims; ROI guarantees."]})


# ===== 27. Launch Control Tower =====
add("launch-control", "Final Launch Control Tower", "برج التحكم النهائي للإطلاق", [
    ("00_FINAL_LAUNCH_CONTROL_TOWER.md", "Final Launch Control Tower", "Single control surface.", "سطح تحكم واحد.",
     s(("Purpose", ["One place to verify the whole company OS is launch-ready and safe."]),
       ("Gates", ["startup_os_verify PASS, final_launch_control_verify PASS, safety audit clean, secret scan clean, tests green."]))),
    ("01_LAUNCH_SCORECARD.md", "Launch Scorecard", "Are we ready?", "بطاقة الإطلاق.",
     s(("Areas", ["all 24 OS areas + scripts + tests + workflows + reports — green/amber/red."]))),
    ("02_GO_NO_GO_MATRIX.md", "Go/No-Go Matrix", "Decide launch.", "مصفوفة القرار.",
     s(("GO", ["site, positioning, 400 review-only drafts, founder review, manual posting, paid diagnostics, discovery, proposals, analytics schema, delivery/support prep, finance/legal templates, investor/partner/hiring readiness."]),
       ("NO-GO", ["automated email/WhatsApp/LinkedIn, auto-submit, bulk send, live paid ads w/o tracking/compliance, sensitive data pre-agreement, external sends from Actions, unbacked claims."]))),
    ("03_EVIDENCE_PACK.md", "Evidence Pack", "Proof index.", "حزمة الأدلة.",
     s(("Contents", ["verifier outputs (`outputs/startup_os/*`), draft factory outputs, safety audit, secret scan, test results."]))),
    ("04_30_DAY_WAR_ROOM.md", "30-Day War Room", "First 30 days.", "غرفة عمليات 30 يوم.",
     s(("Focus", ["site live, drafts+review daily, first diagnostics, weekly metrics."]))),
    ("05_DAILY_COMMAND_CENTER.md", "Daily Command Center", "Daily ops screen.", "مركز القيادة اليومي.",
     s(("Screen", ["draft queue, approvals, pipeline, safety flags, content."]))),
    ("06_FAILURE_RESPONSE_PLAYBOOK.md", "Failure Response Playbook", "When things break.", "دليل الاستجابة للفشل.",
     s(("Plays", ["verifier fail → fix → re-run; safety flag → halt sends; incident → IR process."]))),
    ("07_FOUNDER_EXECUTION_CHECKLIST.md", "Founder Execution Checklist", "Daily founder list.", "قائمة تنفيذ المؤسس.",
     s(("Checklist", ["review drafts, approve sends, log decisions, update scorecard."]))),
    ("08_STARTUP_OS_MAP.md", "Startup OS Map", "How it all connects.", "خريطة نظام الشركة.",
     s(("Map", ["Company → Product/Engineering → Site → Commercial/Sales/Marketing/Media/Ads → RevOps → Delivery/Support → Finance/Legal/Security/Analytics/Evals → People/Partners/Investor/Ops → Go-Live → Launch Control."]))),
    ("09_WEEKLY_CEO_REVIEW.md", "Weekly CEO Review", "Run the company.", "مراجعة الرئيس التنفيذي.",
     s(("Agenda", ["revenue, pipeline, delivery, safety, content, decisions, risks."]))),
], {"filename": "99_FINAL_CONTROL_TOWER_REPORT.md",
    "files": ["`docs/launch-control/*` (incl. discovery report)"],
    "scripts": ["`scripts/final_launch_control_verify.py`", "`scripts/startup_os_verify.py`"],
    "tests": ["`tests/test_final_launch_control_verify.py`", "`tests/test_startup_os_verify.py`"],
    "outputs": ["`outputs/startup_os/startup_os_verification.{json,md}`"],
    "go": ["Whole-company verification gating launch."],
    "nogo": ["Declaring launch without verifiers PASS."]})


def all_expected_paths() -> list[Path]:
    return [DOCS / rel for rel in REGISTRY]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        missing = [str(p) for p in all_expected_paths() if not p.exists()]
        if missing:
            print(f"MISSING {len(missing)} generated docs:")
            for m in missing[:20]:
                print("  -", m)
            return 1
        print(f"OK: all {len(REGISTRY)} generated docs present.")
        return 0

    written = 0
    for rel, content in REGISTRY.items():
        path = DOCS / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written += 1
    print(f"Wrote {written} generated docs under {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
