# Margin Guardrails — حواجز هامش الربح

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [UNIT_ECONOMICS_TEMPLATE.md](UNIT_ECONOMICS_TEMPLATE.md) | [PRICING_RULES.md](PRICING_RULES.md) | [../sales/PRICING_GUARDRAILS.md](../sales/PRICING_GUARDRAILS.md) | [../governance/SOW_TEMPLATE.md](../governance/SOW_TEMPLATE.md)

---

## Margin Decision Framework — إطار قرار الهامش

These thresholds apply before signing any SOW. Calculate gross margin using [UNIT_ECONOMICS_TEMPLATE.md](UNIT_ECONOMICS_TEMPLATE.md) and compare to the thresholds below.

تسري هذه الحدود قبل توقيع أي SOW. احسب هامش الربح الإجمالي باستخدام قالب الاقتصاديات الوحدوية وقارنه بالحدود التالية.

| Margin — الهامش | Classification — التصنيف | Action — الإجراء |
|---|---|---|
| **≥ 70%** | Excellent — ممتاز | Priority project. Proceed immediately. |
| **50% – 69%** | Healthy — جيد | Proceed as planned. Standard monitoring. |
| **35% – 49%** | Review — مراجعة | Founder reviews scope and cost assumptions before SOW is signed. Identify which cost line is compressing margin and whether it can be adjusted. |
| **< 35%** | STOP — توقف | Do not sign. Reprice or reduce scope to restore margin above 35% floor. No exceptions without founder written approval and documented rationale. |

---

## Hard Stop — التوقف الصارم

**Margin < 35% → Do not start without repricing.**

If a project in progress is discovered to have fallen below 35% margin (due to scope creep, cost overrun, or timeline extension without a CR), the following steps apply:

إذا اكتُشف أن مشروعاً قيد التنفيذ انخفض هامشه تحت 35% (بسبب توسع النطاق أو تجاوز التكاليف أو تمديد الجدول الزمني بدون CR):

1. Pause any new work that is not covered by the original SOW.
2. Calculate the actual margin erosion and its source.
3. Notify founder immediately.
4. Raise a Change Request for the additional scope/cost if applicable.
5. If the client will not approve a CR — document the decision and assess whether the project is viable to complete at the current terms.

---

## Cost Tracking Categories — فئات تتبع التكاليف

All costs are tracked against these categories. Every cost recorded in [UNIT_ECONOMICS_TEMPLATE.md](UNIT_ECONOMICS_TEMPLATE.md) maps to one of these.

| Category — الفئة | Description — الوصف | Notes |
|---|---|---|
| LLM API calls | Cost of all AI model API calls consumed by the project | Track per project, per model |
| Cloud hosting | Compute, storage, and networking costs for this project | Pro-rate shared infrastructure |
| Third-party tools | SaaS tools, libraries, or platforms used for this project | Per-project allocation only |
| Contractor hours | Hours billed by any contracted delivery resource | Rate × hours actually worked |
| Founder hours | Founder time at target hourly rate | Use consistent rate; do not omit |

**Founder hours are always included.** Excluding founder time produces phantom margins that misrepresent real project economics.

---

## Margin Killers — قاتلات الهامش

These patterns account for the majority of below-floor margin outcomes. Monitor for each on every project.

### Margin Killer 1 — Scope Creep Without a CR

**What it looks like:** "Can you just add one more field to the report?" / "We'd like to include a second workflow while you're at it."

**Why it kills margin:** Every unscoped addition adds hours and API costs that are not reflected in the contract price. Individually small. Cumulatively devastating.

**Mitigation:** No scope addition begins without a signed Change Request. Train clients on this from the first project kick-off call.

---

### Margin Killer 2 — Fixed Price With Undefined Data Quality

**What it looks like:** Client says "our data is clean" in discovery. On intake, data has 40% null fields, inconsistent date formats, and duplicate records.

**Why it kills margin:** Data cleaning adds days to build time. On a fixed-price contract, this cost falls entirely on Dealix.

**Mitigation:** Always require a sample data review before scoping. Add a data quality assumption to the SOW. If data is worse than assumed — raise a CR.

---

### Margin Killer 3 — Client-Side Delays That Extend Timeline

**What it looks like:** Client takes 3 weeks to provide API access. Project timeline slides. Hosting costs accumulate. Founder spends hours chasing approvals.

**Why it kills margin:** Timeline extension without additional revenue means fixed costs accrue longer. Retainer-style engagements are most exposed.

**Mitigation:** SOW includes client responsibility timeline (data access, UAT reviewer allocation). If client delays cause timeline extension, raise a CR for the additional project management time.

---

### Margin Killer 4 — Underestimating LLM Costs for Complex Documents

**What it looks like:** Scoped the project assuming standard-length documents. Client's actual documents are 50+ pages each. API costs 5× the estimate.

**Why it kills margin:** LLM API costs scale with input length. Underestimated volume at scoping = cost overrun.

**Mitigation:** Always request a sample of the actual documents at scoping. Estimate API costs on the largest documents, not the average.

---

### Margin Killer 5 — Missing the Maintenance Cost in Retainer Pricing

**What it looks like:** Retainer priced based on initial build complexity. After go-live, the system requires 3× more maintenance hours than estimated (client requests changes, model updates, edge case handling).

**Why it kills margin:** Retainer price was set at the wrong baseline. Maintenance hours are open-ended.

**Mitigation:** Retainer scope includes a defined ceiling for minor changes (e.g., "up to 4 hours/month of minor modifications included"). Anything above the ceiling = CR or retainer repricing at renewal.

---

## Monthly Margin Review — المراجعة الشهرية للهامش

At the end of each month, compare estimated margin (from Unit Economics at contract signing) to actual margin (based on actual costs incurred):

| Project | Estimated Margin | Actual Costs (MTD) | Actual Margin (MTD) | Delta | Flag? |
|---|---|---|---|---|---|
| [Label] | [%] | [SAR] | [%] | [+/-] | [ ] Y [ ] N |

**If actual margin is more than 10 points below estimated margin:** Identify the cause. Raise a CR if scope-driven. Adjust cost estimates for future similar projects.

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
