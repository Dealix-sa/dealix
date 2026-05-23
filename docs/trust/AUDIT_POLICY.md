# Audit Policy — سياسة التدقيق

## Purpose
Define the cadence and scope of internal audits across delivery, trust, AI governance, and learning. Audits are how we catch drift before clients do.

## Owner
Founder.

## Inputs
- Public docs/ tree.
- Sprint folders under `docs/audit/sprints/`.
- Registers under `docs/trust/registers/`.
- AI inventory under `docs/ai_management/`.

## Outputs
- Audit report per cycle written to `docs/trust/registers/audits/<date>.md`.
- Findings list with owner and deadline.

## Rules (numbered)
1. Weekly audit: scanner runs, claim-register spot check, A3 log review.
2. Monthly audit: sprint folder completeness, autonomy levels, evidence-system review.
3. Quarterly audit: end-to-end methodology review, public-private boundary sweep, AI risk register update.
4. Auditor is rotated; never the same person two cycles in a row at the same scope.
5. Findings are not closed verbally. Every finding gets a written remediation and a closing signature.
6. Audit findings feed the monthly strategy update.

## Metrics
- Audits completed on schedule (target 100).
- Findings open longer than 30 days (target 0).
- Repeat findings per quarter.

## Cadence
Weekly, monthly, quarterly. See scopes above.

## Evidence (paths)
- `docs/trust/registers/audits/`
- `docs/learning/MONTHLY_STRATEGY_UPDATE.md`

## Verifier
Founder for quarterly audits. Head of Delivery for weekly and monthly.

## Runtime Command
`make trust.audit.run SCOPE=<weekly|monthly|quarterly>` runs the scoped audit scripts and writes the audit file.

## Scope per cadence

**Weekly.**
- Banned-phrase scan across docs/.
- Claim register spot check on 10 random claims.
- A3 log review for completeness.
- Open incident review.
- Sprint gate status across active sprints.

**Monthly.**
- Sprint folder completeness audit (every sprint closed in the month).
- Autonomy level review for every agent in the inventory.
- Evidence system: dead-link rate, stale-evidence rate.
- Banned-phrase rule effectiveness.
- Case study consent records reconciled with published cases.

**Quarterly.**
- Methodology end-to-end review with one full sprint replay.
- Public-private boundary sweep.
- AI risk register update.
- Sector report methodology review.
- Approval matrix review (any classes added, removed, refined).
- Trust posture report to the founder.

## Audit artifact

Each audit produces one markdown file with:
- Scope.
- Method (what was checked, how).
- Findings (numbered).
- Owners (per finding).
- Deadlines (per finding).
- Sign-off (auditor + verifier).

## Operating substance
Audits are the muscle that prevents the slow drift between what Dealix says it does and what Dealix actually does. The drift is always small in any given week; over a quarter, unaudited drift becomes the gap that turns into a public failure.

The rotation rule matters. The same auditor in the same scope will develop blind spots within two cycles. Rotation does not require a large team; even alternating between the founder and the Head of Delivery for the monthly scope is sufficient at this stage.

Findings are written in plain language. "Three of ten sprints in March were missing the QA log countersignature" is more useful than "QA log compliance was suboptimal". Plain language survives translation into checklist updates.

Audits feed strategy. The monthly strategy update reads the audit findings before it reads anything else. This means audit quality directly affects strategic decisions. We invest in audits because they are the highest-leverage input to direction-setting.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
