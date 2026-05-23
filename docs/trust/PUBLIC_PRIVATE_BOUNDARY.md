# Public / Private Boundary

> What lives in `docs/` (public) vs `dealix-ops-private/` (private).
> The repository is public-by-default. Private = explicit.

## Public (in this git repo, `docs/`)

- Strategy and operating model files
- Templates and checklists
- Policies and rules
- Pricing **principles** (not customer-specific quotes)
- Sample outputs (anonymised)
- Sector reports we are willing to publish

## Private (gitignored `dealix-ops-private/`, never committed)

- Customer names, emails, phone numbers, contracts
- Pipeline ledger with named accounts
- Financial ledgers (`cash_collected.csv`, etc.)
- Invoices and receipts
- Specific proposals sent
- Outreach drafts before approval
- Founder time logs
- Risk log entries naming customers, partners, or individuals
- Any document containing PII for Saudi residents

## Forbidden in public

- Customer names without written consent
- Customer-specific revenue numbers
- Customer-specific data of any kind
- Personal data of any kind (names, phone, email, ID)
- Internal financial details
- Internal disputes with partners or customers
- Founder personal financial details

## Forbidden in any repo

- Credentials, API keys, tokens
- Secrets baselined in `.secrets.baseline` exempt from this rule only
  because they are not real secrets
- Bank account details
- Tax authority correspondence

## Enforcement

- `.gitignore` excludes `dealix-ops-private/` and all derivative outputs.
- `make audit` scans `docs/` for PII patterns (emails, phone numbers,
  Saudi national ID shapes).
- Secret scanning (GitHub secret scanning + `detect-secrets`) catches
  credentials at push time.
- A T2 approval is required for any case study or LinkedIn post citing
  a named client.

## Process when private data appears in public

1. Stop. Do not push.
2. Remove the data.
3. Rewrite history if already committed (force push only after CEO
   approval).
4. Log the incident in `INCIDENT_RESPONSE.md`.
5. Update the offender file or workflow to prevent recurrence.

## PDPL Discipline

Any document that includes personal data for Saudi residents:

- Has a lawful basis recorded
- Has a retention period
- Has a deletion procedure
- Is stored in `dealix-ops-private/` only
- Is never indexed by any public-facing tool
