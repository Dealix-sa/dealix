# اعتماد أنماط Meridian Company OS داخل Dealix

## القرار التنفيذي

يُستخدم مشروع `codejunkie99/meridian-company-os` كمصدر **أنماط منتج وتجربة تشغيل فقط**، وليس كـ runtime جديد أو backend بديل أو تطبيق يُنسخ بالكامل داخل Dealix.

السبب:

- Dealix يملك أصلًا Company OS وOpportunity Graph وApproval/Proof ومسار SaaS متعدد المستأجرين.
- إدخال Meridian كاملًا سيخلق واجهة وحالة وتشغيلًا موازيًا بدل تقوية المصدر القانوني الموجود.
- Meridian نفسه local-first ويعتمد حاليًا على محاكاة وحالة محلية، بينما persistence والاختبارات وCI والـadapters الحقيقية ضمن خارطة طريقه.

القرار المعتمد:

```text
Pattern-only + bounded UI pilot
```

لا dependency جديدة، لا استيراد runtime، لا local Kimi bridge في الإنتاج، ولا تغيير لمسار الإرسال أو الدفع أو النشر.

---

## المصدر والترخيص

- المصدر: `https://github.com/codejunkie99/meridian-company-os`
- الترخيص: MIT
- يجب الحفاظ على إشعار حقوق النشر والترخيص عند نسخ أي جزء جوهري من الشفرة، إن حصل ذلك مستقبلًا.

التنفيذ الحالي لا ينسخ حزمة Meridian أو ملفاتها؛ بل يبني واجهة Dealix-native مستلهمة من مبادئ التشغيل المعلنة في المشروع.

---

## ما الذي يستحق الاعتماد؟

### 1. شاشة قيادة تجيب ثلاث أسئلة

كل شاشة تشغيل يجب أن تجيب بالترتيب:

1. ماذا يحدث الآن؟
2. هل يحتاج تدخلي؟
3. ما الإجراء التالي؟

اعتمدنا هذا المبدأ في مسار:

```text
/{tenant}/command
```

### 2. Operator cockpit بدل dashboard تجميلي

الواجهة لا تعرض بطاقات أرقام فقط، بل تجمع:

- حالة المشغل.
- القرارات والتنبيهات المعلقة.
- الحركات المتاحة.
- نبض النشاط.
- مؤشرات العميل الفعلية.
- بوابة رجوع إلى اللوحة المختصرة.

### 3. Governance before autonomy

أي حركة خارجية تبقى خلف Approval Center. الواجهة الجديدة لا ترسل ولا تدفع ولا تنشر ولا تعدل production.

### 4. Ledger-backed truth

لا نعرض spend أو revenue أو token burn أو success rate ما لم تصل من مصدر Dealix قانوني موثق. لا تُستخدم أرقام Meridian التجريبية أو المحاكاة كحقائق عميل.

### 5. Goals → Work → Owner → Evidence

يُعتمد لاحقًا كخريطة UX فوق كيانات Dealix الحالية، لا كـschema موازٍ:

```text
Company Brain
→ Strategy / Goal
→ Opportunity / Work item
→ Owner / Agent
→ Approval
→ Outcome event
→ Proof event
```

### 6. Agent and skill registry

يُستخدم كنمط عرض وإدارة فقط. المصدر القانوني يبقى سجلات Dealix الحالية وسياسات MCP/skills، مع عدم تثبيت skill أو منح صلاحية تلقائيًا.

### 7. Immutable activity surface

النشاط يجب أن يكون evidence-backed، قابلًا للتصدير، ولا يحتوي prompts أو secrets أو بيانات حساسة غير لازمة.

### 8. Multi-company portfolio

يُترجم إلى tenant/workspace switcher داخل SaaS Dealix، وليس إلى store محلي جديد.

---

## ما الذي لا نعتمده؟

### لا نستخدم simulation كحقيقة إنتاج

المحاكاة مفيدة للديمو والتصميم فقط. لا يجوز أن تنتج:

- إيرادًا مزعومًا.
- نشاط عميل مزعومًا.
- مهامًا مكتملة وهمية.
- معدل نجاح أو تكلفة غير مستندة إلى ledger حقيقي.

### لا ننشر local Kimi bridge

أي bridge يستطيع تشغيل CLI محلي يبقى على جهاز موثوق وبموافقة المستخدم فقط. لا يدخل Railway أو Vercel أو multi-tenant SaaS.

### لا ننشئ state store موازٍ

لا React store ثانٍ للشركات والوكلاء والموافقات داخل Dealix. واجهة command تقرأ من:

```text
/api/v1/customer/dashboard/
```

وتستخدم session/runtime API القانوني الموجود.

