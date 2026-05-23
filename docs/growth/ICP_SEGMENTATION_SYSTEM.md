# ICP Segmentation System

The Dealix ICP (Ideal Customer Profile) is **not a single profile**. It is a layered set of segments, each scored independently. The targeting OS only considers an account *in* the ICP if it matches **all three layers**: firmographic, behavioural, and trust.

## 1. Layer 1 — Firmographic

| Field                | Default rule                                          |
|----------------------|-------------------------------------------------------|
| Country              | KSA (Saudi Arabia)                                    |
| Sector               | One of the 8 canonical sectors                        |
| Headcount            | 20–500 (mid-market)                                   |
| Estimated revenue    | 5M – 200M SAR/year                                    |
| Years in business    | ≥ 2                                                   |
| B2B revenue share    | ≥ 60%                                                 |
| Saudi customer share | ≥ 50% of revenue                                       |

## 2. Layer 2 — Behavioural

| Field                              | Default rule                                  |
|-----------------------------------|-----------------------------------------------|
| Active sales motion                | Has a sales team or partner channel           |
| Outbound posture                   | Accepts cold but personalised outreach        |
| Marketing activity                 | Posts content / runs events at least monthly  |
| Bilingual content                  | AR + EN content present in the last 90 days   |
| Pipeline visibility (CRM/sheet)    | Uses *some* tool, even a spreadsheet          |
| Pricing transparency               | Has at least a starting price band published  |

## 3. Layer 3 — Trust

| Field                              | Default rule                                  |
|------------------------------------|-----------------------------------------------|
| Reachable buyer                    | A named buyer + title + reachable channel     |
| Honest about pain                  | Will let us see CRM/data within 7 days        |
| Accepts human-approved outbound    | No insistence on uncontrolled automation      |
| No black-listed verticals          | Not gambling/adult/payday lending/etc.        |
| Founder/CEO endorses               | Senior buy-in for the trust-gated approach    |

## 4. Segments inside the ICP

Within the ICP we run four sub-segments, each with its own pitch angle:

| Segment                  | Pitch angle                                            |
|--------------------------|--------------------------------------------------------|
| **Pipeline-Starved**     | "Your pipeline is the bottleneck — we open it."        |
| **Pipeline-Rich, Slow-Closing** | "Your pipeline is fine — we make it convert faster." |
| **Productisation-Seeking** | "You sell services — we help you package them." |
| **Partner-Ready**        | "You serve the same buyer — let's co-deliver."         |

The recommended offer differs per segment — see `OFFER_CHANNEL_FIT_MATRIX.md`.

## 5. Anti-ICP

We explicitly **do not** pursue:

- Consumer brands.
- Companies whose entire model relies on uncontrolled outbound automation.
- Sectors on the doctrine black-list (gambling, adult, payday lending, MLM).
- Companies < 2 years old with no operating cash flow.
- Companies > 1,500 headcount (enterprise sales motion that we don't yet serve).
- Companies that demand cold-call-only outreach.

## 6. Operational checklist

Before promoting an account into the active queue:

- [ ] All three layers checked.
- [ ] Anti-ICP exclusions confirmed clear.
- [ ] Final priority A or B.
- [ ] Recommended offer + channel set.
- [ ] Owner assigned.
- [ ] Proof artefact identified.
- [ ] Founder informed at weekly review.
