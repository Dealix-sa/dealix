# Dealix — هرم Full Ops والأجنتس — Full Ops Agent Hierarchy
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **مبدأ Full Ops:** كل شيء ذاتي التشغيل **حتى لحظة الفعل الخارجي**. الأجنتس
> ينجزون كل العمل — بحث، تأهيل، تسجيل، صياغة، تجميع Proof Pack، مراجعة،
> تخطيط — تلقائياً وبلا تدخّل. الفعل الخارجي الوحيد (إرسال، تحصيل، نشر،
> بدء تسليم) يتوقف عند **بوابة موافقة بنقرة واحدة**.
>
> هذا ليس قيداً — هذا **هو المنتج**: Governed Revenue & AI Operations.
> الأجنتس بلا حدود = خرق `no_unbounded_agents`. الإرسال التلقائي = خرق
> `no_live_send`. التحصيل التلقائي = خرق `no_live_charge`.

ارجع إلى [`CURRENT_DIRECTION.md`](CURRENT_DIRECTION.md) للاتجاه،
[`TRUST_LAYER.md`](TRUST_LAYER.md) للـ11 غير القابلة للتفاوض، و
[`TOOL_STACK.md`](TOOL_STACK.md) لحدود الأتمتة.

---

## 1. الهرم — The Hierarchy

```
                    ┌─────────────────────────────┐
        Tier 4      │   المؤسس — Founder          │  بوابة الموافقة الوحيدة
                    │   Approval Authority (L4)   │  للأفعال الخارجية
                    └──────────────┬──────────────┘
                                   │ approve / reject
                    ┌──────────────┴──────────────┐
        Tier 1      │  Chief of Staff Orchestrator │  يخطّط اليوم، يوزّع
                    │  وكيل رئاسة الأركان (L3)      │  المهام، يجمع الحزمة
                    └──────┬───────────────┬───────┘
                ┌──────────┘               └──────────┐
        Tier 2  │  الأجنتس الاستراتيجيون   │  Tier 3  │ الأجنتس التنفيذيون │
                │  Strategic Agents        │          │ Executive Agents   │
                └──────────┬───────────────┘          └─────────┬─────────┘
                           └──────────────┬───────────────────────┘
                    ┌──────────────────────┴──────────────────────┐
        Tier 0      │  طبقة الحوكمة والأمان — Governance & Safety   │
                    │  agent_os · secure_agent_runtime_os ·         │
                    │  governance_os · kill switch · audit chain    │
                    └───────────────────────────────────────────────┘
```

كل أجنت — في أي طبقة — يعمل **داخل** Tier 0. لا استثناء.

---

## 2. Tier 0 — طبقة الحوكمة والأمان (الرَّكائز)

ليست أجنتس؛ هي السكك التي تجري فوقها كل الأجنتس.

| المكوّن | الوحدة البرمجية | الدور |
|---------|----------------|-------|
| سجل الأجنتس | `auto_client_acquisition/agent_os/agent_registry.py` | هوية كل أجنت — `AgentCard` |
| مستويات الاستقلالية | `agent_os/autonomy_levels.py` | L0→L4 (L5 محظور في MVP) |
| الحدود الأربع | `secure_agent_runtime_os/four_boundaries.py` | prompt · tool · data · context |
| مفتاح الإيقاف | `secure_agent_runtime_os/kill_switch.py` | إيقاف فوري عام أو لأجنت |
| محرّك السياسة | `secure_agent_runtime_os/policy_engine.py` | يسمح/يمنع كل أداة |
| سجل سياسات الحوكمة | `governance_os/policy_registry.py` | الأفعال المحظورة |
| مصفوفة الموافقة | `governance_os/approval_matrix.py` | متى يلزم توقيع |
| بوابة المسودات | `governance_os/draft_gate.py` | يمنع cold outreach / scraping |
| سلسلة التدقيق | `tests/governance/test_audit_chain.py` | `no_unaudited_changes` |

---

## 3. مستويات الاستقلالية — Autonomy Levels

| المستوى | الاسم | يفعل | يحتاج موافقة؟ |
|---------|------|------|----------------|
| L0 | Read-only | يقرأ بيانات فقط | لا |
| L1 | Analyze | يحلّل، يسجّل نقاطاً | لا |
| L2 | Draft | يكتب مسودات داخلية | لا (المسودة داخلية) |
| L3 | Recommend | يوصي بقرار/خطوة | لا للتوصية — نعم للتنفيذ |
| L4 | Auto-with-audit | ينفّذ داخلياً مع تدقيق كامل | للأفعال الداخلية فقط |
| L5 | Fully autonomous | — | **محظور في MVP** |

**القاعدة الصارمة:** لا أجنت يبلغ L4 لفعل **خارجي**. كل فعل خارجي يمرّ
بـTier 4 (المؤسس) مهما كان مستوى الأجنت.

---

## 4. Tier 1 — Chief of Staff Orchestrator

