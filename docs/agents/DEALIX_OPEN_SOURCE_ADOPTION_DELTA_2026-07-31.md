# Dealix Open-Source Adoption Delta — 2026-07-31

## Executive decision

Dealix should not absorb another CRM, agent company, workflow runtime, vector database, or web-crawling platform into its core.

The repository already has Company Brain, Opportunity/Deal Intelligence, Strategy/Safety, Approval, Proof, model-routing, observability, and commercial execution surfaces. The highest-value path is to adopt narrowly bounded components or patterns behind existing Dealix contracts.

This review extends:

- `docs/agents/DEALIX_AGENTIC_OS_ADOPTION_MATRIX.md`;
- `dealix/registers/tool_intake_july_2026.json`;
- Issue #1012, the first focused Company Intelligence Spine slice;
- Draft PR #1011, the executive market-truth and sequencing control.

No dependency is approved for production merely by appearing in this document.

## Decision rules

Every candidate must pass:

1. **Gap proof** — identify a measured Dealix gap that existing code cannot safely solve.
2. **License gate** — record repository license, restricted directories, model licenses, and redistribution implications.
3. **Security gate** — isolate network access, credentials, customer data, callbacks, and tool authority.
4. **Tenant gate** — prove tenant ownership, isolation, retention, deletion, and auditability.
5. **Operational gate** — define health checks, retries, idempotency, rollback, cost ceiling, and failure behavior.
6. **Commercial gate** — show revenue, delivery, quality, or founder-time benefit.
7. **Exit gate** — adapters must be removable without replacing canonical Dealix entities.

## Adoption matrix

| Candidate | Decision | Dealix use | Why | Required gates |
|---|---|---|---|---|
| LiteLLM | **Pilot as optional gateway adapter** | Provider-neutral model access, budgets, fallbacks, cost records | Supports many providers and OpenAI-compatible routing, but Dealix already has a Model Router | Pin version; feature flag off; no second routing policy; tenant budgets; secret redaction; latency/cost benchmark; OSS/enterprise directory review |
| Langfuse | **Adopt by hardening existing integration** | Tracing, evals, prompt/model lineage, cost and quality evidence | Dealix already contains two Langfuse integration surfaces; adding Phoenix or another platform would duplicate observability | Select one canonical adapter; redact before egress; explicit retention; tenant tags; async failure must not block business flow; no EE assumptions |
| Activepieces | **Connector-only pilot** | Optional customer-owned workflow execution and human approval bridges | Provides self-hosting, approvals, forms, versioned flows and many integrations, but embedding it as Dealix core would duplicate Action/Approval/Execution | Isolated sandbox; customer-owned OAuth; no direct production DB; signed webhook contract; idempotency; egress allowlist; review EE directory/license boundaries |
| Firecrawl | **Connector-only / legal hold for embedded core** | Public-site research and normalized extraction where terms permit | Strong extraction and self-hosting, but primary server license is AGPL-3.0 and crawling creates terms/privacy risk | Legal review; robots/terms policy; domain allowlist; public data only; provenance; rate limits; data minimization; no resale/embedding until AGPL obligations are accepted |
| Docling | **Pilot now for private document intelligence** | Parse PDFs, DOCX, PPTX, XLSX, emails and images into a unified document representation | MIT-licensed, local-capable, directly useful for proposals, meeting packs, company knowledge and due diligence | Model-license review; malicious-document sandbox; file-size/page limits; no macros; PII classification; deterministic export tests; benchmark against current parsers |
| Temporal Python SDK | **Pattern-only until a real durability failure exists** | Durable approval waits, long-running onboarding, delivery and proposal workflows | Strong durable execution and deterministic workflow semantics, but introduces major infrastructure and a second runtime | Demonstrated restart/resume failure; operational owner; migration/rollback plan; deterministic workflow design; cost and deployment benchmark |
| Twenty CRM | **Pattern-only; reject as Dealix core** | UX and extensible-object inspiration; optional external CRM connector later | A full CRM would compete with Dealix's overlay positioning and duplicate companies, contacts, deals, workflows and agents | Do not fork/embed; connector contract only after a paying client uses Twenty; map IDs and consent without duplicating source of truth |
| Qdrant | **Hold** | High-scale semantic search only if PostgreSQL/pgvector becomes insufficient | Apache-2.0 and capable, but another database increases tenancy, backup, security and operations cost | Measured pgvector limitation; scale benchmark; tenant filtering proof; backup/restore; deletion propagation; migration and rollback |
| Playwright MCP / deterministic Playwright | **Pilot MCP only in isolated QA; retain Playwright as default** | Preview QA, accessibility, evidence screenshots and route validation | Browser agents are useful for QA but carry ambient-authority and prompt-injection risks | Disposable profile; read-only preview domains; no founder/customer sessions; no credentials; snapshots sanitized; deterministic tests remain authoritative |
| FastMCP | **Security-bounded pilot** | MCP gateway prototypes for approved tools | Useful for standardized tools, but recent security hardening shows host/origin/SSRF configuration must be explicit | Trusted host/origin allowlists; SSRF and DNS-rebinding tests; no production DB; tool manifest review; per-tool scopes; audit and approval |

