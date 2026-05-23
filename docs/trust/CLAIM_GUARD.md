# Claim Guard

A pre-publish filter that catches over-claims before any message, proposal, or content goes out.

## Banned claim families
- **Revenue guarantees** — "guaranteed leads", "guaranteed meetings", "guaranteed deals".
- **Compliance guarantees** — "fully compliant", "officially certified", "approved by [regulator]" without proof.
- **Outcome promises with numbers** without "estimated" / "based on" plus source.
- **Speed promises** — "in 24 hours", "overnight results" without scope.
- **Exclusive claims** — "only", "first", "best" without verifiable proof.

## Allowed forms
- "We typically see ..." with a sample size noted.
- "Based on our previous engagements, ..." with a public case study link or anonymous reference.
- "Estimated ..." with a method note.

## Where Claim Guard runs
- Every outbound message.
- Every proposal.
- Every public post (LinkedIn, X, website).
- Every report and outreach pack.

## Process
1. Author runs the check manually or via the linter.
2. Any flagged phrase is rewritten or removed.
3. Edge cases escalate to A2 founder approval.
4. Approved exceptions are logged in `dealix-ops-private/trust/claim_approval_log.csv`.

## Rule
A claim that cannot be defended in a regulator meeting cannot be sent in a DM.
