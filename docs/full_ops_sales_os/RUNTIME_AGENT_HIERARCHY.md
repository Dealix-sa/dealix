# Runtime Agent Hierarchy — هرم أجينتس وقت-التشغيل
<!-- WAVE 18 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> هذه أجينتس **داخل المنتج** — تشغّل دورة المبيعات للعملاء. كلٌّ مُمثَّل
> بـ`AgentCard` في `auto_client_acquisition/agent_os/` ومُسجَّل في
> `agent_registry`. لا أجينت بلا هوية (البند ٩).

---

## 1. قاعدة الاستقلالية — Autonomy Rule

`AutonomyLevel`: `L0_READ_ONLY` · `L1_ANALYZE` · `L2_DRAFT` · `L3_RECOMMEND`
· `L4_AUTO_WITH_AUDIT` — والـ`L5` محجوب في الـMVP.

| نوع الأجينت | السقف | السبب |
|-------------|-------|-------|
| منسّق + مراحل داخلية آمنة (`A0`) | `L4` | تنفيذ ذاتي مع تدقيق كامل |
| أجينت يصوغ مخرجاً خارجياً | `L2` | يصوغ مسودّة فقط — لا يرسل |
| أجينت يقيّم/يحلّل | `L1` | لا يكتب مخرجاً |

كل أجينت بـ`L4` يلزمه `kill_switch_owner` مُسمّى في `AgentCard`.

---

## 2. الهرم — The Pyramid

```
Tier 0   revenue-conductor  (L4 — منسّق الحلقة)
            │
Tier 1   ┌──┴───────┬──────────────┬───────────────┐
       sales-     delivery-      growth-        governance-
       director   director       director       warden
       (L3)       (L3)           (L3)            (L1)
            │          │              │
Tier 2   عمّال متخصّصون (L0–L2) — كلٌّ بأداة واحدة ضيّقة
```

---

## 3. Tier 0 — المنسّق

| الأجينت | المستوى | الغرض | الأدوات المسموحة |
|---------|---------|-------|-------------------|
| `revenue-conductor` | `L4` | يملك `WorkflowRun`، يسلسل المراحل الـ12، يبثّ الأحداث، يوجّه للموافقة | `read, analyze, recommend, queue_for_approval` |

المنسّق لا يلمس الخارج إطلاقاً — يوجّه الإجراءات الخارجية إلى `approval_center`.

---

## 4. Tier 1 — مدراء المجالات

| الأجينت | المستوى | يملك المراحل | الغرض |
|---------|---------|--------------|-------|
| `sales-director` | `L3` | 1–8 | من الإشارة إلى بوابة الموافقة |
| `delivery-director` | `L3` | 9–10 | التسليم وإغلاق Proof Pack |
| `growth-director` | `L3` | 11–12 | التوسّع، التعلّم، محتوى السلطة |
| `governance-warden` | `L1` | شامل | يقيّم كل إجراء عبر `agent_governance.evaluate_action` قبل تنفيذه |

---

## 5. Tier 2 — العمّال المتخصّصون

| الأجينت | المستوى | الوحدة | الإجراء |
|---------|---------|--------|---------|
| `lead-intake-agent` | `L2` | `data_os.SourcePassport` | استقبال + Passport |
| `enrichment-agent` | `L1` | `revenue_os.enrichment_waterfall` | `enrichment_query` |
| `scoring-agent` | `L1` | `sales_os.icp_score`, `command_os` | `icp_match` |
| `pain-extraction-agent` | `L1` | محرّك `pain_extract` | `pain_extract` |
| `qualification-agent` | `L2` | `sales_os.qualification` | `qualification_questions` |
| `prioritization-agent` | `L1` | `revenue_pipeline.pipeline` | ترتيب داخلي |
| `draft-agent` | `L2` | `sales_os.proposal_renderer`, `revenue_os.draft_pack` | `proposal_generate_draft` |
| `followup-agent` | `L2` | `gtm_os` + `revenue_pipeline.stage_policy` | مسودّة متابعة |
| `proof-agent` | `L2` | `proof_os.assemble` | تجميع Proof Pack |
| `value-agent` | `L1` | `value_os.add_event` | تسجيل أحداث القيمة |
| `expansion-agent` | `L1` | `adoption_os.retainer_readiness` | جاهزية Retainer |
| `content-agent` | `L2` | `gtm_os.content_calendar` | مسودّة محتوى السلطة |
| `friction-agent` | `L1` | `friction_log.aggregate` | تجميع الاحتكاك |

لا أجينت في Tier 2 يتجاوز `L2` — أيٌّ منهم ينتج مسودّة على الأكثر، والإرسال
يبقى خلف بوابة الموافقة.

---

## 6. عقد الـ`AgentCard` — Identity Contract

كل أجينت يُسجَّل بـ:

```
agent_id, name, owner, purpose,
autonomy_level (≤ L4),
status (PROPOSED|ACTIVE|SUSPENDED|KILLED),
allowed_tools (من ALLOWED_TOOLS_MVP فقط),
kill_switch_owner (إلزامي إذا L4+)
```

الأدوات المحظورة (`send_email`, `send_whatsapp`, `web_scrape`,
`linkedin_automation`, `export_pii_bulk`) تُرفض عند التسجيل — لا يُمنح أيٌّ
منها لأي أجينت في هذا الهرم.

---

## 7. التسلسل التنفيذي — Execution Flow

1. `revenue-conductor` يفتح `WorkflowRun` ويبثّ `EventEnvelope` للمرحلة.
2. مدير المجال يستدعي عامل Tier 2 المناسب.
3. العامل ينتج `DecisionOutput` بفئات A/R/S.
4. `governance-warden` يقيّم: `A0` آمن → تنفيذ ذاتي؛ غير ذلك → `ApprovalTicket`.
5. كل خطوة تكتب `AuditEntry`؛ المنسّق ينتقل للمرحلة التالية.

البناء الفعلي لهذا الهرم على موجات — انظر [WAVE_PLAN.md](WAVE_PLAN.md).

---

*Version 1.0 | Every agent carries an AgentCard | External-facing agents cap at L2.*
