# Command Sprint Delivery OS — مصنع التسليم — The 7-Day Delivery Runbook

## ما هذه الوثيقة — What this is

هذا هو **runbook التسليم** للـ Command Sprint. كل عميل مدفوع يدخل **مصنع تسليم (delivery factory)**: مجلّد عميل واحد + Proof Pack واحدة. هذه الوثيقة تحوّل العرض ([COMMAND_SPRINT_OFFER](../01_go_to_market/COMMAND_SPRINT_OFFER.md)) إلى خطوات يومية قابلة للتنفيذ.

> القاعدة العليا — The supreme rule: لا ادعاء بلا دليل. كل مُخرَج قابل للمراجعة وخلف بوابة موافقة (approval-gated).

**هدف التسليم — Delivery target:** 6–10 ساعات عمل فعلية إجمالًا لكل Sprint كامل (موزّعة على 7 أيام تقويمية).

**هدف التراكم — Template-compounding goal:** كل تسليم يصبح **template**. ما نكتبه يدويًا للعميل رقم 1 يصبح هيكلًا جاهزًا للعميل رقم 2. الهدف: كل Sprint أسرع من الذي قبله، بنفس الجودة أو أعلى. التسليم لا يُكرَّر — يُركَّب فوق نفسه.

## القواعد الصارمة — Hard rules (تُطبَّق على كل يوم)

- لا إرسال تلقائي — No auto-send.
- لا واتساب جماعي — No mass WhatsApp.
- لا دليل مزيّف — No fake proof.
- لا ضمان إيراد — No guaranteed revenue claims.
- لا نشر اسم عميل بلا موافقة — No client name published without approval.
- لا استخدام بيانات العميل في تدريب أي نموذج — No customer data used for model training.
- لا إجراء خارجي يواجه العميل دون موافقة المؤسس — No external customer-facing action without founder approval.
- كل عميل مدفوع له مجلّد تسليم + Proof Pack — Every paid customer needs a delivery folder + proof pack.

## مجلّد العميل — Customer folder reference

كل Sprint يعيش داخل مجلّد واحد: `customers/{company}/`. الهيكل الكامل وملف لكل يوم موصوفان في [CUSTOMER_FOLDER_TEMPLATE](CUSTOMER_FOLDER_TEMPLATE.md). بذرة جاهزة موجودة تحت `customers/_TEMPLATE/`. لا تبدأ Sprint قبل نسخ البذرة وإعادة تسميتها باسم الشركة.

## جدول الـ SLA — The 7-Day SLA Table

كل يوم له: **المدخلات (inputs)** · **الأرتيفاكت المُنتَج (artifact)** · **فحص القبول (acceptance check)** · **بوابة الموافقة (approval gate)**. كل أرتيفاكت يجب أن يحمل حقول [DELIVERY_ACCEPTANCE_CRITERIA](DELIVERY_ACCEPTANCE_CRITERIA.md) (source · analysis · assumption · confidence · recommendation · approval_required · next_action · owner · due_date).

### Day 1 — Intake + Company Intelligence

- **Inputs:** ردود نموذج الاستلام، أي بيانات يشاركها العميل (مصادر عامة فقط)، نطاق الشركة، السوق.
- **Artifact:** `00_intake.md` + `01_company_intelligence.md` — من هي الشركة، السوق، المنافسون، نقاط الضعف التشغيلية المُوثَّقة بمصدر.
- **Acceptance check:** كل سطر في Company Intelligence مربوط بمصدر (source). لا توجد أرقام بلا مرجع.
- **Approval gate:** المؤسس يؤكّد أن النطاق يطابق ما دُفع مقابله. لا جمع بيانات خلف تسجيل دخول ولا scraping يخالف الشروط.

### Day 2 — Diagnostic Summary

- **Inputs:** `01_company_intelligence.md`، ملاحظات اليوم 1.
- **Artifact:** `02_diagnostic_summary.md` — التشخيص التشغيلي: أين الفوضى، ما الذي يكلّف، ما الذي يُعطّل القرار.
- **Acceptance check:** كل تشخيص مفصول إلى (ملاحظة + مصدر + assumption + confidence). لا تشخيص بلا confidence مُصرَّح.
- **Approval gate:** لا (داخلي). يُراجَع ضمن مراجعة اليوم 6.

### Day 3 — Revenue Map

