# اتفاقية معالجة البيانات — Data Processing Agreement (DPA)

> **حالة:** قالب جاهز للتوقيع. مراجعة قانونية مطلوبة قبل التطبيق على عملاء Enterprise.
> **الإصدار:** v1.0 — 2026-05-12.
> **الأطراف:** Dealix (المعالج) ↔ العميل (المتحكم).

---

## 1. التعريفات

- **«القانون»**: نظام حماية البيانات الشخصية السعودي (PDPL) الصادر بالمرسوم الملكي رقم (م/١٩) وتاريخ ٩/٢/١٤٤٣هـ، ولوائحه التنفيذية الصادرة عن الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA).
- **«البيانات الشخصية»**: كل بيانات يمكن أن تُعرّف شخصًا طبيعيًا، يعالجها Dealix بالنيابة عن العميل.
- **«المتحكم»**: العميل (الطرف الذي يحدد أغراض ووسائل المعالجة).
- **«المعالج»**: Dealix.
- **«صاحب البيانات»**: الشخص الطبيعي الذي تتعلق به البيانات.

---

## 2. الغرض من المعالجة

يعالج Dealix البيانات الشخصية حصرًا للأغراض التالية:
- تشغيل منصة Dealix للعميل
- تقديم خدمات الإيراد والشراكات والنمو المُعتمَدة
- النسخ الاحتياطية الأمنية والاستعادة عند الكوارث
- التحليلات التشغيلية (مع تنقيح PII حيث ينطبق)
- الامتثال لالتزامات قانونية (محاسبية، تنظيمية)

أي معالجة لغرض آخر تتطلب موافقة كتابية مسبقة من المتحكم.

---

## 3. فئات البيانات وأصحابها

| فئة البيانات | فئة صاحب البيانات | مدة الاحتفاظ |
|--------------|-------------------|----------------|
| اسم، بريد، هاتف، شركة | عملاء محتملون | 12 شهرًا من آخر تفاعل |
| اسم، بريد، هاتف، عنوان فوترة | عملاء دافعون | مدة العقد + 7 سنوات |
| رقم معاملة، آخر 4 من البطاقة | عملاء دافعون | 10 سنوات (نظام الزكاة) |
| محتوى المراسلات (إيميل، WhatsApp) | جميع الفئات | 24 شهرًا |
| سجلات تدقيق (auditلوج) | عاملو النظام | 24 شهرًا |

(جدول مفصّل في `docs/ops/PDPL_RETENTION_POLICY.md`)

---

## 4. التزامات Dealix كمعالج (PDPL م. ١٧)

يتعهد Dealix بـ:
1. **عدم معالجة** البيانات الشخصية إلا وفق تعليمات المتحكم الموثقة.
2. تطبيق **ضوابط أمنية تقنية وتنظيمية** مناسبة (تشفير في النقل والسكون، التحكم بالوصول، تدقيق الوصول).
3. ضمان **سرية** البيانات من قبل جميع الموظفين والمعالجين الفرعيين.
4. مساعدة المتحكم في الرد على **طلبات أصحاب البيانات** خلال 30 يومًا (م. ١٢).
5. **إبلاغ** المتحكم بأي اختراق محتمل خلال 72 ساعة من العلم به (م. ٢٠).
6. حذف أو إعادة البيانات عند انتهاء الخدمة وفق طلب المتحكم.
7. تمكين عمليات **التدقيق** على التزامات الاتفاقية مرة سنويًا أو عند الحاجة.

---

## 5. المعالجون الفرعيون (Sub-processors)

يستعين Dealix بالمعالجين الفرعيين الواردين في `https://dealix.sa/sub-processors.html`. أي إضافة لمعالج فرعي جديد يلمس بيانات شخصية يُخطر بها العميل **قبل 30 يومًا** من التفعيل، مع حق المتحكم في الاعتراض المعلَّل.

---

## 6. نقل البيانات خارج المملكة

البيانات التشغيلية الرئيسية مستضافة على Railway (US-East) مع نسخ احتياطية مشفّرة في AWS S3 منطقة `me-south-1` (المنامة).

أي نقل دولي يتم بموجب:
- عقد قياسي يتضمن ضمانات مكافئة لـ PDPL، أو
- موافقة صريحة من المتحكم لكل عملية نقل، أو
- استثناء قانوني صريح.

