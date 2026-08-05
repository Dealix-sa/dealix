# Founder Hour ROI — العائد المتوقَّع لساعة المؤسس

**Purpose / الغرض**
Methodology to score each founder activity by SAR-per-hour expected return so attention can be allocated against the highest-return work.
منهجية لتقدير العائد المتوقَّع بالريال السعودي لكل ساعة من نشاط المؤسس، حتى يُخصَّص الانتباه للعمل الأعلى عائدًا.

**Owner placeholder:** `<founder>` with periodic challenge from independent finance advisor.
**Cadence:** Quarterly recalibration. Spot-check whenever a new activity type emerges. / إعادة معايرة فصلية. فحص فوري عند ظهور نشاط جديد.
**KPIs:** (1) % of founder hours in activities with score ≥ median, (2) variance between estimated and observed return after 90 days, (3) number of activities removed from founder's plate this quarter because score < threshold.
**Risk if missing / مخاطر الغياب:** Hours flow toward what feels productive instead of what produces. The founder over-invests in building over selling, or vice versa, without data. / الساعات تنساب نحو ما يبدو منتجًا بدلًا مما يُنتج. المؤسس يبالغ في البناء على حساب البيع أو العكس بلا بيانات.

---

## EN summary

Each founder activity is given a SAR/hour expected return score. The score is not a forecast — it's a comparative ranking that says "if I had only one extra hour, where would it produce the most value?". The math is deliberately simple so the score is auditable and re-runnable.

## ملخص بالعربية

كل نشاط للمؤسس يأخذ درجة عائد متوقَّع بالريال/ساعة. الدرجة ليست توقعًا — هي ترتيب مقارن يجيب على «لو كان لديّ ساعة إضافية فقط، أين تنتج أكبر قيمة؟». الحساب بسيط عمدًا حتى يكون قابلًا للتدقيق وللإعادة.

---

## معادلة العائد لكل ساعة / The formula

```
HourROI = (EV × P × R) / H

EV = Expected revenue or saving from the outcome in SAR
P  = Probability the activity actually produces the outcome (0.0–1.0)
R  = Reusability factor (1.0 = single use, 2.0 = compounds across customers)
H  = Founder hours to ship the activity end-to-end
```

- **EV** is the marginal value of the outcome, not the lifetime contract value.
- **P** is a sober estimate based on past observations, not aspiration.
- **R** captures whether the work creates an asset (template, system, doc) that reduces future hours.
- **H** includes preparation, the activity itself, and the follow-up.

---

## مثال محسوب لخمسة أنواع نشاط / Worked example: 5 activity types

> القيم مدخلات افتراضية لتوضيح المنهجية. سيستبدلها المؤسس بأرقامه الخاصة وفق الملاحظة. / Placeholder figures for illustration. The founder replaces them with his own observations.

### 1) Outreach — اجتماع توضيحي مع مشتري مؤهَّل / Qualified discovery meeting

- EV = `<sprint_price_placeholder>` SAR
- P = 0.15
- R = 1.0
- H = 2.5 hours (prep 1h + meeting 1h + follow-up 0.5h)
- **HourROI = (EV × 0.15) / 2.5**

تفسير: نشاط أحادي الاستخدام، احتمال إغلاق متوسط الحساسية لجودة الإحالة. تحسين P بإحالة دافئة يضاعف العائد.

### 2) Demo — عرض منتج لمشتري اقتصادي / Demo to economic buyer

- EV = `<sprint_price_placeholder>` SAR
- P = 0.30
- R = 1.2 (يحسّن سكربت العرض ويُعاد استخدامه)
- H = 3.0 hours
- **HourROI = (EV × 0.30 × 1.2) / 3.0**

تفسير: أعلى عادةً من Outreach بسبب P أعلى ومضاعف R.

### 3) Building — تطوير قالب مقترح قابل لإعادة الاستخدام / Building a reusable proposal template

- EV = saving of `<hours_saved_per_proposal>` × `<founder_blended_rate>` × `<proposals_per_quarter>` SAR
- P = 0.9 (سيُستخدم فعلًا إن أُكمل)
- R = 2.0 (يضاعف على كل مقترح لاحق)
- H = 8.0 hours
- **HourROI = (EV × 0.9 × 2.0) / 8.0**

