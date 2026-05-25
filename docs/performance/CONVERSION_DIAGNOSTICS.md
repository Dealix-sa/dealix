# Conversion Diagnostics

How to read the funnel and find the bottleneck.

## 1. Funnel stages (canonical)

```
Sourced  →  ICP-matched  →  A-priority  →  Draft queued  →  Approved  →  Sent  →
Reply  →  Positive reply  →  Sample request  →  Proposal  →  Payment  →
Delivered  →  Renewed
```

## 2. Per-stage diagnostic

| Stage drop                              | Likely cause                                                 | First fix                                  |
|-----------------------------------------|--------------------------------------------------------------|--------------------------------------------|
| Sourced → ICP-matched < 50%             | Sourcing too broad                                           | Tighten ICP filters                        |
| ICP-matched → A-priority < 25%          | Scoring weights miscalibrated                                | Founder-review scoring weights             |
| A-priority → Draft queued < 80%         | Outreach Draft Machine throttled                             | Unblock evidence sources                   |
| Draft queued → Approved < 50%           | Draft quality issue                                          | Re-tune draft prompts; brand verifier      |
| Approved → Sent < 95%                   | Founder bandwidth                                            | Trim approval queue; throttle machines     |
| Sent → Reply < 8%                       | Subject + hook weak; off-persona                             | A/B subject lines; revisit persona match   |
| Reply → Positive < 25%                  | Offer mismatch                                               | Revisit offer-channel-fit matrix           |
| Positive → Sample request < 50%         | Sample friction (asking too early?)                          | Simplify sample request flow               |
| Sample → Proposal < 50%                 | Sample quality                                               | Improve Proof Pack quality                 |
| Proposal → Payment < 30%                | Price/value mismatch or trust gap                            | Strengthen trust note + proof              |
| Payment → Delivered ≠ 100%              | Delivery capacity                                            | Throttle Sales; document failure           |
| Delivered → Renewed < 60%               | Retention signal weak                                        | Retention Expansion Engine                 |

## 3. Decision rule

Pick the **single biggest gap vs. heuristic** (not absolute number). That's the bottleneck.

If two stages are roughly equally weak, pick the **earlier** stage — fixing upstream sometimes resolves downstream.

## 4. Anti-patterns

- Working on multiple bottlenecks at once.
- Optimising a stage that isn't actually the bottleneck.
- Changing the funnel definition mid-quarter (breaks comparability).

## 5. Audit

Every weekly diagnosis writes a one-paragraph note: **"Last week's bottleneck was X. We picked experiment Y. Result Z."**

The notes accumulate in `LEARNING_LOOP.md`.
