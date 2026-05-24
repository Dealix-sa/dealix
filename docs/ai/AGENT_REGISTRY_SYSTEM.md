# Agent Registry System — نظام سجل الوكلاء

Status: v1 (binding)
Owner: Founder + Trust Guardian
Location: `registries/agent_registry.yaml`

## 1. Purpose — الغرض

The Agent Registry is the single source of truth for every AI agent that runs inside Dealix.
No agent may execute work in any environment unless it is registered, eval-passed, and policy-bound.

سجل الوكلاء هو المرجع الوحيد لأي وكيل ذكاء اصطناعي يعمل داخل Dealix.
لا يُسمح بأي وكيل دون تسجيل، اختبار، وضوابط سياسة.

## 2. Required Schema — البنية المطلوبة

Every entry MUST include the fields below. Missing fields => the registry loader refuses to start.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string (snake_case) | yes | Globally unique agent identifier |
| `name` | string | yes | Human readable name (AR/EN) |
| `purpose` | string | yes | One-sentence reason this agent exists |
| `approval_class_max` | enum `A1|A2|A3` | yes | Maximum class this agent may produce. Never auto-bypassed |
| `tools` | list[string] | yes | Allowlist of tool names (from `registries/tools.yaml`) |
| `outputs` | list[string] | yes | Artifact types this agent may write |
| `external_action_allowed` | bool | yes | If `false`, no network egress, no send, draft-only |
| `kill_switch` | string | yes | Path to feature flag that disables this agent in <1s |
| `eval_required` | list[string] | yes | Eval suite IDs that gate any release of this agent |
| `owner` | string (email) | yes | Accountable human |
| `audit_required` | bool | yes | If `true`, every run is logged to immutable audit trail |
| `data_access_level` | enum `public|internal|confidential|restricted` | yes | Highest data tier this agent may read |
| `allowed_write_targets` | list[path glob] | yes | The only filesystem/DB locations this agent may write to |

## 3. Approval Classes — فئات الموافقة

- A1 — Auto Safe. Drafts, internal summaries, scorecards. No external side effects.
- A2 — Founder Approval. Outreach drafts, proposal drafts, proof candidates, pricing analyses.
- A3 — Escalation. Contract terms, payment terms, regulated communications. NEVER auto.

`approval_class_max` is enforced at write time by the Trust Guardian. An agent that attempts to emit above its class is killed and audited.

## 4. Lifecycle — دورة الحياة

1. Proposal — author drafts entry + eval suite design.
2. Eval — every suite in `eval_required` must pass at the threshold in `evals/gates/dealix_agent_eval_gate.yaml`.
3. Registration — entry is merged into `registries/agent_registry.yaml`.
4. Activation — kill switch flipped on; first runs go to shadow mode.
5. Promotion — after N shadow runs with zero policy violations, agent is promoted to live (drafts only).
6. Retirement — kill switch flipped off; entry kept for audit; runs blocked.

## 5. Loader Contract — عقد المُحمِّل

The loader (`src/dealix/agents/registry.py`) MUST:

- Fail closed: if YAML is unparsable or any required field is missing, no agent starts.
- Verify each `tools` entry exists in the tool allowlist.
- Verify each `allowed_write_targets` glob resolves under approved roots.
- Verify each `eval_required` suite exists and passed within the last release.
- Emit a hash of the registry to the audit log on every boot.

## 6. Non-Negotiables — خطوط حمراء

- No agent may have `external_action_allowed: true` without explicit founder sign-off recorded in the registry diff.
- No agent may carry `approval_class_max: A3` and `audit_required: false` — that combination is invalid.
- No agent may write outside `allowed_write_targets`. Any attempt is a P0 incident.
- The registry is policy-as-code. Changes go through PR review with the Trust Guardian as required reviewer.

## 7. Example Entry — مثال

```yaml
- id: revenue_outreach_drafter
  name: "Revenue Outreach Drafter — مُحرِّر الرسائل"
  purpose: "Draft Arabic+English first-touch messages for qualified ICP accounts."
  approval_class_max: A2
  tools: [icp_lookup, message_template, language_qc]
  outputs: [outreach_draft]
  external_action_allowed: false
  kill_switch: flags.agents.revenue_outreach_drafter.enabled
  eval_required:
    - no_guaranteed_claims
    - prompt_injection
    - arabic_business_quality
    - approval_bypass
  owner: founder@dealix.sa
  audit_required: true
  data_access_level: internal
  allowed_write_targets:
    - /opt/dealix-ops-private/outreach/drafts/**
```

## 8. References — مراجع

- `policies/dealix_control_policy.yaml`
- `evals/gates/dealix_agent_eval_gate.yaml`
- `docs/ai/TRUST_GUARDIAN_AGENT.md`
- `docs/ai/EVAL_RED_TEAM_SYSTEM.md`
