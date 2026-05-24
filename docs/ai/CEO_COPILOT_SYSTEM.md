# CEO Copilot System — مساعد الرئيس التنفيذي

Status: v1
Owner: Founder
Approval class ceiling: A2 (drafts + analyses only)

## 1. Purpose — الغرض

The CEO Copilot is the founder's primary AI interface to run Dealix as a Saudi B2B Revenue Operating Company.
It composes context from every Dealix layer (intelligence, revenue, trust, finance, runtime) and produces drafts, summaries, decisions-to-make, and risk callouts.

مساعد الرئيس التنفيذي هو الواجهة الأساسية للمؤسس لإدارة Dealix.
يجمع السياق من كل طبقات Dealix وينتج مسوّدات، ملخصات، قرارات مطلوبة، وتنبيهات مخاطر.

## 2. What it CAN do — ما يستطيع

- Read the full internal state via the Control Plane API.
- Draft outreach, proposals, internal memos (A2).
- Produce a daily founder briefing (revenue, pipeline, agent runs, eval status, risks).
- Suggest next actions ranked by expected revenue impact and risk.
- Surface escalations from any agent in the swarm.
- Generate scorecards from worker output (no manual numbers).

## 3. What it CANNOT do — ما لا يستطيع

- Send anything externally.
- Publish proof, case studies, pricing, or any public content.
- Commit pricing, contract terms, payment terms, or revenue guarantees.
- Modify the agent registry or the policy file.
- Promote any agent or release.

All A3 actions are escalated to the founder with full evidence.

## 4. Inputs — المدخلات

- Control Plane summary (`GET /api/v1/internal/control/summary`)
- Active policies, agent registry, scorecards, risks
- Latest worker outputs (intelligence, outreach drafts, finance, trust)
- Founder's pinned objectives for the day/week
- Eval gate state

## 5. Outputs — المخرجات

| Output | Class | Destination |
|---|---|---|
| Founder daily briefing | A1 | `/opt/dealix-ops-private/runtime/briefings/` |
| Outreach drafts | A2 | `/opt/dealix-ops-private/outreach/drafts/` |
| Proposal drafts | A2 | `/opt/dealix-ops-private/outreach/proposals/` |
| Decision packs (A3 candidates) | A2 | `/opt/dealix-ops-private/approvals/queue/` |
| Risk callouts | A1 | `/opt/dealix-ops-private/trust/risks/` |

## 6. Loop — حلقة التشغيل

1. Pull state from Control Plane (read-only).
2. Compose context within token budget; redact `restricted` data.
3. Run candidate generation.
4. Pass every candidate through the Trust Guardian.
5. Persist only what the Guardian accepts; rejected items go to the audit log.
6. Surface the queue to the founder console.

## 7. Safety Rails — حواجز الأمان

- Hard cap: `approval_class_max: A2`.
- `external_action_allowed: false`.
- `kill_switch: flags.agents.ceo_copilot.enabled`.
- Eval suites required: `no_guaranteed_claims`, `prompt_injection`, `sensitive_data_leakage`, `approval_bypass`, `pricing_safety`, `contract_safety`, `payment_terms_safety`, `arabic_business_quality`.
- Audit: every prompt, every tool call, every output is logged.

## 8. Founder UX Contract — تجربة المؤسس

- One screen, one queue, one decision at a time.
- Each item carries: title, evidence, recommended action, risk class, and approve/reject/edit.
- No item disappears without an audit entry.
- Arabic-first; English mirrored where the audience demands.

## 9. Failure Modes — أنماط الفشل

- LLM unavailable => Copilot serves the last cached briefing and a "stale" banner. No silent failure.
- Policy file unparsable => Copilot refuses to run.
- Registry hash mismatch => Copilot refuses to run.
- Eval gate red => Copilot runs in read-only mode (no drafts produced).

## 10. References — مراجع

- `docs/ai/AGENT_REGISTRY_SYSTEM.md`
- `docs/ai/TRUST_GUARDIAN_AGENT.md`
- `docs/api/CONTROL_PLANE_API.md`
- `docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md`
