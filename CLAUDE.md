# Dealix — Project Memory for Claude Code

## What This Project Is

**Dealix** is a Sovereign B2B Growth OS for the Saudi Arabia market. It automates the full commercial stack: lead intelligence → revenue sprint → proof delivery → retainer expansion → M&A. It serves Saudi SMEs and enterprises that need an AI-powered operations layer without hiring a full growth team.

**Live production**: `https://api.dealix.me` (Railway, auto-deploy from `main`)
**Frontend**: `https://dealix.me` (Next.js 15, GitHub Pages or Vercel)
**Stack**: FastAPI 0.115 + PostgreSQL (async SQLAlchemy 2.0) + Next.js 15 + Railway

---

## Active Development Branch

Always develop on: `claude/dealix-autonomous-systems-abMT0`

Never push directly to `main` without a PR review.

---

## 11 Non-Negotiables (Governance Rules)

These rules are **absolute**. No code, script, or agent may violate them:

1. **no_cold_whatsapp** — Never send unsolicited WhatsApp messages automatically
2. **no_linkedin_automation** — Never auto-post or auto-DM on LinkedIn
3. **no_fake_revenue** — invoice_created ≠ revenue; only payment_confirmed = revenue
4. **no_upsell_without_proof** — Never upsell a customer without completed proof event
5. **no_auto_execute_offer** — Never execute a commercial offer without founder approval
6. **approval_required_for_external_actions** — All external comms must be queued for approval
7. **is_estimate_always_true** — All AI-generated valuations/scores carry is_estimate=True
8. **no_pii_in_logs** — No personal data in logs (PDPL Article 18 compliance)
9. **pdpl_consent_required** — Every contact must have recorded consent before outreach
10. **delivery_requires_payment_confirmed** — No service delivery until payment confirmed
11. **no_destructive_schema_changes** — All DB changes via Alembic migrations, never `CREATE TABLE` / `DROP` directly

---

## Commercial Offer Ladder (5 Tiers)

| Tier | Offer | Price |
|------|-------|-------|
| 1 | Free Diagnostic | 0 SAR |
| 2 | Revenue Intelligence Sprint | 499 SAR |
| 3 | Data-to-Revenue Pack | 1,500 SAR |
| 4 | Managed Growth Ops (Retainer) | 2,999–4,999 SAR/mo |
| 5 | Custom AI Implementation | 5,000–25,000 SAR |

---

## Architecture Overview

