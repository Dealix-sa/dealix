# Trust Guardian Agent — وكيل حارس الثقة

Status: v1 (binding, fail-closed)
Owner: Founder
Role: Last gate before any artifact, draft, or action is persisted or surfaced.

## 1. Purpose — الغرض

The Trust Guardian is a non-bypassable safety layer between every other agent and the world.
It enforces Dealix's non-negotiables, the policy file, and the approval class system.

حارس الثقة طبقة أمان لا يمكن تجاوزها بين كل وكيل آخر وبين العالم.
يفرض الخطوط الحمراء، ملف السياسة، ونظام فئات الموافقة.

## 2. What it gates — ما يتم تمريره عبره

- Every agent output before it is written to disk or DB.
- Every queued external action before it appears in the founder approvals queue.
- Every classification decision (A1/A2/A3) — Guardian may upgrade class, never downgrade.
- Every policy lookup result before it is consumed.

## 3. Checks — الفحوصات

### 3.1 Content Checks
- No guaranteed revenue, ROI, conversion, or growth claims.
- No pricing commitment language.
- No contract or payment term commitments.
- No proof publication without explicit approval token.
- No PII at restricted tier in any prompt or output.
- Arabic copy passes business quality threshold.
- Prompt-injection markers stripped or quarantined.

### 3.2 Structural Checks
- Output type matches the agent's `outputs` declaration.
- Write target matches `allowed_write_targets` globs.
- Class on output is <= agent's `approval_class_max`.
- Tool calls were all within the agent's `tools` allowlist.
- `external_action_allowed` was honored.

### 3.3 Policy-as-Code Checks
- Loads `policies/dealix_control_policy.yaml`.
- Evaluates every rule for the given (agent, output, target) tuple.
- Fail-closed on any unknown rule outcome.

## 4. Outputs of the Guardian — مخرجات الحارس

For each item, the Guardian emits one of:

- `ACCEPT` — proceed, log decision.
- `ACCEPT_WITH_UPGRADE` — class raised (e.g. A2 -> A3); requires founder approval.
- `REJECT` — item dropped, full reason logged, calling agent notified.
- `QUARANTINE` — item written to `/opt/dealix-ops-private/trust/quarantine/` for review.

Guardian decisions are themselves logged immutably (append-only).

## 5. Non-Negotiables — خطوط حمراء

- The Guardian cannot be disabled by any other agent.
- The Guardian's kill switch is owner-only and requires a written reason in the audit log.
- A Guardian failure (crash, timeout) blocks all dependent agent writes. No silent pass-through.
- The Guardian's own evals (`approval_bypass`, `prompt_injection`, `tool_misuse`) must pass on every release.

## 6. Eval Suites It Powers — حزم التقييم

The Guardian is the runtime enforcer; the eval gate is the offline enforcer. Both must agree.

Suites: `no_guaranteed_claims`, `approval_bypass`, `prompt_injection`, `sensitive_data_leakage`,
`suppression_compliance`, `evidence_required`, `proposal_safety`, `tool_misuse`, `A3_escalation`,
`proof_safety`, `pricing_safety`, `data_export_safety`, `contract_safety`, `payment_terms_safety`.

## 7. NIST AI RMF Mapping — ربط NIST

- Govern — Guardian is the policy enforcement point; policy is version-controlled.
- Map — every gated item carries agent, purpose, data tier, risk tags.
- Measure — Guardian metrics feed the scorecard (reject rate, upgrade rate, quarantine rate).
- Manage — kill switches, quarantines, escalations, rollbacks are first-class operations.

## 8. Performance — الأداء

- p50 latency budget: 250 ms per item.
- p99 budget: 1.5 s.
- Throughput target: 100 items/s sustained.
- Backpressure: if the queue exceeds threshold, the swarm pauses; no item is skipped.

## 9. References — مراجع

- `policies/dealix_control_policy.yaml`
- `evals/gates/dealix_agent_eval_gate.yaml`
- `docs/ai/AGENT_REGISTRY_SYSTEM.md`
- `docs/evals/EVAL_GATE_V1.md`
