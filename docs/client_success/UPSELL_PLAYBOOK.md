# Upsell Playbook — دليل توسيع نطاق الخدمة

## Purpose
Define when and how Dealix proposes scope expansion. Upsell is only proposed after value is proven; never as a default at renewal, never to soften an at-risk situation.

## Owner
Founder. Analyst prepares the proof pack.

## Inputs
- Verified outcome evidence from current engagement.
- Health score from `docs/client_success/CLIENT_HEALTH_SCORE.md`.
- Feedback log expressing unmet needs.
- Productization candidates from `docs/product/PRODUCTIZATION_COMMAND_CENTER.md`.

## Outputs
- Upsell proof pack (≤ 1 page).
- Scope-expansion proposal using `templates/PROPOSAL_*.md.j2`.
- Decision logged: accepted / deferred / declined.

## Gates — All Must Be True Before Proposing
1. Engagement age ≥ 60 days.
2. Health score ≥ 75 for at least 3 consecutive weeks.
3. At least one verified outcome (numbers, not estimates).
4. Client raised an unmet need in feedback (not us guessing).
5. The proposed expansion is a stage-up workflow Dealix has run before (no new bets).
6. Founder has bandwidth (not pushing past `docs/client_success/CLIENT_TIERING.md` Strategic cap).

## The Conversation
- Open with the verified outcome from current engagement.
- Reference the client's stated need.
- Present a focused scope, not a menu.
- Offer one option, with clear deliverables and kill criterion.
- No bundling. No "limited time".

## Rules
1. No upsell to At-Risk or Watch tier clients; resolve first.
2. No discounts to close upsell; outcomes carry the price.
3. No upsell on speculative or new-to-Dealix workflows.
4. The proposal carries the disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
5. Decline recorded honestly; no retries within 60 days unless new evidence emerges.
6. Upsell decision logged in `docs/client_success/CLIENT_SUCCESS_COMMAND_CENTER.md`.

## Metrics
- Upsell proposals per quarter.
- Win rate (target ≥ 40% given the gates).
- Average scope-expansion size.
- Health-score impact 60 days post-upsell (must remain ≥ 70).

## Cadence
- Triggered by gates, not by calendar.
- Reviewed monthly in client success review.

## Evidence
- `evidence/upsell/<client_id>/<YYYY-MM-DD>/` with proof pack and decision.

## Verifier
Founder.

## Runtime Command
`make upsell-check CLIENT=<id>` — verifies all six gates; refuses to draft proposal if any gate fails.

## Arabic Summary — ملخص عربي
لا توسيع نطاق إلا بعد إثبات القيمة. ستة بوابات يجب أن تجتاز قبل عرض التوسيع. لا تخفيضات. لا عروض مفتوحة لعملاء في خانة المراقبة أو الخطر. القيم التقديرية ليست مُتحقَّقة.
