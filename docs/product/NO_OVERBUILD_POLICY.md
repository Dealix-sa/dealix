# No-Overbuild Policy

> Dealix is a one-founder operation. The single most expensive failure mode is
> **building anything a paying customer didn't ask for**. This policy makes
> that failure mode explicit and refusable.

## The rule

A new feature, framework, dependency, or abstraction may be added if and only
if **all three** are true:

1. **A named paying customer is asking for it** — by name, in writing,
   captured in `founder/decision_queue.md`.
2. **They are paying for it** — a payment, PO, or written approval recorded in
   `revenue/revenue_action_log.csv`.
3. **The build fits in one current sprint** (`docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md`).

If any of the three fails, the answer is **no** — log the request in the
"future sprints" section of `founder/decision_queue.md` and move on.

## Examples

| Request | Verdict | Why |
|---|---|---|
| "Add a Slack integration so we get alerts" | ❌ NO — internal, no customer paid | use existing email / make daily |
| "Customer A paid SAR 7,500 for a Pricing Reset; they need an Arabic version of the deck" | ✅ YES — paying, named, in-sprint | scope already covers it |
| "Let's rewrite the CLI in Rust for speed" | ❌ NO — framework swap, no customer | open issue, do not start |
| "Add a webhook so future customers can self-onboard" | ❌ NO — speculative future | log + park |
| "Customer B requested a custom export format inside their sprint" | ✅ YES — paying, named, in-sprint | ship it |

## Refusals are first-class

When the founder refuses a build, it gets logged in:

```
docs/product/refusals_log.md
```

A refusal log entry has:

- date
- who asked
- what they asked for
- why refused (which of the 3 rules failed)
- what was offered instead (if anything)

Refusals are *evidence of discipline*, not failure. Empty refusal log over 30
days is itself a flag — it means the founder is saying yes too much.

## The exception: trust and safety bugs

The only thing that can be built without the 3-rule check is a fix to:

- A failing `scripts/verify_*.py`.
- A red-list violation in `docs/trust/TRUST_COMMAND_CENTER.md`.
- A live-data leak or secret exposure.

These are not "features". They are restoring the contract Dealix already made.

## How this policy is enforced

- Audit prints "MARKET EVIDENCE" — if it is empty for 30 days, the audit
  refuses to advance the stage even if all verifiers are green.
- Every commit to `dealix/`, `dealix_cli/`, or `execution_engine/` that adds
  new top-level modules should reference the paying customer in the commit
  message.
- `scripts/verify_no_autonomous_external_actions.py` blocks code that adds
  outbound network calls without an explicit approval gate.

## Related

- `docs/founder/GO_NO_GO_DECISION_SYSTEM.md` — how to refuse fast.
- `DEALIX_30_DAY_EXECUTION_PLAN.md` — what is in scope right now.
- `DEALIX_STAGE_GATED_ROADMAP.md` — stages and exit criteria.