```
dealix/
├── api/                         # FastAPI application (162 routers)
│   ├── main.py                  # App factory, router registration, security gates
│   ├── routers/                 # 162 HTTP routers (domains/ + flat)
│   │   ├── domains/             # 8 domain aggregators
│   │   ├── m_and_a.py           # Wave 15.1: M&A Radar
│   │   ├── capital_os.py        # Wave 15.1: Capital OS
│   │   ├── expansion_engine.py  # Wave 12.7: Expansion recommendations
│   │   └── payment_ops.py       # Wave 14B: Moyasar payments
│   ├── security/                # JWT, API keys, RBAC, rate limit, SSRF guard
│   └── middleware/              # Audit, ETag, security headers, rate limit
├── auto_client_acquisition/     # 174 domain modules (core business logic)
│   ├── capital_os/              # Capital asset ledger (JSONL-backed)
│   ├── investment_os/           # PMF score, funding readiness, valuation drivers
│   ├── expansion_engine/        # Expansion readiness + next-best-offer
│   ├── payment_ops/             # Payment flow, Moyasar, evidence gate
│   ├── data_os/                 # Data governance
│   ├── governance_os/           # Approval workflows
│   ├── proof_os/                # Proof generation
│   ├── value_os/                # Value capture
│   ├── adoption_os/             # Customer adoption
│   ├── friction_log/            # Pain point tracking
│   ├── sales_os/                # Sales automation
│   └── saudi_layer/             # PDPL, ZATCA, Khaliji culture
├── core/                        # Shared infrastructure
│   ├── llm/                     # Multi-provider LLM router (Anthropic → Groq → OpenAI)
│   ├── agents/                  # Base agent + multi-agent orchestration
│   ├── memory/                  # Revenue memory (pgvector embeddings)
│   └── prompts/                 # Saudi Arabic dialect prompts
├── db/                          # SQLAlchemy models + Alembic migrations
│   ├── models.py                # 32 core models (tenants, leads, deals, audit, etc.)
│   └── session.py               # Async DB session
├── frontend/                    # Next.js 15 application
│   ├── src/app/[locale]/        # Page routes (ar/en)
│   │   └── ops/                 # Ops dashboard pages
│   │       ├── founder/         # Founder command center
│   │       ├── m-and-a/         # M&A Radar page (new)
│   │       ├── war-room/        # Revenue war room
│   │       ├── targeting/       # P0 targeting
│   │       ├── sales/           # Sales pipeline
│   │       ├── marketing/       # Social content
│   │       ├── partners/        # Partner management
│   │       ├── evidence/        # Evidence ledger
│   │       └── support/         # Support queue
│   ├── src/components/
│   │   ├── gtm/                 # 27 founder/ops components
│   │   │   └── OpsMandARadar.tsx  # M&A Radar component (new)
│   │   ├── layout/              # AppLayout, Sidebar, Header
│   │   └── ui/                  # Design system primitives
│   ├── src/lib/api.ts           # 70+ typed API methods
│   └── messages/                # i18n (ar.json + en.json)
├── scripts/                     # 172 automation scripts
│   ├── run_m_and_a_radar_scan.py   # M&A daily scan (new)
│   ├── run_capital_os_brief.py     # Capital OS weekly brief (new)
│   └── run_dealix_complete_autonomous_day.py
├── tests/                       # 507+ tests
│   └── unit/                    # Unit tests (incl. test_m_and_a.py, test_capital_os.py)
├── .github/workflows/           # 29 CI/CD workflows
│   ├── ci.yml                   # Main CI (70% coverage gate)
│   ├── m_and_a_intelligence_daily.yml  # Daily M&A scan (new)
│   └── capital_os_weekly.yml    # Weekly Capital OS brief (new)
└── docs/                        # 100+ governance + commercial docs
    ├── company/DEALIX_OPERATING_KERNEL.md
    └── commercial/              # GTM playbooks, pricing, proposals
```

---

## Development Commands

```bash
# Run all tests
pytest tests/ -x --timeout=60

# Run specific new tests
pytest tests/unit/test_m_and_a.py tests/unit/test_capital_os.py -v

# Lint
ruff check api/ auto_client_acquisition/ core/
black --check api/ auto_client_acquisition/ core/

# Type check
mypy api/ --ignore-missing-imports

# DB migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Start API locally
uvicorn api.main:app --reload --port 8000

# Start frontend
cd frontend && npm run dev

# Run autonomous day (dry-run)
python scripts/run_dealix_complete_autonomous_day.py --dry-run

# M&A radar scan (dry-run)
python scripts/run_m_and_a_radar_scan.py --dry-run

# Capital OS brief (dry-run)
python scripts/run_capital_os_brief.py --dry-run
```

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `api/main.py` | Router registration, security gates, lifespan hooks |
| `api/routers/m_and_a.py` | M&A Radar: evaluate → LOI → ledger |
| `api/routers/capital_os.py` | Capital OS: assets, PMF, readiness, exit valuation |
| `api/routers/expansion_engine.py` | Expansion readiness + next-best-offer (Wave 12.7 pattern) |
| `api/routers/payment_ops.py` | Moyasar payments, evidence gate |
| `auto_client_acquisition/capital_os/` | Capital asset JSONL ledger |
| `auto_client_acquisition/investment_os/` | PMF score, funding readiness, valuation drivers |
| `frontend/src/lib/api.ts` | All 70+ typed API client methods |
| `frontend/src/components/gtm/OpsFounderCommandCenter.tsx` | Main ops dashboard pattern |
| `frontend/src/components/gtm/OpsMandARadar.tsx` | M&A Radar component |
| `db/models.py` | 32 SQLAlchemy models |
| `docs/company/DEALIX_OPERATING_KERNEL.md` | 8 core engines + Dealix Standard |

