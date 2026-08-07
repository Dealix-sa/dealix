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

## Canonical facade — COMPLETED (PR #1041)

The canonical facade is now implemented in `dealix/company_intelligence/`:

```text
dealix/company_intelligence/
  __init__.py              # 170+ exports, single canonical import surface
  adapter_registry.py      # maps all 22 entities to their normalize functions
  company_brain.py         # CanonicalCompanyBrain facade (internal + customer)
  action_adapter.py        # normalize_next_best_action
  consent_adapter.py       # normalize_consent
  graph_adapter.py         # normalize_lead_to_company, normalize_lead_to_contact
  learning_adapter.py      # normalize_learning_event, normalize_win_loss
  offer_adapter.py         # normalize_service_offering, normalize_catalog
  pipeline_adapter.py      # normalize_pipeline_lead
  playbook_adapter.py      # normalize_sector_playbook
  proof_adapter.py         # normalize_proof_event
  proposal_adapter.py      # normalize_proposal
  revenue_graph_adapter.py # normalize_graph_edge
  signal_adapter.py        # normalize_signal
  source_adapter.py        # normalize_source_passport
  execution_contracts.py   # normalize_opportunity, normalize_approval, normalize_draft
  outcome_contracts.py     # build_outcome_event, build_proof_event, build_learning_event
  *_contracts.py           # 15 frozen Pydantic contract modules with state machines
```

CI gates (all required):
- `scripts/verify_company_intelligence_entity_ownership.py` — 22 entities
- `scripts/verify_company_intelligence_adapters.py` — 18 normalize functions
- `tests/test_company_intelligence_adapter_registry.py` — 20 tests
- `tests/test_company_intelligence_spine_integration.py` — frozen-entity validation
- `tests/test_company_intelligence_e2e_scenario.py` — 12-entity customer journey

## No-delete gate

No file listed here may be deleted until all conditions pass:

1. complete caller/import inventory;
2. canonical facade exists;
3. compatibility tests cover current API and script behavior;
4. tenant/provenance fields are preserved;
5. forbidden-channel and no-live-send behavior is preserved;
6. rollback path is documented;
7. explicit deletion approval is provided.

## Runtime consolidation order (progress)

1. ✅ Finish and green PR #1014 entity ownership guard — 22 entities registered.
2. ✅ Canonical CompanyBrain facade added (PR #1041) — internal + customer builders.
3. ✅ 12 adapter modules mapping all operational sources to canonical contracts.
4. ✅ Adapter registry with entity-ownership cross-check (22/22 covered).
5. ✅ CI gates: entity ownership, adapter verification, adapter registry tests.
6. Route both API adapters and Hermes consumer through the facade.
7. Consolidate Langfuse behind one redacted adapter in a separate PR.
8. Only then consider Docling or LiteLLM pilots.

## Current blockers

- Full import/caller inventory is not yet recorded.
- Exact persistence ownership for several canonical entities remains unverified.
- PostgreSQL tenant/RLS proof remains a separate held prerequisite.
- No deletion, schema migration, production change, or external action is authorized.
