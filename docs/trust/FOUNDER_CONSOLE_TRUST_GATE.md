# Founder Console Trust Gate

The Founder Console (`apps/web/`) is the single human-in-the-loop
control surface for Dealix. Every external-impact action passes through
the gate.

## Guarantees

1. **No write-only buttons.** Every action a founder can click in the
   console results in a recorded decision row in
   `trust/approval_decisions.csv`. There is no "secret" action.
2. **No external send from the frontend.** The frontend never holds API
   credentials for third parties; it can only POST to the internal API.
3. **Failure-closed defaults.** If the internal API is down, all reads
   show `source: "fallback"` and all action buttons return an error.
4. **No raw secrets in the browser.** `DEALIX_INTERNAL_TOKEN` is set on
   the Node process and used server-side.

## Token rotation

The internal token is rotated by changing `DEALIX_INTERNAL_TOKEN` in the
deploy environment. The next Founder Console request will return 401
until the new token is also set in the browser tier; `/security`
surfaces the current `auth_mode`.
