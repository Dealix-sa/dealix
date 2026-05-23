# Claim Governance System

## Purpose
Every external claim (LinkedIn post, proposal, sales DM, sector report) is checked for accuracy and proof.

## Claim levels
- **Opinion** — labelled clearly as opinion.
- **Method** — describes our methodology generically.
- **Anonymized case** — sector + role + outcome, no names.
- **Named case** — requires written approval from named party.

## Required for any quantified claim
- Source value (where the number comes from).
- Source date (when it was true).
- Source artifact (the report, the CSV row, the email).

## Review workflow
1. Author drafts claim.
2. Author logs the draft in `trust/claim_review_log.csv` with proof level + source.
3. Founder reviews; sets decision.
4. Only Approved claims may go external.

## Automated check
`scripts/review_content_claims.py` scans content drafts for high-risk patterns (specific numbers without citation, named clients, absolutes).

## Anti-patterns
- "Our customers see 3x improvement" without a CSV row.
- "Trusted by X" when X has not approved that language.
- "Industry-leading" with no benchmark cited.

## Decay
- A claim must be reviewed annually.
- A claim that loses its source artifact is retracted within 30 days.
