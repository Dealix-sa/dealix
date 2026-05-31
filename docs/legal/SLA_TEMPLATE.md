# اتفاقية مستوى الخدمة — نموذج | Service Level Agreement — Template

> **هذا النموذج للمراجعة الداخلية — يجب مراجعة مستشار قانوني قبل الاستخدام**
>
> This template is for internal review only. Saudi legal counsel must review before execution.
>
> [Founder review required] on all sections marked accordingly before sending to any client.
>
> وثائق ذات صلة: [`docs/legal/ENTERPRISE_MSA_TEMPLATE.md`](./ENTERPRISE_MSA_TEMPLATE.md) | [`docs/legal/DPA_TEMPLATE_AR.md`](./DPA_TEMPLATE_AR.md) | [`docs/05_governance_os/APPROVAL_POLICY.md`](../05_governance_os/APPROVAL_POLICY.md)

---

## 1. الأطراف | Parties

**مزود الخدمة | Service Provider:**
شركة ديلكس [الاسم القانوني الرسمي يُدرج هنا — Founder review required]، سجل تجاري رقم {CR_NUMBER}، عنوان مسجل: {ADDRESS}، الرياض، المملكة العربية السعودية.

Dealix [official entity name — Founder review required], Commercial Registration No. {CR_NUMBER}, registered address: {ADDRESS}, Riyadh, Kingdom of Saudi Arabia.

**العميل | Customer:**
{CUSTOMER_LEGAL_NAME}، سجل تجاري رقم {CUSTOMER_CR}، عنوان مسجل: {CUSTOMER_ADDRESS}.

{CUSTOMER_LEGAL_NAME}, Commercial Registration No. {CUSTOMER_CR}, registered address: {CUSTOMER_ADDRESS}.

**تاريخ النفاذ | Effective Date:** {EFFECTIVE_DATE}

**رقم العقد المرجعي | Contract Reference:** {CONTRACT_REF} [Founder review required]

---

## 2. نطاق الخدمة | Service Scope

تُطبَّق هذه الاتفاقية على مستوى الخدمة المُختار أدناه. يُحدَّد المستوى في أمر الخدمة المرفق.

This agreement applies to the selected service tier below. Tier is defined in the accompanying Service Order.

| المستوى | Tier | وصف الخدمة | Service Description | السعر المرجعي | Reference Price |
|---------|------|-------------|---------------------|----------------|-----------------|
| سبرنت الإيرادات | Revenue Sprint | تحليل بيانات وتقرير فرص مُثبتة بأدلة، 7 أيام | Evidence-based opportunity report, 7 calendar days | 499 ريال | 499 SAR |
| حزمة البيانات | Data Pack | تدقيق جودة بيانات، رسم خرائط، تقرير DQ Score | Data quality audit, mapping, DQ Score report | 1,500 ريال | 1,500 SAR |
| العمليات المُدارة | Managed Ops | عمليات إيرادات شهرية مُحوكَمة، تقارير دورية | Monthly governed revenue operations, periodic reporting | 2,999–4,999 ريال/شهر | 2,999–4,999 SAR/mo |
| حلول الذكاء المخصصة | Custom AI | نشر وكلاء مخصصين، حوكمة متقدمة، تكاملات | Custom agent deployment, advanced governance, integrations | 5,000–25,000 ريال | 5,000–25,000 SAR |

المستوى المُختار لهذا العقد: **{SELECTED_TIER}** [Founder review required]

Selected tier for this contract: **{SELECTED_TIER}** [Founder review required]

---

## 3. مستويات الخدمة | Service Levels

### 3.1 أوقات الاستجابة — حسب الأولوية | Response Times by Priority

| الأولوية | Priority | التعريف | Definition | وقت الاستجابة الأول | First Response | وقت الحل المستهدف | Target Resolution |
|----------|----------|----------|------------|---------------------|----------------|-------------------|-------------------|
| P1 — حرجة | P1 — Critical | توقف كامل للخدمة، خرق بيانات، توقف عمليات العميل | Full service outage, data breach, complete client ops stoppage | 4 ساعات | 4 hours | 24 ساعة | 24 hours |
| P2 — عالية | P2 — High | تدهور ملموس في الأداء، خلل في وظيفة رئيسية | Material performance degradation, core function defect | 24 ساعة | 24 hours | 72 ساعة | 72 hours |
| P3 — متوسطة | P3 — Medium | خلل في وظيفة ثانوية، استفسار تشغيلي | Minor function defect, operational query | 72 ساعة | 72 hours | 10 أيام عمل | 10 business days |

