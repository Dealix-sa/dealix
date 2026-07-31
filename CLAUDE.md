# Dealix — Canonical Operating Manual

## Mission

Dealix is a Saudi B2B AI-native Revenue Command OS delivered first as a concierge-assisted operating service. It overlays the customer's existing CRM, ERP, email, WhatsApp, spreadsheets, and reporting. It is not a CRM replacement, generic chatbot, blind automation agency, or self-serve SaaS at this stage.

The product goal is not maximum feature count. The goal is one trusted operating layer that turns company context, opportunities, actions, approvals, outcomes, proof, and learning into a measurable daily command.

## Canonical product spine

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

Canonical entity ownership is defined in:

```text
dealix/registers/company_intelligence_entity_ownership.json
```

Do not create a second Company Brain, Opportunity object, Approval Center, Proof Ledger, or Daily Command under a new name.

## Commercial truth

Canonical sources:

- `docs/DEALIX_BUSINESS_MODEL.md` — founder-governed business model;
- `auto_client_acquisition/service_catalog/registry.py` — executable offer status;
- `landing/assets/data/services-catalog.json` — synchronized committed export.

Only two offers are commercially active:

| Offer | Commercial status | Pricing rule |
|---|---|---|
| Free Mini Diagnostic | `free_entry` | Free |
| Revenue Command Pilot — 30 days | `quote_only` | Quote after discovery; no public fixed price |

All other catalog entries are `internal_experiment` until separately approved. Do not quote, market, or sell them as live offers.

A proposal is not an invoice. An invoice is not revenue. Revenue requires payment evidence.

## First-five ICP

Focus the first five customers on Saudi B2B SaaS and business-service companies with approximately 20–200 employees that have:

- direct founder or GM access;
- a specific revenue-operations pain;
- usable lawful data;
- an accountable owner;
- willingness to run a measured 30-day pilot;
- acceptance of human approval gates.

Defer banks, government, heavily regulated enterprise transformation, anonymous mass outbound, and customers requesting guaranteed revenue until Dealix has repeatable proof and references.

## Product priorities

Execute in this order:

1. Production trust: CI, startup, auth, deployment SHA, smoke tests, secrets, tenancy.
2. Canonical Company Brain and entity ownership.
3. Opportunity Graph and evidence-backed prioritization.
4. Action, Draft, Approval, Outcome, and Proof loop.
5. Revenue Command Pilot delivery quality.
6. Self-improvement from verified failures and outcomes.
7. Optional integrations only behind existing Dealix contracts.

Do not add another CRM, workflow runtime, vector database, crawler, model router, or observability platform without a measured gap and an approved adapter boundary.

## Architecture map

```text
api/                 FastAPI app and routers
core/                settings, logging, errors, database, LLM foundations
db/                  SQLAlchemy and Alembic
dealix/              canonical Company Intelligence and agent surfaces
auto_client_acquisition/  commercial and customer acquisition engines
company/             daily internal operating engines
scripts/             verification and operating commands
scripts/ops/         CI, deployment, security, and production checks
apps/web/            Next.js command-room frontend
docs/                product, strategy, architecture, and runbooks
sales/               proposals, playbooks, and delivery assets
reports/runtime/     generated runtime output; never canonical source truth
```

Important files:

- `api/main.py`
- `core/config/settings.py`
- `railway.toml`
- `Dockerfile`
- `Makefile`
- `docs/DEALIX_BUSINESS_MODEL.md`
- `dealix/registers/company_intelligence_entity_ownership.json`
- `dealix/company_intelligence/`
- `auto_client_acquisition/service_catalog/registry.py`

## Autonomy and approval model

### Automatically allowed

- reading, searching, analysis, and classification;
- tests, static verification, and safe diagnostics;
- internal drafts, reports, queues, proof packs, and plans;
- branches, commits, and Draft PRs;
- internal data organization without deleting source evidence.

### Explicit approval required

- sending any external message;
- publishing public content;
- issuing or sending a quote, proposal, invoice, or contract;
- charging a customer or recording revenue;
- merging to `main`;
- rotating secrets;
- changing Railway, Vercel, production, billing, or branch protection;
- running migrations or enabling RLS;
- deleting material data or branches.

## External-action safety — NON-NEGOTIABLE

These settings remain disabled unless a controlled approval explicitly authorizes a live action:

