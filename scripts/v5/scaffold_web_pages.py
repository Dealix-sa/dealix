#!/usr/bin/env python3
"""Generate V5 marketing/launch pages as static Next.js (App Router) server components.

Low-risk: each page is a plain server component returning static JSX with per-page
metadata. No client forms that auto-submit, no external calls, no ROI guarantees.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "apps" / "web" / "app"

SAFETY = ("AI prepares and recommends; you approve and act. Nothing is sent or submitted "
          "automatically. No ROI guarantees — we show evidence and estimates.")

OFFERS = [
    ("AI Workflow Audit", "499–2,500 SAR", "Review-only diagnostic of one workflow with prioritized fixes."),
    ("Paid Pilot", "5,000–25,000 SAR", "Scoped, time-boxed proof on one workflow."),
    ("Department OS", "25,000–150,000 SAR", "An operating system for one department."),
    ("Monthly Retainer", "3,000–25,000 SAR/month", "Ongoing draft, review, and delivery ops."),
    ("Enterprise Custom OS", "150,000+ SAR", "Multi-department, custom integrations."),
]

VERTICALS = [
    ("facilities-management", "Facilities Management & Maintenance", "إدارة المرافق والصيانة",
     "Reduce manual work-order triage and SLA reporting across multiple sites."),
    ("contracting-project-controls", "Contracting & Project Controls", "المقاولات وضبط المشاريع",
     "Cut manual progress, cost, and variation reporting across active projects."),
    ("real-estate-property-ops", "Real Estate & Property Operations", "العقارات وعمليات الأملاك",
     "Streamline tenant requests, lease tracking, and owner reporting."),
    ("legal-professional-services", "Legal & Professional Services", "الخدمات القانونية والمهنية",
     "Speed up intake, matter reporting, and document draft prep — review-only."),
    ("consulting-training-b2b", "Consulting, Training & B2B Services", "الاستشارات والتدريب وخدمات الأعمال",
     "Tighten pipeline, proposal turnaround, and engagement reporting."),
]


def page(title: str, description: str, body: str) -> str:
    return f'''import type {{ Metadata }} from "next";

export const metadata: Metadata = {{
  title: {title!r},
  description: {description!r},
}};

export default function Page() {{
  return (
    <main className="grid" style={{{{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}}}>
{body}
      <p style={{{{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}}}>
        <strong>Safety:</strong> {SAFETY}
      </p>
    </main>
  );
}}
'''


def li(items):
    return "\n".join(f'      <li>{i}</li>' for i in items)


PAGES: dict[str, str] = {}


def add(route: str, title: str, description: str, body: str):
    PAGES[route] = page(title, description, body)


add("en", "Dealix — Trust-first AI Revenue & Ops OS",
    "Dealix is a Saudi/GCC B2B AI Revenue & Operations OS. AI prepares; you approve; nothing sends without you.",
    '''      <h1>Dealix — the trust-first AI Revenue &amp; Ops OS</h1>
      <p>For Saudi/GCC B2B operators. AI drafts, scores, and prepares your revenue work.
         You review, approve, and send manually. The system never sends externally.</p>
      <p><a href="/commercial">See the commercial offers →</a> · <a href="/trust">How we keep it safe →</a></p>''')

add("commercial", "Commercial — Offers & Approach",
    "Dealix commercial offers: review-only AI workflow audits, pilots, department OS, retainers. SAR pricing.",
    f'''      <h1>Commercial</h1>
      <p>A trust-first path from a low-risk diagnostic to ongoing delivery — always review-only.</p>
      <h2>Offer ladder (SAR)</h2>
      <ul>
{li([f"<strong>{n}</strong> — {p}: {d}" for n, p, d in OFFERS])}
      </ul>
      <p><a href="/pricing">Pricing details →</a> · <a href="/contact">Request an audit →</a></p>''')

add("services", "Services — What We Deliver",
    "Dealix services across the first five verticals — review-only AI ops, delivered with founder oversight.",
    f'''      <h1>Services</h1>
      <p>We focus on five verticals where manual revenue/ops work is heaviest:</p>
      <ul>
{li([f'<a href="/verticals/{slug}">{t}</a> — {d}' for slug, t, _ar, d in VERTICALS])}
      </ul>''')

add("pricing", "Pricing (SAR)",
    "Transparent SAR pricing for Dealix offers. No ROI guarantees — evidence and estimates only.",
    f'''      <h1>Pricing (SAR)</h1>
      <ul>
{li([f"<strong>{n}</strong> — {p}: {d}" for n, p, d in OFFERS])}
      </ul>
      <p>All prices in SAR. Value is framed in time saved and quality, backed by evidence — we never promise a specific return.</p>''')

add("trust", "Trust & Safety",
    "How Dealix stays trustworthy: human-in-the-loop, review-only drafts, no blind automation, PDPL-aware.",
    '''      <h1>Trust &amp; Safety</h1>
      <ul>
      <li>Human-in-the-loop: the founder approves every external action.</li>
      <li>Review-only drafts: the system prepares, never sends.</li>
      <li>No scraping, no mass-sending, no automation of outreach.</li>
      <li>PDPL-aware data handling; no sensitive data before an agreement.</li>
      <li>Evidence over claims — no ROI guarantees.</li>
      </ul>''')

add("launch", "Launch Status",
    "Dealix launch readiness — what is live, what is review-only, and what remains founder-gated.",
    '''      <h1>Launch</h1>
      <p>We launch trust-first. Live now: public site, review-only draft preparation, founder-led
         outreach, paid diagnostics. Always founder-gated: any external sending, paid ads, and
         sensitive-data processing.</p>
      <p><a href="/status">System status →</a></p>''')

add("contact", "Contact",
    "Contact Dealix to request a review-only AI workflow audit. Opt-in only; no auto-submission.",
    '''      <h1>Contact</h1>
      <p>Request a review-only AI workflow audit (from 499 SAR). We reply personally — opt-in only.</p>
      <p>This page does not auto-submit or send anything. Reach out via the channel shared by the founder
         during your conversation, or your existing introduction.</p>
      <p><a href="/commercial">Review the offers →</a></p>''')

add("faq", "FAQ",
    "Frequently asked questions about Dealix: safety, pricing, data handling, and the review-only model.",
    '''      <h1>FAQ</h1>
      <h3>Is this spam / automated outreach?</h3>
      <p>No. Everything is review-only and the founder sends manually. Opt-out is always honored.</p>
      <h3>Do you guarantee ROI?</h3>
      <p>No. We show evidence and estimates, never guarantees.</p>
      <h3>How is my data handled?</h3>
      <p>PDPL-aware, minimized, and never processed before an agreement.</p>''')

add("privacy", "Privacy Policy",
    "Dealix privacy policy (template — pending legal review). PDPL-aware data handling.",
    '''      <h1>Privacy Policy</h1>
      <p><em>Template — pending qualified legal review. Not legal advice.</em></p>
      <p>We collect only what you provide with consent, use it to respond to your request,
         retain it minimally, and honor access/deletion requests. PDPL-aware.</p>''')

add("terms", "Terms of Service",
    "Dealix terms of service (template — pending legal review).",
    '''      <h1>Terms of Service</h1>
      <p><em>Template — pending qualified legal review. Not legal advice.</em></p>
      <p>Use of this site is subject to acceptable-use and liability terms finalized with legal counsel
         before any commercial engagement.</p>''')

add("case-method", "Case Method",
    "How Dealix turns delivery into proof: evidence capture, client approval, anonymized case studies.",
    '''      <h1>Case Method</h1>
      <p>We turn delivery into proof: capture evidence during delivery, get client approval,
         and publish anonymized outcomes. Every claim is backed by an artifact or labeled an estimate.</p>''')

add("media", "Media & Press",
    "Dealix media and press resources. Factual claims only.",
    '''      <h1>Media &amp; Press</h1>
      <p>Boilerplate, founder background, and logo usage available on request. We make factual
         claims only — no inflated metrics.</p>''')

add("verticals", "Verticals",
    "The five verticals Dealix focuses on first across Saudi Arabia and the GCC.",
    f'''      <h1>Verticals</h1>
      <p>We start where manual revenue/ops work is heaviest:</p>
      <ul>
{li([f'<a href="/verticals/{slug}">{t}</a> <span dir="rtl">({ar})</span> — {d}' for slug, t, ar, d in VERTICALS])}
      </ul>''')

for slug, t, ar, d in VERTICALS:
    add(f"verticals/{slug}", f"{t} — Dealix",
        f"Dealix for {t}: review-only AI ops that reduce manual work. {d}",
        f'''      <h1>{t}</h1>
      <p dir="rtl" lang="ar">{ar}</p>
      <p>{d}</p>
      <h2>What we prepare (review-only)</h2>
      <ul>
      <li>Workflow audit findings and prioritized fixes.</li>
      <li>Drafted communications you approve and send manually.</li>
      <li>Reporting templates and evidence capture.</li>
      </ul>
      <h2>Offers (SAR)</h2>
      <ul>
{li([f"<strong>{n}</strong> — {p}" for n, p, _ in OFFERS])}
      </ul>
      <p><a href="/contact">Request an audit →</a></p>''')


def main() -> int:
    check = "--check" in sys.argv
    if check:
        missing = [r for r in PAGES if not (APP / r / "page.tsx").exists()]
        if missing:
            print("MISSING pages:", missing)
            return 1
        print(f"OK: all {len(PAGES)} V5 web pages present.")
        return 0
    for route, content in PAGES.items():
        p = APP / route / "page.tsx"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    print(f"Wrote {len(PAGES)} V5 web pages under {APP}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
