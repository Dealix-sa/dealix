# Dealix — Pricing Model V7 — نموذج التسعير V7

> Section 153-154 of the positioning brief. Bilingual fence-bound pricing. This is a parallel doc, not a replacement for [`PRICING_AND_PACKAGES.md`](PRICING_AND_PACKAGES.md). Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### 1. مبدأ التسعير
السعر ليس انعكاس «قيمة عاطفية» بل **حقّ تشغيل** نظام تشغيل محكوم. القيمة الحقيقية لا تظهر إلا في Verified Revenue + Trust Incidents Avoided. لذلك تُحصَّن الأسعار بـ fences لا تُخصَم.

### 2. ثلاث قواعد ذهبية
- **القاعدة 1**: لا خصم تحت الحدّ المُعلَن. الخصم يُغيّر الفئة، لا الرقم.
- **القاعدة 2**: السعر منشور. لا أسعار «بالطلب» إلا فوق الفئة الأعلى.
- **القاعدة 3**: السعر يُعكَس داخل الكود (راجع `api/routers/pricing.py`). أي انحراف بين الكود والوثيقة بَق.

### 3. الجدول (Fences)

| العرض | المُشتري | الحد الأدنى (SAR) | الالتزام | السقف الأسبوعي للقبول |
|---|---|---|---|---|
| Revenue Hunter Pilot | مالك B2B | 4,900 | 14 يومًا | 2 |
| AI Trust Kit | مدير شركة متوسطة | 18,000 | 4 أسابيع | 1 |
| Agency White-label Kit | وكالة | 25,000 + 1,000/شهر + 25% rev share | بدون حصرية | 1 |
| Revenue Command | مؤسس/مدير تجاري | 9,000/شهر | 90 يومًا أدنى | 2 |
| Market Radar | مدير استراتيجي | 7,500/تقرير | لا توجد | 4 |
| Agentic Control Plane Setup | CIO/CISO | 75,000 | 6-8 أسابيع | 1 |
| Governance OS Retainer | CIO/CISO | 35,000/شهر | 12 شهرًا | 2 |
| Executive PMO | راعي تنفيذي | 100,000/شهر | فصلي | 1 |

### 4. لماذا fences؟
- يحمي الجودة (لا يُختصَر النطاق سرًا).
- يحمي الوقت (لا 50 محادثة خصم).
- يحمي السمعة (السعر إشارة جودة في سياق Enterprise).

### 5. ما الذي يُسعَّر كيف
- **التشغيل** (إعداد + شهري): fence ثابت.
- **الاستهلاك** (LaaS، تقارير): سعر منشور لكل وحدة.
- **PMO**: شهري ثابت + رسوم مشروع منفصلة.
- **white-label**: شهري + rev share.

### 6. ما لا نُسعّره
- ساعات عمل المؤسس عند العملاء دون عقد مُعلَن.
- «مكافآت» مرتبطة بأرقام مبيعات.
- تنازلات تحت الحد لإغلاق ربع.

### 7. تجديد ورفع
- التجديد التلقائي ما لم يُخطَر بإنهاء قبل 60 يومًا.
- زيادة سعر سنوية تصل 10% (مرتبطة بمؤشر تكلفة).
- العميل يستطيع «التبريد» إلى فئة أدنى وفق fence فئة الهدف.

### 8. التنفيذ في الكود
- الأسعار في `api/routers/pricing.py` PLANS dict.
- اختبارات تمنع نشر إصدار يخالف الجدول أعلاه.
- وثيقة V7 هذه + الكود = مصدر الحقيقة.

---

## English

### 1. Pricing Principle
Price is not a reflection of "emotional value"; it is the **right to operate** a governed AI operating system. Real value shows only in Verified Revenue + Trust Incidents Avoided. Prices are therefore fence-bound and non-discountable.

### 2. Three Golden Rules
- **Rule 1**: no discount below the declared floor. Discount changes the tier, not the number.
- **Rule 2**: prices are published. No "on request" pricing except above the top tier.
- **Rule 3**: price is reflected inside the code (see `api/routers/pricing.py`). Any drift between code and doc is a bug.

### 3. The Fences

| Offer | Buyer | Floor (SAR) | Term | Weekly Intake Cap |
|---|---|---|---|---|
| Revenue Hunter Pilot | B2B owner | 4,900 | 14 days | 2 |
| AI Trust Kit | Mid-market director | 18,000 | 4 weeks | 1 |
| Agency White-label Kit | Agency | 25,000 + 1,000/mo + 25% rev share | non-exclusive | 1 |
| Revenue Command | Founder/Commercial lead | 9,000/mo | 90-day minimum | 2 |
| Market Radar | Strategy lead | 7,500/report | none | 4 |
| Agentic Control Plane Setup | CIO/CISO | 75,000 | 6-8 weeks | 1 |
| Governance OS Retainer | CIO/CISO | 35,000/mo | 12 months | 2 |
| Executive PMO | Executive sponsor | 100,000/mo | quarterly | 1 |

### 4. Why Fences
- Protects quality (no quiet scope reduction).
- Protects time (no 50 discount conversations).
- Protects reputation (price is a quality signal in enterprise).

### 5. What Is Priced and How
- **Operate** (setup + monthly): fixed fence.
- **Consume** (LaaS, reports): published unit price.
- **PMO**: fixed monthly + separate project fee.
- **White-label**: monthly + rev share.

### 6. What Is Not Priced
- Founder hours at customers without a published contract.
- "Bonuses" tied to sales numbers.
- Below-floor concessions to close a quarter.

### 7. Renewal and Uplift
- Auto-renewal unless 60 days notice.
- Annual uplift up to 10% (indexed to a cost measure).
- Customer may "cool down" to a lower tier following the target tier's fence.

### 8. Code Enforcement
- Prices live in `api/routers/pricing.py` PLANS dict.
- Tests block releases that violate the table above.
- This V7 doc + code = source of truth.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
