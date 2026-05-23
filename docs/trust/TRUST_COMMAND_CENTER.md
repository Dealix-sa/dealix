# Trust Command Center — مركز قيادة الثقة

## Purpose
Single dashboard view of Dealix's trust posture at any moment: approvals pending, open incidents, claims under review, audit status. The founder opens this file daily.

## Owner
Founder. Backup: Head of Delivery.

## Inputs
- Open A3 approvals from `docs/trust/APPROVAL_MATRIX.md`.
- Open incidents from `docs/trust/INCIDENT_RESPONSE.md` register.
- Pending claim reviews from `docs/trust/EVIDENCE_SYSTEM.md`.
- Audit calendar from `docs/trust/AUDIT_POLICY.md`.

## Outputs
- Daily dashboard snapshot.
- Weekly trust posture summary into `docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md`.

## Rules (numbered)
1. Every A3 approval is logged with requester, request, decision, decider, timestamp.
2. Open incidents are listed with severity and owner. None go silent for more than 24h.
3. Claims in public materials must be linked to evidence before publish.
4. The dashboard is reviewed daily by the founder and weekly with the leadership group.
5. No exceptions for "small" trust violations. Sev-3 still gets logged.
6. Banned phrases detected in any published material trigger Sev-2.

## Metrics
- Open A3 count and median age.
- Open incident count by severity.
- Claim coverage: % of public claims with linked evidence.
- Audit completion rate against the calendar.

## Cadence
Daily glance, weekly written summary, monthly audit roll-up.

## Evidence (paths)
- `docs/trust/registers/a3_log.md`
- `docs/trust/registers/incident_log.md`
- `docs/trust/registers/claim_review_log.md`

## Verifier
Founder.

## Runtime Command
`make trust.dashboard` — prints the current dashboard with counts and ages.

## Dashboard sections

**Section A — A3 approvals.** Table of currently pending A3 requests. Columns: request ID, requester, action class, requested at, decider, status, decision timestamp.

**Section B — Open incidents.** Table by severity. Columns: incident ID, severity, opened at, owner, status, last update, target close.

**Section C — Claims under review.** Public claims newly added or modified in the last 14 days. Columns: claim ID, source doc path, evidence path, reviewer, status.

**Section D — Audit calendar.** Upcoming audits in the next 30 days. Owner, scope, scheduled date.

**Section E — Banned-phrase scans.** Last scan timestamp across `docs/`, hits found, action taken.

**Section F — Autonomy posture.** Current per-agent autonomy levels from `docs/ai_management/AI_HUMAN_OVERSIGHT.md`. Anything raised in the last 30 days flagged for review.

## Operating substance
Trust does not maintain itself. The Command Center exists because trust signals are otherwise scattered across files, threads, and memory. Pulling them into one daily view is what allows the founder to act on patterns instead of incidents one at a time.

The daily glance is not optional. It is a five-minute discipline that prevents the slow drift where small issues accumulate until one of them becomes a public problem. The weekly written summary is the artifact that feeds the strategy update.

The dashboard is a mirror, not a control surface. Actions are taken in the underlying registers (A3 log, incident log, claim review log). The dashboard reflects state; it does not change it. This separation prevents the dashboard from becoming a place where things "look fine" while the registers tell a different story.

Anything that touches the public reputation of Dealix runs through this view first. New case study, new website copy, new sector report, new sales asset — all of them have a claim-review row before publish. If the row is open, the asset does not ship.

The Command Center is also the place where autonomy decisions get visibility. Raising an agent from A1 to A2 is a trust decision; it appears on the dashboard until it is reviewed and either ratified or rolled back.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
