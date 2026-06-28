# Dealix Client Growth Negotiation OS

## الهدف

هذه الطبقة تجعل Dealix قادرًا على خدمة Dealix داخليًا وخدمة الشركات كـ Growth Operator يفهم الردود، يصنف الاعتراضات، يقترح التفاوض، يجهز الخطوة التالية، ويحمي الشركة من الالتزامات غير المعتمدة.

النظام ليس chatbot، وليس CRM notes، وليس إرسال عشوائي.

هو نظام تشغيل تجاري يربط:

- فهم العميل.
- تصنيف الرد.
- اقتراح رد تفاوضي.
- اقتراح next action.
- تجهيز meeting أو proposal brief.
- منع الالتزامات الخطرة.
- تسجيل audit وproof.

## ما يستطيع فعله

- فهم اعتراض السعر.
- اقتراح pilot أصغر.
- اقتراح diagnostic sprint.
- تحويل not now إلى nurture.
- تجهيز booking options عند طلب اجتماع.
- تجهيز proposal brief عند طلب التفاصيل.
- تجهيز partner brief عند طلب شراكة.
- تحويل طلب العقد إلى legal review handoff.
- إيقاف التواصل عند unsubscribe.

## ما لا يستطيع فعله بدون موافقة

- اعتماد خصم.
- تحديد سعر نهائي.
- قبول شروط قانونية.
- توقيع عقد.
- الالتزام بتاريخ تسليم نهائي بدون capacity check.
- الوعد بإيراد أو ROI مضمون.
- الالتزام باسترجاع أو دفع.
- إرسال خارجي بدون موافقة وقواعد القناة.

## مستويات الاستقلالية

| المستوى | الوصف |
|---|---|
| A0 Draft Only | يولد مسودات وخطط فقط |
| A1 Assisted Operator | يجهز كروت موافقة للمالك أو مسؤول المبيعات |
| A2 Controlled Live | يرسل فقط بعد approval وpolicy gates وrate limits |
| A3 Restricted | السعر النهائي، الخصومات، العقود، الضمانات، والالتزامات القانونية ممنوعة بدون founder/client approval |

## التشغيل اليومي الداخلي لـ Dealix

```bash
python scripts/commercial/run_negotiation_operator_day.py
```

المخرجات:

```text
reports/commercial/negotiation_operator/latest.json
reports/commercial/negotiation_operator/latest.md
```

## تجربة العميل

العميل يرى:

1. الرد الوارد.
2. تصنيف الاعتراض.
3. الرد المقترح.
4. ما يسمح للنظام بقوله.
5. ما يمنع النظام من الالتزام به.
6. الخطوة التالية.
7. هل يحتاج موافقة.
8. سبب المخاطر.

## كيف يباع

اسم العرض:

**Dealix Client Growth Operator OS**

الوصف:

> Dealix يشغل لك طبقة نمو ذكية فوق واتساب، الإيميل، لينكدإن، التقويم، والـCRM. النظام يكتشف الفرص، يجهز الرسائل، يصنف الردود، يقترح التفاوض، يحضر المواعيد والعروض، ويتابع يوميًا — مع موافقات واضحة قبل أي إجراء خارجي حساس.

## شروط النجاح

- كل reply له تصنيف.
- كل اعتراض له next action.
- كل تفاوض له forbidden commitments.
- لا يوجد live commitments.
- لا يوجد إرسال بدون review.
- كل proposal brief يبقى غير ملزم حتى الاعتماد.
- كل طلب عقد يذهب إلى legal review.
- كل unsubscribe يذهب إلى suppression.

## المرحلة التالية

بعد هذه الطبقة، نربطها بـ:

- Channel Control Plane.
- Proposal Factory.
- Booking Desk.
- Client Command Room.
- HubSpot / CRM sync.
- Controlled Live Outbound بعد الموافقات.
