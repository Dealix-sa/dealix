# Dealix Backend v5 — Production Engine

Node.js / Express / TypeScript backend for the Dealix RevOps platform.
PostgreSQL via Drizzle ORM. JWT auth. WebSocket live feed. AI integration
(OpenAI / Anthropic with intelligent static fallback). Full Founder
Console v5 with A1/A2/A3 policy evaluator and immutable audit log.

## Quickstart

```bash
# from repo root
pnpm install
cp artifacts/api-server/.env.example artifacts/api-server/.env
# edit DATABASE_URL, JWT_SECRET, DEALIX_ADMIN_API_KEY, DEALIX_INTERNAL_TOKEN

# push schema
pnpm --filter @workspace/db push

# seed
pnpm --filter @workspace/api-server seed

# dev
pnpm --filter @workspace/api-server dev

# production
pnpm run build
pnpm --filter @workspace/api-server start
```

Admin credentials after seed: `admin@dealix.ai` / `Dealix2024!`

## Layout

```
artifacts/api-server/         # Express app
  src/
    app.ts                    # Express factory (helmet, CORS, error handler)
    index.ts                  # HTTP + WebSocket bootstrap
    env.ts                    # Typed env config
    lib/
      ai.ts                   # OpenAI/Anthropic wrapper with fallback
      jwt.ts                  # Access / refresh token helpers
      policyEvaluator.ts      # Founder Console A1/A2/A3 classifier
      auditLog.ts             # Immutable audit trail writer
      scoring.ts              # Lead/risk scoring heuristics
      wsHub.ts                # /ws/agents broadcast hub
      errors.ts               # HttpError class + helpers
    middleware/
      requireAuth.ts          # JWT bearer guard
      requireAdminKey.ts      # X-Admin-API-Key guard
      internalAuth.ts         # X-Dealix-Internal-Token guard
      validate.ts             # Zod request validators
      rateLimit.ts            # Public / internal / auth limits
      errorHandler.ts         # Structured JSON errors
    routes/
      v1/
        auth.ts               # POST /api/v1/auth/{register,login,refresh,logout}
        dashboard.ts          # GET /api/v1/dashboard/metrics
        pipeline.ts           # GET /api/v1/revenue-pipeline/summary
        aiWorkforce.ts        # GET /api/v1/ai-workforce/agents
        approvals.ts          # GET pending/history, POST :id/{approve,reject}
        publicRoutes.ts       # /public/leads, risk-score, booking, knowledge
        businessNow.ts        # snapshot, commercial-strategy, simulate
        business.ts           # GTM playbook, sales script, proof pack
        transformation.ts     # KPI snapshot
        misc.ts               # decision-passport, revenue-os, gmail/li drafts
        internal.ts           # /internal/audit + /workers/health (gated)
        opsAutopilot/
          warRoom.ts          # War Room CRUD + outreach generator
          targeting.ts        # Today / pool / P0 / CSV import
          marketing.ts        # Calendar, publish-kit, UTM builder
          salesEvidence.ts    # Sales pipeline, evidence ledger, brief
          support.ts          # Tickets, classify, draft response, KB search
          founder.ts          # Cockpit, run-morning/evening/weekly/unified
    scripts/seed.ts           # Realistic Saudi-market seed data
lib/db/                       # @workspace/db — Drizzle schema package
  src/schema/                 # users, sessions, leads, deals, approvals,
                              # audit_log, workers, evidence_events,
                              # support_tickets, marketing_calendar, knowledge_base
```

## Surface area

The server implements every endpoint called by `frontend/src/lib/api.ts`,
including:

- Auth: `/api/v1/auth/{register,login,refresh,logout,me}`
- Dashboard / Pipeline: `/api/v1/dashboard/metrics`,
  `/api/v1/revenue-pipeline/summary`,
  `/api/v1/dashboard/revenue-series`
- AI Workforce: `/api/v1/ai-workforce/agents`
- Approvals: `/api/v1/approvals/{pending,history,:id,:id/approve,:id/reject,:id/request-edit}`
- Public: `/api/v1/public/{leads,risk-score,booking-request,knowledge/answer}`,
  `/api/v1/pricing/plans`
- Business Now: `/api/v1/business-now/{snapshot,commercial-strategy,
  commercial-strategy/simulate,operator-signals}`
