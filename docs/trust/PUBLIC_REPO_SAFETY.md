# Public Repo Safety

> The rules that keep `voxc2/dealix` safe to be public.
> Enforced by `scripts/verify_public_safety.py` in CI.

## What Must Never Appear In The Public Repo

1. **Client data** — any data attributable to a named or pseudonymous client
2. **Buyer contacts** — emails, phones, LinkedIn URLs of specific real people
3. **Pricing experiments / discounts** — keep in `revenue/pricing_experiments.md` (private)
4. **Win/loss reasoning with client names** — keep in `pipeline/win_loss_log.md` (private)
5. **Founder financial records** — anywhere
6. **API keys, secrets, tokens** — enforced by gitleaks + secret scanning + push protection
7. **Internal Slack/WhatsApp/email content** — anywhere
8. **Sensitive prompts that reveal trade secrets** (per `PRIVATE_DATA_POLICY.md`)
9. **Anything from `clients/`, `revenue/`, `trust/`, `sales/`, `delivery/` paths of the private repo**
10. **Unverified compliance / regulatory claims**

## What's Safe To Be Public

- Architecture docs, methodology, processes
- Approval matrix, claim guard rules, trust policies (templates, not customer-specific)
- Sample artifacts (with `SAMPLE ARTIFACT` header)
- Aggregated learnings (n ≥ 3, anonymized)
- Strategic posture (current quarter focus, principles)
- Code (with no embedded secrets)
- Public claims that pass `claim_guard.py`

## CI Enforcement

`verify_public_safety.py` runs on every PR and checks:

1. **Secret scanning** (gitleaks + native GitHub)
2. **Client data patterns** — long CSVs in non-sample paths; lists matching "company + revenue + buyer name" patterns
3. **Suspicious file types** — `.xlsx`, large `.csv` in unexpected paths
4. **Saudi PII patterns** — phone formats, ID-number-like sequences
5. **Banned paths** — anything matching `clients/` or `pipeline/*.csv` (private-only) — fails the build
6. **claim_guard sweep** — runs over `landing/`, `README*`, `docs/` for banned language

If any check fails → PR blocked.

## Pre-Commit Hook (recommended)

Run locally before pushing:
```
.pre-commit-config.yaml already includes:
- gitleaks
- detect-secrets
- check-merge-conflict
- check-added-large-files
```

Add (if not present):
- `claim-guard-sweep`
- `client-data-pattern-check`

## When CI Catches Something

1. Fix the file (move to private repo if needed)
2. **Do not** rebase to hide the violating commit — git history won't forget
3. If the violation was committed but not yet pushed: amend / drop the commit
4. If pushed: BFG / git-filter-repo to scrub history (rare, requires founder + advisor)
5. Log as SEV-3 incident at minimum (SEV-1 if pushed to public + visible)

## Sanitization Workflow For Sample Artifacts

When prepping a sample from real data:
1. Copy data to a working file in `_sanitization/` (gitignored)
2. Replace identifiers: company names → fictional ("Acme Logistics Co."), people → role only ("Head of Sales"), numbers → ranges
3. Apply `SAMPLE ARTIFACT` header
4. Run claim_guard
5. Founder reviews → approves
6. Move to `content/proof_library/sector/{sector}/`
7. Public-safe path may then be created in public repo `landing/` or similar

## What Founder Must Avoid

- Pasting client emails into PR bodies / issue descriptions
- Pasting screenshots that include client UI / data into public repo
- Writing case studies in public README without explicit consent + sanitization
- Demoing the dashboard with real data on a public live stream
- Linking from public repo to private repo paths (the path itself can be sensitive)

## What This Refuses

- "Just temporarily" public exposure
- "Their data was already public on their website" rationalizations (still requires consent)
- "Nobody will notice this column" optimism
- Force-push to public main to hide violations
- Pull-requesting from a fork that includes client data
