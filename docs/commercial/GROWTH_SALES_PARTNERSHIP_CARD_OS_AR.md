# Dealix Growth, Sales & Partnership Card OS

## الهدف

هذه الطبقة تحول واتساب/الإيميل/لينكدإن/الشراكات من رسائل عشوائية إلى **نظام تشغيل تجاري يومي** يخدم الشركات في:

- المبيعات الجديدة
- نمو الحسابات الحالية
- الشراكات
- استرجاع العملاء المتوقفين
- دفع العروض المفتوحة
- تصنيف الردود
- توجيه الفريق إلى next action واضح

الفكرة ليست أن Dealix يكون مجرد بوت يرسل رسائل. الفكرة أن Dealix يكون **Commercial Co-Pilot للشركة**: يقرأ الحسابات والفرص، يجهز كروت قرار، يولد مسودات، يطلب موافقة بشرية، ثم يسجل كل شيء في غرفة القيادة.

---

## التموضع التجاري

**Dealix Growth Card OS** هو منتج للشركات التي عندها مبيعات أو شراكات أو متابعات كثيرة لكنها تضيع بين واتساب، الإيميل، CRM، ملفات Excel، والموظفين.

الرسالة للعميل:

> Dealix يرتب لك فرص المبيعات والشراكات والمتابعات في كروت قرار يومية: من نكلم، لماذا، ماذا نرسل، ما الخطوة التالية، ومن يوافق قبل أي إرسال خارجي.

---

## ماذا يستلم العميل؟

### 1. Commercial Command Room

لوحة تعرض:

- الحسابات الساخنة
- فرص الشراكة
- العروض المفتوحة
- المتابعات المتأخرة
- العملاء الذين يحتاجون إنقاذ
- الرسائل الجاهزة للمراجعة
- القرارات المطلوبة من المالك/مدير المبيعات

### 2. WhatsApp / Inbox Action Cards

كروت عملية لكل فرصة، مثل:

```text
شركة: مثال للخدمات اللوجستية
الهدف: شراكة توزيع / تكامل
الألم المتوقع: تأخر المتابعة وضياع عروض B2B
القناة المقترحة: WhatsApp بعد opt-in أو email كبديل
الرسالة: مسودة قصيرة جاهزة
الأزرار: اعتماد / تعديل / تخطي
الحالة: Draft only until approved
```

### 3. Growth Motions

النظام لا يكتفي بـ cold outreach. يدعم 7 حركات نمو:

| الحركة | الهدف | أمثلة |
|---|---|---|
| Sales Prospecting | فتح فرص جديدة | عيادات، عقار، تدريب، لوجستيات |
| Partnership Outreach | شراكات توزيع/تكامل | وكالات، مزودي CRM، شركات خدمات |
| Proposal Push | تحريك عروض مفتوحة | متابعة عرض، توضيح قيمة، طلب اجتماع |
| Revival | استرجاع عميل/lead توقف | آخر تواصل قديم، ردود لم تغلق |
| Upsell | بيع طبقة أعلى | Command Room ثم Company Brain |
| Retention | تقليل churn | تقرير قيمة أسبوعي وnext value |
| Referral | طلب إحالة | عميل راضٍ أو شريك مناسب |

---

## المبادئ غير القابلة للكسر

1. **لا إرسال خارجي افتراضيًا.**
2. **لا واتساب بارد لجهة غير مصرح بها.**
3. **كل رسالة تبدأ كمسودة.**
4. **كل إرسال حساس يحتاج موافقة بشرية.**
5. **كل هدف يحتاج source_url أو مصدر واضح.**
6. **لا وعود ROI مضمونة.**
7. **لا شهادات أو عملاء وهميين.**
8. **كل opt-out يحترم فورًا.**
9. **كل كرت له owner_decision: review / send / call / hold / discard.**
10. **غرفة القيادة هي المصدر اليومي للقرار.**

---

## حالات الاستخدام التجارية

### أ. مبيعات B2B

النظام يقرأ قائمة الشركات، يصنف الأولوية، ويولد كروت:

- سبب الاستهداف
- pain hypothesis
- المنتج المناسب من Dealix
- مسودة رسالة
- next action
- owner decision

### ب. الشراكات