---

## 7. أمن المعلومات

ضوابط أمنية مطبقة (موثّقة في `docs/security/`):
- تشفير في النقل (TLS 1.2+) وفي السكون (AES-256)
- مفاتيح API دورانية كل 90 يومًا
- تدقيق وصول لكل عمليات `/api/v1/admin/*`
- اختبار اختراق سنوي
- نسخ احتياطية ساعية مشفّرة

---

## 8. الإبلاغ عن اختراق البيانات

عند اكتشاف اختراق أو شبهة اختراق:
1. يخطر Dealix المتحكم خلال **24 ساعة** عبر `privacy@dealix.sa` + اتصال هاتفي بـ DPO المتحكم.
2. يوفر Dealix كل المعلومات المطلوبة لتمكين المتحكم من الوفاء بالتزامه القانوني تجاه SDAIA (72 ساعة).
3. يتعاون Dealix كاملاً في التحقيق والاحتواء (راجع `docs/ops/PDPL_BREACH_RUNBOOK.md`).

---

## 9. إنهاء الاتفاقية

عند الإنهاء:
- يتوقف Dealix عن المعالجة فورًا.
- يحذف Dealix كل البيانات الشخصية خلال **30 يومًا**، أو يعيدها بصيغة قابلة للقراءة الآلية حسب طلب المتحكم.
- النسخ الاحتياطية المشفّرة تنتهي صلاحيتها وفق دورة `BACKUP_RESTORE.md` (مدة أقصى: 30 يومًا للنسخ الساعية).
- يُسلَّم تقرير تأكيد الحذف خلال 7 أيام من اكتمال العملية.

---

## 10. التعويض والمسؤولية

كل طرف يتحمل المسؤولية القانونية تجاه الطرف الآخر عن الأضرار المباشرة الناشئة عن إخلاله بهذه الاتفاقية، بسقف يعادل **رسوم 12 شهرًا** المدفوعة من المتحكم لـ Dealix.

التعديات المُتعمَّدة أو الإهمال الجسيم أو خرق التزامات السرية لا تخضع لهذا السقف.

---

## 11. القانون والاختصاص

تخضع هذه الاتفاقية لأنظمة المملكة العربية السعودية، وتختص بالنظر في أي نزاع المحاكم السعودية المختصة، أو التحكيم وفقًا لنظام التحكيم السعودي بناءً على اختيار الأطراف عند التوقيع.

---

## 12. الأطراف

### المعالج (Dealix)
- الاسم القانوني: _<السجل التجاري الكامل>_
- العنوان الوطني: _<العنوان>_
- DPO: _<الاسم>_ — `privacy@dealix.sa`
- المخوّل بالتوقيع: _<الاسم والصفة>_
- التوقيع: ____________________  التاريخ: __________

### المتحكم (العميل)
- الاسم القانوني: ____________________
- العنوان: ____________________
- نقطة الاتصال (DPO إن وجد): ____________________
- المخوّل بالتوقيع: ____________________
- التوقيع: ____________________  التاريخ: __________

---

## ملاحق

- **الملحق أ:** قائمة محدّثة بالمعالجين الفرعيين — `https://dealix.sa/sub-processors.html`
- **الملحق ب:** تفاصيل المعالجة (الفئات، المدد، الضوابط) — `docs/ops/PDPL_RETENTION_POLICY.md`
- **الملحق ج:** Runbook خرق البيانات — `docs/ops/PDPL_BREACH_RUNBOOK.md`

---

# English Companion Summary — Data Processing Agreement

> This English summary accompanies the Arabic DPA above for bilingual
> readability. The Arabic text is the operative version. **A licensed Saudi
> lawyer must review both before signing with any customer.**

**Parties.** Dealix (Processor) and the Customer (Controller).

**Governing law.** The Saudi Personal Data Protection Law (PDPL), Royal
Decree M/19, and its SDAIA implementing regulations. Disputes are heard by
the competent Saudi courts, or by arbitration under the Saudi Arbitration
Law if the parties so elect at signing.

**Purpose.** Dealix processes personal data solely to operate the Dealix
platform for the Customer, deliver approved revenue/growth services,
maintain secure backups, run PII-redacted operational analytics, and meet
legal obligations. Any other purpose needs prior written Controller consent.