تفسير: ينافس البيع عندما عدد المقترحات الربعي مرتفع. تحت عتبة معينة، البناء يخسر.

### 4) Hiring — إجراء مقابلة استكشافية لدور أساسي / Exploratory interview for a key role

- EV = الأثر الصافي للتعيين على ربعين (إيرادات إضافية + وقت محرر للمؤسس) SAR
- P = 0.10 (هذه المقابلة تحديدًا تؤدي لتعيين)
- R = 3.0+ (التعيين الصحيح يضاعف)
- H = 2.0 hours
- **HourROI = (EV × 0.10 × 3.0) / 2.0**

تفسير: تبدو P منخفضة لكن R مرتفع جدًا. هذه أنشطة "high variance" — أقلية من الساعات تنتج أغلب القيمة.

### 5) Content — منشور LinkedIn مدروس / A considered LinkedIn post

- EV = القيمة المتوقعة لإحالات قادمة من المنشور (مكالمات مؤهَّلة × P × EV لكل مكالمة) SAR
- P = 0.05 (احتمال أن ينتج المنشور مكالمة مؤهلة)
- R = 1.5 (يبقى المنشور قابلًا للاستشهاد)
- H = 1.5 hours
- **HourROI = (EV × 0.05 × 1.5) / 1.5**

تفسير: العائد لكل منشور صغير، لكن المنشورات تتراكم. القرار: 1–2 منشور أسبوعيًا، لا أكثر.

---

## ترتيب الأنشطة / Ranking

في نهاية الربع، يُملأ هذا الجدول بأرقام حقيقية:

| Activity | HourROI (SAR/hr) | Notes |
|---|---|---|
| Demo to economic buyer | <calculated> | |
| Outreach (warm-only) | <calculated> | |
| Building reusable asset | <calculated> | يتأثر بعدد الاستخدامات. |
| Hiring conversation | <calculated> | high variance, raise allocation by 50% as buffer. |
| Content | <calculated> | underweighted but compounding. |

> القاعدة: لا تُلغ نشاطًا فقط لأن درجته أقل. ألغه إذا كانت أقل من نصف أعلى نشاط، وكان قابلًا للتفويض، ولديك شخص للتفويض إليه. / Rule: do not kill a low-score activity by score alone. Kill it only if it is < 50% of the top activity AND it is delegable AND you have someone to delegate to.

---

## ملاحظات حذرة / Caveats

### EN

- HourROI is a **comparative** tool, not a forecast. It does not promise revenue.
- Reusability (R) is the most over-estimated variable. Discount by 30% by default.
- Probability (P) is the most over-estimated variable on a founder's good day. Run the worst-case P too.
- Personal hours (sleep, family, prayer) have a HourROI that does not appear in this register — but they are non-negotiable per `docs/founder/CEO_ATTENTION_BUDGET.md`.

### AR

- العائد لكل ساعة أداة **مقارنة**، ليست توقعًا. لا يَعِد بإيراد.
- إعادة الاستخدام (R) المتغير الأكثر تضخيمًا. اخفضه 30% افتراضيًا.
- الاحتمال (P) المتغير الأكثر تضخيمًا في يوم مؤسس مزدهر. احسب أيضًا حالة P الأسوأ.
- ساعات الشخصي (نوم، عائلة، صلاة) لا تظهر في هذا السجل — لكنها غير قابلة للتفاوض حسب ميزانية الانتباه.

---

## إعادة المعايرة / Recalibration

كل 90 يومًا، قارن HourROI المُقدَّر مع EV المُلاحَظ:

```
Calibration error = (Observed_EV − Estimated_EV) / Estimated_EV
```

- إذا كان الخطأ أكبر من ±40% لنشاطين متتاليين، راجع P و R لذلك النشاط.
- ولا تعدّل النشاط الفردي — عدّل المنهجية، لأن الانحياز يتكرر.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
No revenue, conversion, or ROI number in this doc is a promise. All figures are observation targets to be replaced by real data over time.

## Related canonical docs

- `docs/operating_finance/CAPITAL_ALLOCATION_SCORE.md`
- `docs/operating_finance/OPPORTUNITY_COST_SYSTEM.md`
- `docs/operating_finance/CAPITAL_ALLOCATION_THESIS.md`
- `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`
- `docs/founder/CEO_ATTENTION_BUDGET.md`
- `docs/company/PRICING_DECISION.md`
