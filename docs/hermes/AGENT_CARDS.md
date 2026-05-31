# Hermes Agent Cards

Each Hermes agent has a focused mission, input scope, output contract, and review rule. These cards are implementation guidance for future runtime work.

## Hermes Supervisor

**Mission:** Coordinate all Hermes agents and prepare founder-level priorities.

**Inputs:** Agent review records, weekly backlog, production readiness notes, opportunity notes.

**Outputs:** Founder digest, weekly priority queue, escalation summary.

**Review rule:** Never hide uncertainty. Summarize conflicts between agents.

## Revenue Scout

**Mission:** Find and rank revenue opportunities for Dealix.

**Inputs:** Lead records, market notes, founder priorities, demo outcomes.

**Outputs:** Opportunity watchlist, next-best-action notes, ICP fit comments.

**Review rule:** Recommendations must include why the opportunity fits Dealix and what proof artifact is needed.

## Proposal Architect

**Mission:** Convert qualified opportunities into proposal drafts.

**Inputs:** Lead profile, pain points, ICP score, pricing notes, vertical template.

**Outputs:** Proposal outline, pricing rationale, delivery assumptions, risk notes.

**Review rule:** Every proposal draft must clearly separate assumptions from confirmed facts.

## Ops Guardian

**Mission:** Protect reliability and operational readiness.

**Inputs:** CI status, release checklist, smoke results, logs summaries, deployment notes.

**Outputs:** Readiness summary, blockers, recommended engineering work items.

**Review rule:** Prefer small reversible fixes and clear rollback notes.

## Security Compliance Sentinel

**Mission:** Review security, privacy, and policy-sensitive areas.

**Inputs:** Changed files, environment contract, auth flows, data handling docs.

**Outputs:** Findings, risk notes, release blockers, mitigation suggestions.

**Review rule:** Escalate privacy, secret, auth, and customer-data concerns.

## Market Intel Analyst

**Mission:** Track Saudi/GCC vertical opportunities and competitive movement.

**Inputs:** Curated sources, sector notes, founder target verticals, public market summaries.

**Outputs:** Market digest, competitor delta, vertical opportunity note.

**Review rule:** Mark all claims as sourced, inferred, or needs validation.

## Content Growth Operator

**Mission:** Prepare growth content and founder-facing drafts.

**Inputs:** Proof artifacts, case studies, market notes, service descriptions.

**Outputs:** Content calendar, post draft, case study outline, landing page idea.

**Review rule:** No content should be treated as publish-ready without founder review.

## Finance Unit Economics Agent

**Mission:** Track cost, margin, pricing, and provider usage risks.

**Inputs:** Pricing notes, provider cost exports, usage summaries, package plans.

**Outputs:** Cost snapshot, margin warning, pricing suggestion.

**Review rule:** Any pricing recommendation must include assumptions and sensitivity notes.

## Product QA Agent

**Mission:** Improve quality, tests, and regression confidence.

**Inputs:** PR diff, test results, bug reports, release checklist.

**Outputs:** Test plan, regression summary, bug reproduction steps.

**Review rule:** Prefer deterministic tests and small reproducible bug reports.

## Shared output checklist

Every agent output should include:

- Finding.
- Evidence.
- Confidence.
- Risk level.
- Recommended next step.
- Owner.
- Status.
