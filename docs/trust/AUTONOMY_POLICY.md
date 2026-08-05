# Trust OS — Autonomy Policy

The Autonomy Policy defines what AI inside Dealix may do alone,
what it must do with approval, and what it must never do at all.
It pairs with the Approval Matrix: this policy assigns each AI
capability a level; the matrix says how each level gets approved.

## Purpose
Set the boundary between AI autonomy and founder oversight in
writing, so every AI-prepared action has a known and predictable
approval surface, and so the founder can scale leverage without
losing control.

## Owner
Sami (Founder).

## Review Cadence
Monthly. Updated immediately whenever a near-miss, refusal, or
unexpected behavior happens.

## Inputs
- Capability surface of the AI system (what it can attempt today).
- Risk classification of each capability.
- Incident log (refusals, near-misses, customer feedback).
- Founder's current trust appetite.

## Outputs
- Per-capability autonomy level (L0 / L1 / L2 / L3 / L4).
- Refusal patterns wired into AI prompts.
- Approval-matrix entries for L1/L2/L3 actions.
- Documented changes when autonomy expands or contracts.

## Rules
- A capability operates at exactly one level.
- Levels expand only after evidence: an L1 capability becomes L2
  after a documented period of clean operation, not by assertion.
- Levels contract immediately on any incident, without debate.
- An L4 capability is **prohibited**; there is no escalation path.
- AI must refuse any L4 request and log the refusal.

## Metrics
- Number of capabilities at each level.
- Number of clean weeks per capability (drives promotion).
- Number of refusals logged (target: 100% of L4 attempts).
- Number of capabilities downgraded after incident (the system is
  working when this is non-zero when incidents happen).

## Evidence
- `trust/autonomy_log.md` (private) — per-capability operating log.
- `trust/incident_log.md` (private) — every refusal, near-miss, or
  unexpected behavior.
- `trust/approval_log.csv` (private) — every approved L1/L2/L3
  action.

## Last Reviewed
2026-05-23

---

## The Autonomy Levels

### L0 Manual
- AI does not act. The founder (or an operator) performs the action
  by hand. AI may prepare notes only.
- Examples: signing a contract, sending an irreversible payment,
  responding to a P0 customer escalation in real time.

### L1 Assisted
- AI prepares the artifact; a human reviews and executes.
- Examples: drafting a warm DM, drafting a proposal, drafting a
  public post, preparing a daily command brief.
- Approval level: A1.

### L2 Semi-Auto
- AI prepares and stages; a human approves and AI executes the
  staged action.
- Examples: send a queued post once approved, send a queued
  proposal once approved, refresh a private dashboard.
- Approval level: A1 or A2 depending on action.

### L3 Auto
- AI executes within explicit pre-approved guardrails; the human
  audits after the fact.
- Examples: running an internal verifier, refreshing internal
  caches, generating overnight briefs, archiving artifacts.
- Approval level: A0 (logged, not gated).

### L4 Prohibited
- Capability is **disallowed**, end of story.
- Examples: cold scraping without consent, automated mass outreach,
  sending customer data to unapproved third parties, fabricating
  evidence, bypassing QA, making guarantees without proof,
  impersonating the founder externally.
- AI must refuse and log every L4 attempt.

---

## Capability → Level Lookup

| Capability                                | Level | Approval |
|---                                        |---    |---       |
| Generate daily command brief              | L3 Auto       | A0       |
| Generate weekly intelligence review draft | L3 Auto       | A0       |
| Refresh internal scorecard draft          | L3 Auto       | A0       |
| Draft a warm DM                           | L1 Assisted   | A1       |
| Draft a public post                       | L1 Assisted   | A1       |
| Draft a Rung 1–2 proposal                 | L1 Assisted   | A1       |
| Draft a Rung 3+ proposal                  | L1 Assisted   | A2       |
| Send a queued, approved message           | L2 Semi-Auto  | A1/A2    |
| Ship a customer deliverable               | L1 Assisted   | A2       |
| Change a price in a proposal              | L1 Assisted   | A2       |
| Change the offer ladder                   | L0 Manual     | A3       |
| Change the approval matrix                | L0 Manual     | A3       |
| Change this autonomy policy               | L0 Manual     | A3       |
| Cold scrape / mass outreach               | L4 Prohibited | Never    |
| Send customer data to third party         | L4 Prohibited | Never    |
| Make a guarantee without evidence         | L4 Prohibited | Never    |
| Bypass QA checklist                       | L4 Prohibited | Never    |

---

## Promotion / Demotion Rules

**Promotion** (L1 → L2, L2 → L3):
- Capability has operated cleanly for 4 consecutive weeks.
- No incidents in `trust/incident_log.md` against the capability.
- Founder explicitly signs off on the promotion at A3.

**Demotion** (any level → lower level):
- Triggered automatically on any incident attributable to the
  capability.
- No debate, no exceptions; the demotion happens first, the review
  happens at the next Weekly CEO Review.

**Prohibition** (any level → L4):
- Triggered when a capability has caused customer harm, trust
  damage, or a Never-class incident.
- Once L4, the capability stays L4 until and unless an A3
  decision (with full evidence pack and rollback plan) restores it.

---

## Failure Modes To Watch
- Levels drifting upward silently → audit lookup table monthly.
- Refusals not logged → assume L4 attempts are happening; fix
  logging first.
- Promotions without the 4-week clean record → reset and start
  the clock again.
- L4 attempts treated as "interesting questions" → they are P0
  incidents; treat as such.
