# خطة تنفيذ Dealix — أقوى شركة تبيع أنظمة تشغيل للشركات

**تاريخ الإنشاء:** 2026-06-10  
**الحالة:** ACTIVE  
**الهدف:** تحويل Dealix من منصة جاهزة تقنيًا إلى شركة تشغيلية تبيع وتسلّم يوميًا

---

## الوضع الحالي (Baseline)

### ✅ ما هو جاهز (95% تقنيًا)
- **17 عرض تجاري** معرّف في `service_catalog/registry.py`
- **APIs كاملة**: 120+ router، FastAPI، Postgres، Redis
- **Frontend**: Next.js، `/ar/ops/founder`،`/ar/business-now`
- **الأتمتة المحكومة**: `run_founder_commercial_day.sh` (أمر صباحي واحد)
- **الوثائق الشاملة**: 
  - سلم البيع: Diagnostic (4,999) → Sprint (499) → Data Pack (1,500) → Growth (2,999)
  - 4 Motions: A (Agency), B (Direct), C (Consultant), D (Executive)
  - SOAEN Standard: Source → Owner → Approval → Evidence → Next Action
- **الحوكمة**: لا WhatsApp بارد، لا LinkedIn آلي، كل شيء بموافقة

### ❌ الفجوة الوحيدة (5% تنفيذ)
- **لا عميل مدفوع** (First Paid Diagnostic)
- **لا Proof Packs مسلّمة** (لا أدلة حقيقية)
- **238 هدف ABM بلا تاريخ متابعة** في War Room
- **Moyasar live** غير مفعّل (فواتير يدوية)

---

## الخطة التنفيذية (3 مراحل × 90 يوم)

### 🎯 المرحلة 0: الإطلاق الفوري (يوم 0-7)

**الهدف:** أول محادثة مبيعات حقيقية + 10 لمسات يومية

#### الإجراءات اليومية (5 دقائق صباحًا)

```bash
# 1. الأمر الصباحي الموحّد
bash scripts/run_founder_commercial_day.sh

# 2. افتح War Room
# واجهة: /ar/ops/founder
# أضف تاريخ متابعة لـ 10 أهداف high priority

# 3. سجّل حدث أدلة واحد على الأقل (مساءً)
python3 scripts/founder_evening_evidence.py --append \
  --event-type message_sent_manual \
  --company "Agency Name"
```

#### Control Tower (3 أسئلة يومية)

1. **ما أفضل شريحة؟**  
   → **Motion A: الوكالات** (وكالات تسويق/إعلان/محتوى)

2. **ما أفضل رسالة؟**  
   → "أنتم تجيبون الاهتمام. Dealix يثبت ماذا حدث **بعد** الاهتمام."

3. **ما أفضل عرض؟**  
   → **Agency Proof Pack (990 SAR)** أو **Diagnostic (4,999)**

#### War Room (10 targets يوميًا)

| # | Target | Segment | Pain Hypothesis | Offer | Next Action | Status |
|---|--------|---------|-----------------|-------|-------------|--------|
| 1 | وكالة X | Agency | leads تضيع بعد الحملة | Agency Proof Pack | مسودة LinkedIn | not_contacted |
| 2 | وكالة Y | Agency | العميل يسأل عن النتائج | Diagnostic | بريد دافئ | message_drafted |
| ... | ... | ... | ... | ... | ... | ... |

#### Evidence Events (حدث واحد على الأقل يوميًا)

- `message_sent_manual` — إرسال/مسودة بموافقة
- `reply_received` — رد مسجّل
- `demo_booked` — ديمو محجوز
- `scope_requested` — طلب نطاق
- `invoice_sent` — فاتورة
- `payment_received` — دفع ✅
- `proof_pack_delivered` — Proof مسلّم ✅

#### المخرجات المطلوبة (يوم 7)

- ✅ 10 محادثات دافئة (LinkedIn/Email يدوي)
- ✅ 3 ردود
- ✅ 1 اجتماع محجوز
- ✅ 1 طلب scope/diagnostic

---

### 🎯 المرحلة 1: أول دفع (يوم 8-30)

**الهدف:** `payment_received` + `proof_pack_delivered`

#### 1. تفعيل Moyasar Sandbox

```bash
# في .env
MOYASAR_SECRET_KEY=sk_test_...
MOYASAR_LIVE_MODE=0

# اختبار
curl -X POST http://localhost:8000/api/v1/payment-ops/invoice-intent \
  -H "Content-Type: application/json" \
  -d '{"amount":4999,"customer_email":"test@agency.sa"}'

# تحديث Integration Truth Matrix
# dealix/transformation/founder_integration_truth.yaml
# moyasar_sandbox: green
```

