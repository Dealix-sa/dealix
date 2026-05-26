# استراتيجية Dealix / Hermes — الخطة الرئيسية
# Dealix Hermes Master Strategy — Arabic

**التصنيف:** وثيقة استراتيجية سرية — مؤسس  
**المسؤول:** سامي  
**التاريخ:** 2026-05-26  
**المراجعة:** شهرية

---

## الجملة الحاكمة

> **Dealix لا يجب أن تكون شركة تنفّذ مهام. Dealix يجب أن تكون آلة تراكم استراتيجية: كل رسالة، كل عميل، كل تجربة، كل فشل، كل شريك، وكل نتيجة تتحول إلى دخل أو أصل أو بيانات أو ثقة أو قناة توزيع.**

وهذا هو دور Hermes:

> **Hermes يرى الإشارات، يرتب الأولويات، يشغل الوكلاء، يحمي الثقة، يُثبت القيمة، ويجعل سامي يقرر كـ CEO لا كمنفذ يومي.**

---

## 0. الرؤية النهائية

```
Dealix = Revenue OS + AI Agent Control Plane + Proof Engine + Saudi-native Trust Layer
```

بصيغة تنفيذية للعملاء:

> **نظام يحوّل الذكاء الاصطناعي إلى دخل قابل للقياس، مع حوكمة تقلل المخاطر.**

لا نبيع "ذكاء اصطناعي". لا نبيع "أتمتة". لا نبيع "CRM".  
نبيع شيئًا أعلى قيمة:

**نظام تشغيل متكامل يربط وكلاء AI بالقيمة التجارية الحقيقية، مع إثبات نتائج، سجل تدقيق، وموافقة بشرية للقرارات الحساسة.**

---

## 1. لماذا الفرصة قوية الآن؟

### 1.1 قرار هيئة النقل (TGA) — يناير 2026
شركات توصيل الطرود مطالبة برفض أي شحنة لا تحتوي على عنوان وطني صالح ابتداءً من يناير 2026. هذا يفتح فرصة **Address Verification + Delivery Intelligence** لـ Dealix.

**الفرصة المباشرة:**
- منتج "Dealix National Address Intelligence" لشركات التجارة الإلكترونية
- تحقق من العنوان الوطني قبل الشحن
- تقليل RTO وتحسين تجربة التوصيل

### 1.2 SDAIA والحوكمة الوطنية للذكاء الاصطناعي
SDAIA تؤكد دورها كمرجع وطني لقطاع البيانات والذكاء الاصطناعي. مبادئ أخلاقيات الذكاء الاصطناعي السعودية تركز على المواءمة مع القيم والحقوق والمتطلبات المحلية.

**الفرصة المباشرة:**
- الحوكمة ليست تفصيلًا جانبيًا — هي **مدخل بيع للشركات الكبيرة والجهات الحساسة**
- Dealix يمكنه أن يكون "SDAIA-aligned Governance Layer" لوكلاء AI

### 1.3 مخاطر MCP وسطح الهجوم
الأبحاث الحديثة (arXiv:2603.22489) تشير إلى أن MCP يفتح سطح مخاطر مهم:
- Tool Poisoning
- Prompt Injection عبر تعريفات الأدوات والميتاداتا
- تتبع مسار قرار النموذج

**الفرصة المباشرة:**
- Dealix MCP Gateway كطبقة حماية وحوكمة
- AI Trust Diagnostic كخدمة تشخيص للشركات المعرضة للخطر

### 1.4 السوق يتحرك من "AI Tools" إلى "AI Operations"
الشركات لا تحتاج أدوات AI فقط. تحتاج:
1. من يحق له فعل ماذا؟
2. أي أداة استخدم؟
3. لماذا اتخذ القرار؟
4. هل خرجت بيانات حساسة؟
5. هل توجد موافقة بشرية؟
6. هل النتيجة جلبت دخلًا؟
7. هل نستطيع إثبات ذلك؟

**هذه هي منطقة الخندق الاستراتيجي لـ Dealix.**

---

## 2. Hermes — 6 محركات تشغيلية

