# Dealix Goal Tree — شجرة أهداف Dealix

**Purpose / الغرض**
Single-page tree that connects the existing North Star → strategic goals → operating metrics → machine metrics → daily actions. This doc does NOT redefine the North Star; it references the canonical definition in `docs/company/NORTH_STAR_METRICS.md`.
شجرة في صفحة واحدة تربط North Star الموجود → الأهداف الاستراتيجية → المقاييس التشغيلية → مقاييس الآلة → الإجراءات اليومية. لا يُعرَّف North Star هنا؛ المرجع `docs/company/NORTH_STAR_METRICS.md`.

**Owner placeholder:** `<founder>`
**Cadence:** Quarterly tree review. Weekly operating-metric refresh. / مراجعة فصلية للشجرة. تحديث أسبوعي للمقاييس التشغيلية.
**KPIs:** (1) North Star value (per canonical doc), (2) Strategic-goal status (on-track / drifting / off), (3) operating-metric freshness in days.
**Risk if missing / مخاطر الغياب:** Teams optimize a local metric that does not roll up. Daily work loses its line of sight to the North Star. / الفرق تحسّن مقياسًا محليًا لا يصبّ في الأعلى. العمل اليومي يفقد خطه إلى North Star.

---

## EN summary

The Dealix Goal Tree is a layered map. Each layer answers one question:

- **North Star** — what business outcome do we exist to produce?
- **Strategic goals** — what 3–5 multi-quarter bets compound toward the North Star?
- **Operating metrics** — what weekly/monthly numbers tell us a goal is moving?
- **Machine metrics** — what system numbers (latency, error rate, eval pass-rate) support the operating metrics?
- **Daily actions** — what does the team actually do this morning?

The rule: no goal exists in this tree unless it can be drawn to the North Star with a real arrow.

## ملخص بالعربية

شجرة الأهداف خريطة طبقية. كل طبقة تجيب على سؤال واحد:

- **North Star** — ما النتيجة التي نوجد لإنتاجها؟
- **الأهداف الاستراتيجية** — أي 3–5 رهانات متعددة الأرباع تتراكم نحو North Star؟
- **المقاييس التشغيلية** — أي أرقام أسبوعية/شهرية تخبرنا أن الهدف يتحرك؟
- **مقاييس الآلة** — أي أرقام نظام تدعم المقاييس التشغيلية؟
- **الإجراءات اليومية** — ماذا يفعل الفريق فعليًا هذا الصباح؟

القاعدة: لا يوجد هدف في الشجرة إن لم يمكن رسم سهم حقيقي منه إلى North Star.

---

## الشجرة (ASCII) / The tree

```
                          ┌────────────────────────────────────────────┐
                          │              NORTH STAR                    │
                          │ (canonical: docs/company/NORTH_STAR_METRICS.md) │
                          │ Client business workflows transformed into │
                          │ measurable AI operating systems            │
                          └─────────────────────┬──────────────────────┘
                                                │
        ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
        │                   │                   │                   │                   │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │  G1     │         │  G2     │         │  G3     │         │  G4     │         │  G5     │
   │ Paid    │         │ Proof   │         │ Trust   │         │ Founder │         │ Capital │
   │ delivery│         │ stack   │         │ surface │         │ leverage│         │ disci-  │
   │ depth   │         │ depth   │         │ depth   │         │         │         │ pline   │
   └────┬────┘         └────┬────┘         └────┬────┘         └────┬────┘         └────┬────┘
        │                   │                   │                   │                   │
   ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
   │ Operating│        │ Operating│        │ Operating│        │ Operating│        │ Operating│
   │ metrics  │        │ metrics  │        │ metrics  │        │ metrics  │        │ metrics  │
   │ ──────── │        │ ──────── │        │ ──────── │        │ ──────── │        │ ──────── │
   │ paid     │        │ proof    │        │ trust    │        │ leverage │        │ runway   │
   │ engage-  │        │ events   │        │ pack     │        │ score    │        │ months   │
   │ ments    │        │ /sprint  │        │ views    │        │          │        │          │
   │ /qtr     │        │          │        │          │        │          │        │          │
   │ rework % │        │ verified │        │ NPS on   │        │ founder  │        │ HourROI  │
   │          │        │ value    │        │ trust    │        │ rework % │        │ median   │
   │          │        │ rows     │        │ pages    │        │          │        │          │
   └────┬─────┘        └────┬─────┘        └────┬─────┘        └────┬─────┘        └────┬─────┘
        │                   │                   │                   │                   │
   ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
   │ Machine  │        │ Machine  │        │ Machine  │        │ Machine  │        │ Machine  │
   │ metrics  │        │ metrics  │        │ metrics  │        │ metrics  │        │ metrics  │
   │ ──────── │        │ ──────── │        │ ──────── │        │ ──────── │        │ ──────── │
   │ pipeline │        │ eval pass│        │ uptime,  │        │ approval │        │ unit     │
   │ latency, │        │ rate,    │        │ p95      │        │ queue    │        │ econ.    │
   │ run      │        │ red-team │        │ latency, │        │ depth,   │        │ per      │
   │ ledger   │        │ deltas   │        │ alerts   │        │ reply    │        │ sprint   │
   │ count    │        │          │        │          │        │ lag      │        │          │
   └────┬─────┘        └────┬─────┘        └────┬─────┘        └────┬─────┘        └────┬─────┘
        │                   │                   │                   │                   │
   ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
   │ Daily    │        │ Daily    │        │ Daily    │        │ Daily    │        │ Daily    │
   │ actions  │        │ actions  │        │ actions  │        │ actions  │        │ actions  │
   │ ──────── │        │ ──────── │        │ ──────── │        │ ──────── │        │ ──────── │
   │ ship 1   │        │ log 1    │        │ refresh  │        │ delegate │        │ review   │
   │ sprint   │        │ verified │        │ 1 trust  │        │ 1 task   │        │ spend    │
   │ step,    │        │ value    │        │ section, │        │ off the  │        │ vs       │
   │ close 1  │        │ row, run │        │ confirm  │        │ founder's│        │ budget,  │
   │ feedback │        │ 1 red-   │        │ all PII  │        │ plate,   │        │ flag     │
   │ loop     │        │ team     │        │ redacted │        │ log time │        │ over     │
   │          │        │ probe    │        │          │        │ audit    │        │ ceilings │
   └──────────┘        └──────────┘        └──────────┘        └──────────┘        └──────────┘
```