أوقات الاستجابة تُحسب خلال ساعات العمل الرسمية: الأحد–الخميس، 09:00–17:00 بتوقيت الرياض، ما لم يُحدد خلاف ذلك في أمر الخدمة.

Response times are calculated during business hours: Sunday–Thursday, 09:00–17:00 AST, unless the Service Order specifies otherwise.

### 3.2 التوافر | Uptime

- **التوافر الشهري المستهدف | Monthly Uptime Target:** 99.5% (حوسبته: المنصة + API / measured: platform + API)
- نوافذ الصيانة المجدولة (إشعار مسبق ≥ 48 ساعة) مُستثناة من حساب التوافر.
- Scheduled maintenance windows (≥ 48h advance notice) are excluded from uptime calculation.
- قياس التوافر: عبر مراقبة UptimeRobot الداخلية. السجلات متاحة للعميل عند الطلب.
- Uptime is measured via internal UptimeRobot monitoring. Logs available to client upon request.

### 3.3 تسليم السبرنت | Sprint Delivery

- يُسلَّم تقرير سبرنت الإيرادات (499 ريال) خلال **7 أيام تقويمية** من تاريخ الانطلاق الرسمي.
- يُحسب تاريخ الانطلاق من استلام جواز المصدر الموقَّع وبيانات العميل الكاملة.
- Revenue Sprint (499 SAR) report is delivered within **7 calendar days** from official kickoff date.
- Kickoff date is counted from receipt of signed Source Passport and complete client data.

### 3.4 تقارير العمليات المُدارة | Managed Ops Monthly Reporting

- يُرسَل تقرير الأداء الشهري خلال **5 أيام عمل** من نهاية كل شهر ميلادي.
- يتضمن التقرير: ملخص الأنشطة، مقاييس Proof Pack المُحدَّثة، توصيات الشهر التالي.
- Monthly performance report is delivered within **5 business days** from the end of each calendar month.
- Report includes: activity summary, updated Proof Pack metrics, next-month recommendations.

---

## 4. الاستثناءات | Exclusions

لا تسري التزامات مستوى الخدمة في الحالات التالية:

Service level commitments do not apply in the following circumstances:

- **القوة القاهرة | Force Majeure:** حوادث خارجة عن السيطرة المعقولة، شاملة كوارث طبيعية، إجراءات حكومية، انقطاع واسع للإنترنت. Events beyond reasonable control, including natural disasters, government actions, or widespread internet outages.
- **بيانات العميل | Client Data Issues:** تأخر ناتج عن تقديم بيانات ناقصة، خاطئة، أو متأخرة من العميل. Delays resulting from incomplete, inaccurate, or late data submission by the client.
- **توقف ZATCA API | ZATCA API Downtime:** عدم توافر نقاط API الخاصة بهيئة الزكاة والضريبة والجمارك خارج سيطرة ديلكس. Unavailability of ZATCA API endpoints outside Dealix's control.
- **الصيانة المُجدولة | Scheduled Maintenance:** نوافذ صيانة مُعلَنة بإشعار مسبق ≥ 48 ساعة. Maintenance windows announced with ≥ 48h advance notice.
- **موردو طرف ثالث | Third-Party Providers:** توقف أنظمة خارجية كشبكات الدفع أو واجهات التكاملات المعتمدة، طالما اتخذت ديلكس إجراءات المخففة المعقولة. Outages in external systems such as payment networks or approved integration interfaces, provided Dealix has taken reasonable mitigation steps.
- **الإجراءات بدون موافقة | Unapproved Actions:** أي تأخر ناجم عن انتظار موافقة العميل المطلوبة بموجب سياسة APPROVAL_FIRST. Any delay caused by awaiting client approval required under the APPROVAL_FIRST governance policy.

---

## 5. العلاج عند الإخفاق | Remedy upon SLA Breach

عند عدم الوفاء بمستوى خدمة ثابت وموثَّق:

Upon a verified and documented SLA breach:

- **الائتمان | Credit:** 5% من رسوم الخدمة الشهرية عن كل يوم إخفاق مُثبَّت. 5% of the monthly service fee per verified missed SLA day.
- **الحد الأقصى | Maximum:** 20% من الرسوم الشهرية لأي شهر واحد. 20% of monthly fees for any single month.
- **الطريقة | Method:** يُخصَّم الائتمان من الفاتورة التالية؛ لا يُستبدَل نقداً. Credit is applied to the next invoice; not redeemable as cash.
- **الإجراء | Procedure:** يقدم العميل طلب ائتمان كتابياً خلال 14 يوماً من تاريخ الإخفاق المُزعَم. ترد ديلكس بتأكيد أو نفي خلال 5 أيام عمل. Client submits written credit request within 14 days of alleged breach date. Dealix responds with confirmation or rebuttal within 5 business days.
- **الحصرية | Exclusivity:** الائتمانات المنصوص عليها هي العلاج الحصري لإخفاقات مستوى الخدمة، دون المساس بحقوق الإنهاء المنصوص عليها في العقد الرئيسي. Credits are the exclusive remedy for SLA failures, without prejudice to termination rights in the Master Agreement.

[Founder review required — credit percentages and caps to be confirmed against operational capacity]

---

## 6. مسار التصعيد | Escalation Path

**المرحلة 1 — مدير نجاح العملاء | Stage 1 — Customer Success Manager**
الإبلاغ عن المشكلة عبر القناة المُعتمَدة. الاستجابة خلال وقت الاستجابة المناسب للأولوية (القسم 3.1).
Report issue via approved channel. Response within the priority-appropriate time (Section 3.1).

**المرحلة 2 — المؤسس | Stage 2 — Founder**
إذا لم يُحَل P1 خلال 4 ساعات، أو P2 خلال 24 ساعة: يُصعَّد تلقائياً إلى المؤسس.
If P1 unresolved within 4 hours, or P2 within 24 hours: automatic escalation to Founder.
التواصل المباشر: {FOUNDER_CONTACT} [Founder review required]

**المرحلة 3 — الحل الخارجي | Stage 3 — External Resolution**
عند فشل مراحل 1 و2 خلال 30 يوماً: يحق لأي طرف طلب التوسط أو التحكيم وفق القسم 7.
If Stages 1 and 2 fail within 30 days: either party may invoke mediation or arbitration per Section 7.

---

## 7. القانون الحاكم | Governing Law

تخضع هذه الاتفاقية وتُفسَّر وفقاً لأنظمة المملكة العربية السعودية. تختص محاكم مدينة الرياض بالنظر في أي نزاع ناشئ عنها. يُعتمد التحكيم أمام المركز السعودي للتحكيم التجاري (SCCA) في حال اتفاق الطرفين كتابةً.

This agreement is governed by and construed in accordance with the laws of the Kingdom of Saudi Arabia. The courts of Riyadh have jurisdiction over any dispute arising hereunder. Arbitration before the Saudi Center for Commercial Arbitration (SCCA) may be used if both parties agree in writing.

---

## 8. المراجعة الدورية | Review Cycle

- تُراجَع هذه الاتفاقية **سنوياً** من تاريخ نفاذها، أو فور أي تغيير في مستوى الخدمة المُشترَك.
- أي تعديل يتطلب موافقة خطية من الطرفين. [Founder review required]
- This agreement is reviewed **annually** from its effective date, or immediately upon any change in subscribed service tier.
- Any amendment requires written consent from both parties. [Founder review required]

---

## 9. كتلة التوقيعات | Signature Block

### عن ديلكس | For Dealix

| الاسم | الصفة | التوقيع | التاريخ |
|-------|-------|---------|---------|
| Name | Title | Signature | Date |
| {DEALIX_SIGNATORY_NAME} [Founder review required] | {TITLE} | ________________ | {DATE} |

### عن العميل | For Customer

| الاسم | الصفة | التوقيع | التاريخ |
|-------|-------|---------|---------|
| Name | Title | Signature | Date |
| {CUSTOMER_SIGNATORY_NAME} | {TITLE} | ________________ | {DATE} |

الختم الرسمي للعميل (إن وُجد): ________________
Official customer stamp (if applicable): ________________

---

> **القيمة التقديرية ليست قيمة مُتحقَّقة**
> Estimated value is not Verified value.

---

*آخر مراجعة: 2026-05-31 | Last reviewed: 2026-05-31*
*[Founder review required before any client distribution]*