- Business / GTM: `/api/v1/business/{verticals/recommend,recommend-plan,
  gtm/first-10,sales-script,proof-pack/demo}`, `/api/v1/transformation/kpi-snapshot`
- Decision Passport: `/api/v1/decision-passport/{golden-chain,evidence-levels}`
- Revenue OS: `/api/v1/revenue-os/{catalog,learning/weekly-template,anti-waste/check}`
- War Room (admin): `/api/v1/ops-autopilot/war-room` + CRUD + summary + today-pack + outreach + import
- Targeting (admin): `/api/v1/ops-autopilot/targeting/{today,pool,p0-today,import}`
- Marketing (admin): `/api/v1/ops-autopilot/marketing/{calendar,utm,social-today,
  social-today/mark,queue-approval,weekly-pack/apply,objection-draft,
  calendar/:id,calendar/:id/publish-kit}`
- Sales / Evidence / Support (admin): `/api/v1/sales/pipeline`,
  `/api/v1/evidence/events`, `/api/v1/ops-autopilot/founder/evidence/csv-append`,
  `/api/v1/support/tickets`, `/api/v1/support/tickets/:id/{classify,draft-response}`,
  `/api/v1/invoices/draft`, `/api/v1/knowledge/search`
- Ops Leads (admin): `/api/v1/ops-autopilot/leads`,
  `/api/v1/ops-autopilot/leads/:id/{meeting-brief,advance-stage}`
- Founder Cockpit (admin): `/api/v1/ops-autopilot/founder/cockpit` +
  `run-{morning,evening,weekly,unified-day}`,
  `/api/v1/ops-autopilot/founder/complete-autonomous-day/run`,
  `/value-plan`, `/gtm-stack`, `/full-autonomous-ops`(+/run),
  `/commercial-value-map`, `/strongest-plan`, `/strongest-ops`(+/run),
  `/expansion-status`, `/daily-pack`, `/full-ops-health`,
  `/client-pack/generate`, `/founder-dashboard`
- Internal Trust Layer (token-gated):
  `/api/v1/internal/{status,audit,audit/approval/:id,workers/health,
  workers/:name/heartbeat}`
- Realtime: WebSocket on `/ws/agents` broadcasting agent activity events

## Founder Console v5

Every state-changing approval action runs through the policy evaluator
which classifies the request as **A1 / A2 / A3**:

- **A1** — Founder approves; low-risk, no external action allowed.
- **A2** — Requires evidence/justification; founder approves with audit.
- **A3** — Never auto-execute; blocked at the external boundary.

The decision is written to `audit_log` with `external_action_allowed`,
the matched policy reasons, risk level, and submitted evidence. Audit
entries are immutable. `/api/v1/internal/audit` returns the full
trail; per-approval history is at
`/api/v1/internal/audit/approval/:approvalId`.

## AI Integration

`src/lib/ai.ts` is a provider-agnostic wrapper. It tries OpenAI first,
then Anthropic, then falls back to a contextual static response. No
endpoint is blocked by missing keys.

Used by:
- `POST /api/v1/ops-autopilot/war-room/:id/generate-outreach` (Arabic outreach)
- `POST /api/v1/ops-autopilot/client-pack/generate` (client proof pack)
- `POST /api/v1/support/tickets/:id/draft-response` (support reply)
- `POST /api/v1/ops-autopilot/leads/:id/advance-stage` (next-step suggestion)
- `GET  /api/v1/ops-autopilot/leads/:id/meeting-brief` (founder meeting brief)
- `POST /api/v1/ops-autopilot/founder/strongest-ops/run` (founder brief)

## Worker health

`/api/v1/internal/workers/health` returns each worker's status. A worker
is auto-tagged **stale** when its `lastRunAt` is older than
`WORKER_STALE_MINUTES` (default 30) and its status is `running`. Workers
report in via `POST /api/v1/internal/workers/:name/heartbeat`.

## Production hardening

- `helmet` security headers, `cors` allow-list, `trust proxy` on
- Zod validation on every request body and most query strings
- `express-rate-limit`: 100 req/min public, 500 req/min internal,
  20 req per 15 min for `/auth/*`
- Centralized error handler returns structured `{ error, code, details }`
- JWT access (15 min) + refresh (7 days) tokens, refresh rotation on use,
  refresh revocation on logout
- `bcryptjs` cost 12 for password hashing
- Database SSL auto-enabled for Supabase / Render / Railway connection strings
