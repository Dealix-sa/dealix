# Client Onboarding Playbook

> **Status:** Operating doc for the first 14 days.
> **Companion:** `FIRST_14_DAYS_CLIENT_DELIVERY_AR.md` + `CLIENT_VALUE_REPORTING_AR.md`.

## The 14-day shape

| Day | Activity | Owner | Output |
| --- | --- | --- | --- |
| 1 | Kickoff call | founder + client lead | aligned on scope, success metrics, access |
| 2 | Access setup | client IT | access list complete |
| 3 | Audit re-cap | founder | 1-page summary of the audit findings |
| 4–5 | First implementation sprint | Dealix | routing + tags live |
| 6 | Team training | Dealix + client lead | 60 min training session |
| 7 | First daily digest | Dealix | digest in client's inbox |
| 8 | First review | founder + client lead | 30 min review |
| 9–10 | Second implementation sprint | Dealix | approval queue live |
| 11 | Pilot survey | founder | 1-question survey |
| 12–13 | Tuning | Dealix | based on survey + digest feedback |
| 14 | Pilot review + decision | founder + client lead | continue / pause / pivot |

## The kickoff call (Day 1)

60 minutes. The agenda:

1. **Who is who** (10 min). Names, roles, contact channels.
2. **What we agreed to** (10 min). Re-cap the proposal.
3. **What success looks like** (10 min). The proof metric. The secondary metrics.
4. **What access we need** (10 min). The access checklist. The IT contact.
5. **What the next 14 days look like** (10 min). Walk the day-by-day above.
6. **The next call** (10 min). Schedule Day 8 review + Day 14 decision.

## The access checklist (Day 2)

- [ ] WhatsApp Business read access (with consent record).
- [ ] CRM read access (if applicable).
- [ ] Email read access (if applicable).
- [ ] Shared doc for the audit report.
- [ ] Shared calendar for the reviews.
- [ ] Approval channel (where does the founder review?).
- [ ] Billing channel (where does the payment handoff go?).

## The audit re-cap (Day 3)

A 1-page summary of the audit findings, sent to the client. Structure:

- 10 specific findings (with severity).
- 1 quick win to run this week.
- 1 medium-term fix for week 2.
- 1 long-term direction for week 4+.

## The first implementation sprint (Days 4–5)

- Routing rules drafted.
- Tag taxonomy defined.
- Approval queue stubbed.
- Daily digest format agreed.

## The team training (Day 6)

60 minutes. The agenda:

1. **The routing rules** (15 min). Which thread goes where.
2. **The tag taxonomy** (15 min). What each tag means.
3. **The approval flow** (15 min). How the queue works.
4. **The daily digest** (15 min). What to read, when to act.

## The first daily digest (Day 7)

The first digest is the proof. The client opens their inbox and sees 5 follow-ups they should do today. If the digest is empty, something is broken. If it has 50 items, the threshold is wrong.

## The first review (Day 8)

30 minutes. The agenda:

1. **Did the digest show up?** (5 min).
2. **Are the 5 items right?** (10 min).
3. **What did the team do with them?** (10 min).
4. **What to tune?** (5 min).

## The second sprint (Days 9–10)

- Approval queue in production.
- Daily digest refined.
- First week-end retrospective written.

## The pilot survey (Day 11)

One question: "If you could change one thing about the OS, what would it be?" (Open text, anonymized.)

## The tuning sprint (Days 12–13)

- Apply the survey feedback.
- Tune the routing.
- Tune the digest threshold.
- Write the Day 14 review.

## The pilot review (Day 14)

60 minutes. The decision: continue, pause, or pivot.

The structure:

1. **What worked** (15 min). The 3 specific wins.
2. **What didn't** (15 min). The 3 specific gaps.
3. **The proof metric** (10 min). Did we hit it? Why / why not?
4. **The decision** (10 min). Continue / pause / pivot.
5. **The next step** (10 min). Continue path → expand to the next offer. Pause path → exit gracefully. Pivot path → new scope.

## The exit (if the decision is pause)

- Hand off the configuration.
- Document what was built.
- Offer the renewal conversation in 90 days.
- No hard feelings. No fake case study.

## The renewal (if the decision is continue)

- Move to the next offer in the ladder.
- The pricing model may change (see `docs/offers/PRICING_LOGIC_AND_APPROVAL_POLICY_AR.md`).
- The 14-day cycle repeats for the new offer.

## The escalation

If something goes wrong (missed digest, broken approval, client unhappy), the founder calls the client within 24 hours. No email chains.

## The 5 things to never do in onboarding

1. **Don't skip the kickoff.** It's the alignment moment.
2. **Don't assume access is ready.** Verify on Day 2.
3. **Don't skip the training.** It's the adoption moment.
4. **Don't ship the digest without testing.** Day 7 is the proof.
5. **Don't skip the Day 14 decision.** A pilot without a decision is a leak.

## When to update

- After every 5 onboardings: which day had the most friction?
- After every 10: rewrite the day-by-day based on real timing.
