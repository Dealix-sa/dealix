# Founder Leverage Dashboard — لوحة رافعة المؤسس

**الغرض / Purpose**
لوحة أسبوعية تبيّن ما يصنعه المؤسس بنفسه مقابل ما يُفوَّض. الهدف رفع نسبة الوقت في أعمال غير قابلة للتفويض دون كسر الجودة.
A weekly view of what the founder ships himself vs what he delegates. Goal: raise time-in-non-delegable work without breaking quality.

**Owner placeholder:** `<founder>`
**Cadence:** كل يوم أحد، 30 دقيقة / Every Sunday, 30 minutes.
**KPIs:** (1) Leverage Score (0–100), (2) ساعات المؤسس المباشرة في عمل غير قابل للتفويض / Founder hours in non-delegable work, (3) Anti-bottleneck signal count.
**Risk if missing / مخاطر الغياب:** المؤسس يصبح عنق الزجاجة دون أن يلاحظ. النمو يتوقف عند سعة شخص واحد. The founder silently becomes the bottleneck; growth caps at one person's capacity.

---

## ملخص بالإنجليزية / EN summary

The Leverage Dashboard measures three things every week:

1. **Where founder hours went** — by category (revenue-direct, customer, building, delegation, learning, personal).
2. **What got delegated and stuck** — items handed off that came back unfinished or required founder rework.
3. **Anti-bottleneck signals** — queue depth on approvals, reply lag, decision-log gaps.

If the score drops two weeks in a row, the founder pauses one external commitment and runs the bottleneck-removal playbook in `docs/people/FOUNDER_BOTTLENECK_REMOVAL.md`.

---

## معادلة درجة الرافعة / Leverage Score formula

```
Leverage Score = 100 × (NDH / TFH) − P − Q

NDH = Non-Delegable Hours
      (هذه فقط: قرارات استراتيجية، تسعير، اعتماد عميل، رسائل مفتاحية،
       حوار توظيف للأدوار الأولى، توقيع عقود)
TFH = Total Founder Hours (تشمل كل ساعة عمل مسجّلة في تدقيق الوقت)
P   = عقوبة عنق الزجاجة (Bottleneck penalty)
       = 5 × (count of approval items waiting > 24h)
Q   = عقوبة الجودة (Quality penalty)
       = 10 × (count of delivered items that needed founder rework)
```

- درجة 80+ = صحية.
- 60–79 = راقب.
- < 60 = أوقف التزامًا خارجيًا واحدًا، شغّل playbook إزالة عنق الزجاجة.

> 80+ healthy. 60–79 watch. < 60 stop one external commitment and run the bottleneck-removal playbook.

---

## ما يصنعه المؤسس بنفسه (Things only the founder can do)

### AR

- صياغة وعد المنتج (Positioning) وتغيير اللغة المركزية.
- اعتماد سعر غير قياسي يتجاوز عتبة `docs/company/PRICING_DECISION.md`.
- موافقة على عقد عميل، شراكة، أو استثناء حوكمي.
- المحادثة الأولى مع المشتري الاقتصادي في صفقة Enterprise.
- توظيف أول شخص في أي دور جديد.
- اعتماد رواية شهرية للمستثمر/المجلس.
- اتخاذ قرار "نقول لا" لقطاع أو عميل.

### EN

- Authoring positioning and changing core language.
- Approving non-standard pricing beyond the threshold in `docs/company/PRICING_DECISION.md`.
- Signing customer contracts, partnerships, or governance exceptions.
- First conversation with the economic buyer on an enterprise deal.
- First hire into any new role.
- Approving the monthly investor/board narrative.
- Saying "no" to a sector or a customer.

---

## ما يجب أن يُفوَّض (Things that must be delegated)

### AR

- إعداد بيانات SOQL/تنظيف ملفات → Data Ops Assistant.
- تنسيق المقترحات / تصميم PDF → Sales Asset Designer.
- متابعة جدولة العروض → RevOps Assistant.
- بحث القطاع وتجميع قوائم ICP → Saudi B2B Researcher.
- صياغة المنشورات بعد إقرار الرسالة من المؤسس → Growth Operator.
- مراجعة جودة المخرجات → Trust/QA Reviewer.

### EN

- Data prep, file hygiene → Data Ops Assistant.
- Proposal layout, PDF design → Sales Asset Designer.
- Demo scheduling follow-ups → RevOps Assistant.
- Sector research, ICP list assembly → Saudi B2B Researcher.
- Post drafting after founder approves the message → Growth Operator.
- Output quality review → Trust/QA Reviewer.

---

## أهداف الرافعة الأسبوعية / Weekly leverage targets

| Category | Target hours/week | Floor | Ceiling |
|---|---|---|---|
| Revenue-direct (customer calls, demos, close conversations) | 18 | 12 | 25 |
| Customer (delivery, QA on live engagements) | 10 | 6 | 14 |
| Building (system, doc, automation) | 8 | 5 | 12 |
| Delegation (briefing, reviewing, unblocking team) | 6 | 4 | 8 |
| Learning (founder reading, sector study) | 3 | 2 | 5 |
| Personal (no calls, no doc) | 14 | 10 | — |

Cap on total work week: 65 hours. Above that, quality and judgement degrade.

---

## إشارات عنق الزجاجة / Anti-bottleneck signals

أي إشارة من التالي يجب أن تُكتب وتُعالج خلال 48 ساعة:

- طابور موافقات بعمر أكثر من 24 ساعة → عدد العناصر.
- متوسط وقت ردّ المؤسس على رسالة عميل > 6 ساعات في أيام العمل.
- ثغرة في `docs/founder/DECISION_LOG.md` لأكثر من 5 أيام.
- إعادة عمل من المؤسس على مخرجات الفريق > 20% أسبوعيًا.
- اجتماعات تخطّى المؤسس فيها الحضور لكنه مذكور كمعتمد.

Any one of these must be written down and addressed within 48 hours.

---

## نموذج إدخال أسبوعي / Weekly entry template

```yaml
week_of: 2026-05-24
leverage_score: <calculated>
ndh_hours: <number>
tfh_hours: <number>
bottleneck_penalty: <number>
quality_penalty: <number>
top_3_non_delegable_wins:
  - <one line>
  - <one line>
  - <one line>
top_3_should_have_delegated:
  - <one line + who should have owned it>
  - <one line + who should have owned it>
  - <one line + who should have owned it>
anti_bottleneck_signals:
  approval_queue_over_24h: <count>
  customer_reply_lag_p50_hours: <number>
  decision_log_gap_days: <number>
  rework_pct: <number>
next_week_one_thing_to_stop: <one line>
```

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Related canonical docs

- `docs/team/founder_sop.md`
- `docs/ops/FOUNDER_DAILY_ANCHOR_AR.md`
- `docs/V14_FOUNDER_DAILY_OPS.md`
- `docs/ops/FOUNDER_WEEKLY_METRICS_AR.md`
- `docs/people/FOUNDER_BOTTLENECK_REMOVAL.md`
- `docs/founder/FOUNDER_TIME_AUDIT.md`
- `docs/founder/CEO_ATTENTION_BUDGET.md`
