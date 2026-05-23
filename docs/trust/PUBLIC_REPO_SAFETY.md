# Public Repo Safety

> Owner: Founder. Module: `dealix/trust/public_safety.py`. Verifier:
> `scripts/verify_public_safety.py`.

## What this guards against

The public repo must never contain:

- Customer PII (names, emails, phone numbers) of actual prospects or clients.
- Live API keys, IBANs, credit-card-shaped numbers, private keys.
- Internal pricing exceptions, refund decisions, or private call notes.

The scanner allowlists:

- Example domains (`example.com`, `example.sa`, `yourco.sa`, etc.).
- Dealix's own service emails (`security@dealix.me`, etc.).
- Well-known git identities (`git@github.com`, `noreply@github.com`).
- Documented secret format markers when written as `sk_live_xxxxx`,
  `sk_live_...`, `sk_live_<REDACTED>`, etc.
- Placeholder phone numbers ending in `0000000` or `1234567`.

## Forward-looking guard

Every PR that touches a file in the Master Tree manifest is checked. A
single real finding fails the build.

## Acknowledged legacy findings

Two pre-existing files contain founder contact information that pre-dates
the Master Tree. They are tracked in `verify_public_safety.py`'s
`LEGACY_ACKNOWLEDGED` set and are reviewed in the founder's monthly
safety pass rather than the per-PR gate:

- `DEPLOYMENT.md` — references the founder's own email in deployment notes.
- `landing/index.html` — uses the founder's email as a contact handle.

To inspect these (and any other legacy findings) run:

```bash
python scripts/verify_public_safety.py --legacy
```

The `--legacy` report is non-blocking; cleaning each one up is a
separate, founder-approved change.

## Promotion criteria

A file moves out of `LEGACY_ACKNOWLEDGED` once:

1. The PII is replaced with an example/template equivalent, OR
2. The founder explicitly publishes the contact (recorded in
   `dealix/registers/public_claims.yaml`).

## Last reviewed

Set at Master Tree initialization. Next review: 30 days from this commit.
