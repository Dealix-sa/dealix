# CEO Not-Now List — قائمة "ليس الآن"

## Purpose
The founder's explicit list of what NOT to build, hire, market, or commit to right now. Pre-proof investments destroy runway and dilute focus. This list is read every Monday before the CEO master dashboard.

## Owner
Founder. List modified only by founder with written rationale.

## Inputs
- Current proof gate from `docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md`.
- Cash and runway snapshot.
- `docs/product/NO_OVERBUILD_POLICY.md`.
- `docs/people/HIRING_TRIGGERS.md`.

## Outputs
- This list.
- Auto-Kill flag for any feature intake matching the list.

## The Not-Now List

### Products
1. **Full multi-tenant SaaS platform** — not before 10 automated runs of one workflow.
2. **Mobile app (native or hybrid)** — not before any web product earns retention.
3. **White-label / reseller portal** — not before 5 manual partner deals proven.
4. **Enterprise admin / RBAC console** — not before 3 enterprise contracts demand it in writing.
5. **Agent marketplace, agent catalogue, agent expansion** — not before 1 agent earns its keep on paid work.
6. **Public LLM gateway product** — not before internal usage demonstrates margin.

### Sales / Marketing
7. **Long-form pitch deck (>10 slides)** — not before Phase 3 (Proof of Delivery) is passed.
8. **Paid advertising at scale** — not before unit economics are verified.
9. **Conferences and sponsorships** — not before sector report cadence is established (1+ published).
10. **Outbound automation, cold WhatsApp, LinkedIn bots, scraping** — never; this is not a "not now" but a permanent refusal.

### Hiring
11. **Full-time hires before triggers fire** (`docs/people/HIRING_TRIGGERS.md`).
12. **Sales leader** — not before founder has personally closed 10 deals.
13. **Engineering full-time** — not before 1 SaaS candidate passes the gate.
14. **Agency to do delivery** — not before founder has run 5 sprints in person.

### Investor
15. **Series A pitching** — not before all four proof gates are passed.
16. **Angel sweep** — not before 1 signed SOW + 1 verified delivery + 1 written feedback.
17. **Accelerator applications** — only if they materially serve a named proof gate.

### Operational
18. **Custom UI design system / branded component library** — not before 3 paying customers see the same UI.
19. **Office space (beyond a desk)** — not before team > 3 and revenue justifies.
20. **International expansion** — not before Saudi proof gates passed and Saudi book stable.

## Rules
1. The founder reads this list aloud at every Monday master dashboard review.
2. Removing an item requires a written rationale signed and dated.
3. Adding an item is easy and welcomed; the list grows when temptation grows.
4. Any feature intake matching this list is auto-Killed in `docs/product/BUILD_DEFER_KILL.md`.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to estimated savings from saying no.
6. The list is visible on the CEO master dashboard summary panel.

## Metrics
- Items added per quarter (signals discipline).
- Items removed per quarter (target 0-2; high removal signals weak discipline).
- Intakes auto-Killed by the list (count).
- Founder hours saved (estimated, labelled).

## Cadence
- Read every Monday.
- Quarterly review.

## Evidence
- `evidence/founder/not-now/<YYYY-Qn>_review.md`.

## Verifier
Founder.

## Runtime Command
`make not-now-read` — prints the list at the top of every Monday review, refuses to close the review without acknowledgment.

## Arabic Summary — ملخص عربي
قائمة ما لن نبنيه أو نوظفه أو نروج له الآن: منتج SaaS كامل، تطبيق جوال، بوابة شركاء، إدارة مؤسسات، توسعة وكلاء، أتمتة خارجية محظورة دائمًا، توظيف قبل المُحفِّزات، تمويل قبل بوابات الإثبات، اتساع دولي مبكر. تُقرأ كل اثنين. القيم التقديرية ليست مُتحقَّقة.