```
┌─────────────────────────────────────────────────────────────┐
│                    HERMES OPERATING SYSTEM                  │
├─────────────────────────────────────────────────────────────┤
│  Signal Engine  │  يلتقط فرص السوق والعملاء والمخاطر        │
│  Revenue Engine │  يحوّل الإشارات إلى عروض وصفقات           │
│  Governance     │  يدير الصلاحيات والموافقات والتدقيق        │
│  Proof Engine   │  يحوّل كل نتيجة إلى Evidence Pack         │
│  Partner Engine │  يدير الشركاء والوكالات والإحالات          │
│  Founder Engine │  يعطي سامي موجز قرارات يومي وأسبوعي        │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Hermes Signal Engine
**الوظيفة:** يلتقط الإشارات من السوق، العملاء، الشركاء، والمخاطر.  
**المدخلات:** أخبار السوق، نشاط العملاء، ردود الفعل، إشارات المنافسين  
**المخرجات:** قائمة إشارات مصنّفة بالأولوية (HIGH/MEDIUM/LOW)  
**الناتج التجاري:** Pipeline مستمر

**API:** `POST /api/v1/hermes-integration/signals`

### 2.2 Hermes Revenue Engine
**الوظيفة:** يحوّل الإشارات إلى عروض ومتابعات وصفقات.  
**المدخلات:** إشارة مصنّفة، ICP match، pain hypothesis  
**المخرجات:** رسالة تواصل، عرض خدمة، جدول متابعة  
**الناتج التجاري:** Cash Flow

**CLI:** `py -3 dealix.py recommend --problem "..."`

### 2.3 Hermes Governance Engine
**الوظيفة:** يدير الصلاحيات، الموافقات، وسجلات التدقيق.  
**المدخلات:** طلب تنفيذ من وكيل AI  
**المخرجات:** APPROVED / BLOCKED / PENDING + سجل تدقيق  
**الناتج التجاري:** Trust + Compliance

**API:** `POST /api/v1/hermes-integration/executions/approve`

### 2.4 Hermes Proof Engine
**الوظيفة:** يحوّل كل نتيجة إلى Evidence Pack.  
**المدخلات:** نتائج التنفيذ، المؤشرات، الأدلة  
**المخرجات:** Proof Pack كامل بـ 9 أقسام  
**الناتج التجاري:** Case Studies + Upsell + Partner Trust

**CLI:** `py -3 dealix.py proof-pack --client "..." --service "..."`

### 2.5 Hermes Partner Engine
**الوظيفة:** يدير الشركاء والوكالات والإحالات.  
**المدخلات:** قائمة وكالات مستهدفة، نسب عمولة  
**المخرجات:** Partner pitch، عقد إحالة، تقرير أداء  
**الناتج التجاري:** Distribution Channel

**وثيقة:** `docs/partners/AGENCY_WHITE_LABEL_KIT.md`

### 2.6 Hermes Founder Engine
**الوظيفة:** يعطي سامي موجز قرارات يومي وأسبوعي.  
**المدخلات:** حالة Pipeline، المخاطر، الفرص، الموافقات المعلقة  
**المخرجات:** Daily Command Brief (9 items)  
**الناتج التجاري:** Founder Leverage

**CLI:** `py -3 dealix.py command-brief`

---

## 3. Dealix Agentic Revenue Control Plane

### 3.1 الاسم الرسمي
**Dealix Agentic Revenue Control Plane**

### 3.2 ماذا يفعل؟
يربط كل المكوّنات في منظومة متكاملة:

```
AI Agents
    ↓
CRM + Outreach
    ↓
Proposals + Follow-ups
    ↓
Approval Gates + Audit Logs
    ↓
Revenue Attribution
    ↓
Evidence Packs
    ↓
Partner Workflows
```

### 3.3 السؤال الذي يجيب عليه Dealix
| السؤال | Dealix يجيب |
|--------|-------------|
| من يحق له فعل ماذا؟ | Permission Matrix |
| أي أداة استخدم الوكيل؟ | Tool Registry |
| لماذا اتخذ القرار؟ | Audit Log |
| هل خرجت بيانات حساسة؟ | PII Check |
| هل توجد موافقة بشرية؟ | Approval Workflow |
| هل النتيجة جلبت دخلًا؟ | Revenue Attribution |
| هل نستطيع إثبات ذلك؟ | Proof Pack |

---

## 4. العروض الأساسية

### 4.1 Fast Cash Offers

#### Revenue Hunter Pilot
- **لمن:** وكالات، استشاريون، شركات B2B، عقار، تدريب
- **النتيجة:** فرص مؤهلة + رسائل + متابعة + تقرير
- **المدة:** 7–14 يوم
- **السعر:** 3,000–12,000 ريال
- **CLI:** `py -3 dealix.py proposal --client "..." --service revenue-hunter`

#### AI Trust Diagnostic
- **لمن:** شركات تستخدم ChatGPT أو Agents داخليًا
- **النتيجة:** خريطة مخاطر + سياسة + Agent Permission Matrix
- **السعر:** 5,000–20,000 ريال
- **CLI:** `py -3 dealix.py proposal --client "..." --service ai-diagnostic`

#### Proposal Factory Pack
- **لمن:** شركات خدمات B2B
- **النتيجة:** قوالب عروض + رسائل اعتراضات + follow-up + proof pack
- **السعر:** 2,500–10,000 ريال

### 4.2 Recurring Offers

#### Monthly Revenue Command
- **الاشتراك:** 4,000–25,000 ريال/شهر
- **يشمل:** Leads + Follow-ups + Proposals + Outcome tracking + Weekly CEO report

#### AI Governance Retainer
- **الاشتراك:** 8,000–50,000 ريال/شهر
- **يشمل:** Agent registry + Tool permissions + Audit logs + Policy updates + Risk review

### 4.3 Enterprise Offers

#### Enterprise Agent Control Plane
- **لمن:** الشركات الكبيرة
- **يشمل:** MCP Gateway + Role-based access + Human approval + Tool registry + Evidence trail
- **السعر:** مشروع مخصص يبدأ من 75,000 ريال + retainer شهري

---

## 5. Strategic Priority Score

```
درجة الأولوية الاستراتيجية =
  × 0.20  إمكانية الإيراد
  × 0.15  سرعة الوصول للنقد
  × 0.15  قابلية التكرار
  × 0.15  حصن البيانات
  × 0.10  رافعة الشراكة
  × 0.10  بناء الثقة
  × 0.10  رافعة المؤسس
  − 0.10  المخاطرة
  − 0.05  عبء التسليم
  ─────────────────────
  النتيجة: 0–100
