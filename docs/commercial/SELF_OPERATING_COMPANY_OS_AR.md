# Dealix Self-Operating Company OS

## الهدف

تحويل Dealix إلى نظام تشغيل شركة شبه مستقل يدير التشغيل التجاري اليومي من غير ما يعتمد على تشتت المؤسس.

النظام لا يكون بوت سبام ولا CRM عادي. هو عقل تشغيل يومي يقوم بـ:

1. قراءة حالة الإنتاج والـ CI والـ PRs.
2. تحديد أهم أعمال اليوم.
3. ترتيب الاستهداف التجاري.
4. بناء قائمة فرص مرتبة.
5. كتابة مسودات رسائل وعروض.
6. تجهيز Approval Queue.
7. تجهيز Proof Pack.
8. إنتاج محتوى مبني على إثبات.
9. تسجيل التعلم والنتائج.
10. تكرار الدورة يوميًا.

## القاعدة الأساسية

```txt
الذكاء، التحليل، التصنيف، الكتابة، التقارير، والتعلم تكون تلقائية.
الإرسال، النشر، الدفع، الدمج، وتعديل الإنتاج تحتاج موافقة صريحة.
```

## الطبقات

### 1. Production Trust Layer

قبل التوسع التجاري، يجب تثبيت الثقة:

- Production Smoke.
- Railway config.
- Security checks.
- OpenSSF / hardening.
- No broken deploy claims.

الأولوية الحالية:

1. #872 لإصلاح protected API smoke.
2. #858 لتثبيت Railway config.

### 2. Money Now Layer

الهدف الأول ليس بناء كل المنصة، بل إغلاق أول دخل حقيقي.

أقرب عرض:

**Revenue Proof Sprint — 499 SAR**

المسار:

```txt
lead_selected
-> offer_drafted
-> founder_approved
-> offer_sent_manually
-> payment_instruction_approved
-> invoice_sent
-> payment_received
-> work_started
-> proof_pack_delivered
-> closed_won
```

لا يتم احتساب الإيراد قبل `payment_received`.

### 3. Grand Targeting Layer

النظام يبني TargetCard لكل فرصة:

```txt
company_name
sector
target_type
source
pain_hypothesis
offer_fit
score
risk_level
recommended_channel
next_action
approval_status
```

يتم التقييم حسب:

- ملاءمة العميل.
- وضوح الألم.
- احتمالية الدفع.
- سهولة الوصول لصاحب القرار.
- قيمة الصفقة.
- وجود proof مناسب.
- مستوى المخاطر.

### 4. Drafting Layer

النظام يكتب:

- LinkedIn draft.
- Email draft.
- WhatsApp manual draft فقط في سياق دافئ أو بموافقة.
- phone script.
- follow-up script.
- one-page offer.
- meeting prep brief.

كلها مسودات، لا إرسال مباشر.

### 5. Approval Layer

أي عمل خارجي يدخل Approval Queue:

```txt
target_id
action_type
channel
draft_text
risk_flags
proof_to_attach
status
```

### 6. Proof Layer

كل شيء مهم يسجل كدليل:

- عرض أرسل.
- فاتورة أرسلت.
- دفع وصل.
- عمل بدأ.
- Proof Pack سلم.
- عميل أغلق.

بدون proof لا توجد claims.

### 7. Content Layer

النظام يحول العمل إلى محتوى:

- تحديث مؤسس.
- LinkedIn post draft.
- Market insight.
- case note بدون أسماء عملاء إلا بموافقة.
- SEO report draft.

### 8. Learning Layer

يتعلم من:

- الردود.
- عدم الرد.
- الاعتراضات.
- الاجتماعات.
- الفواتير.
- الدفع.
- proof delivery.

## التشغيل

```bash
python scripts/commercial/run_self_operating_company_os.py --mode draft-only --limit 50
```

المخرجات:

```txt
reports/self_operating_company_os/daily/YYYY-MM-DD.md
reports/self_operating_company_os/actions/YYYY-MM-DD.json
reports/self_operating_company_os/approvals/YYYY-MM-DD.json
reports/self_operating_company_os/targets/YYYY-MM-DD.json
reports/self_operating_company_os/proof/YYYY-MM-DD.json
reports/self_operating_company_os/content/YYYY-MM-DD.md
```

## الممنوعات

- لا cold WhatsApp.
- لا mass LinkedIn.
- لا scraping مخالف.
- لا fake proof.
- لا guaranteed revenue claims.
- لا government access claims.
- لا إرسال خارجي بدون موافقة.
- لا live payment بدون PR موافقة.
- لا دمج PR تلقائي.
- لا secrets في الكود أو التقارير.

## الخطة التنفيذية

1. ثبّت production trust: #872 ثم #858.
2. نفّذ أول close: #873.
3. شغّل acquisition queue: #871.
4. شغّل grand targeting: #874.
5. اربط autonomous OS: #869.
6. وسّع التجاري: #849 ثم #850.

## النتيجة المتوقعة

كل صباح يعطيك النظام:

- أهم 10 فرص.
- أهم 12 عمل داخلي.
- مسودات تحتاج موافقة.
- Proof log.
- محتوى جاهز للمراجعة.
- قرار واضح: ماذا نصلح؟ ماذا نبيع؟ ماذا نرسل يدويًا؟ ماذا نثبت؟
