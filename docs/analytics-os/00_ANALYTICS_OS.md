# Analytics OS — نظام التحليلات

The measurement system for the Dealix commercial motion. It defines every metric from first website visit to realized revenue, how each is captured, and how they roll up into weekly and board reports. No metric is fabricated; manual-entry metrics are marked as such.

نظام القياس لحركة ديليكس التجارية. يُعرّف كل مقياس من أول زيارة للموقع حتى الإيراد المُحقَّق، وكيف يُلتقط، وكيف يتجمّع في تقارير أسبوعية ومجلس إدارة. لا مقياس مُختلَق، والمقاييس اليدوية مُعلَّمة كذلك.

## Governing rule — القاعدة الحاكمة

**AI drafts, ranks, and recommends. Founder reviews, approves, and sends manually. The system never sends externally.**

Analytics measure this motion; they never trigger external sends.

## What this OS contains — مكوّنات النظام

| # | Document | Purpose |
|---|---|---|
| 00 | This file | Index and principles |
| 01 | [Event Taxonomy](01_EVENT_TAXONOMY.md) | Every metric: schema + capture method |
| 02 | [Dashboard Spec](02_DASHBOARD_SPEC.md) | Live dashboard layout |
| 03 | [Weekly Report Template](03_WEEKLY_REPORT_TEMPLATE.md) | Internal weekly review |
| 04 | [Monthly Board Report](04_MONTHLY_BOARD_REPORT.md) | Board-level summary |

## The funnel — القمع

Visitors → CTA clicks → audit requests → leads created → drafts generated → founder review → manual sends → replies → positive replies → booked diagnostics → paid diagnostics → pilots proposed → pilots sold → retainer starts → pipeline SAR → realized revenue SAR. Two safety counters run alongside: safety violations and compliance rejections.

## Principles — المبادئ

- **No invented numbers.** Templates ship with blank fields and `—` placeholders. Real values are entered manually or exported from ledgers.
- **Manual-entry is labeled.** Each metric in [01_EVENT_TAXONOMY.md](01_EVENT_TAXONOMY.md) is tagged `auto` or `manual`.
- **Safety is a top-line metric, not a footnote.** Safety violations and compliance rejections appear on every report.
- **SAR figures are pipeline or realized, never projected as fact.**

## Forbidden — ممنوع

No "guaranteed ROI", "100%", "replace your team", "automate everything", "no human needed", or fabricated urgency in any chart, caption, or report.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
