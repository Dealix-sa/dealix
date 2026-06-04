# Repository Discovery Report — Dealix Startup OS

## تقرير اكتشاف المستودع

> Produced before implementation, per the Execution Mode requirement. Real
> findings from inspecting the repository on the working branch.

---

## 1. Current structure / البنية الحالية

Dealix is a **large, mature monorepo**, not a greenfield project:

- **Backend:** FastAPI app under `api/` (routers, schemas, security, middleware),
  with `core/`, `dealix/`, `platform_core/`, `auto_client_acquisition/` (175+
  internal OS modules), and Alembic migrations.
- **Website:** Next.js (App Router) under `apps/web/` — `app/` with
  `sitemap.ts`, `robots.ts`, `manifest.ts`, `layout.tsx` (metadata), and pages
  including `ar/`, `go-to-market`, `revenue-os`, `status`, `safety`, etc.
  `npm run verify` = `typecheck && build`.
- **Scripts:** 243 Python/shell scripts under `scripts/` (commercial, launch,
  founder, readiness families).
- **Docs:** 219 directories under `docs/` including an existing `company-os/`
  (numbered system docs), plus `commercial/`, `sales/`, `marketing/`, `legal/`,
  `security/`, `finance/`, `delivery/`, etc.
- **CI:** 51 workflows under `.github/workflows/`.
- **Config OS:** `os/` holds YAML offers/markets/scoring and founder manuals.

## 2. What exists / ما هو موجود

- A previous "Agentic AI Company OS" (PR #559) with extensive internal modules.
- Existing offers catalog (`os/03_OFFERS.yml`) — note: it prices the AI Workflow
  Audit at 5,000–25,000 SAR.
- Existing safety culture: `.gitleaks.toml`, `.secrets.baseline`, a
  `make security-smoke` repo scanner, approval-first registers.

## 3. What was missing / ما الناقص

The specific **Startup OS** requested did not exist as a coherent tree:
`docs/commercial-launch/`, `docs/site-launch/`, `docs/launch-control/`,
`docs/media-social-os/`, `docs/sales-os/`, `docs/marketing-os/`, `docs/ads-os/`,
`docs/revops-os/`, `docs/delivery-os/`, `docs/support-os/`, `docs/finance-os/`,
`docs/legal-os/`, `docs/security-os/`, `docs/analytics-os/`, `docs/people-os/`,
`docs/partnerships-os/`, `docs/investor-os/`, `docs/operations-os/`,
`docs/go-live/`, `docs/product-os/` — and the 400+ daily **review-only** draft
factory, the media/social calendar generator, and the unified verifier spine.

## 4. Key facts / حقائق أساسية

| Question | Answer |
|---|---|
| Is the website Next.js? | **Yes** — `apps/web` (App Router), builds via `npm run verify`. |
| Is the API FastAPI? | **Yes** — `api/main.py`. |
| Is there deploy config? | **Yes** — Railway + Vercel + Docker. |
| Are there workflows? | **Yes** — 51 existing. |
| Prior commercial systems? | **Yes** — extensive; this initiative is additive. |
| Duplicates? | Avoided — new trees use distinct `-os` directory names. |
| Old VoXc2 links? | README CI badge points to `VoXc2/dealix`; clone URL standardized to `Dealix-sa/dealix` in the new Startup OS section. |

## 5. Execution decision / قرار التنفيذ

**EXTEND.** The repository is mature; this initiative **adds** a coherent Startup
OS layer (docs + executable scripts + tests + workflows) without modifying the
existing backend, web pages, or migrations. No destructive change. No file owned
by another system was overwritten.

## 6. Risks before execution / المخاطر قبل التنفيذ

- **Pre-existing `make security-smoke` findings** in unrelated test fixtures and
  docs (fake `sk_live_`, `ghp_`, `AKIA` values). Not introduced here; the
  Startup OS scoped scanner (`final_secret_and_risk_scan.py`) passes cleanly.
- **Pricing discrepancy:** the new offer ladder sets the Audit at 499–2,500 SAR
  (per task), differing from `os/03_OFFERS.yml`. Documented intentionally; the
  founder reconciles.
- **Root `tests/conftest.py`** requires the full app dependency tree; the Startup
  OS tests are stdlib-only and run once those deps are installed.

## 7. Merge plan without breaking main / خطة الدمج

1. Develop on the designated feature branch only.
2. Add new directories/files; never edit backend, migrations, or web pages.
3. Keep all new CI workflows `permissions: contents: read`, artifact-only.
4. Verify locally: `startup_os_verify.py` + `final_launch_control_verify.py`
   PASS, 16 test suites green, web `npm run verify` green.
5. Open a **draft** PR for founder review.