## Immediate implementation queue

### P0 — Canonical Langfuse integration

Current repository evidence shows:

- `core/observability/langfuse_integration.py`;
- `auto_client_acquisition/observability_adapters/langfuse_adapter.py`;
- observability and eval documentation.

Required action:

1. Select one canonical integration owner.
2. Add a compatibility adapter for the other path.
3. Add a redaction contract before network export.
4. Attach `tenant_id`, `run_id`, strategy, action, approval, proof and model-route lineage.
5. Add tests proving observability failure is non-blocking and secret values are never recorded.

### P0 — Docling private-document pilot

Use one synthetic and one public document pack only.

Acceptance path:

```text
input file
→ malware/type/size gate
→ Docling parse
→ normalized Dealix document record
→ provenance and page references
→ Company Brain candidate facts
→ human review
→ approved knowledge record
```

Required outputs:

- parse-quality benchmark;
- table and reading-order comparison;
- runtime and memory measurements;
- rejected-file report;
- zero customer data committed to Git.

### P1 — LiteLLM adapter benchmark

Do not install a proxy first. Begin with an isolated adapter benchmark against the current Model Router.

Evaluate:

- local Qwen/Ollama;
- current hosted route;
- one premium provider;
- Arabic sales/proposal quality;
- structured-output validity;
- latency;
- cost;
- fallback behavior;
- tenant budget enforcement.

Adopt only if the adapter reduces provider-specific code or materially improves cost/failure handling.

### P1 — Activepieces approval bridge proof

Build no customer workflow yet.

First prove a synthetic loop:

```text
Dealix Action
→ signed outbound request
→ Activepieces approval/form step
→ signed callback
→ Dealix Approval event
→ idempotent resume
→ Proof event
```

The Dealix Approval ledger remains authoritative. Activepieces is an execution bridge, not the source of truth.

### P1 — Public research connector contract

Before Firecrawl or any crawler:

```text
source_name
source_url
retrieved_at
retrieval_method
terms_or_license_note
robots_state
confidence
content_hash
sensitive_data_status
tenant_id
retention_until
```

No contact is marked reachable or consented merely because it appears on a public page.

## Explicit rejections and holds

Do not:

- import Twenty as the Dealix application shell;
- run Activepieces or n8n as a second canonical scheduler;
- install Temporal before a measured durability failure;
- add Qdrant while PostgreSQL/pgvector is unbenchmarked;
- deploy Firecrawl as an unrestricted crawler;
- add Phoenix while Langfuse is the selected observability slot;
- expose browser-agent control to logged-in founder or customer profiles;
- grant an MCP server production credentials by default;
- let external tools create revenue, consent, payment or proof truth outside Dealix ledgers.

## Repository architecture boundary

External tools may implement adapters for this lifecycle only:

```text
Company Brain
→ Sources and Consent
→ Company / Contact / Signal Graph
→ Opportunity / Partnership
→ Department Plan
→ Action
→ Draft
→ Approval
→ Controlled Execution
→ Outcome
→ Finance / Delivery / Proof
→ Learning
→ Daily Command
```

Canonical entity ownership remains inside Dealix.

## Verification checklist

For every pilot:

- [ ] exact version/commit pinned;
- [ ] license and restricted directories reviewed;
- [ ] SBOM and vulnerability scan recorded;
- [ ] feature flag defaults off;
- [ ] synthetic/public data only;
- [ ] no external send or production mutation;
- [ ] tenant isolation test;
- [ ] provenance and retention fields present;
- [ ] secrets redacted;
- [ ] timeout/retry/idempotency tests;
- [ ] cost and resource ceiling;
- [ ] removal/rollback test;
- [ ] proof artifact attached to a focused Draft PR.

## Recommended execution order

1. Complete #1012 consolidation and entity ownership map.
2. Harden the existing Langfuse path instead of adding another observability platform.
3. Pilot Docling locally for Company Brain document ingestion.
4. Benchmark LiteLLM behind the existing Model Router.
5. Prove an Activepieces synthetic approval bridge.
6. Add a public-research connector only after source/terms/retention contracts are executable.
7. Reconsider durable workflow or vector infrastructure only after measured failures.

## Sources reviewed

Official project repositories and license files:

- `langfuse/langfuse` — observability/evals; MIT core with restricted EE directories.
- `BerriAI/litellm` — unified model gateway; MIT core with enterprise directory restrictions.
- `activepieces/activepieces` — workflow automation and human approval; MIT core with EE directories.
- `mendableai/firecrawl` — extraction/search; primarily AGPL-3.0, with separately licensed SDK/components.
- `docling-project/docling` — document processing; MIT, with separate model-license considerations.
- `temporalio/sdk-python` — durable workflow SDK; MIT.
- `twentyhq/twenty` — extensible open CRM; use as pattern/connector, not core.
- `qdrant/qdrant` — vector database; Apache-2.0.

Research date: 2026-07-31.