للشركات التي تحتاج توزيع أو تكامل أو referral channel:

- partner fit score
- mutual value angle
- partnership ask
- draft intro
- follow-up sequence

### ج. نمو العملاء الحاليين

للحسابات التي تم تسليم خدمة لها:

- proof achieved
- next value opportunity
- upsell path
- renewal risk
- value report draft

### د. متابعة العروض

لكل عرض مفتوح:

- قيمة العرض
- آخر تواصل
- سبب التعطل
- follow-up draft
- objection angle
- next meeting ask

---

## شكل الكرت التجاري

كل كرت يجب أن يحتوي:

```yaml
card_id:
company_name:
sector:
city:
motion: sales | partnership | proposal_push | revival | upsell | retention | referral
recommended_channel: email | whatsapp | linkedin_manual | phone | partner_referral
risk_level: low | medium | high
approval_required: true
source_url:
verification_status:
pain_hypothesis:
dealix_angle:
draft_message_ar:
draft_message_en:
buttons:
  - approve
  - edit
  - skip
owner_decision: review
next_action:
```

---

## واتساب كروت وأزرار

واتساب يدعم في هذا النظام:

- كرت فرصة
- كرت اعتماد رسالة
- كرت متابعة
- كرت اجتماع
- كرت شراكة
- كرت تقرير يومي

لكن الإرسال الحي يبقى مقفلًا إلا إذا تحققت كل الشروط:

```text
EXTERNAL_SEND_ENABLED=true
WHATSAPP_SEND_ENABLED=true
WHATSAPP_ALLOW_LIVE_SEND=true
OUTBOUND_MODE=controlled_live
contact.whatsapp_opt_in=true
message.status=approved
template approved if outside session window
```

---

## الباقات التجارية المقترحة

| الباقة | المدة | السعر المقترح | المخرجات |
|---|---:|---:|---|
| Growth Diagnostic | 3 أيام | 1,500–3,000 ريال | فحص قنوات ومتابعات وفرص |
| Growth Card Sprint | 7 أيام | 5,000–12,000 ريال | 50–100 فرصة، 25 كرت، غرفة قيادة |
| Partnership Sprint | 10 أيام | 8,000–18,000 ريال | قائمة شركاء، كروت شراكة، رسائل متابعة |
| Revenue Command Room | 14 يوم | 15,000–35,000 ريال | تشغيل كامل + تقارير + proof pack |
| Managed Growth OS | شهري | 5,000–25,000 ريال | تشغيل أسبوعي + متابعة + تحسين مستمر |

الأسعار نطاقات تشغيلية وليست وعود سوقية ثابتة.

---

## روتين التشغيل اليومي

```text
1. تحميل الحسابات/الفرص
2. التحقق من المصدر والحالة
3. scoring للأولوية
4. توليد كروت sales/partnership/growth
5. توليد مسودات رسائل
6. عرضها في Command Room
7. موافقة المؤسس/العميل
8. إرسال يدوي أو controlled-live لاحقًا
9. تسجيل الردود
10. تحديث التقرير اليومي
```

---

## معيار النجاح

بعد أول Sprint، يجب أن يحصل العميل على:

- قائمة فرص مرتبة وليست مبعثرة
- مسودات تواصل قابلة للمراجعة
- كروت قرار واضحة لفريقه
- تقرير يومي/أسبوعي يبين ماذا حصل
- proof pack يثبت العمل المنجز
- مسار واضح للشهر القادم

---

## ما لا نعد به

- لا نعد بإيراد مضمون.
- لا نعد بنتائج بدون بيانات أو متابعة.
- لا نرسل واتساب بارد عشوائيًا.
- لا نستخدم أسماء عملاء أو أرقام وهمية.
- لا نفتح إرسال حي بدون موافقة وسياسات.

---

## الخطوة التالية في الريبو

هذه الطبقة يجب أن ترتبط بـ:

- `auto_client_acquisition/personal_operator/whatsapp_cards.py`
- `docs/WHATSAPP_OPERATOR_FLOW.md`
- `scripts/commercial/generate_growth_sales_cards.py`
- `reports/commercial/growth_cards/latest.json`
- `apps/web` Commercial Command Room لاحقًا
