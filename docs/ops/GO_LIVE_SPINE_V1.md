# Go-Live — Activation Spine v1

_Last updated: 2026-06-07_

The minimum to make Dealix **operate daily**: the public site captures inbound,
the daily engine produces a real lead board, and the founder approves + sends
**manually** (Article 4 — no auto-send, no scraping, no live charge).

## The loop (verify each link)

| # | Link | How to verify | File / endpoint |
|---|---|---|---|
| 1 | Website form → backend | Submit the demo + custom form on `frontend` | `POST /api/v1/public/demo-request`, `/custom-request` |
| 2 | Backend → lead-inbox (store A) | Lead appears in founder feed | `auto_client_acquisition/lead_inbox.py`, `GET /api/v1/founder/leads` |
| 3 | War-room (store B) → lead-inbox bridge | `/public/leads` lead is visible in `lead_inbox.list_leads(status="new")` | `dealix/revenue_ops_autopilot/orchestrator.py:capture_lead` (test: `tests/test_public_lead_bridge.py`) |
| 4 | Warm-list seed | `python3 scripts/dealix_build_warmlist.py` → 150+ PII-free candidates | `data/wave12/warmlist/candidates.csv` (gitignored) |
| 5 | Daily board | `python3 scripts/dealix_daily_lead_prep.py --top-n 10` → JSON+MD | `data/wave12/daily_lead_prep/{date}.json` |
| 6 | Founder board surface | `GET /api/v1/founder/daily-board` returns the latest board | `api/routers/founder.py`; UI `frontend/.../founder/board` |
| 7 | Approve + **manual** send | Founder copies the draft, sends via LinkedIn/email himself | action_mode = `approved_manual` |
| 8 | Log reply → pipeline | `POST /api/v1/founder/leads/{id}/status` (contacted/qualified/…) | `lead_inbox.update_status` |

Scheduled run: `.github/workflows/dealix_daily_lead_board.yml` (05:00 UTC Sun–Thu)
builds the warm-list, runs the prep, and uploads the board as an artifact
(**never committed** — may contain inbound PII; `data/*` is gitignored).

### One-command local check
```bash
python3 scripts/dealix_build_warmlist.py && \
python3 scripts/dealix_daily_lead_prep.py --top-n 10 && \
ls -1 data/wave12/daily_lead_prep/
```

## Repo-side readiness (done in this branch)

- Canonical offer/pricing aligned to `service_catalog/registry.py`; wrong
  `5,000–25,000` enterprise tier removed from the site.
- Public website forms wired (`frontend/`), custom-solution intake live + in nav.
- Daily engine seeded + scheduled; founder board endpoint + UI.
- Frontend forbidden-claims guard added (`tests/test_frontend_forbidden_claims.py`).
- `frontend/.env.example` + daily-engine env documented in root `.env.example`.
- `apps/web/` deprecated; 2 orphan modules archived (`CANONICAL_MAP.md`).

## Founder-only / external (cannot be done in the repo)

| Item | Where | Notes |
|---|---|---|
| DNS + TLS for `dealix.me` / `api.dealix.me` | DNS + hosting dashboard | Issue #469 |
| Production secrets | Railway/Vercel | `NEXT_PUBLIC_API_URL`, admin key, `CALENDLY_URL`, PostHog, Gmail OAuth — Issue #467 |
| Enable GitHub Actions schedule | GitHub → Actions | Daily lead board + CI — Issue #471 |
| Moyasar live charge | Payment dashboard | **Stays BLOCKED by constitution** until founder explicitly enables (`finance_os`) |
| Real outreach | LinkedIn / email | Founder sends approved drafts manually — never automated |

## Known pre-existing item (out of spine scope — P2)

`tests/test_landing_forbidden_claims.py` has **pre-existing** failures:
many `landing/*.html` pages (e.g. `data-pack.html`, `bespoke-ai.html`,
`architecture.html`) carry un-allowlisted `guaranteed/مضمون/cold/scraping`
tokens. These predate this branch (`git status landing/` is clean here) and
need a founder copy review (rephrase vs. allowlist as negation). The **canonical
`frontend/` guard is green** — the static landing satellite is the P2 cleanup.
