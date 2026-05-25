# No-Overclaim Policy

> We do not claim what we cannot demonstrate.
> Every claim has evidence, or it is not made.

## Forbidden Language (public, contracts, proposals, sales)

- "Guaranteed revenue"
- "Guaranteed leads"
- "Guaranteed [anything outcome-bound]"
- "Best in Saudi Arabia / MENA / world" (without evidence)
- "AI-powered" used as a claim of capability (use only as a description)
- "Fully autonomous" (we are not, and we should not be)
- "100% accurate"
- "Zero human work required"
- "Real-time" (unless the underlying system is actually real-time)
- "Compliant with [regulation]" (unless audited by counsel)
- "Trusted by [N]" (unless N is a counted, named list with consent)
- "Used by [client]" (without explicit written consent)

## Required Language (evidence-bound alternatives)

| Avoid | Use instead |
|-------|-------------|
| "Guarantees X" | "Built to deliver X under [stated conditions]" |
| "Best" | "Built for [specific ICP] with [specific evidence]" |
| "AI-powered" | "Uses [named model] for [specific step]" |
| "Fully autonomous" | "Agents prepare; humans approve" |
| "Real-time" | "Updated [frequency]" |
| "Used by [client]" | (only with written consent + named scope) |
| "Trusted by [N]" | "[N] delivered sprints, [M] approved case studies" |

See `SAFE_LANGUAGE_LIBRARY.md` for the canonical phrase bank.

## Where the policy applies

- Website
- Proposals
- Contracts
- LinkedIn / X / public posts
- Email signatures
- Slide decks
- Case studies
- Product UI text
- Documentation
- Outreach DMs and emails

## Enforcement

- `make audit` greps for forbidden phrases across `docs/` and `frontend/`.
- The Doctrine Verifier CI gate fails the build on detected violations.
- A detected violation is a **Trust Incident** and goes into
  `INCIDENT_RESPONSE.md` triage.

## Founder Personal Discipline

The founder's personal social media is treated as Dealix surface.
Founder posts about Dealix follow this policy.

## Review

Monthly. New industry buzzwords are added to the forbidden list as they
appear if they overclaim.
