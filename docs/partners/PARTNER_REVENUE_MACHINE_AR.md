# ماكينة إيرادات الشركاء

> النسخة الإنجليزية القانونية: [`PARTNER_REVENUE_MACHINE.md`](./PARTNER_REVENUE_MACHINE.md).

## مرجع الدوكترين
- الالتزامات: #1، #2، #5.
- القرارات المثبّتة: الموافقة-أولًا للأفعال الخارجية وغير القابلة للرجوع.

## الغرض

تحويل الشركاء إلى قنوات إحالة وبيع مشترك مؤهّلة. في B2B السعودي، المقدمة الدافئة من مشغّل ذي مصداقية تحوّل أسرع من التواصل البارد. لذلك حركة الشركاء قناة تصريف من الدرجة الأولى، مو تابعة.

## أنواع الشركاء

- مستشارون مستقلون.
- وكالات تسويق/مبيعات/تكامل.
- مطبّقو ERP.
- مستشارو الأمن السيبراني.
- محاسبون.
- مشغّلو نظام الشركات الناشئة.
- جهات اتصال الغرف التجارية والفعاليات.

## الحركة الأسبوعية (إحماء)

- 10 طلب إحالة/أسبوع.
- 3 محادثات شريك/أسبوع.
- 1 فرصة بيع مشترك/أسبوع.
- 1 مقدمة مؤهّلة مستلمة/أسبوع.

أهداف نشاط، مو وعود.

## القواعد الجوهرية

- الشريك ما يستطيع وعد بنتيجة نيابة عن Dealix.
- الشريك ما يستطيع تغيير السعر أو النطاق نيابة عن Dealix.
- العمولة فقط على **نقد مُحصَّل**، لا على pipeline أو PO موقّع وحده.
- كل إحالة تُتتبَّع مع شريكها المصدر.
- شريك يمد leads سيئة باستمرار → ملاحظات مرة، ثم تخفيض أولوية.
- علاقة شريك بدون مقدمات مؤهّلة لشهرين → مراجعة وإعادة وضع أو إيقاف.

## سجل الإحالات

شريك المصدر، الحساب المُحال، تاريخ المقدمة، الحالة، شروط العمولة، العمولة المدفوعة، رابط دليل المصدر لحدث النقد.

## الإيقاع

- أسبوعي: مراجعة حركة الشركاء.
- شهري: بطاقة الشركاء.
- ربع سنوي: مراجعة مزيج الشركاء.

## الربط بالتشغيل

- وثائق الشركاء القائمة في `docs/partners/` (6 ملفات).
- `db/models.py::AuditLogRecord`.
- `auto_client_acquisition/revenue_memory/event_store.py`.
- `db/models.py::LeadRecord`.

## روابط ذات صلة

- وثائق `docs/partners/`
- [`../distribution/DEALIX_DISTRIBUTION_OS_AR.md`](../distribution/DEALIX_DISTRIBUTION_OS_AR.md)
- [`../distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md`](../distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md)
- [`../legal/COMMERCIAL_CONTRACT_PACK_AR.md`](../legal/COMMERCIAL_CONTRACT_PACK_AR.md)
- [`../founder/REVENUE_WAR_ROOM_OS_AR.md`](../founder/REVENUE_WAR_ROOM_OS_AR.md)
- [`../finance/BILLING_RECEIVABLES_OS_AR.md`](../finance/BILLING_RECEIVABLES_OS_AR.md)

## بنود مفتوحة

- جداول `partner` و`referral` first-class في `db/models.py`: غير موجودة؛ السجل اليوم markdown/spreadsheet.
- بوابة شريك في المنتج: خارج النطاق هذا الربع.
- نموذج اتفاقية شريك معياري مرجعي في `docs/legal/COMMERCIAL_CONTRACT_PACK_AR.md` لكنه يعيش عبر ملفات.
