# Dealix Env Unlock Matrix

Quick-glance: which env var unlocks which capability + how to verify.

## How to add a Railway env var

1. Railway → Project → Environment `Dealix` → Service `web` → Variables.
2. Add `KEY=VALUE`.
3. Click **Review** → **Deploy** (Railway changes are staged until you deploy).
4. Wait for green build.
5. Hit `https://api.dealix.me/api/v1/prospect/search-diag` and check the key's `set: true`.

## Capability matrix

| Capability | Env var(s) | Verify with | Without it |
|---|---|---|---|
| Persistence | `DATABASE_URL=${{Postgres.DATABASE_URL}}` | `/api/v1/admin/db-diag` returns positive length | All write endpoints return `skipped_db_unreachable` |
| Web discovery | `GOOGLE_SEARCH_API_KEY` + `GOOGLE_SEARCH_CX` | POST `/api/v1/leads/discover/web` returns results | static fallback |
| Local discovery | `GOOGLE_MAPS_API_KEY` (Places API enabled) | POST `/api/v1/leads/discover/local` returns results | static fallback |
| LLM messaging | `GROQ_API_KEY` (or `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`) | POST `/api/v1/prospect/discover` returns non-degraded results | rules-only |
| Crawler | `FIRECRAWL_API_KEY` | n/a — internal | falls back to httpx + bs4 |
| Email intel | `HUNTER_API_KEY` or `ABSTRACT_API_KEY` | POST `/api/v1/leads/enrich/full` body has `contacts` from `email_intel:hunter` | regex-only |
| Tech detection | `WAPPALYZER_API_KEY` (optional) | enrich response merges Wappalyzer block | internal only |
| Errors | `SENTRY_DSN` | exceptions appear in Sentry | logs only |

## Single one-liner check (server-side)

```
curl https://api.dealix.me/api/v1/prospect/search-diag | jq '{tier1_ready, tier2_ready, hint}'
```

If `tier1_ready: true` → your DB + Google CSE + LLM + Sentry are all wired.
If `tier2_ready: true` → Maps + at least one of Tavily/Firecrawl/Hunter is wired.

## Recommended Saudi-launch minimum

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
GOOGLE_SEARCH_API_KEY=...
GOOGLE_SEARCH_CX=75ae2277dfd754a1a
GOOGLE_MAPS_API_KEY=...      # restrict to Places API in GCP
GROQ_API_KEY=...
SENTRY_DSN=...
```

That's the cheapest config that unlocks the full Dealix lead machine for Saudi B2B.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
