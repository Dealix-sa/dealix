# Frontend `NEXT_PUBLIC_*` policy

`scripts/verify_railway_readiness.py` enforces this policy.

## Rule

Any environment variable prefixed `NEXT_PUBLIC_` is shipped to the browser
and visible to every visitor. Treat them as **public**.

The verifier **fails** if it finds a reference in `frontend/src/**` to a
`NEXT_PUBLIC_*` name containing any of the following:

- `TOKEN`
- `SECRET`
- `API_KEY`
- `ADMIN_KEY`
- `PASSWORD`

Exceptions are the explicitly public SaaS keys (PostHog, Moyasar
publishable, Sentry DSN, base URL, app env) declared in
`PUBLIC_FRONTEND_NAMES_OK` inside the verifier.

## Allow-list (tech debt — must be removed before live sending real workloads)

The following files reference `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` and/or
`NEXT_PUBLIC_DEMO_API_KEY`. They predate the policy and are accepted as
**WARN** rather than **FAIL** so the certification gate can still pass.

Each file MUST move to a backend proxy (Next.js API route → FastAPI) before
production sending is enabled for any real customer workload.

- `frontend/src/components/brand/PublicLaunchShell.tsx`
- `frontend/src/components/business/BusinessNowContent.tsx`
- `frontend/src/components/gtm/FounderCommandCenter.tsx`
- `frontend/src/components/gtm/OpsPartnersPanel.tsx`
- `frontend/src/components/gtm/OpsHubHealthCards.tsx`
- `frontend/src/components/gtm/OpsTargetingPanel.tsx`
- `frontend/src/components/revenue-autopilot/OpsConsoles.tsx`
- `frontend/src/components/services/SprintToolsPanel.tsx`
- `frontend/src/lib/api.ts`

## Adding a new public variable

Edit `scripts/verify_railway_readiness.py` and add the variable to
`PUBLIC_FRONTEND_NAMES_OK` ONLY if the value is genuinely safe to ship to
every browser (no privileged backend access).

## Removing a file from the allow-list

Remove the bullet above; the next CI run will FAIL until the file no
longer references the secret-looking `NEXT_PUBLIC_*` name. Then close the
loop by routing the call through a server-side proxy.
