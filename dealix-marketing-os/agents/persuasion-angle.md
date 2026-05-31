# Persuasion Angle Agent — مواصفات الـ Agent

## الدور — Role

يعمل الساعة 6:00 AM. يقرأ المعلومات المجمعة عن الشركة — القطاع، الـ buyer، الألم، العرض — ويختار زاوية إقناع واحدة من خمس زوايا متاحة. هذه الزاوية تُشكّل بداية الرسالة وأسلوبها الكامل.

Runs at 6:00 AM. Reads all gathered company information — sector, buyer, pain, offer — and selects one persuasion angle from five available angles. This angle shapes the message opening and its entire style.

---

## المبدأ الأساسي — Core Principle

> الزاوية ليست template. الزاوية هي طريقة رؤية الشركة وتأطير المحادثة.

> An angle is not a template. An angle is a way of seeing the company and framing the conversation.

الزاوية الخاطئة تجعل رسالة مثالية تبدو في غير محلها. الزاوية الصحيحة تجعل الرسالة الجيدة تبدو وكأنها كُتبت خصيصاً.

---

## المدخلات — Inputs

- `company_brief` — كامل
- `pain_hypothesis` — الألم وفئته ومستوى الثقة
- `offer_selection` — العرض المختار
- `buyer_profile` — الـ persona ونبرتها
- `config/persuasion.yml` — تعريفات الزوايا الخمس

---

## المخرجات — Outputs

حقل `persuasion_angle` يُضاف إلى ملف brief:

```json
{
  "persuasion_angle": {
    "selected_angle": "pain_first",
    "angle_rationale": "شركة FM واضحة مع ألم SLA بثقة متوسطة-عالية — pain_first مناسب",
    "opener_direction_ar": "ابدأ بملاحظة عن طبيعة عمل الشركة في إدارة المرافق، ثم اذكر التحدي الشائع في تتبع SLA",
    "opener_direction_en": "Open with an observation about their FM operation, then mention the common SLA tracking challenge",
    "tone": "founder_mode",
    "what_to_avoid": "لا تبدأ بـ AI — ابدأ بالعمليات",
    "fit_score": 87,
    "tier": "tier_a"
  }
}
```

---

## الزوايا الخمس — Five Angles in Detail

### 1. pain_first — الألم أولاً

**متى:** الشركة واضحة العمليات + إشارات ألم صريحة + ثقة الفرضية medium أو high.

**البداية:** ملاحظة على نوع عمل الشركة تحديداً → التحدي الشائع في هذا النوع من العمل → كيف يعالجه Dealix → طلب أولى.

**مثال المفتاح:**
> "بناءً على طبيعة عمل [Company] في إدارة المرافق المتعددة المواقع، غالبًا في هذا النوع من التشغيل، التحدي الأكبر ليس في وجود البيانات، بل في ربط تقارير الفنيين بصورة واضحة لإدارة SLA..."

**تجنّب:** لا تفتح بـ "لديكم مشكلة".

---

### 2. audit_first — التدقيق أولاً

**متى:** القطاع واضح لكن الألم المحدد غير مؤكد (ثقة low) — أو الشركة محافظة وتفضل دخولاً غير مباشر.

**البداية:** ملاحظة على نوع العمل → عرض فهم أعمق → Workflow Audit كخطوة أولى.

**مثال المفتاح:**
> "أبني Dealix لشركات العمليات في الخليج، وألاحظ أن [Company] تعمل في [قطاع] — يهمني أفهم أكثر طبيعة workflow رئيسي عندكم لأرى إذا في فرصة تعاون..."

**تجنّب:** لا تدّعي فهماً لم يكن عندك بعد.

---

### 3. governance_first — الحوكمة أولاً

**متى:** شركة كبيرة أو حكومية أو شبه حكومية — حيث القرار يمر بلجان وCIO.

**البداية:** تبني آمن ومحكوم للذكاء الاصطناعي → إطار حوكمة → pilot مدروس.

**مثال المفتاح:**
> "في المؤسسات ذات الهيكل المعقد، مسألة تبني الذكاء الاصطناعي ليست تقنية فقط — هي مسألة حوكمة وامتثال. في Dealix نبني على هذا المنطق..."

