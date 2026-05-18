# Full Ops Sales System — خطة البناء على موجات
<!-- WAVE 18 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> آخر موجة منجَزة في المستودع: Wave 17. هذه الخطة تبدأ من **Wave 18**.
> لا موجة تُغلَق ببوابة حمراء — `dealix-qa` و`dealix-governance` يصدران الحكم.

---

## القاعدة العامة — Per-wave gate

كل موجة تُغلَق فقط عند:
1. كل دالة عامّة جديدة لها اختبار.
2. بوابات الدوكترين (`tests/test_no_*`, `test_doctrine_guardrails.py`) خضراء.
3. كل إجراء جديد مُصنَّف في `ACTION_CLASSIFICATIONS`.
4. كل مخرج API يحمل `governance_decision`.
5. لا انتقال مرحلة بلا `AuditEntry`.

---

## Wave 18 — العقود وعمود التنسيق
**الهدف:** عمود فقري للتنسيق بلا منطق مراحل بعد.

| البند | الوحدة | الأجينت |
|-------|--------|---------|
| `FullOpsOrchestrator` فوق `control_plane_os.WorkflowRun` | `auto_client_acquisition/full_ops_os/` (جديد) | architect → engineer |
| سجلّ المراحل الـ12 + توصيفها | `full_ops_os/stages.py` | engineer |
| بثّ `EventEnvelope` + كتابة `AuditEntry` لكل انتقال | `full_ops_os/` | engineer |
| `auto_exec_allowed(action)` فوق `classifications` | `full_ops_os/gate.py` | governance |
| اختبارات العمود + حدّ الأتمتة | `tests/test_full_ops_orchestrator.py` | qa |

**المخرج:** منسّق يفتح `WorkflowRun`، يسلسل مراحل فارغة، يبثّ أحداثاً، يصنّف.

---

## Wave 19 — هرم أجينتس وقت-التشغيل
**الهدف:** تسجيل الهرم وربط الحوكمة.

| البند | الوحدة | الأجينت |
|-------|--------|---------|
| `AgentCard` لكل أجينت Tier 0–2 (16 أجينت) | `agent_os.agent_registry` | architect → engineer |
| موزّع `revenue-conductor` → مدراء → عمّال | `full_ops_os/dispatcher.py` | engineer |
| خطّاف `governance-warden` (`evaluate_action` قبل كل إجراء) | `agent_governance` | governance |
| موزّع التنفيذ الذاتي (`A0` فقط) | `full_ops_os/auto_exec.py` | governance + engineer |
| اختبارات الهوية والاستقلالية والحدّ | `tests/test_full_ops_agents.py` | qa |

**المخرج:** الهرم مُسجَّل، كل إجراء يمرّ بالحوكمة، `A0` ينفّذ ذاتياً.

---

## Wave 20 — أتمتة قمع المبيعات (المراحل 1–8)
**الهدف:** من الإشارة إلى بوابة الموافقة، ذاتياً.

| البند | الوحدة | الأجينت |
|-------|--------|---------|
| ربط المراحل 1–7 عبر المنسّق | `full_ops_os/` ↔ `data_os/sales_os/revenue_os` | engineer + data |
| تكامل بوابة الموافقة (المرحلة 8) | `approval_center` | engineer |
| موجِّهات `prefix=/api/v1/full-ops` | `api/routers/full_ops.py` (جديد) | engineer |
| تخصيب بلا scraping — مصادر معلنة فقط | `data_os` + `enrichment_waterfall` | data |
| اختبارات المراحل + smoke الموجِّهات | `tests/` | qa |

**المخرج:** lead يدخل → يُخصَّب ويُقيَّم ويُؤهَّل تلقائياً → مسودّة تنتظر الموافقة.

---

## Wave 21 — أتمتة التسليم والتوسّع (المراحل 9–12)
**الهدف:** إغلاق الحلقة بعد الموافقة.

| البند | الوحدة | الأجينت |
|-------|--------|---------|
| ربط التسليم وProof Pack (score ≥ 70) | `proof_os`, `value_os` | delivery + engineer |
| جاهزية Retainer + إشارات التوسّع | `adoption_os`, `client_os` | engineer |
| تجميع الاحتكاك + تسجيل Capital Asset | `friction_log`, `capital_os` | delivery |
| إعادة تقييم التعلّم | `command_os` | engineer |
| اختبارات الحلقة الكاملة E2E | `tests/test_full_ops_e2e.py` | qa |

**المخرج:** الحلقة الـ12 تعمل كاملةً حتى بوابة الموافقة.

---

## Wave 22 — Full Ops Console (الواجهة)
**الهدف:** واجهة المؤسس.

| البند | الموقع | الأجينت |
|-------|--------|---------|
| لوحة pipeline | `frontend/src/app/[locale]/pipeline/` | frontend |
| تغذية نشاط الأجينتس | `frontend/.../agents/` | frontend |
| صندوق الموافقات (موافقة بضغطة، تجميعية) | `frontend/.../approvals/` | frontend |
| اللوحة اليومية للتصريف | `frontend/.../dashboard/` | frontend |
| E2E للواجهة + ربط `api.ts` | `frontend/` | frontend + qa |

**المخرج:** المؤسس يرى الحلقة كاملةً ويوافق من مكان واحد.

---

## بوابة القرار — Decision Gate

بعد Wave 22: إن استقرّت الحلقة وتكرّر workflow عبر 3+ عملاء، يُقترح Wave 23
(تشديد المؤسسة: تتبّع موزّع، تصدير تدقيق، أداء). لا توسّع قبل تكرار مُثبَت —
نفس مبدأ "لا ترقية قبل نتيجة موثّقة" في
[`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

---

*Version 1.0 | Waves 18–22 | No wave closes on a red gate.*
