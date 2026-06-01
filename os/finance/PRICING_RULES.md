# Pricing Rules — قواعد التسعير

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [MARGIN_GUARDRAILS.md](MARGIN_GUARDRAILS.md) | [UNIT_ECONOMICS_TEMPLATE.md](UNIT_ECONOMICS_TEMPLATE.md) | [../sales/PRICING_GUARDRAILS.md](../sales/PRICING_GUARDRAILS.md) | [../governance/SOW_TEMPLATE.md](../governance/SOW_TEMPLATE.md)

---

## Purpose — الغرض

This file defines the complete Dealix pricing ladder, rules for setting and adjusting prices, and the relationship between price and margin. [../sales/PRICING_GUARDRAILS.md](../sales/PRICING_GUARDRAILS.md) covers the sales-facing rules (discounts, payment terms). This file covers the foundational pricing logic.

يحدد هذا الملف سلّم أسعار ديليكس الكامل وقواعد تحديد الأسعار وتعديلها والعلاقة بين السعر والهامش. يغطي [../sales/PRICING_GUARDRAILS.md](../sales/PRICING_GUARDRAILS.md) القواعد التجارية (الخصومات، شروط الدفع). هذا الملف يغطي منطق التسعير الأساسي.

---

## Complete Pricing Ladder — سلّم الأسعار الكامل

| Offer — العرض | Price Range | Structure | Duration | Min Margin Target |
|---|---|---|---|---|
| **AI Workflow Audit** | 5,000 – 25,000 SAR | Fixed price | 2–4 weeks | ≥ 65% |
| **Agentic Pilot** | 30,000 – 150,000 SAR | Scoped fixed price | 4–12 weeks | ≥ 55% |
| **Full Agentic System** | 150,000 – 750,000 SAR | Project-based (3 payments) | 3–9 months | ≥ 50% |
| **Monthly Retainer** | 8,000 – 80,000 SAR/month | Monthly recurring | Ongoing (min 3-month term) | ≥ 70% |
| **Expansion Module** | 25,000 – 250,000 SAR | Scoped fixed price | 4–8 weeks | ≥ 60% |

---

## Pricing Logic by Offer Type — منطق التسعير لكل نوع

### AI Workflow Audit — تدقيق سير العمل الذكي

**What drives price within the range:**
- Number of workflows assessed: 1-2 = 5,000–10,000 SAR; 3-5 = 10,000–20,000 SAR; 6+ = 20,000–25,000 SAR
- Output format: report only vs. report + interactive session + recommendations
- Sector complexity: standard sector = base price; highly regulated sector (legal, financial) = +15-20%

**Never price below 5,000 SAR.** Below this floor, the engagement takes more time than the revenue justifies.

### Agentic Pilot — التجريب الوكيلي

**Pricing inputs:**
1. Number of workflows automated (max 3 for pilot)
2. Complexity of data integration (API-ready = lower; manual export = higher)
3. Number of output formats and destinations
4. Timeline sensitivity (standard = base; rushed = +20% for compressed timeline)

**Scoping before pricing:** Do not price an Agentic Pilot before completing MVP Scope Template. Pricing before scoping is the most common cause of below-floor margins.

### Full Agentic System — النظام الوكيلي الكامل

**Pricing inputs:**
- All Pilot inputs above, scaled to fuller scope
- Number of team members and roles the system serves
- Integration complexity (number of systems connected)
- Ongoing maintenance requirements built into post-delivery retainer

**Large project risks:** Fixed-price projects > 300,000 SAR carry significant schedule risk. Consider milestone-based pricing with defined scope gates at each milestone.

### Monthly Retainer — الاستيعاب الشهري

**Retainer components (document each):**
- AI system operation and monitoring: [hours/month]
- System updates and maintenance: [hours/month]
- Client success check-in: [session/month]
- Priority support SLA: [response time]
- Capacity for minor additions: [hours/month — defined ceiling]

**Retainer term:** Minimum 3-month commitment. Cancel with 30 days' written notice after initial term.

### Expansion Module — وحدة التوسع

Priced identically to a new Pilot engagement — treat as a new scoped project. Do not underestimate because the client is familiar. Data integration complexity may be higher if expanding to a different system.

---

## Price-Setting Process — عملية تحديد السعر

**Step 1:** Complete MVP Scope Template — define what is being built.

**Step 2:** Complete Unit Economics Template — estimate all costs.

**Step 3:** Calculate target price from the bottom up:
```
Target price = Total direct costs / (1 - target margin %)
Example: Costs = SAR 15,000 | Target margin = 60%
Target price = 15,000 / (1 - 0.60) = SAR 37,500
```

**Step 4:** Compare to pricing ladder range — is the calculated price within range?

**Step 5:** Sanity-check against client budget signal (from discovery).

**Step 6:** Founder reviews and confirms before proposal is generated.

---

## Currency Rules — قواعد العملة

| Client Type | Currency | Conversion |
|---|---|---|
| GCC domestic clients | SAR | Primary |
| International clients (USD-preferred) | USD | 1 USD = 3.75 SAR (fixed peg) |
| International clients (EUR or GBP) | Quote in USD | Convert at current rate, document date of conversion in SOW |

**Rule:** Never quote two currencies simultaneously in the same proposal. Choose one and state it clearly in the payment section.

---

## What Never to Do — ما يُمنع فعله

These are non-negotiable pricing prohibitions:

| Prohibited — المحظور | Reason — السبب |
|---|---|
| Verbal price quote without written follow-up within 24 hours | Verbal quotes become anchor points with no documentation |
| "We'll figure out pricing later" | Price ambiguity creates budget disputes. Price before build. |
| Ballpark estimate before scoping | Uninformed estimates always anchor at values you cannot maintain |
| Discounting because the client pushed back verbally | Pressure-based discounts set a precedent and erode value perception |
| Fixed price with undefined data quality | Data quality risk is a margin killer on fixed-price contracts |
| "Payment on results" or contingency pricing | This implies guaranteed outcomes, which Dealix does not offer |
| Pricing below the ladder minimums | These minimums reflect real cost floors, not targets |

---

## Annual Pricing Review — المراجعة السنوية للأسعار

Review pricing ladder annually (Q1 each year):
- Compare LLM/API cost trends — have costs changed significantly?
- Review delivered project margins — are actual margins tracking to targets?
- Assess market — has competitor pricing shifted?
- Update pricing rules based on findings. Founder signs off on any range changes.

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
