# Revenue Lab — تشغيل Dealix على Dealix لمدة 14 يومًا

## الهدف

إثبات أن Dealix يستطيع يوميًا تحويل إشارات موثقة إلى فرص مرتبة، واستراتيجيات، وعروض، وخطط تسليم، وطلبات موافقة، وسجل إثبات — بدون إرسال خارجي تلقائي وبدون اختراع نتيجة أو عميل.

## الحدود غير القابلة للتجاوز

- لا scraping، ولا شراء بيانات مجهولة المصدر، ولا cold WhatsApp.
- لا إرسال أو نشر أو خصم أو عقد أو دفع أو تغيير Production دون موافقة صريحة.
- `priority_score` لترتيب العمل فقط، وليس احتمال إغلاق.
- كل ألم محتمل يبقى `hypothesis` حتى يؤكده العميل.
- Demo لا يدخل Proof Ledger ولا يصلح كدراسة حالة.
- التعلم يقترح تجربة، ولا يغيّر الأوزان ذاتيًا قبل مراجعة بشرية ونتائج متكررة.

## ملف الإدخال الحقيقي

انسخ الملف التجريبي `data/examples/revenue_lab_signals.demo.json` إلى ملف داخلي غير منشور، ثم لكل شركة:

1. استبدل `demo=true` بـ `false`.
2. أضف مصدرًا مؤرخًا ومسموحًا: موقع الشركة، إعلان رسمي، وظيفة منشورة، خبر أصلي، CRM داخلي بموافقة، أو إحالة موثقة.
3. سجّل حالة الإذن: `research_only`, `warm`, `inbound`, `referral`, `opted_in`, أو `approved`.
4. لا تضع اسم شخص أو هاتفًا أو بريدًا ما لم يكن جمعه واستخدامه مشروعًا ومطلوبًا.
5. اترك `known_metrics` فارغًا حتى تحصل على baseline من العميل.

## الأمر اليومي

```bash
python scripts/commercial/run_revenue_lab_daily.py \
  --input /secure/path/dealix_signals.json \
  --output-dir reports/revenue_lab/$(date -u +%F) \
  --proof-ledger-dir docs/proof-events
```

للتأكد من البنية فقط:

```bash
python scripts/commercial/run_revenue_lab_daily.py --demo
python scripts/commercial/verify_master_startup_phase0.py
```

## إيقاع 14 يومًا

| اليوم | العمل | الدليل المطلوب |
|---:|---|---|
| 1 | تعريف ICP والعروض المسموح بها | نسخة مؤرخة من معايير الاختيار |
| 2 | إدخال 5–10 إشارات موثقة | Source refs وتاريخ الرصد |
| 3 | مراجعة الفرضيات والمجهول | قبول/رفض بشري لكل فرضية |
| 4 | ترتيب Opportunity Graph | Priority score مع أسبابه، بلا win probability |
| 5 | تجهيز 3 diagnostics drafts | Approval Queue فقط |
| 6 | اختبار الاعتراضات في Sales Arena | سجل ردود وفشل وممنوعات |
| 7 | تقرير أسبوع أول | ما اكتشف، ما حُجب، ولا ادعاء نتيجة |
| 8 | إدخال outcomes حقيقية من CRM/ردود مصرح بها | Source ref لكل outcome |
| 9 | اقتراح تجربة واحدة | فرضية، عينة، guardrail، معيار إيقاف |
| 10 | بناء Proposal + ROI scenario لمن يملك baseline | الافتراضات والـ disclaimer |
| 11 | مراجعة خطة Delivery لـ14 يومًا | acceptance criteria وproof targets |
| 12 | فحص Approval/Proof linkage | كل action له audit_ref وproof_target |
| 13 | إغلاق الفجوات وإعادة التشغيل | Test logs وartifact diff |
| 14 | Proof Pack داخلي | نتائج فعلية فقط، وموافقة نشر منفصلة |

## معيار النجاح قبل البيع

- 10 أيام تشغيل ناجحة على الأقل من أصل 14.
- صفر external action غير معتمد.
- 100% من الفرص لها مصدر وحالة إذن ومعلومات مجهولة واضحة.
- 100% من المسودات الخارجية في Approval Queue.
- صفر conversion probability غير معاير.
- نتائج فعلية مؤرخة ومسنودة بمصدر؛ لا يكفي أن الكود اشتغل.
- أي دراسة حالة عامة تحتاج موافقة العميل وProof Ledger صالحًا للنشر.

## مخرجات كل يوم

- `latest.json` و`latest.md`
- `opportunity_graph.csv`
- `approval_queue.csv`
- `proof_log.json`

هذه الملفات هي سجل تشغيل داخلي؛ لا تتحول تلقائيًا إلى مادة تسويقية.
