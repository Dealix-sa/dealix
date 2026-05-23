# Ultimate Product Platform

> Turn repeated service workflows into product modules.
> The platform is the **side effect** of doing the service well, not a parallel project.

---

## 1. Purpose

Convert work that Dealix repeats by hand into **reusable, observable, sellable** modules — without turning into a SaaS company prematurely.

The platform exists for three reasons, in this order:
1. **Internal leverage** — the founder operates a 5× larger company with the same hours.
2. **Customer-facing value** — paid customers get a portal that surfaces what we already do for them.
3. **Optional SaaS** — modules that survive customer use become candidate SaaS features.

A module that doesn't deliver (1) is not built. A module that doesn't deliver (1) **and** (2) is not exposed to customers. A module that doesn't deliver (1) + (2) + repeated demand is not promoted to SaaS.

---

## 2. Productization path

```
Manual service          (founder does it from scratch)
   │
   ▼
Template                (a markdown/Jinja template captures the structure)
   │
   ▼
Script                  (a script renders the template with inputs)
   │
   ▼
Internal tool           (the founder runs the script from CLI / console)
   │
   ▼
Command center module   (the script appears as a page in /ceo's console)
   │
   ▼
Customer-facing feature (the customer sees their version in the portal)
   │
   ▼
SaaS module             (the feature is sold and operated as a product)
```

Promotion to the next step requires evidence (see §5).

---

## 3. Candidate modules

These are the modules that **already exist as services** at Dealix and are therefore valid productization candidates. Each module names the team workflow it productizes and the gate it must pass to move up.

| Module                          | Productizes the workflow…                                  | Next gate                            |
|----------------------------------|------------------------------------------------------------|--------------------------------------|
| Lead Intelligence               | Researching + enriching + scoring an account.              | Used by ≥ 2 paid sectors.            |
| Approval Center                  | Founder review of A2/A3 actions.                           | All A2 routes through it.            |
| Sales Cockpit                    | Funnel awareness + next-action pick.                       | All revenue stages reflected.        |
| Trust Center                     | Policy flags + suppression + incidents.                    | All checks exercised in production.  |
| Sector Reports                   | Sector pulse / data pack delivery.                         | ≥ 3 sectors delivered.               |
| Revenue Sprint Workspace        | The 499 SAR Sprint engagement.                             | ≥ 5 sprints completed.               |
| Client Delivery Portal           | Workspace + status + artifacts for paid engagements.       | ≥ 3 paid clients delivered.          |
| Partner Referral Portal          | Partner registers an intro and tracks status.              | ≥ 2 partner-sourced engagements.     |
| AI Eval Center                   | Run + view eval suites + triage failing examples.          | All prompt templates covered.        |
| Finance / Payment Capture        | Cash, MRR, runway, payment follow-up.                      | All `finance_events` flowing.        |

---

## 4. Module contract

Every module that exists in the platform conforms to this contract. Without conformance, the module is not registered.

| Property                | Requirement                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| `module_id`              | Unique, kebab-case slug (`lead-intelligence`).                              |
| `owner`                  | Single accountable person.                                                  |
| `data_model`             | All tables it reads/writes are listed and exist in the data platform.       |
| `api_surface`            | All endpoints it exposes are documented in `docs/api/`.                     |
| `permissions`            | Roles allowed to use it; roles explicitly denied.                           |
| `trust_class`            | Default class for the module's actions (A0–A3).                             |
| `workers`                | Workers it owns are listed in `docs/runtime/ULTIMATE_WORKER_MESH.md` §8.    |
| `telemetry`              | Usage counters wired into `product_usage`.                                  |
| `customer_facing`        | Boolean — whether end-customers see this module.                            |
| `productized`            | Boolean — whether it has graduated to SaaS pricing.                         |
| `runbook`                | Link to operational runbook (incidents, recovery, scaling).                 |

The registry lives in `dealix/product/modules.yaml`.

---

## 5. Productization gate (the only "do we build the next step" decision)

Do **not** build the next step in the path (§2) unless **all** of these are true.

1. **Repeated workflow exists.** The current step has been used to produce the same outcome ≥ 3 times.
2. **Paid customer used it.** A customer paid for the outcome at least once.
3. **Manual process is painful.** Re-doing it by hand costs > 2 hrs each time **or** is error-prone.
4. **Data model is stable.** The underlying tables (`docs/data/...`) have not changed in 30 days.
5. **Trust requirement is clear.** The action's class (A0–A3), approvals, and audit are defined.

This is the **single** gate. There are no exceptions.

---

## 6. Customer portal (the L9 deliverable)

When a module is promoted to customer-facing, it appears in the **customer portal** at the same level of visibility we offer the founder:
- The customer sees the same data we see (filtered to their account).
- The customer sees the same approvals (those that touch them).
- The customer sees the same proof artifacts (only their own + ones we are co-publishing).

Roles inside the portal:
- **Customer Admin** — full view of the customer's data; can change their suppression preferences; can request a new engagement.
- **Customer Operator** — view-only; can comment on artifacts.
- **Partner** — sees the engagements they referred; no view of unrelated accounts.

The portal is built **after** L6 (Delivery OS) is stable.

---

## 7. Module → SaaS promotion gate

A customer-facing module becomes a **priced SaaS module** only when:

1. ≥ 3 customers have used it in the same way (independent use, not co-pilot).
2. The customer is willing to pay for it as a standalone product (verified in a paid pilot).
3. Margin at scale is ≥ 70%.
4. A support runbook exists.
5. The legal contract surface (TOS, DPA, SLA) is reviewed.

Until all five are true, the module remains internal or customer-facing-by-account, **not** a SaaS line.

---

## 8. APIs & integrations

- Every productized module exposes a documented API surface (under `/api/v2/public/...` after L9).
- Webhooks for state transitions (e.g., `engagement.qa_passed`, `proof.published`).
- A small set of inbound integrations: HubSpot/Salesforce CRM (read-only), email provider, WhatsApp Business API, payment provider.
- No outbound integration that does not pass the trust plane.

---

## 9. Telemetry

Every module emits:
- `product_usage` rows per use.
- `worker_runs` rows per background invocation.
- `finance_events` rows for AI / tool cost attributable to the module.

This telemetry powers:
- `/product/usage`
- `/product/repeated-workflows`
- The "kill / keep / scale" decision for each module.

---

## 10. Failure modes the platform prevents

| Failure mode                                                | Prevention                                            |
|--------------------------------------------------------------|-------------------------------------------------------|
| Build a SaaS feature for a workflow that hasn't been sold.  | Gate §5 (paid customer used it).                      |
| Build a customer portal before delivery is stable.          | Customer portal blocked until L6 evidence.            |
| Expose unfinished modules to customers.                     | `customer_facing` boolean defaults to `false`.        |
| Modules that drift from the data model break silently.      | Module contract requires named tables; verified in CI.|
| Productizing something the customer can't operate alone.    | Handoff doc + runbook required at promotion.          |

---

## 11. Rule

> **Do not build a SaaS feature unless: repeated workflow exists, paid customer used it, manual process is painful, data model is stable, trust requirement is clear.**

This single rule prevents Dealix from turning into "an AI SaaS that nobody uses" — a category we have explicitly chosen not to join.
