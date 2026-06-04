#!/usr/bin/env python3
"""Generate the 5 commercial-launch vertical playbooks with sector-specific content."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "commercial-launch" / "verticals"

NON_NEG = ("**Non-negotiable:** AI drafts/scores/recommends; founder reviews, approves, "
           "and sends manually. The system never sends externally.")

VERTICALS = {
    "01_facilities_management.md": dict(
        title="Facilities Management & Maintenance",
        ar="إدارة المرافق والصيانة",
        icp="FM operators, maintenance contractors, and integrated facility services firms managing multiple sites (malls, offices, compounds, hospitals) in KSA/GCC.",
        excluded="One-person handyman shops; pure equipment resellers with no service ops.",
        personas=["Operations Director (DM)", "FM/Account Manager (influencer)", "Dispatcher/Coordinator (user)", "GM/Owner (budget owner)"],
        pains=["Reactive work orders and SLA breaches", "Manual scheduling and reporting", "Poor visibility across sites", "Slow client reporting"],
        triggers=["New multi-site contract won", "SLA penalties incurred", "Client demands monthly reporting", "Scaling headcount"],
        buying=["Mentions of CAFM/CMMS gaps", "Hiring coordinators", "Complaints about reporting"],
        disqual=["No service contracts", "No budget owner reachable", "Pure product business"],
        workflows=["Work-order intake & triage", "Preventive maintenance scheduling", "Client SLA reporting", "Vendor/technician dispatch"],
        proof=["Anonymized reporting-time reduction (labeled estimate until measured)", "Sample SLA dashboard"],
    ),
    "02_contracting_project_controls.md": dict(
        title="Contracting & Project Controls",
        ar="المقاولات وضبط المشاريع",
        icp="Mid-size contractors and project-controls teams running multiple active projects (civil, MEP, fit-out) in KSA/GCC.",
        excluded="Single-trade subcontractors with no PMO; suppliers only.",
        personas=["Projects Director (DM)", "Project Controls Manager (influencer)", "Planner/QS (user)", "Owner/Partner (budget owner)"],
        pains=["Manual progress & cost reporting", "Variation/claim tracking", "Document control chaos", "Cash-flow visibility"],
        triggers=["New large project award", "Client/consultant reporting demands", "Cost overruns", "Audit/claim disputes"],
        buying=["Hiring planners/QS", "Complaints about reporting cadence", "ERP/Primavera gaps"],
        disqual=["No active projects", "No PMO function", "Owner unreachable"],
        workflows=["Progress reporting", "Cost & variation tracking", "Document control", "Submittals/RFIs"],
        proof=["Sample weekly progress report", "Variation log template (estimate framing)"],
    ),
    "03_real_estate_property_ops.md": dict(
        title="Real Estate & Property Operations",
        ar="العقارات وعمليات الأملاك",
        icp="Property managers, developers, and owners' associations managing residential/commercial portfolios in KSA/GCC.",
        excluded="Individual brokers; pure listing portals.",
        personas=["Property Operations Manager (DM)", "Leasing/CS Lead (influencer)", "Coordinator (user)", "Asset Owner (budget owner)"],
        pains=["Tenant request handling", "Lease & renewal tracking", "Collections follow-up", "Owner reporting"],
        triggers=["Portfolio growth", "High vacancy/churn", "Owner reporting demands", "Collections backlog"],
        buying=["Hiring property coordinators", "Complaints about tenant response", "Manual lease tracking"],
        disqual=["Single unit", "No management mandate"],
        workflows=["Tenant request triage", "Lease/renewal tracking", "Collections reminders (review-only drafts)", "Owner reporting"],
        proof=["Sample owner report", "Renewal-tracking template"],
    ),
    "04_legal_professional_services.md": dict(
        title="Legal & Professional Services",
        ar="الخدمات القانونية والمهنية",
        icp="Law firms, consultancies, audit/accounting and advisory firms in KSA/GCC with recurring client work.",
        excluded="Solo practitioners with no support staff; unregulated advisors.",
        personas=["Managing Partner (DM)", "Practice Lead (influencer)", "Associate/Paralegal (user)", "Partner (budget owner)"],
        pains=["Manual intake & conflict checks", "Document drafting overhead", "Matter status reporting", "Billing follow-up"],
        triggers=["Caseload growth", "New practice area", "Client reporting demands", "Billing leakage"],
        buying=["Hiring associates/paralegals", "Complaints about turnaround", "Manual matter tracking"],
        disqual=["No recurring matters", "No support staff"],
        workflows=["Client intake & triage", "Document draft prep (review-only)", "Matter status reporting", "Billing reminders (review-only)"],
        proof=["Sample matter-status report", "Intake checklist template"],
        compliance_extra="Confidentiality and privilege are paramount; no client data processed before an engagement letter + DPA. Drafts are starting points, not legal advice.",
    ),
    "05_consulting_training_b2b.md": dict(
        title="Consulting, Training & B2B Services",
        ar="الاستشارات والتدريب وخدمات الأعمال",
        icp="Boutique consultancies, training providers, and B2B service firms selling repeatable engagements in KSA/GCC.",
        excluded="B2C-only trainers; one-off freelancers with no pipeline.",
        personas=["Founder/MD (DM)", "Engagement Lead (influencer)", "Coordinator (user)", "Owner (budget owner)"],
        pains=["Inconsistent pipeline", "Proposal turnaround", "Engagement reporting", "Follow-up gaps"],
        triggers=["Pipeline dry spell", "Scaling delivery team", "Client reporting demands", "Lost-deal pattern"],
        buying=["Hiring BD/coordinators", "Complaints about proposal speed", "Manual CRM"],
        disqual=["No repeatable offer", "B2C only"],
        workflows=["Lead qualification", "Proposal draft prep (review-only)", "Engagement reporting", "Follow-up sequencing (manual)"],
        proof=["Sample proposal", "Engagement report template"],
    ),
}

OFFER_LADDER = [
    ("AI Workflow Audit", "499–2,500 SAR"),
    ("Paid Pilot", "5,000–25,000 SAR"),
    ("Department OS", "25,000–150,000 SAR"),
    ("Monthly Retainer", "3,000–25,000 SAR/month"),
    ("Enterprise Custom OS", "150,000+ SAR"),
]


def render(slug: str, v: dict) -> str:
    t = v["title"]
    en_draft = (
        f"Subject: A 30-minute look at your {v['workflows'][0].lower()} workflow\n\n"
        f"Hi {{first_name}}, I work with {t.lower()} teams in the Kingdom on reducing manual "
        f"{v['pains'][0].lower()}. We prepare a review-only AI workflow audit — you approve every step, "
        f"nothing is sent or changed without you. Worth a short call? "
        f"If not, reply 'stop' and I won't follow up.\n— {{founder_name}}, Dealix"
    )
    ar_draft = (
        f"الموضوع: نظرة 30 دقيقة على سير عمل {v['workflows'][0]}\n\n"
        f"مرحبًا {{first_name}}، أعمل مع فرق {v['ar']} في المملكة على تقليل "
        f"{v['pains'][0]} اليدوي. نُجهّز تشخيصًا للمراجعة فقط — أنت تعتمد كل خطوة، "
        f"ولا يُرسل أو يُغيَّر شيء دون موافقتك. هل تناسبك مكالمة قصيرة؟ "
        f"إن لم تكن مهتمًا، اكتب «إيقاف» ولن أتابع.\n— {{founder_name}}، Dealix"
    )
    li_draft = (
        f"(Manual LinkedIn note — founder posts/sends personally) Saw your work in {t.lower()}. "
        f"I'm building review-only AI ops tooling for {v['ar']} teams in KSA — would value your perspective. "
        f"No pitch, no automation."
    )
    form_draft = (
        f"(Website opt-in follow-up draft) Thanks for requesting an audit. Here's what a review-only "
        f"{t} workflow audit covers, the SAR options, and next steps — reply to book."
    )

    def bl(items):
        return "\n".join(f"- {i}" for i in items)

    return f"""# Vertical Playbook — {t}