#### 2. تعبئة KPIs التجارية

```bash
# نسخ القالب
cp dealix/transformation/kpi_founder_commercial_import.example.yaml \
   dealix/transformation/kpi_founder_commercial_import.yaml

# تعبئة من CRM الحقيقي (لا أرقام مخترعة)
# - leads_captured_30d
# - meetings_booked_30d
# - proposals_sent_30d
# - deals_closed_30d
# - revenue_sar_30d
# - customer_count_active

# تطبيق
python3 scripts/apply_kpi_founder_commercial.py

# تحقق
python3 scripts/apply_kpi_founder_commercial.py --status
```

#### 3. تسليم أول Diagnostic

**DoD (Definition of Done):**

1. **Kickoff Call** (30 دقيقة)
   - فهم الألم: leads تضيع؟ CRM مليان؟ لا متابعة؟
   - جمع البيانات: CSV export، وصول CRM للقراءة
   - تحديد النطاق: 10 leads أو workflow واحد

2. **Analysis** (2-3 أيام)
   - تنظيف البيانات (dedupe)
   - Scoring (ICP match)
   - Top 10 opportunities
   - 3 pain points رئيسية

3. **Proof Pack Delivery** (PDF + لوحة)
   - Executive Summary (صفحة واحدة)
   - Top 10 Opportunities (مرتّبة)
   - 3 Pain Points + Cost of Inaction
   - Next Actions (5-10 إجراءات)
   - Draft Messages (3-5 مسودات)
   - Expansion Path (Sprint/Pilot)

4. **Follow-up Call** (20 دقيقة)
   - مراجعة النتائج
   - أسئلة وتوضيحات
   - عرض Sprint/Pilot
   - طلب Referral

**مرجع:** `docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md`

#### 4. Champion Pack (لكل عميل محتمل)

**محتوى الحزمة:**

1. **ملخص مشكلة** (صفحة واحدة)
   - الألم الواضح
   - تكلفة عدم التصرف
   - المخاطر الحالية

2. **Sample Proof Pack**
   - `docs/commercial/operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md`

3. **خريطة قبل/بعد**
   - من: leads تضيع، لا متابعة، لا وضوح
   - إلى: Top 10 واضحة، next action لكل فرصة، أدلة موثّقة

4. **السعر والنطاق**
   - Diagnostic: 4,999-15,000 SAR
   - Sprint: 499 SAR (proof سريع)
   - Data Pack: 1,500 SAR

5. **ماذا نحتاج منكم؟**
   - CSV export أو وصول CRM للقراءة
   - نقطة اتصال واحدة
   - 30 دقيقة kickoff + 20 دقيقة delivery

6. **ماذا لا نفعل؟**
   - ❌ لا WhatsApp بارد
   - ❌ لا إرسال خارجي بدون موافقة
   - ❌ لا scraping إنتاجي
   - ❌ لا ضمان ROI رقمي

7. **لماذا لا نستبدل CRM أو الوكالة؟**
   - Dealix طبقة **تشغيل إيراد محكوم** فوق الأدوات الحالية
   - لا إلغاء الوكالة — **تنسيق ومتابعة وأدلة**

8. **لماذا نبدأ Pilot صغير؟**
   - تقليل مخاطرة القرار
   - إخراج دليل قابل للعرض على الإدارة
   - مدة محددة (7-30 يوم)

#### المخرجات المطلوبة (يوم 30)

- ✅ 1 Diagnostic مدفوع (4,999-15,000 SAR)
- ✅ 1 Proof Pack مسلّم
- ✅ 1 طلب إحالة أو upsell
- ✅ KPIs محدّثة في النظام
- ✅ Moyasar sandbox مفعّل

---

### 🎯 المرحلة 2: التكرار والشركاء (يوم 31-90)

**الهدف:** Motion A متكرر + أول شريك + Retainer شهري

#### 1. Motion A Agency (تكرار)

**الهدف:** 3 وكالات × Agency Proof Pack

**المسار:**

```text
Agency → 10-Lead Audit (499) 
       → Agency Proof Pack (990) 
       → Co-selling Pilot (3,000-7,500) 
       → Partner Program (15-25% عمولة)
```

**ICP (من نستهدف):**