---

## Router Pattern (New Wave)

Always follow the expansion_engine.py pattern when adding a new router:

```python
"""Wave X.Y — <Name> HTTP surface.

<Endpoints>

Hard rules:
- <rule>: <description>
"""
from __future__ import annotations
from fastapi import APIRouter
from auto_client_acquisition.<module> import <functions>

router = APIRouter(prefix="/api/v1/<name>", tags=["<Name>"])

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "is_estimate_always_true": True,
}
```

Register in `api/main.py` after `platform_foundation_router`.

---

## Frontend Component Pattern (Ops Page)

```tsx
// page.tsx
import { AppLayout } from "@/components/layout/AppLayout";
import { MyComponent } from "@/components/gtm/MyComponent";
export default async function MyPage({ params }) {
  const { locale } = await params;
  return <AppLayout title="..." subtitle="..."><MyComponent /></AppLayout>;
}

// component.tsx — always "use client", glass dark UI, gold accents
```

---

## Test Pattern

```python
# tests/unit/test_<module>.py
import os
os.environ.setdefault("APP_ENV", "test")
import pytest
from api.main import create_app
# Use httpx ASGITransport for endpoint tests
# Use pytest.mark.anyio for async tests
```

---

## Strategic Roadmap

### Now (Wave 15.1 — delivered)
- M&A Radar: EBITDA evaluation, LOI drafting, acquisition ledger
- Capital OS: asset ledger, PMF score, investor readiness, exit valuation
- CLAUDE.md: project memory file

### Medium-term (30 days — Wave 16)
- **GCC Expansion Intelligence**: UAE/Kuwait/Bahrain market radar
- **Retainer Conversion Engine**: auto-detect Sprint → Retainer upgrade triggers
- **Customer Health OS**: automated churn prediction + intervention triggers
- **Revenue Forecasting**: 90-day ARR forecast from pipeline signals

### Long-term (90 days — Wave 17)
- **Exit Readiness Module**: full Series A/exit preparation checklist
- **Cross-border Compliance**: UAE DIFC, Kuwait CBK regulatory layer
- **Enterprise PMO 2.0**: multi-stakeholder governance for enterprise deals
- **Investor Dashboard**: live investor-ready metrics pack (ARR, NRR, CAC, LTV)
- **IPO Preparation OS**: financial audit readiness, board reporting automation

---

## Environment Variables (Key Ones)

```bash
APP_ENV=development|test|staging|production
DATABASE_URL=postgresql+asyncpg://...
ANTHROPIC_API_KEY=...            # Primary LLM
MOYASAR_SECRET_KEY=...           # Saudi payments
ADMIN_API_KEYS=...               # For /api/v1/admin/* endpoints
DEALIX_MA_LEDGER_PATH=...        # M&A proposals ledger (default: var/m_and_a_proposals.jsonl)
DEALIX_CAPITAL_LEDGER_PATH=...   # Capital assets ledger (default: var/capital-ledger.jsonl)
```

---

## Compliance Notes

- **PDPL**: All personal data handling is PDPL-compliant (Article 18 audit trail, Article 4 consent)
- **ZATCA**: Saudi e-invoice compliance via `api/routers/zatca.py`
- **Multi-tenancy**: Row-level security via `TenantIsolationMiddleware`
- **Moyasar**: Payments are `test` mode until `DEALIX_MOYASAR_MODE=live` is set

---

## Subagent Types for This Project

| Task | Subagent |
|------|----------|
| Build Python API routers + tests | `dealix-engineer` |
| Write docs, proposals, Arabic content | `dealix-content` |
| Run delivery sprint for a customer | `dealix-delivery` |
| Sales qualification + proposals | `dealix-sales` |
| 90-day plan status + coordination | `dealix-pm` |