```text
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

Forbidden:

- cold WhatsApp blasts;
- mass LinkedIn automation or scraping;
- automatic email/SMS sending;
- fake clients, logos, testimonials, case studies, revenue, or ROI;
- guaranteed sales or outcome claims;
- public exposure of local-model or MCP control surfaces;
- using external tools as canonical truth for consent, payment, approval, or proof.

## Secrets and customer-data policy

- Never commit `.env`, tokens, API keys, passwords, private certificates, or production customer data.
- Never print secret values in logs, markdown, tests, issues, or PRs.
- Use names-only environment diagnostics.
- Use synthetic or public data for integration pilots.
- Keep TestSprite and MCP credentials local or in approved secret stores.
- Do not enable PostgreSQL RLS until PostgreSQL-only tenant tests run without skips and trusted server-side tenant binding is reviewed.

## Claim and evidence rules

Every material claim must have one of:

- code or test evidence;
- GitHub workflow evidence;
- deployment and live-SHA evidence;
- signed commercial evidence;
- payment evidence;
- customer-consented proof.

Use measured language:

- "نتوقع" / "we expect";
- "الهدف هو" / "the goal is";
- "سنقيس" / "we will measure".

Do not use "guaranteed", "مضمون", or unsupported market leadership claims.

## Development constraints

- Inspect existing implementations before creating new modules.
- Search for an existing PR or issue before opening another.
- One bounded concern per PR.
- Split changes that touch unrelated systems.
- Do not weaken security, tests, or production guards to obtain green CI.
- Do not assume generated runtime files exist.
- Do not commit generated lead lists, daily reports, approval queues, or customer data unless the file is an explicitly reviewed static template or governance artifact.
- Do not run a development server inside a PR workflow.
- Do not perform production mutations from tests.

## Required verification

Use the narrowest relevant commands first, then repository gates:

```bash
python scripts/verify_company_intelligence_entity_ownership.py
pytest -q tests/test_company_intelligence_entity_ownership.py
pytest -q tests/test_canonical_company_brain_facade.py
python scripts/verify_no_auto_external_send.py
python scripts/ops/security_smoke_ci.py
python scripts/verify_company_launch_ready.py
python scripts/dealix_export_service_catalog_json.py --check
npm --prefix apps/web run verify
make full-repo-test
```

A merge candidate requires:

- exact-head CI success;
- CodeQL, Security, Docker, Repository Hardening, No-Crash, and product checks successful;
- zero unresolved review threads;
- no unexplained skipped proof for the changed risk surface;
- current-base mergeability;
- explicit merge approval.

An optional live Railway smoke may be skipped when no authorized production secret is available. Do not represent a skipped live smoke as production proof.

## Production trust rules

- Repository CI is not live production proof.
- A READY Vercel preview is not proof that Railway runs the same SHA.
- Production readiness requires exact deployed SHA, public health, protected smoke, and correct authentication behavior.
- Do not remove startup secret guards.
- Fix billing, environment, deployment source, and service configuration rather than weakening security.
- Do not expose secret values while diagnosing production.

## Company Brain rules

The canonical package is:

```text
dealix/company_intelligence/
```

It provides a normalized, persistence-neutral facade over existing authoritative builders. Existing builders remain compatible until callers are migrated deliberately.

Required properties:

- tenant-scoped provenance;
- network-free and LLM-free internal snapshot behavior;
- preservation of forbidden-channel enforcement;
- explicit source identity;
- no silent replacement of existing authoritative behavior.

## Integration rules

External tools may be adapters, never canonical owners.

Current direction:

- Langfuse: harden one existing canonical path;
- Docling: private-document pilot behind file and provenance gates;
- LiteLLM: benchmark only behind the current Model Router;
- Activepieces: optional approval bridge, not Approval truth;
- Firecrawl: legal/privacy/terms hold before embedded use;
- Temporal, Qdrant, Twenty: hold until a measured gap exists;
- Playwright agents: isolated QA only, without founder/customer sessions;
- MCP: trusted hosts, origins, scopes, audit, and no production credentials by default.

## Daily operating outcome

Each operating cycle should produce:

1. highest production-trust blocker;
2. highest money-now action;
3. opportunity and action queue updates;
4. approvals required;
5. proof events;
6. failure and learning events;
7. one safe next execution step.

## Definition of product success

Dealix is stronger when it has:

- one canonical truth per entity;
- fewer contradictory workflows and offers;
- exact production evidence;
- measurable customer outcomes;
- zero unauthorized external actions;
- tenant and provenance guarantees;
- repeatable pilot delivery;
- actual paid proof and renewal evidence.

Do not substitute feature volume for these outcomes.
