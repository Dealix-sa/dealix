# Objection Analytics

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals.

Objections are the cheapest signal we get from customers. They are
free, they are honest, and they are repeatable. Objection Analytics
captures every objection raised, classifies it, and uses the pattern
to sharpen messaging, proof, and offer.

## Sources

Objections arrive in four channels:

| Channel                  | Source                                                           |
| ------------------------ | ---------------------------------------------------------------- |
| Email reply              | `outreach/conversation_log.csv` rows tagged with intent objection.|
| Meeting note             | Conversation log entries with `summary` containing objections.    |
| Proposal feedback        | Notes attached to `sales/proposal_queue.csv` rows.                |
| Customer support         | Notes from delivery and customer success agents.                  |

The Distribution Operator captures email/LinkedIn objections via the
reply routing queue (`outreach/reply_routing_queue.csv`). The
Delivery Copilot captures meeting and proposal objections.

## Schema

The derived table is `performance/objections.csv` (private ops,
created on first use):

| Column          | Notes                                                          |
| --------------- | -------------------------------------------------------------- |
| `id`            | Objection id.                                                  |
| `lead_id`       | Foreign key to conversation log.                               |
| `stage`         | Funnel stage at which the objection was raised.                |
| `channel`       | Channel where the objection arrived.                            |
| `category`      | One of the canonical categories (see below).                   |
| `theme`         | Sub-theme inside the category.                                  |
| `verbatim`      | The customer's exact phrasing (trimmed, language preserved).   |
| `response`      | How we responded (link to draft).                              |
| `resolved`      | `yes`, `no`, `escalated`.                                      |
| `ts`            | ISO ts.                                                        |
| `coded_by`      | `distribution_operator`, `delivery_copilot`, or `founder`.     |

## Canonical categories

| Category              | Typical themes                                                            |
| --------------------- | ------------------------------------------------------------------------- |
| `price`               | "too expensive", "vs. internal hire", "budget cycle"                       |
| `proof`               | "show me a case in our sector", "how have you helped someone like us"     |
| `scope`               | "this is too much / too little for what we need"                          |
| `trust_residency`     | "where is data stored", "PDPL alignment", "Saudi residency"               |
| `trust_governance`    | "who has access", "how is the audit handled"                              |
| `trust_authority`     | "are you certified by X", "what credentials does the founder have"        |
| `timing`              | "not now", "after Q2", "next fiscal year"                                  |
| `process`             | "procurement requires X", "we need three quotes"                          |
| `risk`                | "what if it fails", "what is the exit clause"                             |
| `team_fit`            | "we need a partner who speaks Arabic", "who is on the team"               |
| `competitive`         | "we are talking to vendor X", "we already have Y in place"                |
| `champion`            | "I would need to convince my CFO", "we have no executive sponsor"         |

Categories are stable. Themes evolve.

## Coding discipline

1. Use the customer's words for `verbatim`. Do not paraphrase.
2. Preserve the language of origin (Arabic objections stay Arabic).
3. Code only what the customer actually said. Inferred motivations
   are not objections.
4. One row per distinct objection. Multiple objections in one reply
   produce multiple rows.

## Response library

Each category has a response library inside the Distribution
Operator's draft tooling. Responses are pre-vetted by the Brand
Guardian and approved by the founder. The library lives in
`outreach/objection_responses.md` (private ops). The library is
versioned and updated as patterns shift.

The library is not a script. It is a set of reference frames that the
Distribution Operator drafts adapt. Every response still passes the
eval gate and the policy adapter before queueing.

## Aggregations

Weekly aggregations the Performance Analyst surfaces:

| Aggregation                                       | Use                                          |
| ------------------------------------------------- | -------------------------------------------- |
| Category counts (overall and by sector)           | Where to invest in proof / messaging.        |
| Category counts at each funnel stage              | Where the objection cluster intercepts.      |
| Resolved rate by category                          | Where our responses are landing.             |
| Time-to-respond by category                        | Where we are slow.                           |

## Heatmap

The category × stage heatmap is the single most useful artifact.

```
                lead   engaged   qualified   proposal   negotiation
price            *        *        *          ***          ****
proof            **       ***      ***        **            *
scope            *        **       ***        ***           **
trust_residency  ***      *        *          *             *
trust_governance *        *        **         **            ***
timing           ****     ***      **         *             *
process          *        *        *          ***           ****
risk             *        *        **         **            ***
competitive      **       **       **         **            ***
champion         *        *        **         **            ****
```

Cells with many stars are clusters to investigate.

## Feedback into the operating system

| Cluster                                                                | Action                                                                 |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `proof` heavy at lead/engaged                                          | Strengthen sector proof in opening hook.                                |
| `trust_residency` heavy at any stage                                   | Strengthen sovereign readiness narrative.                              |
| `price` heavy at negotiation                                            | Review offer ladder; consider rung repricing experiment.                |
| `process` heavy at proposal                                             | Build a procurement-aligned proposal template.                          |
| `champion` heavy at negotiation                                         | Add a stakeholder-mapping motion in qualification.                      |
| `competitive` heavy in a sector                                         | Refresh competitive positioning (in `docs/positioning/`).               |

## Anti-patterns

| Anti-pattern                                            | Why                                                                       |
| ------------------------------------------------------- | ------------------------------------------------------------------------- |
| Paraphrasing objections                                  | We lose the signal in the original language.                              |
| Treating every reply as an objection                     | Many replies are neutral or positive. Code only objections.               |
| Responding without coding                                | The pattern never compounds.                                              |
| Coding without responding                               | The customer is left hanging; the pipeline stalls.                        |
| Inventing themes outside the library                    | Themes evolve via the Brand Guardian + founder review, not freelance.    |

## Cadence

| Activity                          | Cadence    |
| --------------------------------- | ---------- |
| Coding new objections             | Within 24 hours |
| Heatmap refresh                    | Weekly     |
| Response library review            | Monthly    |
| Category dictionary review         | Quarterly  |

## Founder Console exposure

Objection counts are not yet exposed via a dedicated endpoint. They
surface in the weekly performance summary in the founder brief. A
future `/api/v1/internal/performance/objections` endpoint will read
the table once the schema stabilizes.

## Discipline

1. Every objection is coded.
2. Every coded objection drives a response.
3. Every cluster drives an operating change.
4. Customer language is the source of truth.
5. Objections are never argued with; they are answered with method
   and proof.