**الدور — وكيل رئاسة الأركان.** عقل التشغيل اليومي.

- يخطّط اليوم: يقرأ scorecard الأمس، يحدّد أولويات اليوم.
- يوزّع المهام على الأجنتس الاستراتيجيين والتنفيذيين.
- يجمع كل المخرجات في **حزمة المؤسس اليومية** (founder daily pack).
- يرفع كل فعل خارجي إلى Approval Center.
- يحدّث [`DAILY_SCORECARD.md`](DAILY_SCORECARD.md).

**الربط البرمجي:** `POST /api/v1/ops-autopilot/founder/full-autonomous-ops/run`
· `OpsFullAutonomousOpsCard.tsx` · `scripts/run_founder_commercial_day.sh`.
**الاستقلالية:** L3 — يخطّط ويوصي، لا يرسل أبداً.

---

## 5. Tier 2 — الأجنتس الاستراتيجيون — Strategic Agents

أفق أطول: تحليل، تخطيط، تموضع، تنبؤ.

| الأجنت (الدور) | الوحدة البرمجية | يفعل | L |
|----------------|----------------|------|---|
| محلّل ICP / السوق | `agents/icp_matcher.py` + `sales_os/icp_score.py` | يسجّل المطابقة 0–100 | L1 |
| محلّل الألم والتموضع | `agents/pain_extractor.py` | يستخرج نقاط الألم | L1 |
| وكيل برج التحكم | KPI scripts + [`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md) | يجمّع KPIs، يكشف الاختناقات | L1 |
| وكيل Benchmark | `benchmark_os/` | تقارير k-anonymous مرجعية | L1 |
| وكيل استراتيجية الشركاء | `partnership_os/` + [`PARTNER_ECONOMY.md`](PARTNER_ECONOMY.md) | يرتّب فرص الشراكة | L3 |

مخرجاتهم تغذّي Chief of Staff والمراجعة الأسبوعية.

---

## 6. Tier 3 — الأجنتس التنفيذيون — Executive Agents

ينجزون مهام دورة الإيراد اليومية. مرتّبون حسب رحلة الـlead.

| # | الأجنت (الدور) | الوحدة البرمجية | يفعل | L |
|---|----------------|----------------|------|---|
| 1 | موظف الاستقبال | `agents/intake.py` + `lead_inbox.py` | يستقبل ويتحقق من الـlead | L2 |
| 2 | الباحث / Prospector | `agents/prospector.py` | بحث وإثراء (بلا scraping) | L1 |
| 3 | موظف التأهيل | `agents/qualification.py` + `sales_os/qualification.py` | درجة + verdict + عرض موصى | L3 |
| 4 | صائغ التواصل | `agents/outreach.py` | مسودات رسائل (draft_only) | L2 |
| 5 | صائغ العروض | `agents/proposal.py` + `sales_os/proposal_renderer.py` | مسودة عرض + تسعير من السلم | L2 |
| 6 | منسّق الحجوزات | `agents/booking.py` | تنسيق المواعيد | L3 |
| 7 | مجدول المتابعة | `agents/followup.py` | تسلسل المتابعات | L3 |
| 8 | مزامن الـCRM | `agents/crm.py` | مزامنة جهات/صفقات | L4 (داخلي) |
| 9 | مشغّل الـSprint | `delivery_factory/delivery_sprint.py` | 10 خطوات تسليم | L4 (داخلي) |
| 10 | مجمّع Proof Pack | `proof_os/proof_pack.py` | 14 قسماً موزونة بالأدلة | L4 (داخلي) |
| 11 | وكيل عمليات الدفع | `payment_ops/orchestrator.py` | invoice intent (لا تحصيل) | L3 |
| 12 | وكيل فرز الدعم | `support_os/` | تصنيف تذاكر + ردود مسودة | L2 |
| 13 | صائغ المحتوى | `scripts/generate_weekly_content_drafts.py` | مسودات LinkedIn / newsletter | L2 |

التسعير في كل مخرج يستخدم السلم الرسمي — [`OFFER_LADDER.md`](OFFER_LADDER.md).

---

## 7. Tier 4 — المؤسس وبوابة الموافقة

المؤسس هو **السلطة الوحيدة** لكل فعل خارجي. كل مسودة جاهزة من Tier 3 تصل
إلى **Approval Center** (`components/approvals/ApprovalCenter.tsx`):

- Pending — مسودات بانتظار قرار (email · LinkedIn · support · compliance).
- History — موافق / مرفوض.
- Today's Drafts — ملخص.
- Channel Gates — حالة السياسة لكل قناة.

نقرة واحدة: `approve` → ينفّذ الأجنت الفعل ويسجّله في سلسلة التدقيق؛
`reject` → يعود للأجنت بالسبب لإعادة الصياغة.

---

## 8. مسار التصعيد — Escalation Path

```
أجنت تنفيذي يصطدم بـ:
   • حد من الحدود الأربع فشل      → secure runtime: RESTRICTED/ESCALATED
   • فعل خارجي جاهز               → Approval Center (Tier 4)
   • ادعاء غير مدعوم / مخاطرة     → governance BLOCK → Chief of Staff
   • غموض استراتيجي               → Chief of Staff → Tier 2
   • خطر جسيم                     → kill switch (أي شخص يملك الصلاحية)
```

أي فعل خطير = `activate_kill_switch(agent_id, reason)` — السبب إلزامي.

---

## 9. الإيقاع الذاتي اليومي — The Autonomous Daily Cadence

| الوقت | الفاعل | المخرج |
|-------|--------|--------|
| 00:00 | Chief of Staff | يقرأ scorecard الأمس، يبني خطة اليوم |
| صباحاً | Tier 2 + Tier 3 | تأهيل، بحث، صياغة، تجميع Proof Packs — تلقائياً |
| صباحاً | Chief of Staff | حزمة المؤسس اليومية + قائمة الموافقات |
| خلال اليوم | المؤسس | موافقات بنقرة — 10 touches، عروض، تسليم |
| مساءً | Tier 3 | تسجيل النتائج، تحديث حالات الـleads |
| مساءً | Chief of Staff | بطاقة [`DAILY_SCORECARD.md`](DAILY_SCORECARD.md) |
| أسبوعياً | Tier 2 | مراجعة [`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md) §6 |

