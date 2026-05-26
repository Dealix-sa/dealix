<div align="center">

# 🏢 Dealix — Saudi B2B Revenue Engine

### AI revenue, growth, and compliance engine for Saudi B2B — PDPL-native, ZATCA-aware, approval-first.
### محرّك إيرادات ونمو وامتثال بـ AI للشركات السعودية — PDPL أصلاً، ZATCA-aware، والموافقة أولاً.

[![CI](https://github.com/VoXc2/dealix/actions/workflows/ci.yml/badge.svg)](https://github.com/VoXc2/dealix/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![PDPL: native](https://img.shields.io/badge/PDPL-native-success)](integrations/pdpl.py)

**[العربية](README.ar.md)** · **English**

### [🚀 Deploy Runbook](docs/ops/DEPLOY_RUNBOOK.md) · [✅ Production Readiness](docs/ops/PRODUCTION_READINESS_CHECKLIST.md) · [🧭 Gap Audit](docs/architecture/REPO_GAP_AUDIT.md) · [🗺️ API Map](docs/architecture/API_MAP.md) · [📦 Env Template](.env.example)

</div>

---

## What Dealix is

Dealix is a Saudi-first B2B revenue operating system with three core engines:

1. **Lead Engine** — Saudi B2B lead discovery, enrichment, ICP scoring, duplicate suppression, and PDPL-aware usage controls.
2. **Service Engine** — productized AI services for diagnostics, sales assistance, decision packs, customer health, proof curation, growth signals, and executive command.
3. **Trust Engine** — approval-first execution, audit trails, evidence packs, policy checks, and compliance registers for Saudi operating requirements.

It is **not** a generic CRM, chatbot, or blind sales automation tool. Its operating rule is:

> AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.

---

## What is in this repository

| Area | Contents |
|---|---|
| Backend | FastAPI, SQLAlchemy async, Postgres-oriented persistence, routers across sales, compliance, analytics, agents, and webhooks. |
| Frontend | Static landing assets plus a Next.js app under `apps/web`. |
| Trust/compliance | PDPL-aware controls, no-overclaim register, Saudi compliance register, approval classes, and audit/evidence concepts. |
| Operations | Docker, docker-compose, Makefile, CI, production readiness docs, deploy/runbook material. |
| Commercial kit | Pricing, service catalog, onboarding, Saudi B2B accounts, outreach/channel material, and service packaging docs. |

---

## Quick start

```bash
git clone https://github.com/VoXc2/dealix.git
cd dealix
make setup
cp .env.example .env
# edit .env, then:
make run
# API docs: http://localhost:8000/docs
```

Full local stack:

```bash
make docker-up
curl http://localhost:8000/health
```

Production-style verification bundle:

```bash
make prod-verify
```

Useful verification commands:

```bash
make env-check        # checks .env.example contract and duplicate keys
make openapi-export   # exports FastAPI OpenAPI schema
make test             # test suite with project pytest defaults
make security         # Bandit + detect-secrets baseline scan when configured
```

---

## Public endpoints

Public endpoints intentionally available without application auth include:

- `/health`
- `/api/v1/public/demo-request`
- `/api/v1/pricing/plans`
- `/api/v1/checkout`
- `/api/v1/webhooks/moyasar`

Admin, customer, and privileged operational routes must remain protected by their configured API-key or future RBAC boundary.

---

## Repository operating controls

Dealix now has explicit repository controls for the most important production risks:

| Control | File / command |
|---|---|
| CI for Python checks, readiness exports, coverage, smoke tests, OpenAPI export, and Next.js build | `.github/workflows/ci.yml` |
| Environment contract validation | `scripts/check_env_contract.py`, `make env-check` |
| OpenAPI contract export | `scripts/export_openapi.py`, `make openapi-export` |
| Production launch checklist | `docs/ops/PRODUCTION_READINESS_CHECKLIST.md` |
| Repository gap register | `docs/architecture/REPO_GAP_AUDIT.md` |
| Production verification bundle | `make prod-verify` |

---

## Architecture model

Dealix is organized into five planes. Features should cross planes through explicit contracts, not hidden shared state.

| Plane | Responsibility | Example modules |
|---|---|---|
| Decision | Agents, reasoning, synthesis, recommendation, evidence assembly | `auto_client_acquisition/`, `autonomous_growth/`, `core/agents/` |
| Execution | Deterministic workflows, retries, compensation, external commitments | `auto_client_acquisition/pipeline.py`, `dealix/execution/` |
| Trust | Policy, approval, audit, verification, evidence packs | `dealix/trust/`, `dealix/registers/` |
| Data | Operational source of truth, lineage, metrics, integrations | `db/`, `integrations/` |
| Operating | CI/CD, Docker, release discipline, repo governance, runbooks | `.github/`, `Dockerfile`, `Makefile`, `docs/ops/` |

Full blueprint: [`docs/blueprint/master-architecture.md`](docs/blueprint/master-architecture.md).

---

## Trust and safety posture

Dealix is designed around:

- Structured outputs with approval, reversibility, and sensitivity classes.
- Policy evaluation before high-impact external actions.
- Human approval for pricing commitments, contract changes, sensitive exports, legal/regulatory messages, and other high-stakes actions.
- Evidence packs for decisions that need traceability.
- Public claim tracking through [`dealix/registers/no_overclaim.yaml`](dealix/registers/no_overclaim.yaml).

Security posture includes `.env`-based configuration, sensitive settings patterns, webhook verification where implemented, Docker hardening, CI checks, and local/CI-compatible security commands. Keep README/security claims aligned with actual configured CI jobs.

---

## Saudi compliance posture

Designed from inception for Saudi B2B operating constraints, including:

- PDPL consent, lawful basis, retention, suppression, breach, and transfer posture.
- Saudi-specific business language, SAR pricing, Riyadh-time operations, and Arabic/English workflows.
- Compliance mappings and registers under [`dealix/registers/`](dealix/registers/).

Compliance documentation does not replace legal review. Production launch requires evidence from tests, controls, logs, and operational procedures.

---

## Development workflow

```bash
make install-dev
make lint
make test
make env-check
make openapi-export
```

Before a production release:

```bash
make prod-verify
```

Then review:

- [`docs/ops/PRODUCTION_READINESS_CHECKLIST.md`](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)
- [`docs/architecture/REPO_GAP_AUDIT.md`](docs/architecture/REPO_GAP_AUDIT.md)
- [`dealix/registers/no_overclaim.yaml`](dealix/registers/no_overclaim.yaml)

---

## Key docs

| Purpose | Document |
|---|---|
| Master architecture | [`docs/blueprint/master-architecture.md`](docs/blueprint/master-architecture.md) |
| API map | [`docs/architecture/API_MAP.md`](docs/architecture/API_MAP.md) |
| Gap audit | [`docs/architecture/REPO_GAP_AUDIT.md`](docs/architecture/REPO_GAP_AUDIT.md) |
| Production readiness | [`docs/ops/PRODUCTION_READINESS_CHECKLIST.md`](docs/ops/PRODUCTION_READINESS_CHECKLIST.md) |
| Deploy runbook | [`docs/ops/DEPLOY_RUNBOOK.md`](docs/ops/DEPLOY_RUNBOOK.md) |
| Customer onboarding | [`docs/ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md`](docs/ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md) |
| No-overclaim register | [`dealix/registers/no_overclaim.yaml`](dealix/registers/no_overclaim.yaml) |
| Saudi compliance register | [`dealix/registers/compliance_saudi.yaml`](dealix/registers/compliance_saudi.yaml) |

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**[📖 Blueprint](docs/blueprint/master-architecture.md)** · **[✅ Production Readiness](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)** · **[🧭 Gap Audit](docs/architecture/REPO_GAP_AUDIT.md)** · **[🇸🇦 Compliance](dealix/registers/compliance_saudi.yaml)**

</div>
