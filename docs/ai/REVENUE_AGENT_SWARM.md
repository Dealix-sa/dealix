# Revenue Agent Swarm — سرب وكلاء الإيراد

Status: v1
Owner: Founder
Approval class ceiling per agent: A2 maximum, A3 escalated to founder.

## 1. Purpose — الغرض

The Revenue Agent Swarm runs the Dealix revenue loop end-to-end as drafts and queues.
No external sends. No public proof. No pricing or contract commitments.
Founder approves every outbound action.

سرب وكلاء الإيراد يدير حلقة الإيراد كاملةً كمسوّدات وقوائم انتظار.
لا إرسال خارجي. لا نشر إثبات. لا التزامات أسعار أو عقود.
المؤسس يوافق على كل خطوة خارجية.

## 2. Roster — قائمة الوكلاء

| Agent ID | Role | Class Max | External? |
|---|---|---|---|
| `icp_intelligence_collector` | Pulls open/licensed signals on Saudi B2B targets | A1 | no |
| `account_qualifier` | Scores accounts vs ICP rubric | A1 | no |
| `revenue_outreach_drafter` | Drafts AR+EN first-touch and follow-up messages | A2 | no |
| `meeting_brief_writer` | Pre-meeting briefs from internal evidence only | A1 | no |
| `proposal_drafter` | Drafts proposals (no pricing commitment, no guarantee) | A2 | no |
| `objection_handler_advisor` | Suggests responses to common objections | A2 | no |
| `pilot_scorecard_compiler` | Compiles pilot outcomes from worker output | A1 | no |
| `proof_candidate_curator` | Selects candidate proofs; never publishes | A2 | no |
| `pricing_analyst` | Analyzes margin/CAC scenarios; flags as A3 | A2 (output marked A3) | no |
| `renewal_signal_watcher` | Flags renewal risk and expansion opportunities | A1 | no |

All entries live in `registries/agent_registry.yaml` with full schema.

## 3. Loop — حلقة العمل

1. Intelligence — collect, normalize, store under `intelligence/`.
2. Qualify — score, deduplicate, persist under `intelligence/qualified/`.
3. Draft — generate outreach drafts; Guardian gate; queue under `outreach/drafts/`.
4. Approve — founder reviews in console; approves or rejects.
5. Execute — founder sends manually (no agent egress).
6. Capture — outcomes recorded; pilot scorecards compiled.
7. Curate — proof candidates surfaced; founder decides publication.

## 4. Non-Negotiables — خطوط حمراء

- No agent in the swarm has `external_action_allowed: true`.
- No agent may write a numeric revenue guarantee, ROI promise, or SLA the company has not signed.
- No agent may state pricing as committed; pricing artifacts are always marked "proposed — requires founder approval".
- No agent may write contract or payment language. Those drafts are A3 only and require legal review.
- All Arabic copy must pass `arabic_business_quality` eval.
- All drafts must pass `no_guaranteed_claims`, `pricing_safety`, `contract_safety`, `payment_terms_safety`.

## 5. Data Boundaries — حدود البيانات

- The swarm reads from `internal` and `confidential` tiers only.
- `restricted` (customer PII at full fidelity, payment data) is off-limits to swarm prompts.
- All outputs are written under `/opt/dealix-ops-private/` per the Private Ops Runtime Contract.

## 6. Observability — الرصد

Every run emits:
- `agent_id`, `run_id`, `prompt_hash`, `tool_calls[]`, `output_hash`, `class`, `policy_decision`.
- Cost in tokens and currency.
- Eval state at time of run.

Surfaced via `GET /api/v1/internal/control/agents` and the founder console.

## 7. Kill Switches — قواطع الإيقاف

Per-agent flags under `flags.agents.<id>.enabled`.
Swarm-wide flag: `flags.swarms.revenue.enabled`.
Flip-off propagates in under one second; in-flight runs are aborted and audited.

## 8. References — مراجع

- `docs/ai/AGENT_REGISTRY_SYSTEM.md`
- `docs/ai/TRUST_GUARDIAN_AGENT.md`
- `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`
- `docs/evals/EVAL_GATE_V1.md`