```

| النتيجة | القرار |
|---------|--------|
| 80–100 | نفّذ أو وسّع — اعتمد الفرصة فورًا |
| 60–79 | اختبر بسرعة — pilot صغير أولًا |
| 40–59 | راقب — أعد التقييم الشهر القادم |
| أقل من 40 | أرشف أو اقتل — وجّه الطاقة لفرصة أخرى |

**CLI:** `py -3 dealix.py score --opportunity "..." --revenue 12000 --speed 8 --repeat 9`

---

## 6. حوكمة MCP Gateway

### 6.1 مسار التنفيذ المحكوم

```
Agent
  → Dealix MCP Gateway
  → Policy Engine
  → Permission Check
  → Risk Scoring
  → Human Approval (if needed)
  → Tool Execution
  → Audit Log
  → Evidence Pack
```

### 6.2 مستويات المخاطر

| المستوى | مثال | القرار |
|---------|------|--------|
| L0 | قراءة ملف عام | مسموح تلقائيًا |
| L1 | تلخيص بيانات غير حساسة | مسموح مع تسجيل |
| L2 | إرسال رسالة عميل | يحتاج مراجعة |
| L3 | تعديل CRM أو عرض سعر | يحتاج موافقة |
| L4 | دفع مالي أو حذف بيانات | ممنوع إلا بموافقة صريحة |
| L5 | بيانات حساسة/قانونية/مالية عالية | حظر أو مراجعة تنفيذية |

### 6.3 القاعدة الذهبية
> **Autonomy is earned, not granted.**  
> أي وكيل لا يحصل على صلاحيات كاملة من البداية. يحصل على صلاحيات تدريجية بناءً على السجل، الدقة، المخاطر، ونوع المهمة.

---

## 7. Proof Engine — بيع الإثبات لا الوعود

### 7.1 معيار Proof Pack — 9 أقسام

```
[1] المشكلة المُثبتة
[2] الفرضية التي اختبرناها
[3] الخطوات المُنفذة
[4] الأصول المُستخدمة
[5] النتائج الموثقة (مع جدول مؤشرات)
[6] الدخل أو المؤشر التجاري
[7] الأدلة (screenshots، سجلات، تواريخ)
[8] المخاطر والقيود
[9] التوصية التالية
```

### 7.2 لماذا Proof Engine تميّزنا؟
السوق مليء بمن يقول "نستخدم AI".  
Dealix تقول:

> **نُثبت ماذا فعل AI، من وافق عليه، وماذا أنتج تجاريًا.**

---

## 8. خطة 30 يومًا التنفيذية

### الأسبوع 1 — إصلاح وتشغيل
**الهدف:** إغلاق أخطاء التنفيذ وتشغيل النظام كـ CLI داخلي.

**المهام:**
- [ ] التأكد أن كل الأوامر تعمل من ملف Python لا من PowerShell مباشر
- [ ] إنشاء ledgers (opportunities، services، partners، agents)
- [ ] تشغيل command brief يومي
- [ ] إنشاء proof pack generator
- [ ] إنشاء proposal generator
- [ ] إنشاء governance check

**معيار النجاح:**
```
DEALIX_CORE_CLI=PASS
HERMES_INTERNAL_OS=READY
```

### الأسبوع 2 — دخل سريع
**الهدف:** بيع أول 3 عروض.

**العروض:**
- Revenue Hunter Pilot (7,500 SAR)
- AI Trust Diagnostic (15,000 SAR)
- Proposal Factory Pack (5,000 SAR)

**القطاعات الأولى:**
- وكالات تسويق رقمي
- شركات استشارات
- مكاتب محاماة وحسابات
- شركات تدريب
- شركات عقار B2B

**معيار النجاح:**
```
3 paid pilots أو 10 مكالمات مؤهلة
```

### الأسبوع 3 — Proof + Trust
**الهدف:** تحويل كل تسليم إلى دليل.

**المهام:**
- [ ] إنشاء 3 Proof Packs
- [ ] إنشاء 2 Case Studies مجهولة الهوية
- [ ] نشر صفحة AI Trust
- [ ] نشر صفحة Revenue Hunter
- [ ] تجهيز Partner Deck

**معيار النجاح:**
```
PROOF_ENGINE_ACTIVE
TRUST_SIGNALS_PUBLIC
```

### الأسبوع 4 — Partner Scale
**الهدف:** تحويل الوكالات إلى قناة توزيع.

**المهام:**
- [ ] Agency White-label Kit
- [ ] Revenue share agreement
- [ ] Partner onboarding checklist
- [ ] 20 وكالة مستهدفة
- [ ] 5 مكالمات شراكة

**معيار النجاح:**
```
PARTNER_PIPELINE_ACTIVE
FIRST_REVENUE_CHANNEL_READY
```

---

## 9. خطة 90 يومًا

| المرحلة | الفترة | الهدف |
|---------|--------|-------|
| Phase 1 | اليوم 1–30 | خدمات مقولبة + CLI داخلي + أول دخل |
| Phase 2 | اليوم 31–60 | بوابة عميل بسيطة (leads، approvals، proof pack، weekly report) |
| Phase 3 | اليوم 61–90 | تحويل النظام إلى SaaS أولي (accounts، subscriptions، agent registry) |

---

## 10. الأوامر الجاهزة

```powershell
# الموجز اليومي
py -3 dealix.py command-brief