### لا ننشئ runtime أو orchestrator ثانيًا

التشغيل اليومي القانوني يبقى مسار Dealix Company OS وStrategy/Approval/Proof الموجودين. Kimi أو Codex أو Claude تكون providers/adapters، وليست مصدر السلطة أو الحالة.

### لا نخزن بيانات العملاء في browser localStorage

يسمح فقط ببيانات الجلسة المحدودة التي يعرّفها runtime helper الحالي. Company Brain والفرص والقرارات والأدلة تبقى في backend المصرح به.

---

## خريطة Meridian → Dealix

| Meridian pattern | Dealix canonical surface | قرار الاعتماد |
| --- | --- | --- |
| Command | `/{tenant}/command` + customer dashboard API | نُفذ كواجهة محدودة |
| Work | Opportunity/Action Queue | إعادة استخدام، لا schema جديد |
| Goals | Strategy/Company Brain goals | pattern لاحقًا |
| Org Chart | Agent/owner registry | pattern لاحقًا |
| Agents | governed agents + runtime metadata | pattern لاحقًا |
| Skills | governed skill/MCP registry | إعادة استخدام الموجود |
| Approvals | Approval Queue/Center | المصدر القانوني Dealix |
| Finance | payment/proof/ledger evidence | لا أرقام محاكاة |
| Activity | Proof/Audit events | المصدر القانوني Dealix |
| Reports | Executive Daily/Weekly/Proof Pack | إعادة استخدام الموجود |
| Portfolio | tenant/workspace selection | ضمن SaaS foundation |
| Kimi Space | provider-neutral command/chat adapter | لا Kimi-only core |

---

## التنفيذ الحالي

### ملفات المنتج

```text
apps/web/app/[tenant]/command/page.tsx
apps/web/app/[tenant]/dashboard/page.tsx
```

### عقد الأمان والتحقق

```text
tests/test_saas_web_journey_contract.py
```

العقد يتحقق من أن:

- المسار يقرأ customer dashboard API المصادق عليه.
- لا يستخدم `x-tenant-id` من المتصفح.
- لا يستدعي local-runtime.
- لا يولد قيمًا عشوائية أو simulation interval.
- يعرض بوضوح أنه لا ينفذ إرسالًا أو دفعًا أو تغيير إنتاج.
- رابط غرفة القيادة ظاهر من dashboard.

---

## بوابة الدمج

قبل دمج هذا الـpilot يجب نجاح:

```bash
python -m pytest -q --no-cov tests/test_saas_web_journey_contract.py

cd apps/web
npm ci
NEXT_PUBLIC_DEALIX_API_BASE=https://api.example.invalid npm run typecheck
NEXT_PUBLIC_DEALIX_API_BASE=https://api.example.invalid npm run build
```

ويجب أيضًا:

- عدم وجود review threads غير محلولة.
- نجاح SaaS Foundation CI.
- نجاح Repository Hardening وSecurity وCodeQL وNo-Crash.
- بقاء التغيير دون dependency أو backend migration.
- عدم تنفيذ deploy أو production mutation من هذا الـPR.

---

## مراحل الاستفادة التالية

### المرحلة 1 — Command pilot

تمثلها الواجهة الحالية، وتستخدم بيانات العميل الفعلية فقط.

### المرحلة 2 — Goal/Work linkage

إظهار لماذا كل Opportunity أو Action مرتبط بهدف شركة محدد، مع المالك والدليل.

### المرحلة 3 — Approval inbox

عرض الموافقات المعلقة من المصدر القانوني، مع policy checks وbefore/after diff، دون تنفيذ خارجي تلقائي.

### المرحلة 4 — Cost and outcome ledger

ربط تكلفة النموذج/الأداة والنتيجة التجارية الحقيقية بالـProof Ledger، لا بالمحاكاة.

### المرحلة 5 — Provider-neutral command surface

واجهة أوامر فوق adapters Dealix الحالية؛ Kimi أحد الخيارات، وليس الاعتماد الوحيد.

---

## شروط التوقف والرجوع

أوقف التوسع أو ارجع التغيير إذا:

- ظهر store أو schema موازٍ.
- احتاجت الواجهة إلى fake data حتى تبدو مكتملة.
- اتسع API browser trust boundary دون مراجعة.
- أصبح local CLI bridge جزءًا من production.
- تسببت الواجهة في تضارب مع المصدر القانوني للـApproval أو Proof أو Revenue.
- لم تضف قيمة تشغيلية قابلة للقياس مقارنة باللوحة المختصرة.

الرجوع آمن بحذف route `/command` وإزالة رابطها واختبارها؛ لا توجد migration أو dependency أو تغيير backend.
