# Dealix — نظام المبيعات الذاتي · Autonomous Sales System

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `INTERNAL_OPS_AUTONOMY.md` · `AGENT_GOVERNANCE_AND_GUARDRAILS.md` · `../launch/MACHINE_ORCHESTRATION_MAP.md` · `../COMMERCIAL_WIRING_MAP.md`

---

## الغرض · Purpose

تصف هذه الوثيقة أقوى نظام مبيعات يمكن لـDealix تشغيله — منفّذًا بطريقة Dealix: الموافقة أولاً. تصمّم هذه الوثيقة المعمارية فقط؛ لا تأذن ببناء كود جديد. التجميد التجاري نشط.

This document describes the strongest sales system Dealix can run — executed the Dealix way: approval-first. This document designs architecture only; it does not authorize new product code. The Commercial Freeze is active.

---

## المعنى الدقيق لكلمة «ذاتي» · What "autonomous" means precisely

«المبيعات الذاتية» في Dealix تعني أن المكينة تنفّذ **100% من التحضير**: الاستقبال، التهديف، استخراج الألم، التأهيل، إعداد التشخيص، صياغة المقترح، صياغة اللمسات، تتبّع المتابعة، تجهيز الحجز. المؤسس يوافق على **كل فعل خارجي** (إرسال / تحصيل) قبل تنفيذه.

"Autonomous sales" at Dealix means the machine performs 100% of the preparation: intake, scoring, pain extraction, qualification, diagnostic prep, proposal drafting, touch drafting, follow-up tracking, booking prep. The founder approves every external action (send / charge) before it executes.

«مبيعات تلقائية بالكامل» تعني تحضيرًا تلقائيًا — **لا إرسالًا تلقائيًا أبدًا**. هذا هو الخندق الدفاعي (moat): لا `no_cold_whatsapp`، لا `no_live_send`، والتزام كامل بنظام حماية البيانات (PDPL).

"Fully automatic sales" means automatic preparation — never automatic sending. That is the moat: `no_cold_whatsapp` and `no_live_send` hold, and PDPL compliance is complete.

---

## القمع من البداية إلى النهاية · The funnel end-to-end

يغذّي دور `RoleName.GROWTH` و`GrowthOrchestrator` أعلى القمع (top-of-funnel) عبر وكلائه: `SectorIntelAgent`, `MarketResearchAgent`, `ContentCreatorAgent`, `DistributionAgent`, `CompetitorMonitorAgent`. يشرف دور `RoleName.SALES` على القمع من الاستقبال حتى تجهيز الحجز.

The `RoleName.GROWTH` role and `GrowthOrchestrator` feed top-of-funnel through its agents. The `RoleName.SALES` role supervises the funnel from intake to booking prep.

1. **الاستقبال · Intake** — `IntakeAgent` يستقبل الـlead، يتحقق من المصدر والموافقة عبر `data_os.SourcePassport`.
2. **تهديف الـICP · ICP scoring** — `ICPMatcherAgent` يستدعي `sales_os.icp_score`؛ وظيفة ARQ `lead_score` عبر `core/queue/tasks.py:run_agent_job()`.
3. **استخراج الألم · Pain extraction** — `PainExtractorAgent` يستخرج الألم المعلن من إشارات موثّقة فقط.
4. **التأهيل · Qualification** — `QualificationAgent` يستدعي `sales_os.qualify`.
5. **إعداد التشخيص · Diagnostic prep** — فعل `prepare_diagnostic` يُجهَّز كمسودة تشخيص.
6. **صياغة المقترح · Proposal draft** — `ProposalAgent` + وظيفة ARQ `proposal_draft` + `sales_os.build_proposal_skeleton` على عرض `revenue_proof_sprint_499` (499 SAR، السجل في [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md)).
7. **صياغة اللمسات · Outreach drafts** — `OutreachAgent` + وظيفة ARQ `outreach_batch` تنتج مسودات فقط.
8. **إيقاع المتابعة · Follow-up cadence** — `FollowUpAgent` يجدول مهام متابعة كمسودات.
9. **تجهيز الحجز · Booking prep** — `BookingAgent` يجهّز نص المكالمة وفتحات الوقت.

