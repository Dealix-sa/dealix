# Revenue KPI Tree

The KPI tree is the **single map** of how Dealix tracks revenue health. Every machine, every agent, every experiment ladders into this tree.

## 1. The tree

```
                                Paid SAR / month
                                       |
            ──────────────────────────────────────────────
            |                          |                  |
   New customer SAR        Expansion / retention SAR   Partner SAR
            |
   ─────────────────────
   |        |          |
 Sprint   Pilot     Retainer
   |        |          |
   ─────── deals closed ───────
                  |
            ─────────────
            |             |
       Proposal sent     Reply positive
            |                    |
            ────────────────
                    |
              Draft approved
                    |
              Draft queued
                    |
            A-priority account
                    |
            ICP-matched account
                    |
            Sourced lead
```

## 2. Canonical KPIs (per week, unless noted)

| KPI                                  | Definition                                          | Target heuristic            |
|--------------------------------------|------------------------------------------------------|-----------------------------|
| Sourced leads                         | New accounts entering the pipeline                  | 10–20                       |
| ICP-matched                          | Sourced leads matching the ICP                       | ≥ 50% of sourced            |
| A-priority accounts                  | Sourced leads with priority A                        | 2–5                         |
| Drafts queued                        | Outreach drafts queued for founder review            | ≥ 5                         |
| Approval rate                        | Approved / queued                                    | ≥ 60%                       |
| Sent / draft rate                    | Externally sent / approved                           | tracked, founder-controlled |
| Reply rate                           | Replies / sent                                       | ≥ 10%                       |
| Positive reply rate                  | Positive replies / replies                           | ≥ 30%                       |
| Sample requests                      | Diagnostic / sample requests                          | ≥ 1                         |
| Proposal sent                        | Proposals sent (after founder approval)              | ≥ 1                         |
| Payment conversion                   | Invoiced / proposal sent                             | ≥ 30%                       |
| Delivery success                     | Sprints delivered with documented outcome / started  | ≥ 90%                       |
| Retention (M2 active / M1 paid)      | Monthly                                              | ≥ 70%                       |
| Proof artefacts published            | Per quarter                                          | ≥ 4                         |
| Referrals booked from delivered work | Per quarter                                          | ≥ 2                         |

## 3. Snapshot format

Each weekly snapshot writes a markdown block:

```
## KPI snapshot — week of YYYY-MM-DD

| KPI                        | Value     |
|----------------------------|-----------|
| Sourced leads              |           |
| ICP-matched                |           |
| A-priority accounts        |           |
| Drafts queued              |           |
| Approval rate              |           |
| Reply rate                 |           |
| Sample requests            |           |
| Proposal sent              |           |
| Payment conversion         |           |
| Delivery success           |           |
| Retention                  |           |
| Proof artefacts            |           |
| Referrals                  |           |
| Bottleneck                 |           |
```

## 4. Bottleneck rule

We pick the **single smallest leak** in the funnel and name it as the bottleneck for the week. Every experiment that week aims at that bottleneck.

## 5. Doctrine

- We do not change KPI definitions without founder + product co-sign.
- Targets are heuristics, not commitments.
- Numbers are unaudited until reviewed weekly by the founder.
- We never report "guaranteed" anything in the KPI tree.
