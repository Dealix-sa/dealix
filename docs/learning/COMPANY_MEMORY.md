# Company Memory — الذاكرة المؤسسية

## Purpose
Single canonical location where Dealix's decisions, lessons, and outcomes are written. The file the founder will hand to the next operator on day one.

## Owner
Founder.

## Inputs
- Weekly learning decisions.
- Closed sprint reviews.
- Incident closures.
- Quarterly strategy updates.

## Outputs
- Dated entries appended in reverse chronological order.
- Cross-links to source artifacts.

## Rules (numbered)
1. Every decision logged here is dated and specific.
2. Entries are written in past tense for outcomes, present tense for current rules.
3. Reversed decisions are not deleted; they are annotated with the reversal entry and date.
4. PII never appears. Client names appear only when consent exists.
5. Entries are at most 200 words each. Long-form analysis lives elsewhere; the memory points to it.
6. The memory is read at the start of every strategy session.

## Metrics
- Entries per quarter (target greater than or equal to 12).
- Entries with cross-links to source artifacts (target 100).
- Entries that have been re-read in the last quarter.

## Cadence
Append continuously. Read quarterly at the strategy update. Full re-read annually.

## Evidence (paths)
- `docs/learning/COMPANY_MEMORY.md` (this file).
- Cross-linked artifacts under `docs/audit/sprints/`, `docs/trust/registers/`, `docs/learning/EXPERIMENT_SYSTEM.md`.

## Verifier
Founder.

## Runtime Command
`make learning.memory.append TITLE=<t>` opens a new entry skeleton.

## Entry format

```
## YYYY-MM-DD — short title
Decision / Lesson / Outcome (one of these)
Body: 100-200 words. What was decided, why, and what we expect to see.
Source: paths to the underlying artifacts.
Status: active | superseded by <date>
```

## Categories

**Decision.** A specific operating choice. Example: narrow sector focus to two sectors for Q3.

**Lesson.** Something we learned the hard way and want to remember. Example: client-side delays in sending invalidate sprint-level reply-rate comparisons.

**Outcome.** A measurable result from a sprint, experiment, or quarter. Example: 12 sprints closed in Q2 with 11 acknowledgements within 48h.

## Worked example entries (seed)

## 2026-05-01 — Decision: Default pack is build-to-handover

We default to delivering the outreach pack for the client to send, not sending on the client's behalf. Sending-on-behalf is supported only via A3 approval per request. The decision sharpens scope, removes a category of compliance risk, and aligns with the no-overclaim policy.
Source: `docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md`, `docs/trust/AUTONOMY_POLICY.md`.
Status: active.

## 2026-05-10 — Lesson: Two-language messages are not optional

Saudi buyers respond differently to AR and EN messages regardless of corporate norms. Sprints delivered with EN-only or AR-only packs underperformed on operator-perceived quality. AR + EN parallel variants are now mandatory in the outreach pack template.
Source: `docs/delivery/revenue_sprint/OUTREACH_PACK_TEMPLATE.md`.
Status: active.

## 2026-05-15 — Decision: Adopt 1-2-3-5-10 escalation rule

All operational patterns are routed through `docs/learning/LEARNING_ROUTER.md`. The discipline is to count before acting and to act at the right tier.
Source: `docs/learning/LEARNING_ROUTER.md`.
Status: active.

## Operating substance
A company without explicit memory rebuilds the same conclusions every quarter. Dealix avoids this by writing decisions when they are made, not when they are remembered. The 200-word cap forces clarity; the date stamp forces accountability; the source link forces traceability.

The memory is read at the start of every strategy session. This is the discipline that prevents decisions from being silently reversed. A founder who reads a decision from six months ago and disagrees must write the reversal entry, dated. The annotated history is the asset.

The annual re-read is a longer ritual. The founder spends a half-day re-reading the year's entries and marking which are still active, which are superseded, which proved wrong, which proved right. The re-read produces the seed for the annual strategy.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