كل لمسة خارجية تصبح `ApprovalRequest` في `approval_center` عبر `ApprovalStore`: `draft_email` أو `draft_linkedin_manual` أو `call_script` أو `follow_up_task`. المكينة تُحضّر وتصفّ؛ المؤسس يوافق.

Every external touch becomes an `ApprovalRequest` in `approval_center` via `ApprovalStore`: `draft_email`, `draft_linkedin_manual`, `call_script`, or `follow_up_task`. The machine prepares and queues; the founder approves.

---

## جدول القمع · Funnel table

| المرحلة · Stage | الوكيل · Agent | مستوى الاستقلالية · Autonomy | المخرج · Output | فعل الموافقة · Approval action_type |
|---|---|---|---|---|
| الاستقبال · Intake | `IntakeAgent` | L1_ANALYZE | lead موثّق المصدر · source-stamped lead | — (داخلي · internal) |
| تهديف ICP · ICP scoring | `ICPMatcherAgent` | L1_ANALYZE | درجة `icp_score` · ICP score | — (داخلي · internal) |
| استخراج الألم · Pain extraction | `PainExtractorAgent` | L1_ANALYZE | ملف ألم · pain profile | — (داخلي · internal) |
| التأهيل · Qualification | `QualificationAgent` | L3_RECOMMEND | توصية تأهيل · qualification verdict | — (داخلي · internal) |
| إعداد التشخيص · Diagnostic prep | `IntakeAgent` / `QualificationAgent` | L2_DRAFT | مسودة تشخيص · diagnostic draft | `prepare_diagnostic` |
| صياغة المقترح · Proposal draft | `ProposalAgent` | L2_DRAFT | هيكل مقترح 499 SAR · 499 SAR proposal skeleton | `upsell_recommendation` (للترقية · for upgrade) |
| صياغة البريد · Email draft | `OutreachAgent` | L2_DRAFT | مسودة بريد · email draft | `draft_email` |
| صياغة LinkedIn · LinkedIn draft | `OutreachAgent` | L2_DRAFT | مسودة LinkedIn يدوية · manual LinkedIn draft | `draft_linkedin_manual` |
| نص المكالمة · Call script | `BookingAgent` | L2_DRAFT | نص مكالمة · call script | `call_script` |
| المتابعة · Follow-up | `FollowUpAgent` | L2_DRAFT | مهمة متابعة · follow-up task | `follow_up_task` |
| تجهيز الحجز · Booking prep | `BookingAgent` | L3_RECOMMEND | فتحات + تأكيد · slots + confirmation | `follow_up_task` |

سقف الاستقلالية للمبيعات هو L3_RECOMMEND؛ لا وكيل مبيعات يبلغ L4 أو L5. راجع [`AGENT_GOVERNANCE_AND_GUARDRAILS.md`](AGENT_GOVERNANCE_AND_GUARDRAILS.md).

The sales autonomy cap is L3_RECOMMEND; no sales agent reaches L4 or L5. See [`AGENT_GOVERNANCE_AND_GUARDRAILS.md`](AGENT_GOVERNANCE_AND_GUARDRAILS.md).

---

## ما لا يفعله النظام أبدًا · What the system never does

- لا إرسال خارجي تلقائي — كل بريد / LinkedIn / مكالمة يحتاج موافقة صريحة في كل مرة (`no_live_send`).
- لا WhatsApp بارد ولا DM جماعي ولا أتمتة تواصل بارد (`no_cold_whatsapp`).
- لا scraping؛ كل lead يحمل `SourcePassport` بموافقة (`no_scraping`, `no_unconsented_data`).
- لا وعد بأرقام مبيعات أو نسب تحويل كحقيقة — كل قيمة موسومة بأحد تيرات `value_os`: `estimated` · `observed` · `verified` · `client_confirmed`.

No automatic external sending; every email / LinkedIn / call needs explicit approval each time. No cold WhatsApp, no mass DMs, no cold-outreach automation. No scraping; every lead carries a consented `SourcePassport`. No promised sales figures or conversion rates as fact.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
