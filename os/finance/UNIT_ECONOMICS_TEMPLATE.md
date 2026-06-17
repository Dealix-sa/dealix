# Unit Economics Template — قالب الاقتصاديات الوحدوية

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [MARGIN_GUARDRAILS.md](MARGIN_GUARDRAILS.md) | [PRICING_RULES.md](PRICING_RULES.md) | [REVENUE_FORECAST.md](REVENUE_FORECAST.md) | [INVOICE_TRACKER_SCHEMA.json](INVOICE_TRACKER_SCHEMA.json)

---

## Rule — القاعدة

Calculate unit economics for every project before signing the SOW. A project with an unknown or below-floor margin does not proceed without founder review.

احسب الاقتصاديات الوحدوية لكل مشروع قبل توقيع SOW. أي مشروع بهامش مجهول أو دون الحد الأدنى لا يُمضَى قدماً دون مراجعة المؤسس.

---

## Calculation Template — نموذج الحساب

### Project Identification — تعريف المشروع

| Field — الحقل | Value — القيمة |
|---|---|
| Project label | [PROJECT_LABEL] |
| Offer type | [Audit / Pilot / Full System / Retainer / Expansion] |
| SOW reference | [SOW-YYYY-NNN] |
| Contract value | [SAR] |
| Duration | [Days / Months] |
| Calculation date | [YYYY-MM-DD] |

---

### Revenue and Cost Breakdown — تفاصيل الإيرادات والتكاليف

```
REVENUE
────────────────────────────────────
Contract value (excl. VAT):         [SAR __________]

DIRECT COSTS — التكاليف المباشرة
────────────────────────────────────
LLM / AI API costs:                 [SAR __________]
  (Estimated calls × cost per call)
  Estimated calls:       [N calls]
  Cost per 1K calls:     [SAR ____]
  Total:                 [SAR ____]

Cloud / hosting costs:              [SAR __________]
  (Monthly cost × project months)
  Monthly cost:          [SAR ____]
  Months:                [N]
  Total:                 [SAR ____]

Third-party tools & licenses:       [SAR __________]
  (Per-project allocations only)

Contractor hours × rate:            [SAR __________]
  Hours:                 [N hours]
  Rate:                  [SAR ____/hr]
  Total:                 [SAR ____]

Founder hours × target rate:        [SAR __________]
  Hours:                 [N hours]
  Target rate:           [SAR 800/hr minimum]
  Total:                 [SAR ____]

────────────────────────────────────
TOTAL DIRECT COSTS:                 [SAR __________]

────────────────────────────────────
GROSS MARGIN:                       [SAR __________]
GROSS MARGIN %:                     [  %          ]
────────────────────────────────────
```

---

### Margin Assessment — تقييم الهامش

Reference [MARGIN_GUARDRAILS.md](MARGIN_GUARDRAILS.md) for thresholds.

| Margin Range | Classification | Action |
|---|---|---|
| ≥ 70% | Excellent | Priority project — proceed |
| 50% – 69% | Healthy | Proceed as planned |
| 35% – 49% | Review | Founder reviews scope before signing |
| < 35% | Stop | Do not sign without repricing or scope reduction |

**This project's margin: [  %] — Classification: [___________]**

**Decision required before signing:**
- [ ] Margin ≥ 50% — proceed
- [ ] Margin 35-49% — founder scope review before signing
- [ ] Margin < 35% — STOP — reprice or reduce scope

---

### Margin Sensitivity Check — فحص حساسية الهامش

What happens to margin if costs increase by 20%?

```
Costs at +20%:                      [SAR __________]
Revised gross margin:               [SAR __________]
Revised margin %:                   [  %          ]
Still above 35% floor?              [ ] Yes  [ ] No
```

If the sensitivity check drops below 35% floor, the project carries significant margin risk and requires additional scope controls or a contingency buffer.

---

### Retainer Unit Economics — اقتصاديات الاستيعاب الشهري

For retainer engagements, calculate monthly:

```
MONTHLY RETAINER REVENUE:           [SAR __________]

Monthly costs:
  LLM/API (monthly estimate):       [SAR __________]
  Hosting (pro-rated):              [SAR __________]
  Tool licenses (pro-rated):        [SAR __________]
  Support hours (hrs × rate):       [SAR __________]
  Founder oversight (hrs × rate):   [SAR __________]
──────────────────────────────────
TOTAL MONTHLY COSTS:                [SAR __________]
MONTHLY GROSS MARGIN:               [SAR __________]
MONTHLY MARGIN %:                   [  %          ]
```

Healthy retainer margin target: ≥ 70%. Review if below 60%.

---

### Healthy Margin Targets by Offer Type — أهداف الهامش الصحية

| Offer Type | Target Margin | Minimum Floor |
|---|---|---|
| AI Workflow Audit | ≥ 65% | 40% |
| Agentic Pilot | ≥ 55% | 35% |
| Full Agentic System | ≥ 50% | 35% |
| Monthly Retainer | ≥ 70% | 50% |
| Expansion Module | ≥ 60% | 40% |

---

### LLM Cost Estimation Guide — دليل تقدير تكاليف LLM

For project estimation, use these input/output cost ranges as a planning baseline. Actual costs depend on model selection and usage patterns. Track and update per project.

| Model Class | Use Case | Estimated Cost per 1K tokens | Notes |
|---|---|---|---|
| Large reasoning model | Complex document analysis | [SAR ____] | High cost — use selectively |
| Standard model | Classification, drafting | [SAR ____] | General use |
| Small/fast model | Simple extraction, routing | [SAR ____] | High volume, low unit cost |
| Embedding model | Vector search, RAG | [SAR ____] | Per document indexed |

*Update these rates from actual API billing monthly.*

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
