# Landing Page Conversion System | نظام تحويل صفحات الهبوط

> Landing pages are the conversion surface of the Marketing OS. Each page has a single job, a single audience, and a single CTA — and meets every Dealix trust gate.

---

## 1. Purpose | الغرض

To deliver predictable, accountable conversion from owned and paid channels into the top rung of the product ladder — typically the **Free Diagnostic** — while reinforcing positioning and respecting every non-negotiable.

---

## 2. Page Inventory | جرد الصفحات

| Page | Audience | Primary CTA |
|---|---|---|
| Homepage | All buyers + partners | Book a Free Diagnostic |
| Revenue Sprint | Founder / Head of Sales | Book a Free Diagnostic |
| Managed Pilot | Head of Sales / Revenue | Talk to the Revenue Desk |
| Revenue Desk Retainer | GM / VP Sales | Talk to the Revenue Desk |
| Founder Console | Founder | Request access |
| Enterprise Revenue OS | BU Head / CRO | Request enterprise call |
| Partner / White-label | Agency / Partner | Apply to partner program |
| Free Diagnostic | All | Book a diagnostic |
| Case study (per approved customer) | Buyer in same sector | Book a Free Diagnostic |
| About / Founder | Investor, hire, partner | Read manifesto / Contact |

Each page exists in **English and Arabic** with bilingual parity.

---

## 3. Anatomy of a Landing Page | تشريح الصفحة

| Section | Job | Must include |
|---|---|---|
| Hero | Frame the category + the page's promise | Eyebrow (L1 echo), H1 (L2 frame), H2 (specific outcome), primary CTA |
| Trust strip | Show credibility without violating proof rules | Sector logos only with approval; otherwise stats with ranges + N |
| Problem | Restate the buyer's real problem | One paragraph in Dealix voice |
| What ships | Concrete outputs of the offer | Bulleted, with approval gates and evidence |
| How it works | The approval-gated motion | 3–5 step diagram or list |
| Proof | Approved customer outcomes | Ranges + conditions + pilot N |
| Objections | Address top 3 in this audience's voice | "What if…" Q&A |
| CTA repeat | Reinforce the single CTA | Same button label as hero |
| Footer | Compliance, links, language toggle | PDPL note, address, unsubscribe (for forms) |

---

## 4. The One-CTA Rule | قاعدة الدعوة الواحدة

- Each page has **exactly one** primary CTA.
- Secondary links are allowed, but they must not visually compete with the primary CTA.
- The primary CTA label is verb-led and outcome-named (e.g., "Book a Free Diagnostic"), never generic ("Learn more").

---

## 5. Conversion Mechanics | آليات التحويل

- Forms ask **only** for what is needed to deliver the next step. For the Free Diagnostic: name, work email, company, role, language preference, two scheduling windows.
- All forms are PDPL-compliant: explicit consent, purpose statement, opt-out.
- Confirmations show what happens next (who reaches out, in what language, within what window).
- No auto-generated outbound from a form submission — every follow-up is human-drafted (the Dealix way).

---

## 6. Bilingual Parity | التماثل الثنائي

- Arabic version is authored, not translated.
- RTL layout, logical CSS properties, mirrored directional icons.
- Equal section count, equal scannability, equal CTA placement.
- Language toggle preserves the user's place in the page.

---

## 7. Performance Budget | ميزانية الأداء

- LCP ≤ 2.5s on 4G median KSA device.
- CLS ≤ 0.1.
- INP ≤ 200ms.
- Total page weight ≤ 1.5 MB initial.
- Web fonts self-hosted, `font-display: swap`, subset to active scripts.

---

## 8. Accessibility | إمكانية الوصول

- Meets WCAG 2.2 AA (see `docs/brand/DEALIX_ACCESSIBILITY_GUIDE.md`).
- Keyboard-operable forms with visible focus.
- Alt text on every meaningful image; decorative SVGs hidden from AT.
- RTL pages tested end to end.

---

## 9. SEO / GEO | الظهور في البحث والـAI

- One primary keyword cluster per page, anchored to Dealix vocabulary (e.g., "Revenue Operating Company KSA," "Saudi B2B revenue OS").
- Page title ≤ 60 chars; meta description ≤ 155 chars; bilingual variants for AR pages.
- Structured data: `Organization`, `WebSite`, `Service`, `FAQPage` where relevant.
- Internal linking favors the rung ladder and the category essays.
- For LLM/AI surfaces: include a clean FAQ section that mirrors the voice and includes ranges + conditions + N.

---

## 10. Testing & Iteration | الاختبار والتحسين

- Run **one test at a time** per page (hero headline, hero subhead, CTA label).
- Minimum sample: 1,000 sessions or 30 conversions per arm — whichever comes first.
- Lock the winner; retire the loser; document in the page changelog.
- Never test claims that violate non-negotiables (e.g., "guaranteed").

---

## 11. Analytics & Consent | التحليلات والموافقة

- Use consented analytics only.
- Track: sessions, qualified form submissions, scheduled diagnostics, source channel, language version, device.
- Do not track or store PII beyond the form submission lifecycle.
- Quarterly data minimization review.

---

## 12. Non-Negotiables | الخطوط الحمراء

- **No external sending** triggered by form submission; all follow-ups are human-drafted.
- **No customer proof** on a landing page without written customer approval.
- **No guaranteed-revenue** claims in copy, hero, or proof sections. Use ranges + conditions + pilot N.
- **No pricing or contract** commitments without escalation; pricing pages, if any, state ranges and direct to a conversation.
- **Approval-gated automation only** — never frame Dealix as autonomous.

---

## 13. Owner & KPI | الملكية والمؤشرات

- **Owner:** Marketing Lead (with Brand Lead and Design Systems Lead).
- **KPI:** Hero CTA conversion rate per page (track baseline; improve via locked-winner testing).
- **KPI:** Bilingual parity rate (target 100%).
- **KPI:** WCAG AA pass rate (target 100%).
- **KPI:** Non-negotiable violations (target 0).
- **KPI:** Diagnostic bookings / week from owned channels.

---

## 14. Related Documents | مراجع

- `DEALIX_MARKETING_OS.md`
- `COPYWRITING_RULES.md`
- `BRAND_VOICE_EXAMPLES.md`
- `docs/brand/DEALIX_ACCESSIBILITY_GUIDE.md`
- `docs/brand/DEALIX_VISUAL_IDENTITY.md`
- `docs/positioning/MESSAGING_HIERARCHY.md`
- `docs/product/DEALIX_PRODUCT_LADDER.md`
