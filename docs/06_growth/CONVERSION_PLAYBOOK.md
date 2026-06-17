# Conversion Playbook — دليل التحويل

> How we convert without manipulation. CTA hierarchy, friction reduction, form design, and
> trust elements — governance-first, proof-first. **No dark patterns, no fake scarcity, no fake
> testimonials, no guaranteed revenue.** Coordinate copy with `proof-governance-reviewer`,
> structure with `seo-geo-agent`. Status: `DOCS_ONLY`.

## تسلسل النداء (CTA hierarchy)

One primary CTA per page, chosen by intent tier:

```text
Cold  → Get Business OS Score   (/risk-score)
Warm  → Book Diagnostic         (/dealix-diagnostic)   ← free, rung 0
Hot   → Start Command Sprint    (/start, 499 SAR)
```

- The primary CTA is the most visually dominant action on the page.
- Secondary links (Trust, Proof, Pricing) are subordinate and never compete visually.
- Never put two equal-weight buyer CTAs on one page.

## تقليل الاحتكاك (Friction reduction)

- Let visitors see value (Score/tool result) before asking for anything.
- Free Diagnostic is the de-risk bridge to the 499 Sprint — lead with "free, no obligation."
- Make the price ladder visible and honest (no hidden costs, no fake discounts).
- Fast pages, Arabic-first, RTL-correct, mobile-first.

## تصميم النماذج (Form design)

| Rule | Why |
|------|-----|
| Ask only what you'll use *now* | Each field drops completion |
| Progressive disclosure | Get the email first, qualify later |
| Visible PDPL consent + purpose | Trust + compliance, not buried |
| Inline validation, Arabic error copy | Reduce abandonment |
| One clear submit = the page's single CTA | No ambiguity |

## عناصر الثقة (Trust elements — our edge)

Dealix converts on **trust**, not pressure:

- **Governance-first:** show "what we refuse" and how data is handled (`landing/trust.html`,
  `docs/growth/trust_page/`).
- **Approval-first:** state that no external message is auto-sent; the founder/operator approves.
- **Proof preview:** show an anonymized Proof Pack sample (`landing/sprint-sample.html`,
  `landing/proof.html`) — real evidence, never fabricated.
- **PDPL discipline** stated plainly.
- Claims are evidence-backed or hypothesis-framed; module status labels shown where relevant.

## ما نرفضه (Anti-patterns — banned)

- ❌ Fake scarcity / countdowns without a real deadline
- ❌ Fake testimonials, fake logos, fake "as seen in"
- ❌ Confirm-shaming opt-outs, hidden unsubscribe, forced continuity
- ❌ Guaranteed-revenue language
- ❌ Pre-checked consent boxes

## خطة 30 يوم (30-day plan)

1. Enforce one primary CTA on the top 10 pages (cross-check `WEBSITE_FUNNEL_MAP.md`).
2. Add a Proof Pack preview + governance trust block to the Diagnostic page.
3. Trim the Diagnostic form to minimum fields; add visible PDPL consent (test in E8).
4. Audit all pages for banned anti-patterns; remove any found.
5. Apply each shipped experiment winner (`GROWTH_EXPERIMENTS.md`) and re-verify with
   `proof-governance-reviewer` + `python scripts/verify_website_positioning.py`.