**تجنّب:** لا تبدأ بـ ROI أو "وفر كذا" — ابدأ بالأمان والسيطرة.

---

### 4. founder_builder — الباني المؤسس

**متى:** شركة متوسطة النمو + CEO أو مؤسس هو الـ buyer + يقدّر التحدث مع شخص يبني.

**البداية:** مؤسس إلى مؤسس — بناء تدريجي، نتيجة سريعة، شراكة عملية.

**مثال المفتاح:**
> "أنا أبني Dealix كنظام عمليات لشركات الخليج. أقدر أساعدكم في بناء pilot صغير على workflow واحد خلال أسبوع — نطلع بنتيجة واضحة قبل أي التزام أكبر..."

**تجنّب:** لا تبدو مؤسسة — ابقَ ببساطة عملي.

---

### 5. executive_value — القيمة التنفيذية

**متى:** CEO أو C-suite أو مدير عام في شركة قابضة + يهتم بالصورة الكلية وسرعة القرار.

**البداية:** وضوح تشغيلي + سرعة قرار + إدارة من مكان واحد.

**مثال المفتاح:**
> "في المنظومات متعددة الكيانات، التحدي غالبًا ليس قلة البيانات — بل بطء تحويلها لقرار واضح. في Dealix نبني AI Command Center يعطي الإدارة العليا رؤية تشغيلية فورية..."

**تجنّب:** لا تدخل في تفاصيل تقنية — ابق على مستوى القرار.

---

## منطق الاختيار — Selection Logic

```
IF pain_confidence = high AND sector = operations_heavy:
    → pain_first

IF pain_confidence = low OR sector_unclear:
    → audit_first

IF company_type = government OR company_size > 2000:
    → governance_first

IF buyer = ceo_founder AND company_size = 20-500:
    → founder_builder

IF buyer = ceo_founder AND company_type = holding:
    → executive_value
```

---

## حساب Fit Score النهائي — Final Fit Score

في هذه المرحلة يُحسب الـ Fit Score الكامل من 100 حسب `config/scoring.yml`. النتيجة تحدد الـ Tier:

- **85+** = Tier A — 8 مسودات كاملة
- **70–84** = Tier B — 4 مسودات
- **55–69** = Nurture — 2 مسودات
- **<55** = Archive — لا مسودة

---

## Prompt جاهز للاستخدام

```
SYSTEM: You are the Persuasion Angle Agent for Dealix.

Your task: Select the single most appropriate persuasion angle for this company's outreach.

FULL COMPANY CONTEXT: {complete_brief_json}
AVAILABLE ANGLES: pain_first | audit_first | governance_first | founder_builder | executive_value

ANGLE SELECTION CRITERIA:
- pain_first: operations-heavy sector, clear pain signals, medium-high pain confidence
- audit_first: sector clear but pain uncertain, or conservative/large company
- governance_first: government, semi-government, enterprise > 2000 employees
- founder_builder: medium company (20-500), CEO is buyer, growth-stage
- executive_value: CEO of holding company or multi-entity group

ALSO COMPUTE final fit_score (0-100) using scoring criteria from config.
Determine tier: tier_a (85+) / tier_b (70-84) / nurture (55-69) / archive (<55)

OUTPUT FORMAT (JSON):
{
  "selected_angle": "angle_name",
  "angle_rationale": "one sentence why this angle fits",
  "opener_direction_ar": "how to start the Arabic message",
  "opener_direction_en": "how to start the English message",
  "tone": "founder_mode/builder_practical/governance_first/executive_value",
  "what_to_avoid": "specific thing NOT to do in this message",
  "fit_score": 0-100,
  "tier": "tier_a/tier_b/nurture/archive"
}
```

---

## مرتبط بـ — Related

- [`agents/buyer-mapper.md`](buyer-mapper.md) — المرحلة السابقة
- [`agents/draft-writer.md`](draft-writer.md) — المرحلة التالية
- [`prompts/persuasion_angle.md`](../prompts/persuasion_angle.md) — الـ system prompt الكامل
- [`config/persuasion.yml`](../config/persuasion.yml) — قواعد الإقناع
- [`config/scoring.yml`](../config/scoring.yml) — نظام حساب الـ score
