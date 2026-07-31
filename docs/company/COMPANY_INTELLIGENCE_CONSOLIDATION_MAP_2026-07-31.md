# Company Intelligence Consolidation Map — 2026-07-31

## Purpose

Translate the canonical entity registry in PR #1014 into a verified retain/adapt/deprecate map against the current repository. This file records ownership decisions only where a concrete path exists on `main@aae97bcefcf73e74aef8c75ac593238dc1ed690e`.

This is a consolidation control, not authorization to delete, migrate, merge, deploy, or change production.

## Decision labels

- **RETAIN** — canonical implementation or public boundary that should remain.
- **ADAPT** — useful implementation that must conform to the canonical entity contract.
- **COMPATIBILITY** — temporary adapter for existing callers; not a second source of truth.
- **UI ONLY** — presentation surface; never owns business truth.
- **DEPRECATE LATER** — candidate for removal only after caller inventory, adapter coverage, tests, and explicit deletion approval.
- **HOLD** — insufficient evidence; do not create a replacement.

## Verified CompanyBrain surfaces

| Path | Current role | Decision | Required next action |
|---|---|---|---|
| `auto_client_acquisition/company_brain/brain.py` | Defensive, read-only internal Dealix snapshot composed from shipped signals; no LLM/network | **RETAIN as internal snapshot adapter** | Keep no-crash behavior; expose through the canonical `CompanyBrain` contract; do not make this the full per-tenant commercial record |
| `auto_client_acquisition/company_brain_v6/schemas.py` | Per-customer schema boundary used by the V6 builder | **ADAPT toward canonical CompanyBrain schema** | Map fields to CompanyBrain, Offer, Persona, Source/Evidence, restrictions, and next-action references; keep version adapter until callers migrate |
| `auto_client_acquisition/company_brain_v6/builder.py` | Pure per-customer composition; enforces forbidden channels and computes service/risk/next action | **RETAIN logic, ADAPT ownership** | Separate entity construction from recommendation outputs; emit canonical IDs and provenance; preserve forbidden-channel enforcement |
| `auto_client_acquisition/company_brain_v6/` | Versioned implementation package | **COMPATIBILITY** | Do not create V7. Introduce a canonical facade and route V6 callers through it before deprecation |
| `api/routers/company_brain.py` | API presentation/integration boundary | **RETAIN as API adapter** | Router must call the canonical facade and must not define independent truth or persistence |
| `api/routers/company_brain_v6.py` | Versioned API boundary | **COMPATIBILITY** | Keep during migration; delegate to canonical facade; publish deprecation criteria before removal |
| `dealix/hermes/agents/company_brain.py` | Agent-specific interpretation/use of Company Brain | **ADAPT as consumer** | Consume canonical CompanyBrain read model; no independent storage or schema ownership |
| `apps/web/app/company-brain-os/page.tsx` | User-facing page | **UI ONLY** | Render API-provided canonical data; no business rules or truth ownership in the page |

## CompanyBrain decision

The repository currently has two legitimate but different concerns:

1. an internal, defensive Dealix operating snapshot; and
2. a per-customer commercial Company Brain builder.

They must not be collapsed by deleting one implementation blindly. The canonical design is:

```text
Canonical CompanyBrain contract and IDs
├── InternalDealixSnapshotAdapter (`company_brain/brain.py`)
├── CustomerBrainV6CompatibilityAdapter (`company_brain_v6/`)
├── API adapters
├── Hermes consumer
└── Web UI consumer
```

One facade owns the entity contract. Existing implementations become adapters or consumers.

## Verified orchestration and agent surfaces

| Path | Current role | Decision | Required next action |
|---|---|---|---|
| `auto_client_acquisition/ai_workforce/orchestrator.py` | Existing AI workforce orchestration | **HOLD / inspect before extension** | Inventory task, action, approval, and proof outputs before adding another orchestrator |
| `auto_client_acquisition/ai_workforce/agent_contracts.py` | Agent contracts | **ADAPT** | Align references to canonical Tenant, Action, Approval, OutcomeEvent, ProofEvent, and LearningEvent IDs |
| `auto_client_acquisition/ai_workforce/agent_registry.py` | Agent registry | **RETAIN as agent registry only** | Must not become the strategy registry or entity registry |
| `auto_client_acquisition/ai_workforce/task_router.py` | Task routing | **ADAPT** | Treat routed work as canonical Action records or derived execution tasks, not an independent action queue |
| `auto_client_acquisition/intelligence/dealix_task_registry.py` | Task catalog/registry | **HOLD / caller inventory required** | Determine overlap with Action and DepartmentPlan before any new task registry is added |

## Canonical boundaries for external tools

External systems may be adapters only:

- CRM systems may supply or receive Company, Contact, Relationship, and Opportunity records, but Dealix retains canonical IDs and provenance.
- Langfuse may receive redacted observability events, but it cannot own OutcomeEvent, ProofEvent, or LearningEvent truth.
- Activepieces/n8n may execute approved actions, but they cannot own Action or Approval state.
- Firecrawl/Exa/search providers may supply Source and Signal candidates, but they cannot imply consent or contactability.
- Docling may parse source documents, but extracted facts remain candidates until reviewed and linked to Source evidence.

## Required canonical facade — next focused PR

A future focused PR, separate from #1014, should add a small facade rather than a new subsystem:

```text
dealix/company_intelligence/
  contracts.py        # canonical entity IDs and read/write DTOs
  company_brain.py    # facade over existing internal + V6 adapters
  provenance.py       # Source/evidence references
  compatibility.py    # explicit adapters for existing callers
```

Before that PR is opened, verify all imports and callers of:

- `build_company_brain`
- `CompanyBrain`
- `build_company_brain_v6`
- `CompanyBrainV6`
- both Company Brain API routers

## No-delete gate

No file listed here may be deleted until all conditions pass:

1. complete caller/import inventory;
2. canonical facade exists;
3. compatibility tests cover current API and script behavior;
4. tenant/provenance fields are preserved;
5. forbidden-channel and no-live-send behavior is preserved;
6. rollback path is documented;
7. explicit deletion approval is provided.

## First runtime consolidation order

1. Finish and green PR #1014 entity ownership guard.
2. Inventory CompanyBrain callers and create compatibility tests.
3. Add the canonical CompanyBrain facade without persistence or migration changes.
4. Route both API adapters and Hermes consumer through the facade.
5. Map Opportunity/Action/Approval/Proof/Learning surfaces using the same evidence standard.
6. Consolidate Langfuse behind one redacted adapter in a separate PR.
7. Only then consider Docling or LiteLLM pilots.

## Current blockers

- Full import/caller inventory is not yet recorded.
- Exact persistence ownership for several canonical entities remains unverified.
- PostgreSQL tenant/RLS proof remains a separate held prerequisite.
- No deletion, schema migration, production change, or external action is authorized.
