# Evidence System

> "Evidence" is not a vibe. It is a link to a verifiable artifact.
> If a claim has no evidence link, we do not make the claim.

## What counts as evidence

| Claim type | Required evidence |
|-----------|-------------------|
| "We delivered N sprints" | A signed-off Proof Pack per sprint |
| "Client X is a customer" | Written consent from client to be named, plus a paid invoice |
| "Reply rate was Y%" | A ledger entry counting DMs sent and replies received |
| "Saudi market data" | A cited source with date and URL |
| "We are PDPL-aware" | A privacy policy + DPIA template + processing log |
| "Compliance with [regulation]" | An audit report or counsel sign-off |

## Evidence Tags

Every customer-facing artifact tags claims with evidence:

```
> Built 5 Sprints in Q1 [evidence: sprint_register#Q1].
> Reply rate of 22% over the last 30 days [evidence: outreach_ledger#30d].
> Trusted by [Client] [evidence: consent_letter_2026-03-15.pdf].
```

In customer-facing PDFs and documents, evidence references are written
in a footer or appendix.

## Evidence Ledgers

Maintained in `dealix-ops-private/trust/`:

- `sprint_register.csv` — every sprint, scope, delivered date, paid amount
- `outreach_ledger.csv` — DMs sent, replies received, by day
- `consent_letters/` — written consent from any named client
- `incident_log.md` — every trust incident with root cause
- `audits/` — periodic audit outputs

## Evidence Audit

Quarterly: `make audit` plus a manual audit:

- Pick 5 public claims at random.
- Find the evidence link for each.
- If no evidence: remove the claim or downgrade the language.

## Anti-Patterns

- "Generally", "typically", "usually" used to soften an unsupported claim.
- "Industry standard" used to imply a benchmark we did not measure.
- "Clients see X" used to imply a sample of clients we do not have.

## Evidence Hierarchy

Strongest → weakest:

1. **Documented and signed off** by a customer
2. **Counted ledger entries** in our private operational data
3. **Cited third-party source** with date and URL
4. **Founder professional judgement, labelled as such**

Anything weaker than (4) is **not** evidence and must not be presented
as such.
