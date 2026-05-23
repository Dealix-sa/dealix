# Ultimate Revenue Factory

> Create repeatable movement from market to cash.
> Without this factory, nothing else in Dealix matters.

---

## 1. Purpose

Build the company's single most important machine: the one that turns a list of Saudi B2B accounts into **collected cash**, on a predictable weekly cadence, with full trust + audit.

If the Founder Console is the windshield and the Trust Plane is the brake, the Revenue Factory is the **transmission**: it converts motion at one stage into motion at the next.

---

## 2. Flow

```
Market accounts
   │
   ▼
Lead intelligence  (research, enrichment, dedupe)
   │
   ▼
Scoring            (fit × intent × signals)
   │
   ▼
Outreach draft     (generated, scored, attached to a contact)
   │
   ▼
Approval           (founder reviews; A2)
   │
   ▼
Send / draft       (send via integration OR push to inbox draft)
   │
   ▼
Follow-up          (scheduled, never lost)
   │
   ▼
Reply              (classified: positive / neutral / negative / OOO)
   │
   ▼
Sample             (sector pulse, mini-report, custom asset)
   │
   ▼
Proposal           (offer mapped to the customer, priced, sent)
   │
   ▼
Payment / PO       (capture, follow up until paid or closed-lost)
   │
   ▼
Delivery           (paid work begins — see Delivery OS)
   │
   ▼
Retention          (health score, retainer, renewal)
   │
   ▼
Proof              (case study, testimonial, sample report)
   │
   ▼
Referral           (warm intro, partner co-sell)
   │
   ▼
Inbound demand     (proof + referral compound into inbound)
```

Every arrow above is a worker (see `docs/runtime/ULTIMATE_WORKER_MESH.md` §8). Every node is a table (see `docs/data/ULTIMATE_DATA_PLATFORM.md` §2). Every approval gate is a trust class (see `docs/trust/ULTIMATE_TRUST_PLANE.md` §4).

---

## 3. Minimum weekly output

These are not aspirations. They are the **definition of "the factory is running"**. Below them, the factory is not running and we are not at L5.

| Stage                  | Minimum / week | Notes                                                   |
|------------------------|----------------|---------------------------------------------------------|
| New researched leads   | **100**        | Sourced + enriched + scored.                            |
| Approved outreach      | **25–50**      | Founder-approved; sent or queued to founder inbox.      |
| Replies                | **≥ 5**        | Any reply category counts.                              |
| Positive replies       | **≥ 2**        | Triggers a sample or a proposal.                        |
| Samples                | **3**          | Generated, QA'd, delivered.                             |
| Proposals              | **1–3**        | Real offers with prices, sent.                          |
| Payment follow-ups     | **1 per proposal** | Until paid, agreed plan, or closed-lost.            |
| Sector decision        | **1**          | Continue / pause / pivot one sector machine.            |
| Channel decision       | **1**          | Continue / pause / pivot one channel.                   |

If any row is missing for two consecutive weeks, the founder pauses the next layer and fixes this one. Scaling on top of a broken layer creates compounding waste.

---

## 4. Scale rule

> **Scale intelligence faster than sending.**
> **Scale sending only with reply handling.**
> **Scale proposals only with payment capture.**
> **Scale delivery only with QA.**

This is the rule that prevents the factory from breaking under its own weight.

Concretely:
- We may double **lead intelligence** at any time (no external impact).
- We may double **sending** only when the reply-routing worker has cleared its backlog for 7 consecutive days.
- We may double **proposals** only when `payment_capture_queue` is current (no proposal older than the configured follow-up cadence without a logged contact).
- We may double **delivery** only when the QA worker has produced at least one pass record for every active engagement.

---

## 5. Sector machines

A **sector machine** is a vertical slice of the factory tuned for one sector (e.g., Insurance, Logistics, Healthcare, Government, Fintech).

Each sector machine has:
- A sector-specific source list (`dealix/data/sources/<sector>.yaml`).
- A sector-specific scoring weight (`dealix/scoring/<sector>.yaml`).
- A sector-specific message library (`dealix/prompts/outreach/<sector>/`).
- A sector-specific suppression overlay (compliance / regulator nuances).
- A sector dashboard panel on `/distribution`.

We run **one** sector machine per weekly cadence at L5, **three** at L6, **five+** at L9. Adding a sector before the prior one has proof is forbidden.

---

## 6. Offer ladder

The factory maps every account to one of these offers. We do not invent new offers per account. Custom scope only happens for L6+ clients after proof.

| Rung | Offer                        | Price (SAR)     | Trigger                                                       |
|------|------------------------------|-----------------|---------------------------------------------------------------|
| 1    | Free Diagnostic              | 0               | Curiosity / inbound / cold reply.                             |
| 2    | 499 SAR Sprint               | 499             | Diagnostic completed; founder wants a tangible artifact.      |
| 3    | 1,500 SAR Data Pack          | 1,500           | Sprint delivered; founder wants a sector data asset.          |
| 4    | 2,999–4,999 SAR/mo Managed Ops | 2,999–4,999/mo | Data Pack delivered; ops handover proposed.                   |
| 5    | 5,000–25,000 SAR Custom AI   | 5,000–25,000     | Multiple Managed Ops cycles; bespoke workflow / model.        |

Routing logic lives in `dealix/sales/offer_mapper.py`.

---

## 7. Founder time budget

The founder has a finite weekly time budget. The factory respects it.

| Activity                         | Founder time budget / week |
|----------------------------------|----------------------------|
| Approval Center                  | ≤ 60 minutes               |
| Sample QA + proposal QA          | ≤ 90 minutes               |
| Sales calls / replies            | ≤ 5 hours                  |
| Trust / incident review          | ≤ 30 minutes               |
| Total founder-facing factory     | ≤ 8 hours / week           |

If the factory exceeds this budget, the next change is **batch sizing** or **automation under A1**, not **more founder hours**.

---

## 8. Failure modes the factory prevents

| Failure mode                                       | How the factory prevents it                                  |
|----------------------------------------------------|--------------------------------------------------------------|
| Founder sends ad-hoc messages outside the queue.   | Approval Center is the only path to send.                    |
| A reply is missed for days.                        | `reply-router` triages every reply within the SLA.           |
| A proposal goes unpaid silently.                   | `payment-followup` walks every proposal until terminal.      |
| Lists go stale and we re-touch dead leads.         | `lead-intelligence` rescore + suppression check at send.     |
| A sector gets over-sent.                           | Per-sector send caps in `dealix/runtime/limits.yaml`.        |
| We promise things we can't deliver.                | `no_overclaim` check at every outreach + proposal step.      |

---

## 9. Metrics that decide the factory's health

These metrics appear on `/sales-cockpit` and on the weekly scorecard:

- **Conversion** at each stage (lead → outreach, outreach → reply, reply → sample, sample → proposal, proposal → payment).
- **Cycle time** per stage (median, p90).
- **Founder approval latency** (median, p90).
- **Send → reply rate** by sector and by channel.
- **Proposal → payment rate** (and time to payment).
- **Backlog** at each stage.

A stage with backlog **and** falling conversion is the **bottleneck**. We work the bottleneck before any other improvement.

---

## 10. Rule

> **Scale intelligence faster than sending. Scale sending only with reply handling. Scale proposals only with payment capture. Scale delivery only with QA.**

This rule is also encoded in `dealix/sales/scale_gates.py` and verified weekly by the `scale-gate-verify` worker.