| نعم ✅ | لا ❌ |
|-------|------|
| وكالة تسويق/إعلان/محتوى | بائع أدوات SaaS فقط |
| تدير حملات لعملاء متعددين | لا leads حقيقية بعد الحملة |
| تحتاج proof لعميلها | تطلب cold blast / scraping |
| تقبل pilot على عميل واحد | ترفض أي موافقة بشرية |

**إشارات شراء:**

- "العميل يسأل ماذا حصل بعد الحملة"
- CRM/جدول مليء بلا متابعة
- فريق مبيعات العميل غير واضح المالك

#### 2. AEO Content Calendar (12 أسبوع)

**الهدف:** استهداف نية البحث — عند سؤال "كيف أثبت ماذا حدث بعد الحملة؟" → Dealix مرجع

| أسبوع | موضوع | CTA |
|-------|--------|-----|
| 1 | Post-Lead Revenue Ops | Risk Score |
| 2 | ما هو Proof Pack | Sample Proof |
| 3 | مراجعة متابعة leads | Diagnostic |
| 4 | SOAEN Standard | قوالب سياسة |
| 5 | Agency Wedge | Agency Proof Pack |
| 6 | Decision Passport | Free Mini Diagnostic |
| 7 | Governed AI Operations | Executive OS |
| 8 | Champion Enablement | Champion Pack |
| 9 | Procurement Pack | Diagnostic |
| 10 | Partner Economy | Partner Kit |
| 11 | Customer Success | Referral Program |
| 12 | Benchmark Engine | Market Report |

**مرجع:** `docs/commercial/operations/AEO_CONTENT_CALENDAR_AR.md`

#### 3. Social Operating Checklist (كل منشور)

| # | حقل SOAEN | سؤال |
|---|-----------|------|
| S | Source | من أين الفكرة؟ (call، Proof، اعتراض، benchmark) |
| O | Owner | من ينشر ويرد على التعليقات؟ |
| A | Approval | هل راجعت المسودة قبل النشر؟ |
| E | Evidence | أي رقم؟ ما Truth Label؟ (Estimate/Observed فقط) |
| N | Next Action | CTA واحد: Risk Score / Sample Proof / ديمو 10 دقائق |

**ممنوع في المنشور:**

- ❌ اسم عميل بلا إذن
- ❌ إيراد غير Payment-confirmed
- ❌ "Dealix يرسل تلقائياً"
- ❌ ROI مضمون

#### 4. Objection Engine

**الهدف:** تحويل كل اعتراض → محتوى → أصل مبيعات

**الحلقة:**

```text
اعتراض مبيعات (من call أو CRM)
  → سجّل في objection_engine_registry.yaml
  → منشور LinkedIn (مجهّل)
  → فيديو قصير (اختياري)
  → قسم Newsletter
  → مقال FAQ / AEO
  → بريد مبيعات / أصل شريك
```

**أمثلة اعتراضات:**

1. "عندنا CRM بالفعل"
   - الرد: Dealix لا يستبدل CRM — طبقة تشغيل فوقه

2. "نحتاج ضمان ROI"
   - الرد: نعطي Proof Pack — أنتم تقررون التوسع بناءً على الدليل

3. "مكلف"
   - الرد: نبدأ صغير (499 أو 990) — لا التزام كبير

4. "ما الفرق بينكم وبين الوكالة؟"
   - الرد: الوكالة تجيب الاهتمام، Dealix يثبت ماذا حدث بعده

5. "نحتاج أتمتة كاملة"
   - الرد: الأتمتة بدون حوكمة = خطر — نبدأ بموافقات ثم نوسّع

**مرجع:** `docs/commercial/operations/objection_engine_registry.yaml`

#### 5. Commercial Weekly Scorecard

**المؤشر الوحيد قبل التوسع:**

- **Pilots النشطة** + **Proof Packs المسلّمة هذا الأسبوع**

**Scorecard كامل (بعد 3 عملاء):**

| KPI | الهدف | الفعلي | ملاحظات |
|-----|--------|--------|---------|
| لمسات يومية | 10 | ? | يدوي + موافقة |
| ردود | 3 | ? | مسجّلة في War Room |
| اجتماعات | 1 | ? | demo_booked |
| طلبات scope | 1 | ? | scope_requested |
| فواتير | 1/أسبوع | ? | invoice_sent |
| دفع | 1/شهر | ? | payment_received ✅ |
| Proof Packs | 1/شهر | ? | proof_pack_delivered ✅ |
| إحالات | 1/شهر | ? | referral_requested |

**مرجع:** `docs/commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md`

#### 6. Partner Program

**الهدف:** أول شريك نشط (وكالة أو مستشار CRM)

