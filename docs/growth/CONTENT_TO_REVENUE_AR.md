# Content-to-Revenue — المحتوى الذي يُترجم إلى إيراد

> Sections 36–37. خمسة أنواع محتوى، مصفوفة Content-to-Cash، والقاعدة الذهبيّة.
> Module path: `dealix/growth_os/content_to_revenue/`

---

## القاعدة الذهبيّة — The 4-Line Rule

1. **لا محتوى بدون CTA.** كل أصل ينتهي بدعوة محدّدة.
2. **لا CTA بدون عرض.** الـ CTA يربط بـ OfferCard موجود.
3. **لا عرض بدون tracking.** الرابط مُعَلَّم (UTM + attribution tag).
4. **لا tracking بدون نتيجة موثَّقة.** كل أصل يُراجَع شهريّاً مقابل أرقامه.

> No content without CTA / no CTA without offer / no offer without tracking / no tracking without outcome.

---

## أنواع المحتوى الخمسة — The 5 Content Types

### 1) Trust Content — محتوى الثقة

**الغرض.** يثبت أن Dealix يفهم الحوكمة ويعمل ضمنها.

**أمثلة عناوين:**
- "ما لا نفعله بـ AI في Dealix — والسبب."
- "كيف نوثّق كل ادعاء قبل نشره."
- "ProofPack: مثال علني من sprint مجهول الهوية."

**CTA افتراضي.** "اطّلع على Trust Pack الكامل."

### 2) Revenue Content — محتوى الإيراد

**الغرض.** يوضّح كيف يتحوّل العمل إلى إيراد قابل للتدقيق.

**أمثلة عناوين:**
- "ما الذي نعتبره إيراداً مُتحقَّقاً (وما لا نعتبره)."
- "Revenue Quality Score: كيف نحسب جودة كل ريال."
- "Sprint بقيمة 10K ر.س مقابل retainer 10K ر.س/شهر — أيّهما أعلى جودة؟"

**CTA افتراضي.** "احجز Revenue Intelligence Sprint."

### 3) Partner Content — محتوى الشركاء

**الغرض.** يجذب وكالات ومستشارين لإعادة بيع Dealix.

**أمثلة عناوين:**
- "كيف باعت Agency X ثلاث Governance Snapshots في 30 يوم."
- "White-label Dealix: ما يدخل وما لا يدخل."
- "هيكل العمولة الموثَّق."

**CTA افتراضي.** "تقديم طلب شراكة."

### 4) Executive Content — محتوى تنفيذي

**الغرض.** يصل لـ C-suite في الشركات الكبيرة بلغة قرار.

**أمثلة عناوين:**
- "لماذا 12 أداة AI لا تساوي طبقة تشغيل واحدة."
- "AI Audit Quarterly: ما يجب أن يصل لمجلس الإدارة."
- "حوكمة AI كميزة تنافسية، لا كعبء."

**CTA افتراضي.** "احجز Enterprise Briefing."

### 5) Market Radar Content — محتوى رادار السوق

**الغرض.** يضع Dealix كمصدر تحليل قطاعي موثوق.

**أمثلة عناوين:**
- "إطار SDAIA الجديد: ما يتغيّر للوكالات."
- "PDPL 2026 — التأثير على عمليات AI."
- "تقرير ربع سنوي: حالة AI الحوكمة في السعودية."

**CTA افتراضي.** "اشترك في تقرير الرادار الشهري."

---

## مصفوفة Content-to-Cash — Section 37

تربط كل نوع محتوى بمسار الإيراد المُتوقَّع.

| Content Type | Funnel Stage | CTA | OfferCard | Tracked Metric | Target Outcome |
|---|---|---|---|---|---|
| Trust | Awareness → Consideration | "اطّلع على Trust Pack" | — (نشر ثقة) | trust_page_visits, time_on_page | trust_visit → meeting_request |
| Revenue | Consideration → Decision | "احجز Sprint" | Revenue Intelligence Sprint | meeting_booked, proposal_drafted | meeting → proposal |
| Partner | Partner Acquisition | "تقديم شراكة" | Partner Tier | partner_applications | application → onboarded_partner |
| Executive | Enterprise Decision | "Briefing تنفيذي" | Enterprise Pilot | briefing_booked | briefing → pilot_signed |
| Market Radar | Top of Funnel | "اشترك" | — (قائمة بريديّة) | subscribers, share_rate | subscriber → meeting (over 60 days) |

---

## دورة حياة الأصل — Content Asset Lifecycle

1. **Topic capture.** من SignalCard أو سؤال تكرّر في 3 محادثات بيع.
2. **Brief.** 1 صفحة تحدّد ICP، CTA، OfferCard، KPI.
3. **Draft.** يكتبها agent، يراجعها Content Lead.
4. **Governance review.** claim-safety + PDPL.
5. **Publish + tag.** UTM + attribution_tag مسجَّلين.
6. **30-day review.** يُقاس مقابل الـ KPI، يُقرَّر: scale / optimize / retire.

---

## مؤشّرات الأداء — KPIs

- `content_assisted_revenue` — ر.س مرتبطة بأصل واحد على الأقل.
- `asset_to_meeting_rate` — % من القرّاء الذين حجزوا اجتماع.
- `asset_lifespan_days` — كم يومًا قبل أن يتقادم.
- `citation_count` — كم مرّة استشهد به AI engine (manual + auto checks).

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
