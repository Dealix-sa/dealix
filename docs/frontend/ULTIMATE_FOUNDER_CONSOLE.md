# Ultimate Founder Console

Next.js app under `apps/web`. Pages live in `app/<route>/page.tsx`.

- `app/page.tsx` — landing page with links.
- `components/founder-shell.tsx` — shared shell + nav + source badge.
- `lib/dealix-runtime.ts` — read client, returns safe fallback.
- `lib/dealix-actions.ts` — action client, POSTs to internal API.

Every page is a server component that calls a `getX()` helper. If the
backend is down the fallback envelope still renders the UI; the source
badge surfaces `fallback` so we never claim live data.

The frontend runs in dev with `npm --prefix apps/web run dev`
(port 3100) and builds with `npm --prefix apps/web run build`.
