# Dealix Control Plane — لوحة تحكم Dealix

Status: v1
Owner: Founder

## 1. Purpose — الغرض

The Control Plane is the layer that makes Dealix observable, governable, and operable from one place. It is the source of truth for "what is the company doing right now?"

لوحة التحكم هي الطبقة التي تجعل Dealix قابلة للرصد والحوكمة والتشغيل من مكان واحد. هي المرجع الوحيد للإجابة عن "ماذا تفعل الشركة الآن؟".

## 2. Components — المكونات

1. Control Plane API — read APIs at `/api/v1/internal/control/*`.
2. Founder Console — single screen UI on top of the API.
3. Approvals Queue — the place where the Trust Guardian's outputs meet the founder.
4. Audit Log — append-only ledger of every meaningful action.
5. Scorecard — maturity, DORA, AI cost, audit completeness, worker freshness.
6. Risk Register — open risks with owners and severities.
7. Kill Switch Board — per-agent, per-swarm, per-worker, per-provider switches.

## 3. Operating Loop — حلقة التشغيل

1. Workers produce artifacts.
2. Agents draft outputs from those artifacts.
3. Trust Guardian gates outputs.
4. Approvals Queue surfaces gated items.
5. Founder approves or rejects.
6. Audit Log records every step.
7. Scorecard updates.
8. Founder Console reflects everything in near real time.

## 4. Sources of Truth — مراجع الحقيقة

| Truth | Source |
|---|---|
| Policy | `policies/dealix_control_policy.yaml` |
| Agents | `registries/agent_registry.yaml` |
| Eval Gate | `evals/gates/dealix_agent_eval_gate.yaml` |
| Audit | append-only audit store |
| State | Postgres `control` schema + materialized views |
| Runtime | Worker mesh heartbeats |

The Control Plane API joins these into a single, redacted view for the console.

## 5. What the Control Plane Does NOT Do — ما لا تفعله

- It does not send anything externally.
- It does not allow A3 approvals from anyone other than the founder.
- It does not modify policy or registry; those are PR-only.
- It does not bypass the Guardian.
- It does not store secrets; secrets live in the managed store.

## 6. Operating Modes — أوضاع التشغيل

| Mode | Trigger | Effect |
|---|---|---|
| Normal | All systems green | Full read, normal approvals |
| Read-only | Eval gate red OR Guardian disabled | No A2/A3 approvals possible |
| Maintenance | Founder-set | Banner; reads only |
| Incident | P0 active | Banner; approvals paused; audit emphasized |

## 7. Founder Drills — تمارين المؤسس

A monthly drill exercises:
- Tripping a kill switch and verifying the agent stops in <1s.
- Filtering audit by class and verifying integrity.
- Approving and rejecting a sample A2 with full evidence.
- Triggering a fake P1 and walking through incident response.
- Verifying scorecard reflects the drill in DORA.

## 8. Non-Negotiables — خطوط حمراء

- The Control Plane never lies; staleness is always labeled.
- Every mutation is audited.
- Every metric has a source.
- A3 actions are founder-only.
- No external sending. No exceptions.

## 9. References — مراجع

- `docs/api/CONTROL_PLANE_API.md`
- `docs/api/ULTIMATE_INTERNAL_API.md`
- `docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md`
- `docs/ai/TRUST_GUARDIAN_AGENT.md`
