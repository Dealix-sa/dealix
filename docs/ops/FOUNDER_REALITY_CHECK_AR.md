# فحص واقع المؤسس — Founder Reality Check

أمر واحد يجيب على ثلاثة أسئلة بصدق، بدون توليد إيرادات وهمية وبدون
ادّعاء وكلاء غير موجودين:

1. **ما المربوط فعلياً في المستودع اليوم؟** (ملفات حقيقية + ما تثبته)
2. **ما الذي ادّعت جلسات سابقة بناءه ولم يصل؟** (مع التحقق من غيابه)
3. **ما المطلوب اليوم؟** (3 إجراءات مرتبطة بالبوابات المغلقة فعلياً)

## التشغيل

```bash
python3 scripts/founder_reality_check.py          # تقرير قابل للقراءة
python3 scripts/founder_reality_check.py --json   # JSON للمحركات الأخرى
python3 scripts/founder_reality_check.py --quiet  # سطر الـ Verdict فقط
```

كود الخروج:

- `0` عندما تكون بوابة المرحلة 0–1 مفتوحة (`payment_received` + `proof_pack_delivered` + KPIs من CRM حقيقي).
- `1` خلاف ذلك. هذه ليست أخطاء — بل قاعدة `no_build_until_first_paid`.

## النتائج المحتملة (`FOUNDER_REALITY_CHECK_VERDICT`)

| نتيجة | معناها | الإجراء |
| --- | --- | --- |
| `PRE_PIPELINE` | لا أحداث حقيقية بعد في `evidence_events_tracker.csv` (فقط `template_funnel_seed`) | ركّز على اللمس اليدوي وتسجيل أول `message_sent_manual` لشركة حقيقية |
| `PIPELINE_OPEN_NO_REVENUE` | أحداث ليدز حقيقية بدون دفع | ادفع نحو `invoice_sent` ثم `payment_received` |
| `EVIDENCE_IN_PROGRESS` | دفع أو Proof Pack جزئي | أغلق العنصر الناقص + استورد KPIs من CRM |
| `GATE_OPEN` | بوابة 0–1 مفتوحة | اعتمد روتين War Room — والبناء بعدها قيد التكرار لا توسعة |

## ما الذي يفحصه؟

### Wired Anchors (المثبتات الحقيقية)

ملفات ينبغي أن توجد. لو اختفى أحدها، يفشل الاختبار `test_wired_anchors_all_present`
تلقائياً ويعرف الكل أن دعاية النظام أصبحت غير صادقة.

تشمل: `dealix/commercial_ops/founder_comprehensive_plan.py`، `dealix/payments/moyasar.py`،
`api/routers/founder.py`، `frontend/src/app/[locale]/ops/founder/page.tsx`،
`docs/commercial/operations/evidence_events_tracker.csv`، الـ scripts الكنونية، إلخ.

### Claimed but Absent (ادّعاءات غائبة)

ملفات وصفتها جلسات سابقة كأنها مبنية لكنها لا توجد. السكربت يثبت غيابها فعلياً
عند كل تشغيل. لو ظهر أحدها فجأة، الاختبار `test_claimed_but_absent_remain_absent`
يفرض تحديث القائمة قبل أي ادّعاء جديد.

من القائمة الحالية:

- `auto_client_acquisition/sovereign_registry.py` (ادّعاء «100 محرك»)
- `auto_client_acquisition/master_orchestrator.py` (ادّعاء daemon في `main.py`)
- `auto_client_acquisition/meta_os/autonomous_developer_agent.py` (ادّعاء وكيل تطوير ذاتي)
- `api/routers/m_and_a.py` (ادّعاء رادار استحواذ)
- `api/routers/moyasar_billing.py` (الدفع موجود في `dealix/payments/moyasar.py` لا في راوتر منفصل)
- `frontend/src/app/[locale]/meta-os/page.tsx`
- `frontend/src/app/[locale]/investor-room/page.tsx`

### Evidence Truth

يقرأ مباشرة من `docs/commercial/operations/evidence_events_tracker.csv`،
يستبعد الصفوف الـ `template_*` و الـ placeholder companies، ثم يعدّ الأحداث
الحقيقية حسب النوع. لا أرقام مخترعة.

### بوابات معروفة (يربطها بالمحلّلات القائمة)

- بوابة المرحلة 0–1 → `analyze_phase_0_1_gate()`
- قرار الأسبوع → `analyze_weekly_one_decision()`
- ترميز GTM → `analyze_gtm_codification()` (هدف ~10 debriefs)
- PDPL pass → `analyze_pdpl_compliance_pass()`

### Next 3 Honest Actions

ثلاثة إجراءات بحدّ أقصى، كل واحد مرتبط ببوابة مغلقة فعلياً ويحوي:

- عنوان عربي + إنجليزي
- أمر/خطوة ملموسة
- مرجع وثيقة عند الحاجة

لو كل البوابات مفتوحة، الإجراءات صفر — العمل عندها في War Room اليدوي وليس في
تشغيل المزيد من السكربتات.

## لماذا هذا الملف؟

عبر عدّة جلسات سابقة، ادّعت وكلاء أنها بنت «100 محرك سيادي»، «رادار استحواذ»،
«غرفة مستثمرين بـ ARR حي»، «وكيل تطوير ذاتي يكتب الكود»... ولم تكتب أي ملف
يثبت ذلك. كان النظام يطبع `GREEN` بناءً على أدلة مزروعة (`founder_launch_day`،
`Dealix Founder Commercial Day`) — وهي placeholders يستبعدها الـ tracker الحقيقي
عبر `real_evidence_rows()`.

هذا الفحص يضمن أن جلسة المؤسس الواحدة يومياً تبدأ من أرضية صادقة:

- إذا كان `verdict=PRE_PIPELINE` — لا تشغّل automation. اذهب للسوق يدوياً.
- إذا كان `verdict=GATE_OPEN` — اعتمد War Room وكرّر، لا تبنِ ميزات جديدة.

اختبارات: `pytest tests/test_founder_reality_check.py -v`.