---

## الأهداف الخمسة بالكلام / The five goals in plain language

### G1 — Paid delivery depth / عمق التسليم المدفوع

Move from "we can deliver one sprint" to "we deliver multiple concurrent sprints at controlled rework". Owned by founder + Delivery Coordinator.
الانتقال من «نستطيع تنفيذ سبرنت واحد» إلى «ننفذ عدة سبرنتات بالتوازي بإعادة عمل مضبوطة».

### G2 — Proof stack depth / عمق طبقة الإثبات

Every paid engagement closes with verifiable evidence per `docs/07_proof_os/PROOF_PACK_STANDARD.md`. No claim ships without a proof row.
كل تسليم مدفوع يُغلق بأدلة قابلة للتحقق. لا ادعاء بدون صف إثبات.

### G3 — Trust surface depth / عمق سطح الثقة

Public trust pages compound. Every delivered engagement adds one referenceable section (with permission) to the trust pack.
صفحات الثقة العامة تتراكم. كل تسليم يضيف قسمًا قابلًا للإحالة (بإذن) إلى Trust Pack.

### G4 — Founder leverage / رافعة المؤسس

Founder hours migrate steadily from delivery into non-delegable strategic work. Tracked by `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`.
ساعات المؤسس تنتقل بثبات من التسليم إلى عمل استراتيجي غير قابل للتفويض.

### G5 — Capital discipline / انضباط رأس المال

Spend decisions go through `docs/operating_finance/CAPITAL_ALLOCATION_SCORE.md`. Runway is monitored monthly. No commitment exceeds three months of cash without board-level approval.
قرارات الإنفاق تمر عبر CAPITAL_ALLOCATION_SCORE. تُراقب الفترة الزمنية شهريًا. لا التزام يتجاوز ثلاثة أشهر من النقد دون موافقة بمستوى مجلس.

---

## قواعد المواءمة / Alignment rules

- لا يجوز إضافة هدف استراتيجي جديد دون حذف هدف قائم أو دمجه. الحد الأقصى 5 أهداف.
- كل مقياس تشغيلي يجب أن يكون مملوكًا لشخص واحد (دور).
- كل مقياس آلة يجب أن يكون له تنبيه آلي أو فحص أسبوعي مكتوب.
- كل إجراء يومي يجب أن يحدث فعلًا اليوم — وإلا لا يكتب كإجراء يومي.

> No new strategic goal is added unless an existing one is removed or merged. Hard cap at 5.
> Each operating metric has exactly one owner (role).
> Each machine metric has either an automated alert or a written weekly check.
> Each daily action must happen today, or it does not belong in this layer.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
This document does not introduce any new North Star metric. The canonical definition lives in `docs/company/NORTH_STAR_METRICS.md`.

## Related canonical docs

- `docs/company/NORTH_STAR_METRICS.md`
- `docs/company/KPI_SYSTEM.md`
- `docs/strategy/CEO_STRATEGY.md`
- `docs/company/OPERATING_SCORECARD.md`
- `docs/company/DEALIX_GRAND_STRATEGY.md`
- `docs/operating_finance/CAPITAL_ALLOCATION_SCORE.md`
- `docs/07_proof_os/PROOF_PACK_STANDARD.md`
