# Growth Engine

The growth engine optimises for **verified** revenue:

```
Campaign -> Touch -> Lead -> Call -> Proposal
         -> Commitment -> Invoice -> Payment
         -> Verified Revenue -> Attribution -> Learning
```

Only `payment_received`, `signed_agreement`, `retainer_activated`, or
`partner_paid_customer` count as verifying events. Likes, views,
meetings booked, verbal interest, and unqualified pipeline are
explicitly excluded by the verification policy.

## GEO (AI search visibility)

The `growth.geo` subpackage ships dedicated pages for high-intent
topics (AI Governance, Agentic Control Plane, Revenue Hunter,
White-Label, MCP Risk Review, Revenue Attribution, Approval
Workflows). Each page includes structured FAQ + comparison +
trust-signal blocks that AI answer engines can ingest reliably.

## Attribution

`growth.attribution` provides first-touch, last-touch, multi-touch,
asset-influenced, agent-influenced, and partner-influenced models.
`revenue_weighting.normalize` collapses them to a single weight map
that sums to 1.0.
