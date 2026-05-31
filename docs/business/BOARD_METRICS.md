# Dealix — Board Metrics — مؤشرات المجلس

> Section 146 of the positioning brief. The 12 metrics with definitions and computation. Bilingual. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### 1. مبدأ الاختيار
لا أرقام بريق. كل مؤشر هنا (أ) قابل للحساب من سجل عملي، (ب) قابل للتدقيق، (ج) يدفع قرارًا، (د) لا يُقاس بـ«شعور».

### 2. المؤشرات الاثنا عشر

**(1) Verified Revenue (SAR)**
- **التعريف**: مجموع الإيراد المُرتبط بـ Evidence Packs بـ `revenue_link.verified = true` في الفترة.
- **الحساب**: SUM(amount_sar) من Evidence Packs السارية.
- **القرار**: حق المجلس في المطالبة بدليل لكل ريال.

**(2) Estimated Pipeline (SAR)**
- **التعريف**: قيمة الفرص الموثَّقة بدون Evidence Pack بعد.
- **الحساب**: من CRM، مفصول عن المؤشر 1.
- **القرار**: مراقبة الفجوة بين التقدير والتحقّق.

**(3) Active Customers (count)**
- **التعريف**: عملاء بفاتورة سارية في الفترة.
- **الحساب**: من ZATCA invoices.
- **القرار**: تحديد سرعة النمو الفعلية.

**(4) Net New Customers (count)**
- **التعريف**: عملاء جدد − عملاء انتهَوا في الفترة.
- **الحساب**: قاعدة العملاء.
- **القرار**: تقييم القناة.

**(5) Pilot-to-SaaS Conversion (%)**
- **التعريف**: نسبة من جرّبوا Revenue Hunter Pilot واشتركوا في SaaS خلال 30 يومًا.
- **الحساب**: (subscribed_within_30d) / (pilots_completed).
- **القرار**: جودة Pilot كبوابة.

**(6) Evidence Packs Published (count)**
- **التعريف**: عدد Evidence Packs المُتاحة للتدقيق الخارجي بموافقة العميل.
- **الحساب**: من Trust Signals.
- **القرار**: مصداقية «معيار الإثبات».

**(7) Trust Incidents (count + severity)**
- **التعريف**: حوادث Tool Permission Matrix أو إرسال خارجي بدون موافقة.
- **الحساب**: من سجل الحوادث.
- **القرار**: صحة طبقة الحوكمة.

**(8) Founder Hours on Customer Work (h/wk)**
- **التعريف**: ساعات المؤسس المباشرة في تشغيل العميل.
- **الحساب**: log أسبوعي.
- **القرار**: إشارة توظيف.

**(9) Agency Tenants Active (count)**
- **التعريف**: وكالات بنشاط شهري دفعت rev share.
- **الحساب**: من R6 ledger.
- **القرار**: صحة قناة التوزيع.

**(10) Burn Rate (SAR/month)**
- **التعريف**: صافي النفقات شهريًا.
- **الحساب**: من السجل المحاسبي.
- **القرار**: مدة التشغيل (Runway).

**(11) Cash Runway (months)**
- **التعريف**: النقد المتاح / Burn Rate.
- **الحساب**: مباشر.
- **القرار**: توقيت الجولة.

**(12) Doctrine Adherence (%)**
- **التعريف**: نسبة الإيراد المُتولَّد بدون كسر للوعود الأربعة.
- **الحساب**: 100% − (إيراد ينتج عن استثناء عقيدة).
- **القرار**: صحة العلامة. الهدف 100%.

### 3. تقرير المجلس
كل اجتماع مجلس يحصل على هذه الـ 12 + Evidence Pack عيّنة. لا «دلائل قصصية» بدون مؤشر.

---

## English

### 1. Selection Principle
No vanity numbers. Each metric here is (a) computable from an operational log, (b) auditable, (c) drives a decision, (d) not measured by "feel".

### 2. The Twelve Metrics

**(1) Verified Revenue (SAR)**
- **Definition**: total revenue tied to Evidence Packs with `revenue_link.verified = true` in the period.
- **Computation**: SUM(amount_sar) over valid Evidence Packs.
- **Decision**: the board's right to demand proof per riyal.

**(2) Estimated Pipeline (SAR)**
- **Definition**: value of recorded opportunities without an Evidence Pack yet.
- **Computation**: from CRM, kept separate from Metric 1.
- **Decision**: track the gap between estimate and verification.

**(3) Active Customers (count)**
- **Definition**: customers with a live invoice in the period.
- **Computation**: from ZATCA invoices.
- **Decision**: actual growth velocity.

**(4) Net New Customers (count)**
- **Definition**: new customers − churned customers.
- **Computation**: customer base.
- **Decision**: channel evaluation.

**(5) Pilot-to-SaaS Conversion (%)**
- **Definition**: share of Revenue Hunter Pilot customers who subscribe to SaaS within 30 days.
- **Computation**: (subscribed_within_30d) / (pilots_completed).
- **Decision**: Pilot quality as gateway.

**(6) Evidence Packs Published (count)**
- **Definition**: Evidence Packs available for external audit with customer consent.
- **Computation**: from Trust Signals.
- **Decision**: credibility of the "proof standard".

**(7) Trust Incidents (count + severity)**
- **Definition**: Tool Permission Matrix or external-send-without-approval incidents.
- **Computation**: from incident log.
- **Decision**: health of the governance layer.

**(8) Founder Hours on Customer Work (h/wk)**
- **Definition**: founder hours directly in customer operations.
- **Computation**: weekly log.
- **Decision**: hiring signal.

**(9) Agency Tenants Active (count)**
- **Definition**: agencies with monthly activity that paid rev share.
- **Computation**: from R6 ledger.
- **Decision**: distribution channel health.

**(10) Burn Rate (SAR/month)**
- **Definition**: net monthly outflow.
- **Computation**: from accounting ledger.
- **Decision**: runway.

**(11) Cash Runway (months)**
- **Definition**: cash on hand / burn rate.
- **Computation**: direct.
- **Decision**: round timing.

**(12) Doctrine Adherence (%)**
- **Definition**: share of revenue generated without breaking any of the Four Promises.
- **Computation**: 100% − (revenue produced by a doctrine exception).
- **Decision**: brand integrity. Target 100%.

### 3. Board Report
Every board meeting receives these 12 plus an Evidence Pack sample. No "anecdotal evidence" without a metric.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