المؤسس يلمس النظام بقدر الموافقات فقط — الباقي ذاتي التشغيل.

---

## 10. الربط فرونت ↔ باك — Front/Back Wiring

```
Next.js Ops UI (frontend/src/app/[locale]/ops/*)
   │  axios + X-Admin-API-Key  (frontend/src/lib/api.ts)
   ▼
ops-autopilot API  (api/routers/revenue_ops_autopilot.py)
   ▼
Chief of Staff Orchestrator  → Strategic + Executive Agents
   ▼
agent_os + secure_agent_runtime_os + governance_os   (Tier 0)
   ▼
Proof / Value / Capital / Audit ledgers
   ▲
Approval Center UI  ◄── كل فعل خارجي
```

أسطح الـUI: `/ops/founder` · `/ops/war-room` · `/ops/sales` ·
`/ops/marketing` · `/ops/approvals` · `/ops/evidence` · `/ops/targeting`
· `/ops/support` · `/business-now`.

---

## 11. ما هو ذاتي التشغيل الآن مقابل الفجوات

**ذاتي التشغيل بالكامل اليوم (بلا تدخّل):** الاستقبال · التأهيل · تسجيل ICP
· تسجيل المخاطر · صياغة العروض · invoice intent · جودة البيانات · ترتيب
الحسابات · تجميع Proof Pack · مراجعة الحوكمة للمسودات · فحص جاهزية الـretainer
· جدولة التجديد.

**يبقى عند بوابة الموافقة (بحكم العقيدة — صحيح):** الإرسال الخارجي · تأكيد
الدفع · بدء التسليم · النشر على القنوات.

**فجوات حقيقية للإغلاق — Real gaps (build roadmap):**

| # | الفجوة | الإجراء | الحالة |
|---|--------|---------|--------|
| 1 | `frontend/src/lib/opsAdmin.ts` مفقود — 12 مكوّن ops تستورده، الـUI لا يُبنى | إنشاء الملف: `getAdminApiKey()` · `isOpsConfigured()` · `opsMissingKeyMessage()` | ✅ مُغلق |
| 2 | لا مجدول دوري للأجنتس (cron) | سكربت/خدمة تستدعي Chief of Staff يومياً | مفتوح |
| 3 | لا أجنت رسمي لـTier 2 "برج التحكم" و"Benchmark" ككائنات `AgentCard` مسجّلة | تسجيلهما في `agent_registry` بـcards L1 | مفتوح |
| 4 | Chief of Staff موزّع عبر سكربتات — لا `AgentCard` واحد له | تسجيله كأجنت L3 صريح | مفتوح |

هذه الفجوات تُغلق كتغييرات مركّزة منفصلة — لا تُبنى دفعة واحدة فوق ريبو
ناضج (290+ اختباراً).

---

## 12. الأمان والمؤشرات — Safety & KPIs

- مفتاح الإيقاف يعمل على كل المستويات — `kill_switch_active()`.
- كل فعل حسّاس → سلسلة تدقيق (`no_unaudited_changes`).
- مؤشرات الأمان في [`DAILY_SCORECARD.md`](DAILY_SCORECARD.md) §5 يجب أن تبقى صفراً:
  cold WhatsApp = 0 · fake proof = 0 · live send بلا موافقة = 0.
- مؤشرات الأداء في [`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md) §2.

> النظام يكبر بالأجنتس — لا بكسر البوابات. كل أجنت جديد يولد بـ`AgentCard`،
> داخل الحدود الأربع، وتحت مفتاح إيقاف.

---

*Estimated outcomes are not guaranteed outcomes — النتائج التقديرية ليست
نتائج مضمونة.*
