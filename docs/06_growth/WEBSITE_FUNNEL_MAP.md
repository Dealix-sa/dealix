# Website Funnel Map — خريطة قمع الموقع

**Status: DOCS_ONLY** — page specs and routing logic. Pages move to BETA/LIVE per [GROWTH_EXPERIMENTS.md](./GROWTH_EXPERIMENTS.md).

> Purpose — الغرض: map the full Dealix funnel from traffic to retainer, assign every website page to one funnel stage and one CTA, and define the lead-capture and routing logic. No auto-send; founder-approval gates everywhere. Cross-link: [CONVERSION_PLAYBOOK.md](./CONVERSION_PLAYBOOK.md), [FREE_TOOLS_STRATEGY.md](./FREE_TOOLS_STRATEGY.md), [NURTURE_SEQUENCES.md](./NURTURE_SEQUENCES.md), [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).

خريطة قمع الموقع تربط كل صفحة بمرحلة واحدة من القمع ومسار CTA واحد، وتعرّف منطق التقاط العملاء وتوجيههم. لا إرسال خارجي تلقائي، وكل نقطة التقاط تمر ببوابة موافقة المؤسس.

---

## The funnel — القمع

Traffic sources → Landing pages → Free tools → Diagnostic → Command Sprint → Retainer.

| Stage | Goal | Primary asset |
|---|---|---|
| 1. Traffic | Reach a Saudi/GCC decision-maker | SEO/GEO, LinkedIn, partners, referrals |
| 2. Landing | Frame the category, name the pain | `/`, `/platform`, `/industries` |
| 3. Free tool | Give value, capture intent | `/business-os` (Score), tools |
| 4. Diagnostic | Qualify and scope | `/start` (Diagnostic) |
| 5. Command Sprint | First paid engagement | `/command-sprint` |
| 6. Retainer | Recurring managed ops | post-sprint offer |

Traffic sources: Arabic-first SEO/GEO ([SEO_GEO_STRATEGY.md](./SEO_GEO_STRATEGY.md)), founder LinkedIn ([CONTENT_FACTORY.md](./CONTENT_FACTORY.md)), partners ([PARTNER_DISTRIBUTION.md](./PARTNER_DISTRIBUTION.md)), referrals ([REFERRAL_ENGINE.md](./REFERRAL_ENGINE.md)). No paid spam, no cold outreach.

---

## Page-by-page map — خريطة الصفحات

| Page | Funnel stage | ONE CTA | Status |
|---|---|---|---|
| `/` | Landing / category framing | Business OS Score | DOCS_ONLY |
| `/platform` | Education (what the OS is) | Business OS Score | DOCS_ONLY |
| `/command-sprint` | Offer (first paid) | Command Sprint (Diagnostic) | DOCS_ONLY |
| `/business-os` | Free tool (priority) | Business OS Score | DOCS_ONLY |
| `/pricing` | Decision support | Diagnostic | DOCS_ONLY |
| `/industries` | Education (sector relevance) | Business OS Score | DOCS_ONLY |
| `/security` | Trust / objection handling | Diagnostic | DOCS_ONLY |
| `/start` | Conversion (book) | Diagnostic | DOCS_ONLY |

**One-CTA rule:** every page routes to exactly one CTA. Pages do not compete for the click. قاعدة المسار الواحد: لكل صفحة مسار واحد فقط. See [CONVERSION_PLAYBOOK.md](./CONVERSION_PLAYBOOK.md).

---

## Page notes — ملاحظات الصفحات

- **`/`** — Navy/Gold executive hero, Arabic-first, names the category (governed AI operations) and the pain. Single CTA: Business OS Score. الواجهة التنفيذية.
- **`/platform`** — explains Dealix as a Business OS (Revenue OS is the first wedge, not the whole). Links to [../00_foundation/STRATEGIC_WEDGE.md](../00_foundation/STRATEGIC_WEDGE.md).
- **`/command-sprint`** — describes the eight Sprint modules (Market Intelligence Lite, Revenue Map, Proof Register, Executive Command Brief, Approval Register, Next Action Board, Delivery Lite, Upsell Recommendation). CTA: book the Diagnostic that scopes the Sprint.
- **`/business-os`** — hosts the Business OS Score, the priority free tool. منتج الالتقاط الأساسي.
- **`/pricing`** — transparent tiers; no fake scarcity, no countdown timers. CTA: Diagnostic.
- **`/industries`** — sector relevance (retail, real estate, healthcare, professional services, contracting). CTA: Score.
- **`/security`** — PDPL-aware, governance, data provenance, no scraping. Handles the trust objection. CTA: Diagnostic. Links to [../14_trust_os/TRUST_PACK.md](../14_trust_os/TRUST_PACK.md).
- **`/start`** — the single booking surface for the Diagnostic.

---

## Lead-capture + routing logic — منطق الالتقاط والتوجيه

```
1. Visitor lands on a page (one CTA visible).
2. Visitor completes a free tool OR books via /start.
3. Capture: name, work email, company, sector, consent (PDPL-aware opt-in).
   - No pre-checked boxes. No purchased lists. No scraped contacts.
4. Lead enters the founder-approval queue as a DRAFT.
   - Nurture emails are queued as drafts, never auto-sent externally.
5. Founder reviews → approves → nurture sequence releases.
6. Routing:
   - Score completed, low maturity  → educate → Diagnostic offer
   - Score completed, high maturity → Diagnostic now
   - Diagnostic completed           → Command Sprint proposal
   - Sprint delivered               → Retainer / upsell
```

Routing rules mirror the nurture triggers in [NURTURE_SEQUENCES.md](./NURTURE_SEQUENCES.md). Every external message is a draft until founder approval, per [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).

---

## Approval gates — بوابات الموافقة

- **Gate 1 — Capture consent.** No lead enters nurture without explicit opt-in. موافقة الالتقاط.
- **Gate 2 — Founder release.** No nurture email leaves as anything but a draft until founder approval. إفراج المؤسس.
- **Gate 3 — Proof claim.** No page or email cites a result without a delivered Proof Pack behind it. ادعاء الإثبات.

These gates are non-negotiable. هذه البوابات غير قابلة للتفاوض.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
