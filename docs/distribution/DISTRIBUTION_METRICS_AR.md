# مقاييس التوزيع — Dealix Distribution Metrics

هذا الملف يحدّد **مؤشرات الأداء اليومية والأسبوعية** لمنظومة التوزيع. الأرقام أهداف ومقاييس داخلية، **لا وعود للعميل ولا ضمانات**.

This file defines the **daily and weekly KPIs** for the distribution system. Numbers are internal targets and measures — **not customer promises or guarantees**.

روابط / Related: [REVENUE_EXECUTION_OS_AR.md](REVENUE_EXECUTION_OS_AR.md) · [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md) · [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md) · [WIN_LOSS_LEARNING_AR.md](WIN_LOSS_LEARNING_AR.md) · [../commercial/NORTH_STAR_METRICS_AR.md](../commercial/NORTH_STAR_METRICS_AR.md)

> هذا الملف خاص بقمع التوزيع. للمقاييس التشغيلية الأشمل (إيراد/تسليم/حوكمة) راجع [../commercial/NORTH_STAR_METRICS_AR.md](../commercial/NORTH_STAR_METRICS_AR.md). / This file covers the distribution funnel; for broader operational metrics see North Star.

---

## المؤشرات اليومية / Daily KPIs

| المؤشر / KPI | التعريف / Definition | المصدر / Source |
|---|---|---|
| عملاء جدد مؤهَّلون / New qualified | عدد الانتقالات `new → qualified` اليوم. / Count of `new → qualified` today. | `prospect.status` |
| مسودات جاهزة / Drafts ready | مسودات بلغت `ready` وتنتظر موافقة. / Drafts reaching `ready`. | `draft.status` |
| موافقات اليوم / Approvals today | مخرجات بلغت `approved`. / Items reaching `approved`. | `governance_status` |
| تواصل تم / Contacts made | متابعات/رسائل بلغت `sent` بعد موافقة. / Items reaching `sent` after approval. | `followup.status` |
| ردود / Replies | عملاء بلغوا `replied`. / Prospects reaching `replied`. | `prospect.status` |
| متابعات مستحقة / Follow-ups due | عدد `followup.due_date = today`. / Follow-ups due today. | `followup.due_date` |
| مخاطر مفتوحة / Open risks | سجلات بـ`risk` غير مغلق. / Records with an open risk. | `prospect.risk` / `followup.risk` |

> هدف يومي: صفر مخالفات جودة عالقة، وصفر إرسال بلا موافقة. / Daily target: zero stuck quality violations, zero send without approval.

---

## المؤشرات الأسبوعية / Weekly KPIs

| المؤشر / KPI | التعريف / Definition | المصدر / Source |
|---|---|---|
| تأهيل القمع / Qualification rate | `qualified / new` خلال الأسبوع. / Weekly qualified over new. | `prospect.status` |
| اكتشافات محجوزة / Discoveries booked | عدد `discovery_booked`. / Count reaching `discovery_booked`. | `prospect.status` |
| عروض مُرسَلة / Proposals sent | عدد `proposal_sent`. / Count reaching `proposal_sent`. | `proposal.approval_status` |
| تسليمات للدفع / Payment handoffs | عدد `ready_for_handoff`. / Count reaching ready for handoff. | `payment_handoff.status` |
| مكاسب / Wins | عدد `won`. / Count reaching `won`. | `win_loss.outcome` |
| خسائر / Losses | عدد `lost` مع أسبابها. / Count reaching `lost` with reasons. | `win_loss.outcome` |
| تجديدات مؤكَّدة / Renewals confirmed | عدد `renewal.status = confirmed`. / Confirmed renewals. | `renewal.status` |
| توزيع مستوى الدليل / Evidence-level mix | توزيع `evidence_level` عبر العروض. / Distribution across proposals. | `proposal.evidence_level` |
| اعتراضات متكرّرة / Recurring objections | أبرز `objection` من Win/Loss. / Top objections from win/loss. | `win_loss.objection` |

> تُقرأ هذه المؤشرات مع الأسئلة الأسبوعية في [WIN_LOSS_LEARNING_AR.md](WIN_LOSS_LEARNING_AR.md). / Read alongside the weekly questions in win/loss learning.

---

## مؤشرات حوكمة لا تُساوَم / Non-negotiable governance signals

| المؤشر / Signal | الهدف / Target |
|---|---|
| إرسال خارجي بلا موافقة / Sends without approval | صفر / Zero |
| حوادث PII في السجلات / PII incidents in logs | صفر / Zero |
| ادعاءات بلا مستوى دليل / Claims without an evidence level | صفر / Zero |
| أسعار خارج الحدود / Out-of-band prices | صفر / Zero |
| استخدام قناة محظورة / Forbidden-channel use | صفر / Zero |

> أي قيمة غير صفرية في الجدول أعلاه = حادث حوكمة يُراجَع فوراً. / Any non-zero value above is a governance incident to review immediately.

---

## قواعد ملزمة / Binding rules

1. كل مؤشر مشتق من حقل كيان قائم؛ لا أرقام مخترَعة. / Every KPI derives from an existing entity field; no invented numbers.
2. الأرقام أهداف داخلية لا وعود للعميل. / Numbers are internal targets, not customer promises.
3. لا PII في أي تقرير مقاييس. / No PII in any metrics report.
4. مؤشرات الحوكمة هدفها صفر دائماً. / Governance signals always target zero.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
