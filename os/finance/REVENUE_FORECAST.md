# Revenue Forecast Template — قالب توقع الإيرادات

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [UNIT_ECONOMICS_TEMPLATE.md](UNIT_ECONOMICS_TEMPLATE.md) | [MARGIN_GUARDRAILS.md](MARGIN_GUARDRAILS.md) | [PRICING_RULES.md](PRICING_RULES.md) | [INVOICE_TRACKER_SCHEMA.json](INVOICE_TRACKER_SCHEMA.json)

---

## Rule — القاعدة

Update this forecast every Monday morning before the weekly pipeline review. "Committed" means a signed SOW and first payment received. "Probable" means a verbal agreement or proposal accepted verbally — not binding, but high confidence. "Pipeline" means everything else in active pursuit. Never book revenue as Committed before the SOW is signed.

حدّث هذا التوقع كل صباح اثنين قبل مراجعة خط المبيعات الأسبوعية. "ملتزم" يعني SOW موقّعاً ودفعة أولى مستلمة. "محتمل" يعني اتفاق شفهي أو اقتراحاً مقبولاً شفهياً — غير ملزم لكن ثقة عالية. "خط المبيعات" يعني كل شيء آخر في المسعى النشط. لا تُسجِّل إيرادات كـ"ملتزم" قبل توقيع SOW.

---

## 6-Month Rolling Forecast — التوقع المتداول لـ 6 أشهر

**Forecast period:** [YYYY-MM] to [YYYY-MM]
**Last updated:** [YYYY-MM-DD]
**Updated by:** [Founder]

### Definitions — التعريفات

| Category — الفئة | Definition — التعريف | Probability |
|---|---|---|
| **Committed** | Signed SOW + first payment received | 100% |
| **Probable** | SOW in review / verbal agreement / accepted proposal | > 70% |
| **Pipeline** | Active pursuit — discovery to proposal stage | < 70% |

---

### Forecast Table (SAR) — جدول التوقع

| Deal / Retainer | Type | [Month 1] | [Month 2] | [Month 3] | [Month 4] | [Month 5] | [Month 6] | Total |
|---|---|---|---|---|---|---|---|---|
| **COMMITTED** | | | | | | | | |
| [Deal A label] | Pilot | [SAR] | [SAR] | — | — | — | — | [SAR] |
| [Client B retainer] | Retainer | [SAR] | [SAR] | [SAR] | [SAR] | [SAR] | [SAR] | [SAR] |
| [Deal C label] | Audit | [SAR] | — | — | — | — | — | [SAR] |
| **Committed Subtotal** | | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** |
| | | | | | | | | |
| **PROBABLE** | | | | | | | | |
| [Deal D label] | Full System | — | [SAR] | [SAR] | [SAR] | — | — | [SAR] |
| [Deal E label] | Retainer | — | — | [SAR] | [SAR] | [SAR] | [SAR] | [SAR] |
| **Probable Subtotal** | | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** |
| | | | | | | | | |
| **PIPELINE** | | | | | | | | |
| [Deal F label] | Pilot | — | — | [SAR] | — | — | — | [SAR] |
| [Deal G label] | Audit | — | [SAR] | — | — | — | — | [SAR] |
| **Pipeline Subtotal** | | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** |
| | | | | | | | | |
| **TOTAL EXPECTED** | | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** | **[SAR]** |

---

## Monthly Summary — الملخص الشهري

**As of [YYYY-MM-DD]:**

| Metric — المقياس | Value — القيمة |
|---|---|
| MRR (Monthly Recurring Revenue — committed retainers) | [SAR] |
| ARR run rate (MRR × 12) | [SAR] |
| Total committed pipeline (next 6 months) | [SAR] |
| Total probable pipeline (next 6 months) | [SAR] |
| Weighted forecast (Committed + 70% of Probable) | [SAR] |
| Cash at hand (current bank balance) | [SAR] |
| Monthly operating costs (estimated) | [SAR] |
| Runway at current spend (months) | [N months] |

---

## Revenue Flags — تنبيهات الإيرادات

Review these flags weekly:

| Flag — التنبيه | Threshold — الحد | Status |
|---|---|---|
| No new committed deal this month | > 30 days with zero new signed SOWs | [ ] OK [ ] FLAG |
| Runway below 3 months | Cash / monthly costs < 3 | [ ] OK [ ] FLAG |
| Single client > 50% of committed revenue | Concentration risk | [ ] OK [ ] FLAG |
| Retainer at risk | Client expressed dissatisfaction or payment delayed > 14 days | [ ] OK [ ] FLAG |
| Probable deals stalled > 30 days | No movement from Probable to Committed | [ ] OK [ ] FLAG |

---

## Forecast Review Cadence — دورية مراجعة التوقع

| Frequency — التكرار | Action — الإجراء |
|---|---|
| Weekly (Monday) | Update committed + probable. Move deals that advanced or stalled. Review flags. |
| Monthly (first Monday) | Full 6-month roll-forward. Update MRR, ARR, runway. |
| Quarterly | Review forecast accuracy (predicted vs. actual). Identify pattern in forecast misses. |

---

## How to Treat Payment Timing — كيفية معالجة توقيت الدفع

- **Audit:** 100% in Month 1 (upfront). Book in the month payment is received.
- **Pilot (2-payment structure):** 50% in Month 1 (SOW signed), 50% in the delivery month.
- **Full System (3-payment):** 40% month of signing, 30% mid-point, 30% delivery month.
- **Retainer:** Monthly, recurring. Each month's value booked in that month.

Do not book revenue in the month the deal is verbally agreed — only in the month payment is received or contractually due.

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
