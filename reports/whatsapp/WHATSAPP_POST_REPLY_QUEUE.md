# طابور واتساب بعد الرد — WhatsApp Post-Reply Queue

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**النوع:** قالب تشغيلي — صفوف نموذجية (placeholder) تُستبدل بجهات حقيقية ردّت.
**المالك:** المؤسس (سامي)
**يقرأ القواعد من:** docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md · docs/whatsapp/WHATSAPP_ACTION_CARDS_AR.md · docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md
**آخر تحديث:** 2026-06-02

---

## قاعدة الدخول (حرجة)

**تظهر الصفوف هنا فقط بعد ردّ وارد أو موافقة صريحة.** لا صفّ لجهة لم تردّ. لا إدخال جماعي. واتساب ليس قناة باردة — هذا الطابور **نتيجة** ردّ، لا بداية تواصل.

## كيف يُستخدم

- صفّ واحد لكل **جهة ردّت إيجاباً** وتُتابَع على واتساب.
- المراحل تطابق التدفّق: عرض القناة → فحص الجاهزية → بطاقة العرض → حزمة الإثبات → تسليم الدفع.
- كل فعل في «آخر إجراء» يتطلّب موافقة المؤسس قبل تنفيذه.

## جدول الطابور (صفوف نموذجية)

| الجهة (بعد الرد) | المرحلة | آخر إجراء | قرار المؤسس |
|------------------|---------|-----------|--------------|
| [جهة ردّت 1] | عرض القناة | عُرض واتساب أو حجز | بانتظار الموافقة على المتابعة |
| [جهة ردّت 2] | فحص الجاهزية | أُرسلت أسئلة الفحص القصيرة | مُعتمَد — جهّز بطاقة عرض |
| [جهة ردّت 3] | تسليم الدفع | قبول كتابي للعرض | مُعتمَد — أرسل رابط الدفع 1:1 |

> هذه صفوف توضيحية فقط. لا تُملأ بأي جهة لم تردّ. الأرقام والحالات تقديرية حتى التأكيد.

## الحدود

- لا cold WhatsApp، لا أتمتة، لا blast، لا جدولة بلا مراجعة بشرية.
- الحد الأقصى للتوقيت: الأحد–الخميس 9ص–6م الرياض.
- لا أسماء عملاء أو بيانات شخصية حسّاسة في الجدول.
- لا رابط دفع قبل قبول كتابي.

## الخطوة التالية

عند ورود ردّ إيجابي جديد: صنّفه عبر docs/ops/reply_playbooks_ar.md، افتح صفّاً واحداً هنا في مرحلة «عرض القناة»، وجهّز البطاقة المناسبة من docs/whatsapp/WHATSAPP_ACTION_CARDS_AR.md للموافقة.

## English summary

A template queue for post-reply WhatsApp work. Critical entry rule: rows appear only after an inbound reply or explicit consent — no row for anyone who has not replied, no bulk entry. WhatsApp is never a cold channel; this queue is the result of a reply, not the start of outreach. One row per positively-replied contact, with stages matching the flow (offer channel → readiness scan → proposal card → proof pack → payment handoff). Every "last action" requires founder approval before execution. Columns: contact-after-reply, stage, last action, founder decision. Rows are illustrative placeholders, never filled with a non-replying contact; numbers and statuses are estimated until confirmed. Boundaries: no cold WhatsApp, no automation, no blast, no scheduling without human review, Riyadh business hours only, no customer names or sensitive personal data, no payment link before written acceptance.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