- **Inputs:** `02_diagnostic_summary.md`، خريطة العملية الحالية للعميل.
- **Artifact:** `04_revenue_map.md` — أين يتسرّب الإيراد، أين الفرص المُثبتة بأدلة، ترتيب الأولويات بالأثر.
- **Acceptance check:** كل فرصة موصوفة كـ **فرصة مُثبتة بأدلة (evidenced opportunity)**، لا كرقم مبيعات مضمون. كل تقدير يحمل كلمة "تقديري".
- **Approval gate:** لا (داخلي).

### Day 4 — Proof Register

- **Inputs:** كل الأرتيفاكتس حتى الآن.
- **Artifact:** `05_proof_register.md` — كل ادعاء قُدّم للعميل مربوط بمصدر/دليل ومستوى Proof (L1–L5، انظر [PROOF_PACK_TEMPLATE](PROOF_PACK_TEMPLATE.md)).
- **Acceptance check:** صفر ادعاءات بلا مصدر. كل بند له Proof Level مُصرَّح.
- **Approval gate:** لا (داخلي). يُغذّي بوابة النشر لاحقًا.

### Day 5 — Next Action Board

- **Inputs:** `04_revenue_map.md`، `05_proof_register.md`.
- **Artifact:** `07_next_action_board.md` — 3 إجراءات تالية مرتّبة بالأثر، لكل إجراء مالك ومُهلة ومتطلّب موافقة.
- **Acceptance check:** كل إجراء له owner + due_date. أي إجراء خارجي يواجه العميل عليه `approval_required: yes`.
- **Approval gate:** المؤسس يعتمد الـ board قبل أن يُذكَر للعميل.

### Day 6 — Executive Command Brief

- **Inputs:** كل ما سبق.
- **Artifact:** `08_executive_command_brief.md` — صفحة قرار واحدة: الوضع، الخيارات، التوصية. يقرأها صاحب القرار في 20 دقيقة.
- **Acceptance check:** صفحة واحدة فعليًا. توصية واحدة واضحة. كل ادعاء فيها يحيل إلى Proof Register.
- **Approval gate:** **مراجعة المؤسس الكاملة (founder review)** + تعبئة `06_approval_register.md`. لا يُرسَل شيء للعميل قبل هذه البوابة.

### Day 7 — Proof Pack + Upsell Recommendation

- **Inputs:** Command Pack الكاملة المعتمدة.
- **Artifact:** `10_proof_pack.md` (انظر [PROOF_PACK_TEMPLATE](PROOF_PACK_TEMPLATE.md)) + `11_upsell_recommendation.md` — توصية واحدة موثّقة لما بعد الـ Sprint.
- **Acceptance check:** Proof Pack تحوي الأقسام السبعة كاملة. Upsell مربوطة بفجوة موثّقة في Revenue Map، لا بإلحاح بيعي.
- **Approval gate:** المؤسس يعتمد التسليم النهائي. بوابة النشر (publish-permission) منفصلة: لا اسم عميل يُنشَر بلا موافقة مكتوبة.

## الحزمة النهائية — The Command Pack final bundle

الـ Command Pack المُسلَّمة للعميل = Company Intelligence Brief + Diagnostic Summary + Revenue Map + Proof Register + Executive Command Brief + Approval Register + Next Action Board + **Upsell Recommendation**، مغلّفة بـ **Proof Pack** واحدة كغلاف للأدلة.

## سجلّ التسليم — Delivery log

كل يوم يُسجَّل في `09_delivery_log.md`: الوقت المصروف، الأرتيفاكت، الانحرافات عن الـ SLA. تأخير التسليم يُسجَّل ويُعوَّض — لا تأخير صامت. مجموع الوقت المصروف يجب أن يبقى ضمن 6–10 ساعات؛ تجاوزه إشارة إلى template ناقص.

## روابط مرجعية — Cross-links

- [CUSTOMER_FOLDER_TEMPLATE.md](CUSTOMER_FOLDER_TEMPLATE.md)
- [PROOF_PACK_TEMPLATE.md](PROOF_PACK_TEMPLATE.md)
- [DELIVERY_ACCEPTANCE_CRITERIA.md](DELIVERY_ACCEPTANCE_CRITERIA.md)
- [../01_go_to_market/COMMAND_SPRINT_OFFER.md](../01_go_to_market/COMMAND_SPRINT_OFFER.md)
- [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)
- [../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
