# Dealix — Paid-Launch Readiness Verdict (2026-06-06)

> تقرير جاهزية الإطلاق المدفوع — قرار Go / No-Go مبني على أدلة مُقاسة.
> Point-in-time, evidence-based verdict. Pairs with the standing checklist in
> [`PUBLIC_LAUNCH_GO_NO_GO.md`](PUBLIC_LAUNCH_GO_NO_GO.md) and
> [`LAUNCH_GATES.md`](LAUNCH_GATES.md). Doctrine: *no measured claim without
> source evidence.*

## Scope of this session

Closed the genuine remaining gaps on the real paying-customer money path and
re-ran the canonical verification bundle. Everything else (ZATCA Phase-2
issuance, refund state machine, reconciliation, GTM/content/legal, pricing
registry) was already implemented and was **not** duplicated.

## Verdict

| Layer | State | Evidence |
|-------|-------|----------|
| Code-level canonical gates | ✅ GREEN | `make prod-verify` → env-check, security-smoke, api-contract-check, dependency-inventory, release-manifest all pass |
| Money-path return page | ✅ CLOSED | `apps/web/app/checkout/return/` — `npm run build` compiles `/checkout/return` |
| Payment status endpoint | ✅ CLOSED | `GET /api/v1/checkout/status` (public, non-PII) + tests |
| Revenue proof (L5) on paid | ✅ CLOSED | webhook records a sourced `payment_confirmed` proof event + tests |
| Doctrine guards | ✅ GREEN | `pytest tests/test_no_*.py tests/test_commercial_doctrine.py` |
| Live-deployment probe | ⏳ FOUNDER_ACTION | `v5-verify` probes `https://api.dealix.me` with prod API keys — needs the live deploy + keys |
| Payment / ZATCA secrets | ⏳ FOUNDER_ACTION | env vars below, by design (NO_LIVE_CHARGE) |

**Overall: GO on code; the remaining items are founder/ops env actions, not
code defects.** The system stays safe-by-default (`DEALIX_MOYASAR_MODE` manual,
`ZATCA_SANDBOX=true`) until those secrets are set.

## What was changed this session

1. **`GET /api/v1/checkout/status`** (`api/routers/pricing.py`) — authoritative
   payment status (Moyasar API → `PaymentRecord` fallback → `pending`). Returns
   only `{state, paid, amount_sar, plan, reference}` — no PII. Added to the
   public-path allowlist (`api/security/api_key.py`).
2. **Checkout return page** (`apps/web/app/checkout/return/`) — the Moyasar
   redirect target (`{APP_URL}/checkout/return`) previously 404'd. Now an
   AR-first bilingual success / pending / failed page that polls (1).
3. **L5 revenue proof event** — on a confirmed `paid` webhook, a sourced
   `payment_confirmed` event is appended to the proof ledger
   (`evidence_source=moyasar://payment/<id>`, `consent_for_publication=False`).
4. **`scripts/security_smoke.py`** — corrected pre-existing false positives:
   `.env*.example` templates are allowlisted; `tests/` fixtures and obvious
   repeated-char placeholders (`sk_live_xxxx…`) no longer trip the live-token
   scan. Real deployed source remains fully scanned; gitleaks stays the
   dedicated scanner for `tests/`.

Tests: `tests/test_checkout_status_and_proof.py` (6) + existing payment/doctrine
suites — all green.

## Remaining FOUNDER_ACTION before flipping to live paid

Set in Railway (or the production secret manager) — keep out of git:

- `MOYASAR_SECRET_KEY`, `MOYASAR_WEBHOOK_SECRET` (and the matching secret in the
  Moyasar dashboard → Webhooks)
- `DEALIX_MOYASAR_MODE=live` (explicit opt-in past the NO_LIVE_CHARGE gate)
- `ZATCA_CSID`, `ZATCA_SECRET`, `ZATCA_SELLER_VAT_NUMBER`, `ZATCA_SANDBOX=false`
  (for real e-invoice clearance)
- `APP_URL` (so the Moyasar callback resolves to the live return page)
- Core: `DATABASE_URL`, `APP_SECRET_KEY`, `ENVIRONMENT`, `CORS_ORIGINS`,
  `ADMIN_API_KEYS`; Frontend: `NEXT_PUBLIC_API_URL`

Then run, against the live deploy:
- `BASE_URL=https://api.dealix.me make v5-verify`
- `python scripts/verify_moyasar_e2e.py` → expect `MOYASAR_E2E_VERDICT=PASS`
- `python scripts/verify_paid_launch_readiness.py --strict`

## How to re-verify locally (no secrets needed)

```bash
make prod-verify                  # code gates (v5-verify needs live API)
pytest tests/test_checkout_status_and_proof.py \
       tests/test_no_*.py tests/test_commercial_doctrine.py -q
(cd apps/web && npm run build)    # /checkout/return compiles
```
