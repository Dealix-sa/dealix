# External Actions Policy

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> Governs anything Dealix does that touches the outside world.

---

## 1. Definition

An **external action** is anything that leaves Dealix and reaches a third party:
a message, an email, a post, an API call to a customer's system, an export, a
payment, a published claim.

## 2. The hard rule

Every external action is at minimum approval class **A3 — always requires human
approval**. Financial/legal/security actions are **A4** (approval + log).
Destructive actions are **A5** (forbidden unless explicitly authorized).

## 3. Explicitly forbidden

| Forbidden | Why |
|---|---|
| Auto-send WhatsApp | No automated customer messaging |
| Bulk / cold email | No spam, no cold mass outreach |
| Scraping | Not from platforms that disallow it |
| List buying | No purchased contact lists |
| Auto-publish case study | Requires customer approval |
| Auto pricing change | Requires `PRICE_AUTHORITY.md` |
| Silent data deletion | Requires a logged record |
| Auto financial/legal commitment | Requires A4 approval + log |

## 4. Allowed (with approval)

- Drafting customer messages, proposals, replies (A2 → human sends).
- Manual, founder-sent warm outreach (one at a time, consented).
- Exports the customer requested (A4, logged).

## 5. Outreach specifics

The first-30-prospects motion is **manual, founder-led, warm**. It is not cold
mass outreach. No automation tools send on Dealix's behalf. See
`docs/01_go_to_market/FIRST_30_PROSPECTS.md`.

## 6. Enforcement

- Agents declare their max approval class in `.agent-contract.md`.
- Workflows that could perform A3+ actions must route through an approval step.
- Violations are incidents — log and review.

## 7. Related

`HUMAN_APPROVAL_POLICY.md` · `SECURITY_BASELINE.md` · `CLAIMS_REGISTER.md`
