# Dealix — Margin Guardrails
# حواجز هامش الربح

**Version:** 1.0

---

## Margin Rules

| Rule | Value | Action if Violated |
|------|-------|-------------------|
| Minimum acceptable margin | 50% | Stop — re-price or re-scope before proceeding |
| Healthy margin target | 60-80% | Target for all projects |
| Floor price for any offer | See PRICING_GUARDRAILS.md | Never quote below floor |
| Retainer floor | 8,000 SAR/month | Never quote retainer below this |

---

## When Margin Falls Below 50%

1. Identify which cost category is driving it (API, contractor, infrastructure)
2. Can scope be reduced to restore margin?
3. Can API costs be optimized (prompt compression, model selection)?
4. If neither: escalate to founder decision before proceeding
5. Never proceed with a project expecting negative margin

---

## Margin by Offer Tier

| Category | Min Margin | Notes |
|----------|-----------|-------|
| Entry (Audit) | 60% | Low cost, high margin possible |
| Pilot | 55% | Some API costs, manageable |
| Vertical OS | 60% | Volume discounts on APIs reduce cost |
| Retainer | 70%+ | Mostly founder time — high margin |
| Expansion | 65%+ | Reuse existing infrastructure |

---

## Cost Control Principles

1. **API costs:** Use smaller models where sufficient. Don't use GPT-4o for every task.
2. **Contractor time:** Define clear scope before engaging contractors.
3. **Infrastructure:** Start with minimal infra — scale when clients pay for it.
4. **Tools:** Every tool subscription must be justified by a client project.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