> **AR:** {v['ar']} · {NON_NEG}

## ICP
{v['icp']}

## Excluded ICP
{v['excluded']}

## Buyer personas
{bl(v['personas'])}

- **Decision maker:** {v['personas'][0]}
- **Influencer:** {v['personas'][1]}
- **User:** {v['personas'][2]}
- **Budget owner:** {v['personas'][3]}

## Main workflows
{bl(v['workflows'])}

## Top pains
{bl(v['pains'])}

## Trigger events
{bl(v['triggers'])}

## Buying signals
{bl(v['buying'])}

## Disqualification signals
{bl(v['disqual'])}

## Offer ladder (SAR)
""" + bl([f"**{n}** — {p}" for n, p in OFFER_LADDER]) + f"""
- **Entry offer:** AI Workflow Audit (499–2,500 SAR)
- **Pilot offer:** Paid Pilot (5,000–25,000 SAR)
- **Department OS:** 25,000–150,000 SAR
- **Retainer:** 3,000–25,000 SAR/month
- **Enterprise:** 150,000+ SAR

## English draft (review-only)
```
{en_draft}
```

## Arabic draft (review-only) — مسودة للمراجعة فقط
```
{ar_draft}
```

## LinkedIn manual draft (founder sends personally)
```
{li_draft}
```

## Website form follow-up draft (opt-in only)
```
{form_draft}
```

## Objections
- "Is this spam?" → Review-only, opt-in, opt-out honored, founder sends personally.
- "ROI?" → We show evidence and estimates, never guarantees.
- "We do it manually." → That's the point — we prepare, you stay in control.

## Delivery scope
- Inputs, outputs, timeline, acceptance, security boundary, handover, upsell path (see `docs/delivery-os/`).

## Proof assets
{bl(v['proof'])}

## Compliance notes
- Opt-in / opt-out respected; PDPL-aware; no scraping; no auto-send.
- {v.get('compliance_extra', 'No sensitive client data processed before agreement.')}

## What NOT to say
- No guaranteed ROI / revenue numbers.
- No "fully automated outreach" claims.
- No unverified client names or results.

## Success metrics
- Audits requested, diagnostics sold, pilots sold, pipeline SAR — manual inputs until real data exists.

---

> {NON_NEG}
>
> **Safety:** No automated sending, scraping, auto-submit, or live ads. Founder-gated throughout.
"""


def main() -> int:
    check = "--check" in sys.argv
    if check:
        missing = [f for f in VERTICALS if not (OUT / f).exists()]
        if missing:
            print("MISSING:", missing)
            return 1
        print(f"OK: all {len(VERTICALS)} vertical playbooks present.")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, v in VERTICALS.items():
        (OUT / slug).write_text(render(slug, v), encoding="utf-8")
    print(f"Wrote {len(VERTICALS)} vertical playbooks under {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
