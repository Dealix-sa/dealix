# عقد التنفيذ — كل مكوّن له مسؤول ومدخلات ومخرجات
# Dealix Execution Contract — Every Engine Has an Owner, Inputs, and Outputs

---

## المبدأ — Principle

كل محرك تنفيذي في Dealix يعمل وفق عقد واضح. لا محرك يعمل بدون مدخلات محددة، ولا مخرج يُسلَّم بدون معيار جودة.

Every Dealix execution engine operates on a clear contract. No engine runs without defined inputs, and no output is delivered without a quality gate.

---

## المحرك الأول — Mini Proposal Engine

**Purpose:** إنتاج عرض صفحة واحدة واضح النطاق لكل فرصة مؤهلة.

**Owner:** المؤسس (dealix-sales يُنتج المسودة، المؤسس يعتمد)

**Inputs:**
- بيانات الحساب من TOP_100_ACCOUNT_QUEUE
- Need Fit Score ≥ 7
- اسم النظام المقترح
- السعر من OFFER_STRATEGY_AR

**Outputs:**
- Mini Proposal مكتمل (1 صفحة)
- قائمة Out-of-Scope واضحة
- قائمة المدخلات المطلوبة من العميل

**Quality Gate:** موافقة المؤسس قبل إرسال أي مقترح. Claim Safety check: لا وعود ROI، لا ضمانات.

**Report:** `reports/proposals/MINI_PROPOSAL_QUEUE.md`

**Check:** `scripts/checks/check_proposal_safety.py`

**Failure Mode:** مقترح يُرسَل بدون موافقة المؤسس، أو يحتوي على وعود غير قابلة للإثبات.

**Recovery:** سحب المقترح، مراجعة Claim Safety، إعادة الاعتماد.

---

## المحرك الثاني — Account Intelligence Engine

**Purpose:** تحليل بيانات العملاء المحتملين وإنتاج Account Pack لكل حساب ذي أولوية.

**Owner:** المؤسس (Data Intelligence Agent يُنتج التحليل)

**Inputs:**
- بيانات الشركة المستهدفة (قطاع، حجم، أدوات حالية)
- بيانات تشغيلية إذا قدمها العميل (في الفحص المجاني)
- BUSINESS_NEEDS_25_AR كمرجع للأنماط

**Outputs:**
- Account Pack (تقرير Need Fit Score + Sprint مقترح)
- تحديث سجل TOP_100_ACCOUNT_QUEUE

**Quality Gate:**
- لا يحتوي على PII غير معالجة
- كل توصية مبنية على بيانات موثقة
- لا ادعاءات غير مدعومة بأدلة

**Report:** `reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md`

**Check:** `scripts/checks/check_pii_redaction.py`

**Failure Mode:** بيانات شخصية تدخل في prompt مباشرة بدون تنظيف.

**Recovery:** إيقاف المحرك، تنظيف البيانات، مراجعة سياسة Sandboxing.

---

## المحرك الثالث — Email Drafts Engine

**Purpose:** صياغة مسودات رسائل التواصل وفق نموذج Hook → Pain → System → Sprint → CTA.

**Owner:** المؤسس (Outreach Draft Agent يُنتج المسودات)

**Inputs:**
- Account Pack من Account Intelligence Engine
- القطاع ونموذج الرسالة المناسب
- موافقة على القائمة المستهدفة

**Outputs:**
- مسودات رسائل معزولة في ملفات مسودة
- قائمة مراجعة SYSTEM_EMAIL_DRAFTS_REVIEW

**Quality Gate:**
- لا إرسال مباشر — المسودة تنتظر موافقة المؤسس
- لا وعود مضمونة في الرسالة
- يُذكر النظام المقترح، لا AI العام

**Report:** `reports/outreach/SYSTEM_EMAIL_DRAFTS_REVIEW.md`

**Check:** `scripts/checks/check_outreach_claims.py`

**Failure Mode:** وكيل يُرسل رسالة مباشرة بدون موافقة.

**Recovery:** إيقاف فوري لوكيل Outreach، مراجعة سجل النشاط، تحديث WORKFLOW_FIRST_AGENT_POLICY.

---

## المحرك الرابع — Call Brief Engine

**Purpose:** إعداد ملخص اتصال مُخصَّص لكل مكالمة مبيعات مجدولة.

**Owner:** المؤسس (dealix-sales يُعد المسودة)

**Inputs:**
- Account Pack من Account Intelligence Engine
- تاريخ التواصل السابق (إن وجد)
- النظام المقترح للنقاش

**Outputs:**
- Call Brief (1 صفحة) يتضمن: السؤال الافتتاحي، الأنظمة للنقاش، الهدف، الخطوة التالية
- تحديث CALL_FOLLOWUP_QUEUE بعد المكالمة

**Quality Gate:**
- الهدف من المكالمة: تحديد الحاجة لا إغلاق الصفقة
- Call Brief يُراجَع قبل المكالمة بـ 30 دقيقة

**Report:** `reports/acquisition/CALL_FOLLOWUP_QUEUE.md`

**Check:** `scripts/checks/check_call_brief_completeness.py`