**Processor obligations (PDPL Art. 17).** Process only on documented
Controller instructions; apply technical and organizational security
(encryption in transit and at rest, access control, access auditing);
ensure staff confidentiality; assist with data-subject requests within 30
days; notify the Controller of any suspected breach within 24 hours so the
Controller can meet its 72-hour SDAIA obligation; delete or return data on
termination; allow annual audit of these commitments.

**Sub-processors.** Listed at `dealix.sa/sub-processors.html`. Any new
sub-processor touching personal data is notified 30 days before activation,
with the Controller's right to a reasoned objection.

**Cross-border.** Primary operational data is hosted on Railway (US-East)
with encrypted backups in AWS S3 `me-south-1` (Bahrain). Any international
transfer requires equivalent contractual safeguards, explicit Controller
consent, or an express legal exception.

**Termination.** Dealix stops processing immediately, deletes all personal
data within 30 days (or returns it machine-readable on request), expires
encrypted backups per the backup cycle, and delivers a deletion-confirmation
report within 7 days.

**Liability.** Each party is liable for direct damages from its breach,
capped at 12 months of fees — except for intentional misconduct, gross
negligence, or confidentiality breaches, which are uncapped.

---

# نموذج موافقة معالجة البيانات (PDPL) — PDPL Data-Processing Consent Form

> ⚠️ نموذج للمراجعة — يحتاج مراجعة محامٍ مرخّص قبل الاستخدام.
> Draft consent form — requires licensed-lawyer review before use.
> يُوقَّع مع DPA أعلاه قبل بدء أي Sprint مدفوع.
> Signed alongside the DPA above before any paid Sprint begins.

**الشركة العميلة / Customer company:** ____________________

**رقم السجل التجاري / CR number:** ____________________

**الممثّل المخوّل / Authorized representative:** ____________________

**المسمّى / Title:** ____________________

---

### الإقرار / Acknowledgement

بصفتي ممثّلاً مخوّلاً عن الشركة العميلة، أقرّ بما يلي:
As the Customer's authorized representative, I acknowledge that:

- [ ] أفوّض Dealix بمعالجة البيانات الشخصية الموضّحة في DPA أعلاه، للأغراض
  المذكورة فيه حصراً. / I authorize Dealix to process the personal data
  described in the DPA above, solely for the purposes stated therein.
- [ ] أفهم أن Dealix **لا يرسل** أي رسالة خارجية نيابةً عن الشركة دون
  موافقة صريحة على كل مسودة. / I understand Dealix **does not send** any
  external message on the company's behalf without explicit per-draft
  approval.
- [ ] أفهم أن Dealix **لا يقوم بـ scraping** ولا تواصل بارد ولا إرسال
  جماعي. / I understand Dealix performs **no scraping**, no cold outreach,
  and no bulk messaging.
- [ ] أفهم أن مخرجات الخدمة تقديرية ما لم تُوثَّق كقيمة مُتحقَّقة، وأن Dealix
  لا يقدّم ضمانات نتائج. / I understand service outputs are estimates
  unless documented as Verified value, and that Dealix offers no
  guaranteed-results claims.
- [ ] أملك الصلاحية القانونية لتقديم البيانات المشمولة بهذه الموافقة. /
  I have the legal authority to provide the data covered by this consent.

**نطاق البيانات المُوافَق عليها / Data scope consented:**
[تُحدَّد بالإشارة إلى جدول §3 من DPA / per the table in §3 of the DPA]

**مدة الموافقة / Consent duration:** مدة العقد، وتُسحب كتابياً في أي وقت /
the contract term; withdrawable in writing at any time.

---

### التوقيع / Signature

**التوقيع / Signature:** ____________________

**الاسم / Name:** ____________________

**التاريخ / Date:** ____________________

> سحب الموافقة: ترسَل كتابياً إلى `privacy@dealix.sa`؛ يتوقّف Dealix عن
> المعالجة وفق §9 من DPA. / Withdrawal: send in writing to
> `privacy@dealix.sa`; Dealix stops processing per DPA §9.

---

*الإصدار v1.1 — 2026-05-18 · أُضيف الملخّص الإنجليزي ونموذج الموافقة الثنائي اللغة · مراجعة قانونية مطلوبة قبل التطبيق.*

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
