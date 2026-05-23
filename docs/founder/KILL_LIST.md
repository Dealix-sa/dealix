# قائمة الإلغاء — Kill List

> What gets killed, when, and the log. Kills are a result, not a failure.

## Purpose
Make stopping deliberate. Most founders fail by continuing too long, not by starting wrong. The Kill List is the antidote.

## Owner
Founder/CEO.

## Inputs
- `STRATEGIC_BETS.md` and their stall tokens.
- `OFFER_LADDER.md` performance.
- `PRICING_EXPERIMENTS.md` outcomes.
- Customer or vendor relationships that have drifted.
- Internal processes that no longer serve a layer.

## Outputs
- Append-only kill log: `dealix-ops-private/kills/log.md`.
- Per-kill file: `dealix-ops-private/kills/YYYY-MM-DD_<slug>.md`.

## Rules
1. Every kill has a written reason and one extracted learning. No silent drops.
2. Kills are made in the Weekly or Monthly Review — never mid-day reactively.
3. A killed item cannot be revived for 90 days unless an A3 Go/No-Go gate is run.
4. Killing protects what stays. Limit active bets to 5; killing is the way to fit a new one.
5. Customer relationships are not "killed" — they are off-boarded per `REFUND_POLICY.md`. Use the kill log only for internal items.

## Metrics
- Kills per month: ≥ 1 target (discipline metric).
- Mean stall token at kill: ≤ 3 (don't drag past 3).
- Learning entries extracted: 100% of kills.
- Revivals within 90 days: target 0; tracked as a quality signal.

## Cadence
Reviewed Weekly; finalized Monthly.

## Evidence
`dealix-ops-private/kills/`.

## Verifier
`make kill-verify` — checks each kill in the log has a per-kill file and a learning field.

## Runtime Command
`make kill slug=<slug>`

---

## What can be killed
- A strategic bet that has not produced its success signal by deadline.
- An offer rung that has not generated paid sprints in the last 60 days.
- A pricing experiment past its kill rule trigger.
- An internal process that has 0 verifier hits in 90 days.
- A vendor or tool that has < 1 hour of monthly value but a recurring cost.
- A doc that has not been read or referenced in 6 months (archive, don't delete).

## What cannot be killed casually
- Anything customer-facing with active obligations.
- Anything required for compliance, governance, or trust.
- Anything tied to a refund, complaint, or open A3 decision.
- A north-star metric (it changes only via strategy review).

## Per-kill file template

```
# Kill: <slug>
Date: YYYY-MM-DD
Owner: <founder or named owner>
Class: bet / offer / experiment / process / vendor / doc

## What is being killed
<one paragraph>

## Why now
- Stall tokens: N
- Evidence the success criteria failed:
- Cost of continuing (SAR / hours):

## Learning extracted (one sentence)
<text>

## What this kill protects
<text — usually a bet that gets the freed capacity>

## Revival rule
Not before YYYY-MM-DD (90 days from today) unless A3 gate is run.

## Linked decision file
<path to the original decision file, if any>
```

## Kill log entry format (append-only)
```
YYYY-MM-DD | slug | class | reason-one-line | learning-one-line | revives-after
```

## The dignity of killing
A kill is not an admission of failure; it is the proof that the operating system works. Reviews that produce zero kills over a quarter are themselves a red flag.

## القواعد العربية
1. لكل إلغاء سبب مكتوب ودرس واحد مستخلَص.
2. الإلغاء يُتخذ في المراجعة، لا تفاعليًا.
3. المُلغى لا يُحيا قبل 90 يومًا إلا ببوابة A3.

## Cross-links
- `docs/strategy/STRATEGIC_BETS.md`
- `WEEKLY_CEO_REVIEW.md`
- `MONTHLY_STRATEGY_REVIEW.md`
- `GO_NO_GO_DECISION_SYSTEM.md`
