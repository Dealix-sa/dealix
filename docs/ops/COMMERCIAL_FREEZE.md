# Commercial Freeze | تجميد لصالح السوق

**Status:** LIFTED (2026-05-18)
**Started:** 2026-05-16  ·  **Lifted:** 2026-05-18
**Exit condition (original):** first paid pilot delivered + customer-approved Proof Pack (L3+).

---

## Lift | رفع التجميد

**Lifted:** 2026-05-18 — by founder decision.

The freeze is lifted **ahead of its original exit condition**: at the time of
lifting, no paid pilot had been delivered and no customer-approved Proof Pack
(L3+) existed. The founder elected to resume building — specifically the
comprehensive Full-Ops system and agent layer — as a deliberate, recorded
override of the freeze.

The original doctrine rationale (preserved below) still stands as a **recorded
caution**: every hour spent building instead of selling has negative expected
value until the first paid pilot proves the motion. This caution was considered
and overridden by founder decision. Recorded in
[`docs/ledgers/DECISION_LEDGER.md`](../ledgers/DECISION_LEDGER.md) as **D-003**.

**The 11 non-negotiables remain fully in force.** The lift removes the *build
freeze* only — it does not relax any guard: no live send, no live charge, no
scraping, no cold outreach, no LinkedIn automation, no fake proof, and
approval-required for every external action all still apply.

رُفع التجميد بقرار المؤسّس بتاريخ 2026-05-18، **قبل** تحقّق شرط الخروج الأصلي
(لم يُسلَّم أي Pilot مدفوع بعد). المؤسّس اختار استئناف البناء — تحديدًا نظام
Full-Ops وطبقة الوكلاء — كتجاوز موثَّق ومقصود. التحذير الأصلي (البناء بدل البيع
= عائد متوقَّع سالب) يبقى مُسجَّلًا. **الحرّاس الـ11 سارية بالكامل** — الرفع
يلغي تجميد البناء فقط ولا يخفّف أي حارس.

---

## Original freeze record | السجل الأصلي للتجميد (history)

> The section below is the freeze as it stood from 2026-05-16 to 2026-05-18.
> Retained for audit history. No longer in force.

### Why | لماذا

The platform is shipped and verified. The constraint on revenue is no longer
code — it is **founder-led selling**. Every hour spent building instead of
selling now has negative expected value. This freeze redirects all effort from
*building* to *operating and selling*, until the first paid pilot proves the
motion.

المنصة جاهزة ومُتحقَّق منها. القيد على الإيراد لم يَعُد الكود — بل **البيع
بقيادة المؤسس**. هذا التجميد يحوّل كل الجهد من *البناء* إلى *التشغيل والبيع*،
حتى يُثبت أول Pilot مدفوع أن الحركة تعمل.

### Scope of the freeze | نطاق التجميد

The freeze covered **rungs 2–5** of the offer ladder. Rungs 3–5 (Managed Ops,
Command Center, Partner OS) are *marketed* but today delivered as
founder-assisted tooling, not fully managed services. Rung 2 (the 1,500 SAR
Data-to-Revenue Pack) was also frozen — it received **no** delivery-finish
exception. The rung 0–1 delivery finish was explicitly permitted.

### Frozen — do NOT do during the freeze | مُجمَّد

- ❌ No new feature PRs for **rungs 2–5**.
- ❌ No new product/architecture docs.
- ❌ No Board OS v2, no new `*_os` modules unrelated to rung 0–1 delivery.
- ❌ No new API routers or endpoints for **rungs 2–5**.
- ❌ No frontend redesign or polish.
- ❌ No new dashboards.

### Allowed — the only work that shipped | مسموح

- ✅ Founder-led selling: warm-list outreach, partner follow-ups, meetings.
- ✅ Market-motion artifacts (the founder's sales tools — see `docs/sales-kit/`).
- ✅ **Rung 0–1 delivery finish**: customer-facing rendered (HTML/PDF) Proof Pack
  and Diagnostic report, the payment→delivery audit link, and the doctrine
  hotfixes that support them.
- ✅ Delivery of a signed pilot + Proof Pack assembly.
- ✅ Production hotfixes and CI hygiene only (P0/P1).
- ✅ Recording to the ledgers (`docs/ledgers/`).

### Exit | الخروج من التجميد

The freeze was to end when **one paid pilot is delivered and its Proof Pack is
customer-approved (evidence level L3 or above)**. It was instead lifted early by
founder decision on 2026-05-18 (see **Lift** section above).
