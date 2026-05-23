# AI-Native Company Architecture — هندسة الشركة الذكية

Status: v1
Owner: Founder

## 1. Premise — المنطلق

Dealix is built as 18 horizontal layers. Every product surface, every workflow, every audit trail crosses these layers. Each layer has an owner, a contract, and a kill switch.

تُبنى Dealix من 18 طبقة أفقية. كل سطح منتج وكل تدفق وكل مسار تدقيق يعبر هذه الطبقات. لكل طبقة مالك وعقد وقاطع إيقاف.

## 2. The 18 Layers — الطبقات الثمانية عشرة

### L1 — Identity and Brand Layer
Public identity, name, design system, bilingual voice.

### L2 — Legal and Compliance Layer
PDPL, ZATCA, ToS, Privacy, DPA, refund policy, cross-border addenda.

### L3 — Data Sovereignty Layer
Data classification (public/internal/confidential/restricted), residency, retention, DSR pipeline.

### L4 — Storage Layer
CSV shadow, Postgres primary, warehouse — see Data Platform doc.

### L5 — Identity and AuthN/AuthZ Layer
Founder identity, internal service identity, per-agent identity, scoped tokens.

### L6 — Policy-as-Code Layer
`policies/dealix_control_policy.yaml` plus loaders. Single source of behavioral rules.

### L7 — Agent Registry Layer
`registries/agent_registry.yaml`. Every agent declared with schema.

### L8 — LLM Gateway Layer
Provider-agnostic routing, key isolation, cost accounting, fallback paths.

### L9 — Tool Layer
Allowlisted tools with typed signatures; per-agent allowlist.

### L10 — Agent Runtime Layer
Sandboxed execution of agents; in-process gates; tool-call mediation.

### L11 — Trust Guardian Layer
Non-bypassable gate; class enforcement; quarantine and reject paths.

### L12 — Eval and Red-Team Layer
Suites, gates, regression corpus, human grading.

### L13 — Workflow and Orchestration Layer
Worker mesh + scheduler. Heartbeats, freshness SLOs, retries.

### L14 — Approvals Layer
Queues per class; founder console; immutable decisions.

### L15 — Audit Layer
Append-only log of every prompt, tool call, gate decision, approval, write.

### L16 — Observability Layer
DORA + AI cost + audit completeness + worker freshness. Metrics, traces, dashboards.

### L17 — Control Plane Layer
Internal APIs that surface state to the founder console. Auth-gated.

### L18 — Founder Console Layer
Single-screen, single-queue UX that drives the company.

## 3. Cross-Cutting Contracts — عقود مستعرضة

- Every write specifies layer, owner, class, audit_required.
- Every external action passes L11 (Guardian) before it is queued in L14.
- Every release passes L12 (Eval Gate) before L7 (Registry) accepts the change.
- Every API at L17 requires the Internal API Auth Gate.

## 4. Kill Switches — قواطع الإيقاف

| Scope | Flag | Effect |
|---|---|---|
| Single agent | `flags.agents.<id>.enabled` | Stop one agent |
| Swarm | `flags.swarms.<id>.enabled` | Stop a swarm |
| LLM provider | `flags.llm.<provider>.enabled` | Route away from provider |
| Worker | `flags.workers.<id>.enabled` | Stop a worker |
| Guardian | `flags.guardian.enabled` | Founder-only; blocks all writes |
| Control plane | `flags.control_plane.enabled` | Read-only mode |

## 5. Data Flow — تدفق البيانات

CSV ingest -> shadow Postgres -> primary Postgres -> warehouse.
Agent outputs -> /opt/dealix-ops-private/<domain>/ -> Postgres if approved -> warehouse.

## 6. Failure Posture — موقف الفشل

- Fail closed at every gate.
- Stale data is shown with a "stale" banner; nothing fakes freshness.
- Missing eval results block release.
- Missing policy file blocks runtime.

## 7. Mapping to NIST AI RMF — ربط NIST

- Govern — L2, L6, L7.
- Map — L3, L7, L9.
- Measure — L12, L15, L16.
- Manage — L11, L13, L14, L17, L18.

## 8. References — مراجع

- `docs/architecture/ULTIMATE_ARCHITECTURE_MAP.md`
- `docs/data/ULTIMATE_DATA_PLATFORM.md`
- `docs/runtime/ULTIMATE_WORKER_MESH.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
