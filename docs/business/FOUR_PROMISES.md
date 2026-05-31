# Dealix — The Four Promises — الوعود الأربعة

> Section 134 of the positioning brief. Bilingual. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الوعود الأربعة
الوعود الأربعة هي **العقيدة التشغيلية** لـ Dealix. لا تُقايَض ولا تُكسَر بحجّة سرعة أو حجم صفقة.

### 1. Evidence-Required Revenue — إيراد مُثبَت بدليل
**القاعدة**: لا إيراد يُحتسب «مُتحقَّقًا» بدون Evidence Pack.

**ماذا يعني للعميل**:
- تقرير القيمة الشهري يفصل Verified Revenue عن Estimated.
- لا «ROI مُسقَط» يُعرَض كأنّه حقيقة.
- المجلس يرى الفرق بوضوح.

**كيف يُفرض**: حقل `revenue_link.verified` في حزمة الإثبات. غياب الحزمة → الإيراد يبقى تقديريًا.

### 2. Founder Sovereignty — سيادة المؤسس
**القاعدة**: الإجراءات الحساسة تتطلّب موافقة المؤسس/المالك المُسمّى صراحةً.

**ماذا يعني للعميل**:
- لا قرار خارجي يُتَّخذ نيابةً عنك خلسةً.
- اسم المُوافق وطابع الزمن مُسجَّلان.
- استثناء الموافقة يستوجب إصدار سياسة جديد، لا تجاوزًا تقنيًا.

**كيف يُفرض**: خانات `approval_required` في Tool Permission Matrix.

### 3. No External Sends Without Approval — لا إرسال خارجي بدون إذن
**القاعدة**: Dealix لا يرسل خارجيًا نيابةً عن العميل دون إذن صريح لكل رسالة.

**ماذا يعني للعميل**:
- لا spam ينطلق من اسمك.
- لا «حملة» تُنفَّذ بزرّ واحد.
- المسودّة جاهزة، لكن الإرسال يحتاج بشرًا.

**كيف يُفرض**: أدوات `send_external_*` مُعرَّفة كـ `approval_required` بشكل افتراضي، ولا يمكن تجاوزها.

### 4. Auditable Trust Layer — طبقة ثقة قابلة للتدقيق
**القاعدة**: كل نشاط وكيل مُسجَّل في AI Run Ledger مع context_hash.

**ماذا يعني للعميل**:
- يمكنك إعادة بناء أي قرار AI.
- المُدقِّق يستطيع فتح Evidence Pack ورؤية كل خطوة.
- لا «صندوق أسود» يحتجز السبب.

**كيف يُفرض**: AI Run Ledger إلزامي لكل تشغيل؛ context_hash مُحتسَب قبل التنفيذ.

### العلاقة بين الأربعة
- وعد 1 (إيراد) **يستوجب** وعد 4 (تدقيق).
- وعد 2 (سيادة) **يستوجب** وعد 3 (لا إرسال).
- إلغاء أيٍّ منها يلغي العقيدة.

---

## English

### The Four Promises
The Four Promises are the **operational doctrine** of Dealix. They are not traded away for speed or deal size.

### 1. Evidence-Required Revenue
**Rule**: no revenue counts as "verified" without an Evidence Pack.

**What it means for the customer**:
- The monthly Value Report separates Verified Revenue from Estimated.
- No "projected ROI" is presented as fact.
- The board sees the gap clearly.

**How it is enforced**: the `revenue_link.verified` field on the Evidence Pack. Missing pack → the revenue stays estimated.

### 2. Founder Sovereignty
**Rule**: sensitive actions require explicit approval from the founder or the named owner.

**What it means for the customer**:
- No external decision is taken behind your back.
- Approver identity and timestamp are recorded.
- Bypass requires a new policy revision, not a technical override.

**How it is enforced**: `approval_required` cells in the Tool Permission Matrix.

### 3. No External Sends Without Approval
**Rule**: Dealix does not send externally on the customer's behalf without explicit per-message consent.

**What it means for the customer**:
- No spam leaves with your name.
- No "campaign" runs from a single button.
- The draft is ready; sending requires a human.

**How it is enforced**: `send_external_*` tools default to `approval_required` and are not bypassable.

### 4. Auditable Trust Layer
**Rule**: every agent activity is logged in the AI Run Ledger with a context_hash.

**What it means for the customer**:
- You can reconstruct any AI decision.
- An auditor can open the Evidence Pack and see every step.
- No "black box" hides the reason.

**How it is enforced**: AI Run Ledger is mandatory for every run; context_hash is computed before execution.

### Relationships
- Promise 1 (revenue) **requires** Promise 4 (audit).
- Promise 2 (sovereignty) **requires** Promise 3 (no sends).
- Removing any of them removes the doctrine.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
