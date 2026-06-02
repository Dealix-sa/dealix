# صف الردود — Reply Queue

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المصدر:** docs/outreach/REPLY_HANDLING_OS_AR.md
**يُولَّد بواسطة:** scripts/verify_market_production_os.py
**التاريخ:** {{ date }}

> قالب — الصفوف عناصر نائبة. unsubscribe و angry و bounce تُكبَح فوراً.

## الردود حسب الفئة

| الفئة | العدد | الإجراء | الكبح؟ |
|-------|------|---------|--------|
| positive | {{ positive_count }} | دعوة اكتشاف/تشخيص | لا |
| interested_later | {{ later_count }} | جدولة إعادة تواصل (nurture) | لا |
| price_question | {{ price_count }} | بطاقة عرض من السلّم | لا |
| send_more_info | {{ info_count }} | حزمة إثبات آمنة | لا |
| wrong_person | {{ wrong_count }} | طلب إحالة | لا |
| not_interested | {{ noint_count }} | إغلاق مهذّب (lost) | لا |
| unsubscribe | {{ unsub_count }} | كبح فوري | **نعم** |
| angry | {{ angry_count }} | اعتذار + كبح فوري | **نعم** |
| auto_reply | {{ auto_count }} | إعادة جدولة | لا |
| bounce | {{ bounce_count }} | كبح البريد المرتدّ | **نعم** |

## الردود الإيجابية (مسار الاجتماع)

| # | الشركة | الدور | الإجراء التالي | واتساب بعد موافقة؟ |
|---|--------|-------|----------------|---------------------|
| 1 | {{ p1_company }} | {{ p1_role }} | {{ p1_next }} | {{ p1_whatsapp_consent }} |

> واتساب بعد رد/موافقة صريحة فقط (docs/whatsapp/). لا واتساب بارد.

## إجراءات الكبح الفوري المنفّذة

| العنوان/المعرّف | الفئة | وقت الكبح |
|------------------|-------|-----------|
| {{ s1_id }} | {{ s1_category }} | {{ s1_time }} |

> يُزامَن مع قائمة الكبح (schemas/suppression.schema.json).

## الخطوة التالية

- تأكيد مواعيد الردود الإيجابية وتحديث `state = meeting_booked`.
- تحديث حالات العملاء المحتملين في docs/outreach/PROSPECT_RESEARCH_OS_AR.md.

## روابط

- معالجة الردود: docs/outreach/REPLY_HANDLING_OS_AR.md
- الانسحاب: docs/outreach/UNSUBSCRIBE_POLICY_AR.md
- واتساب بعد الموافقة: docs/whatsapp/

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