**Failure Mode:** مكالمة بدون Brief → معلومات ناقصة → فرصة ضائعة.

**Recovery:** إضافة القاعدة: لا مكالمة بدون Call Brief معتمد.

---

## المحرك الخامس — Delivery Pipeline Engine

**Purpose:** إدارة تدفق كل Sprint من Intake إلى Sign-Off.

**Owner:** المؤسس (dealix-delivery يتابع الحالة)

**Inputs:**
- نطاق Sprint الموقّع
- مدخلات العميل (ملفات، بيانات)
- جدول التسليم

**Outputs:**
- تحديثات يومية في DELIVERY_PIPELINE_STATUS
- Proof Pack عند الإنجاز
- Sign-Off Template مكتمل

**Quality Gate:**
- لا تسليم بدون Sign-Off من العميل
- كل مرحلة تُكتمَل قبل الانتقال للتالية
- Delivery Health Score ≥ 75

**Report:** `reports/delivery/DELIVERY_PIPELINE_STATUS.md`

**Check:** `scripts/checks/check_delivery_stages.py`

**Failure Mode:** تسليم ناقص يُعلَن مكتملاً.

**Recovery:** Delivery Blocker يُضاف فوراً، مراجعة مع العميل، إعادة جدولة.

---

## المحرك السادس — Agent Governance Engine

**Purpose:** مراقبة وتدقيق أنشطة كل الوكلاء يومياً.

**Owner:** المؤسس

**Inputs:**
- AGENT_DAILY_ACTIVITY_REVIEW من كل وكيل
- AGENT_PERMISSION_MATRIX كمرجع

**Outputs:**
- Agent Governance Score (0–100)
- تنبيهات انتهاك فورية
- AGENT_PERMISSION_AUDIT أسبوعي

**Quality Gate:**
- Agent Governance Score ≥ 90 قبل أي توسع
- أي انتهاك يُوقف الوكيل المخالف فوراً

**Report:** `reports/agents/AGENT_PERMISSION_AUDIT.md`

**Check:** `scripts/checks/check_agent_compliance.py`

**Failure Mode:** وكيل يتصرف خارج صلاحياته بدون كشف.

**Recovery:** مراجعة سجل النشاط، تحديث مصفوفة الصلاحيات، تدريب على السياسة.

---

## المحرك السابع — Deliverability Engine

**Purpose:** ضمان وصول رسائل البريد الإلكتروني لصندوق الوارد، وليس مجلد الرسائل غير المرغوب فيها.

**Owner:** المؤسس

**Inputs:**
- Domain Health Review (SPF/DKIM/DMARC)
- معدلات فتح الرسائل وارتداد البريد

**Outputs:**
- DOMAIN_HEALTH_REVIEW مُحدَّث
- تنبيهات إذا Bounce Rate > 2% أو Spam Rate > 0.1%

**Quality Gate:**
- SPF: صالح
- DKIM: موقَّع
- DMARC: محدد السياسة
- Bounce Rate < 2%
- Spam Rate < 0.1%

**Report:** `reports/deliverability/DAILY_DELIVERABILITY_REVIEW.md`

**Check:** `scripts/checks/check_domain_health.py`

**Failure Mode:** Bounce Rate يرتفع فجأة → الدومين في خطر.

**Recovery:** إيقاف الإرسال، تحليل الأسباب، تنظيف القائمة.

---

## المحرك الثامن — Founder Command Engine

**Purpose:** إنتاج القرار اليومي للمؤسس (GO/HOLD/FIX/SCALE/PAUSE) بناءً على حالة كل المحركات.

**Owner:** المؤسس فقط

**Inputs:**
- حالة كل 7 محركات سابقة
- Launch Score + Scale Score + Delivery Health Score + Agent Governance Score

**Outputs:**
- DAILY_SUPER_COMMAND مُحدَّث
- FOUNDER_WAR_ROOM_DAILY مُحدَّث

**Quality Gate:**
- القرار يصدر من المؤسس مباشرة — لا وكيل يُصدر هذا القرار
- يُسجَّل يومياً الساعة 08:00

**Report:** `reports/founder/DAILY_SUPER_COMMAND.md`

**Check:** `scripts/checks/check_daily_command_completeness.py`

**Failure Mode:** يوم يبدأ بدون قرار واضح.

**Recovery:** الرجوع لآخر DAILY_SUPER_COMMAND + مراجعة الـ 4 Scores.

---

## الوثائق المرتبطة — Related Documents

- [`docs/agents/AGENT_REGISTRY_AR.md`](../agents/AGENT_REGISTRY_AR.md)
- [`docs/operating_factory/DAILY_LOOP_AR.md`](../operating_factory/DAILY_LOOP_AR.md)
- [`reports/founder/DEALIX_EXECUTION_CONTROL_BOARD.md`](../../reports/founder/DEALIX_EXECUTION_CONTROL_BOARD.md)
- [`docs/delivery/AUTOMATED_DELIVERY_PIPELINE_AR.md`](../delivery/AUTOMATED_DELIVERY_PIPELINE_AR.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value*
