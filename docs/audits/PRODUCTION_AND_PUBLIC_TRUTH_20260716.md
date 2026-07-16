# Dealix production and public truth — 2026-07-16

## Executive decision

Do not treat `dealix.vercel.app` as the canonical Dealix production backend. The verified production topology is currently:

- public static site: `https://dealix.me` on GitHub Pages;
- canonical API: `https://api.dealix.me` on Railway;
- Vercel project: FastAPI preview/runtime validation surface, with no `dealix.me` custom domain attached.

The Vercel placeholder-secret failure is real, but it is not evidence that the Railway API is down. Issue #914 should be re-scoped before it blocks the commercial launch sequence.

## Verified evidence

| Surface | Result | Evidence |
| --- | --- | --- |
| Repository source of truth | `main` at `61b7c34b37be3933a6f7c70fa94c6902db7c260d` | local clone of `Dealix-sa/dealix` |
| Railway liveness | HTTP 200 | `GET https://api.dealix.me/healthz` |
| Railway deploy identity | `git_sha=8099b00`, `env=production` | `/healthz`, `/version`, `/api/v1/meta` |
| Railway drift | deployed commit is 930 reachable commits behind current `main` | `git rev-list --count 8099b00..61b7c34` |
| Public website | HTTP 200, Dealix AI Operating Team content | `GET https://dealix.me/` |
| Public website host | GitHub Pages | response header `server: GitHub.com` |
| Public website `/health` | HTTP 404 | expected for the present static host; not an API liveness signal |
| Vercel project | framework `fastapi`, `live=false` | connected project inspection |
| Vercel domains | Vercel aliases only | `dealix.vercel.app`, `dealix-wwwdelaixme.vercel.app`, `dealix-git-main-wwwdelaixme.vercel.app` |
| Vercel alias runtime | HTTP 500 | `FUNCTION_INVOCATION_FAILED` |
| Vercel root cause | production `APP_SECRET_KEY` is still the default placeholder | grouped runtime error; no value inspected or recorded |
| Vercel previews | latest PR #923 preview deployments are `READY` | latest deployment metadata, target is Preview |
| Live pricing contract | 499 SAR managed pilot, 7 days, plus three subscription plans | `GET https://api.dealix.me/api/v1/pricing/plans` |
| Pending commercial contract | PR #923 proposes a 30-day pilot with price hidden until founder approval | PR #923 body and branch diff |

## Source-of-truth blockers

1. **Deployment drift:** the canonical Railway API is healthy but far behind the repository.
2. **Offer conflict:** production exposes the 499 SAR / 7-day offer while PR #923 proposes 30 days and no public price.
3. **Frontend topology drift:** repository runbooks describe a Next.js production frontend, while `dealix.me` is currently the static landing on GitHub Pages.
4. **Vercel ambiguity:** the Vercel project validates previews but its production alias is unhealthy and is not attached to the public custom domain.
5. **Public claim debt:** the static landing contained unverified numeric benchmarks and absolute delivery claims. This branch replaces them with measurable, approval-bound language and adds a regression contract.

## Safe execution order

1. Merge only claim-safe, non-overlapping fixes after CI review.
2. Resolve PR #923 review/CI issues and choose one canonical pilot contract before publishing or charging.
3. Approve a controlled Railway deployment of a known main SHA; apply migrations only through the existing release policy.
4. Verify `/healthz`, `/version`, `/api/v1/meta`, pricing, authenticated staging paths, and rollback evidence.
5. Decide whether the public frontend remains static GitHub Pages or moves to the repository Next.js surface.
6. Only if Vercel remains an approved production runtime: rotate the four Vercel production secrets directly in Vercel, redeploy, and record names/statuses only.
7. Re-scope or close #914 based on the approved topology; do not let a non-canonical Vercel alias misrepresent Railway production health.

## Approval gates

- No production deployment was triggered.
- No environment variable or secret was read, rotated, or printed.
- No DNS or domain binding was changed.
- No price, checkout, payment, outbound message, public proof, or customer commitment was changed.
- No merge to `main` was performed.
