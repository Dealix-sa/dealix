# Dealix — حزمة الأدوات — Tool Stack
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> لا تشترِ أدوات كثيرة. ابنِ على مراحل. **لا تقفز مرحلة قبل أن تثبت
> السابقة.** لا بنية تحتية قبل أول دفعة.

---

## 1. مراحل حزمة التشغيل — The 4 Levels

### Level 1 — الآن (قبل أول Proof Pack)
Google Form · Google Sheet / Airtable · Apps Script · Manual WhatsApp
(warm only) · Manual email · Manual invoice · Sample Proof Pack ·
Daily Scorecard.

### Level 2 — بعد أول Proof Pack
Dealix API connected to Form · Auto-generated opportunity cards ·
Proof Pack draft generator · Dashboard · Partner sheet.

### Level 3 — بعد 3 Pilots
WhatsApp Cloud API (inbound only) · Opt-in registry · Customer portal
(basic) · Proof Pack generator · Partner dashboard.

### Level 4 — بعد 10 Pilots
CRM · Billing automation · Customer success automation · Revenue
analytics · Benchmark engine.

ترتبط بوابات البناء بـ
[`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md).

---

## 2. الأدوات حسب الوظيفة — Tools by Function

| الوظيفة | الآن | لاحقاً |
|---------|------|--------|
| CRM / Pipeline | Google Sheets · Airtable · Notion | HubSpot · Pipedrive · Attio |
| Automation | Apps Script · n8n · Make · Zapier | Prefect · Temporal · Celery / RQ |
| Agents / AI | OpenAI Agents SDK · LangGraph · Pydantic AI · LlamaIndex · MCP | — |
| Knowledge / RAG | Postgres + pgvector · Supabase · Qdrant | Weaviate |
| Observability | OpenTelemetry · Sentry · Langfuse / Phoenix | Prometheus + Grafana |
| Analytics | PostHog · Plausible · GA4 · Metabase | — |
| Content | Canva · Figma · Slides · Typefully · Buffer · Beehiiv | — |
| Billing | Moyasar (manual) · Bank transfer · PDF invoice | Moyasar automated · Stripe (global) |

استخدم CRM فقط لـ: lead status · next action · owner · stage · source ·
proof event.

---

## 3. حدود الأتمتة والوكلاء — Automation & Agent Boundaries

الوكلاء (agents) **مسموح** لهم بـ: lead scoring · message draft · meeting
brief · proof pack draft · support classification · objection
classification · weekly review draft.

الوكلاء **ممنوعون بلا approval** من: external send · invoice send ·
discount · refund · case study · security claim · affiliate payout.

n8n / Make / Zapier للتدفقات الداخلية فقط — لا إرسال خارجي بلا موافقة.
يحمي هذا `no_live_send` · `no_live_charge` · `no_unbounded_agents`.

---

## 4. الرصد — Observability

راقب: `agent_run_id` · `tool_call` · `approval_status` · `policy_result` ·
`latency` · `cost_estimate` · `error_type` · `proof_event`.

**لا تسجّل:** raw phone · raw email · secrets · unredacted PII.

---

## 5. المنع الآن — Hard No (today)

live charge · auto-billing · invoice without approved scope ·
live external send.

---

*Estimated outcomes are not guaranteed outcomes — النتائج التقديرية ليست
نتائج مضمونة.*
