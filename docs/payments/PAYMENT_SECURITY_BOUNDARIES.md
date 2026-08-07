# Payment security boundaries

## Hard rules
- Dealix code never stores PAN (primary account number).
- Dealix code never logs PAN.
- Dealix code never receives webhook payloads with PAN.
- Dealix code never proxies payment forms.

## Stubs
`integrations/payments/*_stub.py` exist to:
- Define the function signatures.
- Document the env vars required for live activation.
- Make the integration plan reviewable in PRs.

They do NOT call any provider.

## Activation gates
Before flipping a stub to a real implementation:
1. Security review of the activation diff.
2. Confirm `MOYASAR_SECRET_KEY` / `STRIPE_SECRET_KEY` are in the secret manager, NOT the repo.
3. Webhook signature verification implemented before any state mutation.
4. Customer SOW explicitly permits the integration.
5. Founder signs off on the PR.

## Rotation
- Keys rotated quarterly.
- Webhook secrets rotated whenever a new endpoint is exposed.
- Old keys revoked from the provider immediately after rotation.

## Logging
- Provider name + amount + status + timestamp: yes.
- Customer ID: yes (their own ID, not card details).
- Card number / CVV / expiry: never.

## Incident response
If a real or suspected payment incident is detected: pause the affected stub, notify the customer within 72h, run `scripts/security_review.py`, and engage external counsel if PII or financial loss is involved.
