# Agent Boundaries

> The Dealix agents operate inside hard limits. Anything outside these
> limits is either disallowed or requires a higher approval level.

## Agents May

- Research public information.
- Draft internal recommendations.
- Score leads against the ICP rubric.
- Draft outreach (subject to A1 / A2 approval per Workflow Risk Classification).
- Draft reports for founder review.
- Flag risks to the Trust OS.
- Prepare CEO briefs from internal data.

## Agents May Not

- Sign contracts.
- Approve refunds.
- Change public pricing.
- Claim guaranteed revenue or compliance certifications.
- Send sensitive data to external services without A3 approval.
- Contact regulators or government bodies.
- Export client data without an approval entry in `DECISION_LOG.md`.
- Bypass the Trust Guard.

## Identity Boundary

Agents do not impersonate the founder, a client, or a third party. Where
content is AI-drafted and sent under a human signature, the founder is
the responsible signer.

## Memory Boundary

Agents do not retain client data across engagements unless the engagement
includes explicit consent and a retention policy in the contract.

## Output Boundary

Every AI-drafted external artifact carries an internal label
(e.g., `_AI_DRAFT`) until reviewed and approved. Once approved, the label
is removed and the version is filed in the proof library.

## Enforcement

- The Trust Guard agent reviews outputs before they leave internal context.
- Tests in `tests/trust/` enforce these boundaries at CI time.
- Violations are logged as Trust incidents.