**أنواع الشركاء:**

| نوع | مكسب مقترح | متى |
|-----|-----------|-----|
| Referral | 15-25% أول دفعة أو 3 أشهر | بعد 1 Diagnostic ناجح |
| Implementation | شريك تنفيذ — Dealix diagnostic/proof | بعد 2 Diagnostics |
| Co-selling | تقسيم pilot / referral | بعد 3 Diagnostics |
| Service exchange | 30 يوم — محدود | حالة خاصة |
| White-label | بعد 3 paid pilots | مرحلة لاحقة |

**Partner Onboarding Kit:**

1. **Partner Brief** (صفحة واحدة)
   - ما Dealix؟
   - لماذا شريك؟
   - ما المكسب؟

2. **Sales Assets**
   - One-pager
   - Sample Proof Pack
   - Demo script
   - Objection handler

3. **Commission Structure**
   - 15% أول دفعة (Referral)
   - 20% 3 أشهر (Implementation)
   - 25% Co-selling

4. **Tracking**
   - Partner code في War Room
   - Commission tracker CSV

**مرجع:** `docs/commercial/operations/PARTNER_ONBOARDING_KIT_AR.md`

#### المخرجات المطلوبة (يوم 90)

- ✅ 3-5 Diagnostics مدفوعة
- ✅ 1 شريك نشط (وكالة أو مستشار CRM)
- ✅ 1 Retainer شهري (15,000-25,000 SAR/شهر)
- ✅ Moyasar Live مفعّل
- ✅ 12 منشور AEO منشورة
- ✅ Newsletter أسبوعي (4 إصدارات)
- ✅ Objection Engine نشط (5+ اعتراضات مسجّلة)

---

## الأدوات الجاهزة (استخدمها الآن)

### 1. الأوامر اليومية

```bash
# صباح (5 دقائق) — الأمر الموحّد
bash scripts/run_founder_commercial_day.sh

# صباح موسّع (+ Business NOW)
bash scripts/run_founder_revenue_day.sh

# مساء (تسجيل أدلة)
python3 scripts/founder_evening_evidence.py --append \
  --event-type message_sent_manual \
  --company "Agency Name"

# تحقق أسبوعي
bash scripts/founder_go_live_verify.sh

# أمر واحد (أقصى أتمتة)
bash scripts/founder_one_command.sh
```

### 2. الواجهات

- **War Room**: `/ar/ops/founder`
- **Business NOW**: `/ar/business-now`
- **Commercial Strategy**: `/ar/business-now#strategy`
- **Approvals**: `/ar/ops/approvals`
- **Marketing**: `/ar/ops/marketing`
- **Evidence**: `/ar/ops/evidence`

### 3. APIs

```bash
# Business NOW snapshot
GET /api/v1/business-now/snapshot

# Commercial strategy
GET /api/v1/business-now/commercial-strategy

# War Room today pack
GET /api/v1/ops-autopilot/war-room/today-pack

# Anti-waste check (قبل أي إرسال خارجي)
POST /api/v1/revenue-os/anti-waste/check

# Evidence events
POST /api/v1/evidence/events
```

### 4. الوثائق

| الموضوع | المرجع |
|--------|--------|
| **يومي (5 دقائق)** | `docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md` |
| **GTM شامل** | `docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md` |
| **محرك إغلاق** | `docs/commercial/FULL_OPS_CLOSE_ENGINE_AR.md` |
| **War Room** | `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md` |
| **أسعار وحزم** | `docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md` |
| **Sales Kit** | `docs/sales-kit/START_HERE.md` |
| **Proof Pack** | `docs/delivery/PROOF_PACK_TEMPLATE.md` |
| **Integration Truth** | `docs/ops/FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md` |
| **Founder OS** | `docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md` |

---

## الممنوعات (غير قابلة للتفاوض)

### ❌ لا تفعل أبدًا

1. **إرسال WhatsApp بارد** — مسودات + موافقة فقط
2. **LinkedIn automation/scraping** — يدوي فقط
3. **Gmail خارجي بدون موافقة** — مسودات أولاً
4. **ادعاء إيراد قبل `invoice_paid`** — لا أرقام مخترعة
5. **وعود ROI مضمون** — Proof Pack فقط
6. **أرقام CRM مخترعة** — من استيراد حقيقي فقط
7. **بناء features قبل أول دفع** — استخدم ما بُني

### ✅ افعل دائمًا