# توصية لمشكلة محددة
py -3 dealix.py recommend --problem "نحتاج فرص B2B مؤهلة"

# حزمة عميل كاملة
py -3 dealix.py client-pack --client "مجموعة الرياض" --sector "استشارات" --problem "ضعف المبيعات"

# توليد عرض
py -3 dealix.py proposal --client "مجموعة الرياض" --service revenue-hunter

# إنشاء proof pack
py -3 dealix.py proof-pack --client "مجموعة الرياض" --service revenue-hunter

# فحص الحوكمة
py -3 dealix.py governance-check --text "نضمن زيادة مبيعاتك 300%"

# تشغيل مهمة AI محكومة
py -3 dealix.py ai-run --project "Dealix" --task "send outreach" --risk "medium"

# تقييم فرصة
py -3 dealix.py score --opportunity "Revenue Hunter Pilot" --revenue 12000 --speed 8 --repeat 9

# مراجعة أسبوعية
py -3 dealix.py week-review

# مراجعة شهرية
py -3 dealix.py month-review

# التحقق من تكامل Hermes
py -3 scripts/verify_hermes_integration.py

# الموجز اليومي المستقل
py -3 scripts/hermes_command_brief.py

# تقييم الفرصة المستقل
py -3 scripts/hermes_score.py --opportunity "Revenue Hunter" --revenue 12000 --speed 8

# فحص الحوكمة المستقل
py -3 scripts/hermes_governance_check.py --text "نضمن نتائج مضمونة"

# توليد proof pack مستقل
py -3 scripts/hermes_proof_pack.py --client "مجموعة الرياض" --service "revenue-hunter"
```

---

## 11. ما الذي لا تفعله الآن

❌ لا تبنِ كل SaaS قبل البيع  
❌ لا تفتح 10 مسارات معًا  
❌ لا تطارد Enterprise قبل إثبات fast cash  
❌ لا تستخدم: "نضمن زيادة المبيعات"  
✅ استخدم: "نساعدك تبني نظامًا لتوليد الفرص وقياس ما يتحول إلى دخل"  
❌ لا تجعل الوكلاء ينفذون قرارات مالية/خارجية بدون موافقة  
❌ لا تلصق كود Python متعدد الأسطر داخل PowerShell مباشرة  

---

## 12. المراجع الاستراتيجية

| المصدر | الأهمية |
|--------|---------|
| [TGA — National Address Mandate 2026](https://www.tga.gov.sa) | فرصة Address Intelligence |
| [SDAIA — AI Ethics](https://sdaia.gov.sa) | الحوكمة كمدخل بيع |
| [arXiv:2603.22489 — MCP Threats](https://arxiv.org/abs/2603.22489) | MCP Gateway justification |
| [BorderGuru — Cross-border](https://borderguru.io) | Logistics Intelligence model |

---

*وثيقة محدّثة تلقائيًا — Dealix Hermes OS*  
*`py -3 dealix.py status` للتحقق من الحالة الحالية*
