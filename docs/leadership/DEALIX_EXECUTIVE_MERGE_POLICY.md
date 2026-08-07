# Dealix Executive Merge Policy

## Rule 1 — No direct main pushes

All material changes must go through:

branch → tests → PR → checks → squash merge

Direct pushes to main are only allowed for emergency recovery and must be documented.

## Rule 2 — Do not bulk-merge draft PRs

Draft PRs must be classified into:

- merge after rebase/test
- extract docs only
- extract tests only
- superseded
- close/archive

## Rule 3 — Source of truth

Dealix must not become a file museum. Every merge must strengthen one of:

- company-day
- command-room
- revenue loop
- controlled outbound with approval gates
- client delivery
- website conversion
- trust/compliance
- production readiness

## Rule 4 — External sending

No uncontrolled external send.

Allowed only when all gates exist:

- approval
- verified target
- source_url
- unsubscribe / opt-out
- rate limits
- logs
- no fake ROI
- no fake testimonials
- WhatsApp opt-in/template gates

## Rule 5 — Founder operating priority

The business priority is:

1. Production health
2. Company-day runs
3. Command room works
4. Revenue loop generates reviewable drafts
5. Founder sends manually
6. First beta client
7. Proof pack
8. Retainer