1. **مسودة + موافقة** قبل أي إرسال خارجي
2. **تسجيل Evidence Events** يوميًا
3. **SOAEN** في كل touchpoint
4. **Champion Pack** لكل صفقة
5. **Proof Pack** بعد كل دفع
6. **Anti-waste check** قبل أي حملة
7. **War Room update** يوميًا (10 targets)

---

## مؤشرات النجاح (KPIs)

### المرحلة 0 (يوم 7)
- ✅ 10 محادثات دافئة
- ✅ 3 ردود
- ✅ 1 اجتماع
- ✅ 1 طلب scope

### المرحلة 1 (يوم 30)
- ✅ 1 Diagnostic مدفوع
- ✅ 1 Proof Pack مسلّم
- ✅ KPIs محدّثة
- ✅ Moyasar sandbox

### المرحلة 2 (يوم 90)
- ✅ 3-5 Diagnostics
- ✅ 1 شريك نشط
- ✅ 1 Retainer شهري
- ✅ Moyasar Live
- ✅ 12 منشور AEO
- ✅ 4 Newsletters

---

## الخطوة التالية (الآن)

### الخيار A: ابدأ التشغيل اليومي (موصى به)

```bash
# 1. الأمر الصباحي
bash scripts/run_founder_commercial_day.sh

# 2. افتح War Room
# واجهة: /ar/ops/founder
# أضف تاريخ متابعة لـ 10 أهداف high priority

# 3. سجّل حدث أدلة (مساءً)
python3 scripts/founder_evening_evidence.py --append
```

### الخيار B: تحقق من الجاهزية أولاً

```bash
# تحقق شامل
bash scripts/founder_go_live_verify.sh

# Business NOW
bash scripts/run_business_now.sh

# Revenue OS
bash scripts/revenue_os_master_verify.sh
```

### الخيار C: شاهد الديمو

- افتح `/ar/business-now#strategy`
- جرّب Simulate → Focus → GTM
- راجع Offers في `/ar/services`

---

## الدعم والمراجع

### GitHub Workflows (Automated)

- **Daily Revenue Machine**: `.github/workflows/daily-revenue-machine.yml` (04:00 UTC)
- **Founder Commercial Daily**: `.github/workflows/founder_commercial_daily.yml` (05:00 UTC Sun-Thu)
- **Evening Evidence**: `.github/workflows/founder_evening_evidence.yml`

### Scripts Index

| Script | الغرض |
|--------|--------|
| `run_founder_commercial_day.sh` | الأمر الصباحي الموحّد |
| `run_founder_revenue_day.sh` | صباح موسّع (+ Business NOW) |
| `founder_evening_evidence.py` | تسجيل أدلة مساءً |
| `founder_go_live_verify.sh` | تحقق جاهزية |
| `founder_one_command.sh` | أقصى أتمتة |
| `run_business_now.sh` | لقطة Business NOW |
| `revenue_os_master_verify.sh` | تحقق Revenue OS |
| `apply_kpi_founder_commercial.py` | تطبيق KPIs |

### Config Files

| File | الغرض |
|------|--------|
| `dealix/config/social_content_queue.yaml` | قائمة محتوى سوشال |
| `dealix/config/icp_agency_wedge.yaml` | ICP للوكالات |
| `dealix/transformation/founder_integration_truth.yaml` | مصفوفة التكاملات |
| `dealix/transformation/kpi_founder_commercial_import.yaml` | KPIs تجارية |
| `docs/commercial/operations/evidence_events_tracker.csv` | تتبع أدلة |
| `docs/commercial/operations/targeting/agency_accounts_seed.csv` | بذرة أهداف |

---

## الخلاصة

**Dealix جاهز تقنيًا 95%**. الفجوة الوحيدة هي **التنفيذ التجاري اليومي**.

**الخطوة الأولى (الآن):**

```bash
bash scripts/run_founder_commercial_day.sh
```

**ثم:**

1. افتح `/ar/ops/founder`
2. أضف 10 أهداف في War Room
3. جهّز مسودة واحدة (يدوي + موافقة)
4. سجّل حدث أدلة (مساءً)

**بعد 7 أيام:**

- 10 محادثات
- 3 ردود
- 1 اجتماع
- 1 طلب scope

**بعد 30 يوم:**

- 1 Diagnostic مدفوع ✅
- 1 Proof Pack مسلّم ✅

**بعد 90 يوم:**

- 3-5 Diagnostics
- 1 شريك
- 1 Retainer شهري
- **Dealix أقوى شركة في السوق** 🚀

---

*آخر تحديث: 2026-06-10*  
*الحالة: ACTIVE — جاهز للتنفيذ الفوري*
