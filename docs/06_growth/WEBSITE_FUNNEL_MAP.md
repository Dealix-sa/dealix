# Website Funnel Map — خريطة المسار

> Visitor → Page → CTA → Next step, across the real surfaces: `landing/` (static HTML) and
> `frontend/[locale]` (Next.js, RTL). **One primary CTA per page** (CLAUDE.md hard rule).
> Status: `DOCS_ONLY` strategy spec.

## مستويات النية (Intent tiers → CTA)

| Tier | Visitor mindset | Primary CTA |
|------|-----------------|-------------|
| Cold | "What is this?" | Get Business OS Score |
| Warm | "I have this pain" | Book Diagnostic |
| Hot | "I'm ready to act" | Start Command Sprint (499) |

## الخريطة (Page → CTA → Next step)

| Page | Surface | Visitor intent | Primary CTA | Next step |
|------|---------|----------------|-------------|-----------|
| Launch home / `index` | `landing/index.html` · `frontend/[locale]` | Cold | **Get Business OS Score** | `/risk-score` |
| Business OS Score | `frontend/[locale]/risk-score` | Cold→Warm | **Book Diagnostic** | `/dealix-diagnostic` |
| Diagnostic | `frontend/[locale]/dealix-diagnostic` · `landing/diagnostic.html` | Warm | **Start Command Sprint** | `/start` |
| Sprint start | `landing/start.html` | Hot | **Start Command Sprint (499)** | checkout |
| Sprint sample | `landing/sprint-sample.html` | Warm | **Start Command Sprint** | `/start` |
| Proof Pack | `frontend/[locale]/proof-pack` · `landing/proof.html` | Warm | **Book Diagnostic** | `/dealix-diagnostic` |
| Learn / article | `frontend/[locale]/learn/[slug]` · `landing/blog/` | Cold→Warm | **Get Business OS Score** | `/risk-score` |
| Sector page | `landing/diagnostic-real-estate.html`, `verticals.html` | Warm | **Book Diagnostic** | `/dealix-diagnostic` |
| Free tools | `landing/free-tools/`, `roi.html`, `ltv-calculator.html` | Cold→Warm | **Book Diagnostic** | `/dealix-diagnostic` |
| Partners | `frontend/[locale]/partners` · `landing/partners.html` | Partner | **Apply to partner program** (partner CTA, not the 3 buyer CTAs) | partner form |
| Academy | `landing/academy.html` | Cold | **Get Business OS Score** | `/risk-score` |
| Trust / Trust Center | `landing/trust.html`, `trust-center.html` | Warm (objection-handling) | **Book Diagnostic** | `/dealix-diagnostic` |
| Pricing | `landing/pricing.html` | Hot | **Start Command Sprint** | `/start` |

> Partner pages carry a **partner-program** CTA, the one allowed exception to the 3 buyer CTAs.
> Everything else uses exactly one of Score / Diagnostic / Sprint.

## منطق التدرّج (Ladder logic)

Score (lowest friction) catches cold traffic and hands them to Diagnostic. Diagnostic (rung 0,
free) qualifies pain and hands the ready to the 499 Sprint. Proof, Learn, Trust and Sector pages
exist to **de-risk** the jump, each pushing back to the nearest appropriate rung — never skipping
a buyer straight from a blog post to checkout.

## حواجز (Guardrails)

- One H1-level primary CTA per page; secondary links must be visually subordinate.
- No exit-intent fake scarcity, no countdown timers without a real deadline.
- Sector/proof claims must link to a Proof Pack or be hypothesis-framed.

## خطة 30 يوم (30-day plan)

1. Inventory every live page and record its single primary CTA in this table; flag violations.
2. Remove or demote competing CTAs on the top 10 trafficked pages.
3. Verify Score → Diagnostic → Sprint links resolve on both `landing/` and `frontend/`.
4. Add Trust and Proof Pack as objection-handling waypoints linked from Diagnostic.
5. Run `python scripts/verify_website_positioning.py` and fix flagged CTA conflicts.
