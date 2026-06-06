# First Revenue Plan / خطة أول إيراد

**Owner:** Founder · **Updated:** 2026-06-06 · **Wave:** 7 — Private Launch
Verification & First Revenue

**Goal:** prepare and send the first **5 manual, founder-approved** outreach
messages → 2 Diagnostics → 1 offer → 1 paid Command Sprint → 1 Proof Pack.

> Disclaimer: Estimated outcomes are not guaranteed outcomes /
> النتائج التقديرية ليست نتائج مضمونة. No auto-send. No spam. No fake proof.

---

## 1. The motion (manual, founder-led)

```
30 warm targets  →  top-10 shortlist  →  5 personalized drafts
      →  founder approval  →  5 manual sends  →  2 Diagnostics booked
      →  1 Command Sprint offer  →  1 paid Sprint  →  1 Proof Pack  →  upsell
```

Targets: [`../../data/growth/first_30_targets.csv`](../../data/growth/first_30_targets.csv)
Queue: [`outreach_approval_queue.md`](outreach_approval_queue.md)

---

## 2. First 30 targets — structure

CSV columns: `rank, company, sector, source, consent_basis, contact_owner,
relationship, shortlist, notes`. Every row is **warm** with a declared
`consent_basis` (existing_relationship / referral / inbound opt-in). No scraped
or cold contacts.

## 3. Top-10 shortlist

Rows 1-10 in the CSV (`shortlist=yes`). Selection criteria: known
decision-maker, warm relationship, sector fit, near-term timing.

## 4. First 5 outreach drafts

Drafts 1-5 in [`outreach_approval_queue.md`](outreach_approval_queue.md). All
`approval_required`. Founder approves before any send.

## 5. Diagnostic booking path

Script: [`../../sales/DIAGNOSTIC_SCRIPT.md`](../../sales/DIAGNOSTIC_SCRIPT.md).
Page: `frontend/src/app/[locale]/dealix-diagnostic/page.tsx`. Outcome logged in
sales ledger; follow-up drafted (not auto-sent).

## 6. Command Sprint proposal path

One-pager: [`../../sales/COMMAND_SPRINT_ONE_PAGER.md`](../../sales/COMMAND_SPRINT_ONE_PAGER.md).
Proposal rendered for founder approval before sending.

## 7. Customer workspace creation path

On payment, create `clients/<slug>/` from
[`../../docs/04_delivery/CUSTOMER_FOLDER_TEMPLATE.md`](../../docs/04_delivery/CUSTOMER_FOLDER_TEMPLATE.md).
First gate: signed Source Passport.

## 8. Proof Pack path

Assemble from
[`../../docs/04_delivery/PROOF_PACK_TEMPLATE.md`](../../docs/04_delivery/PROOF_PACK_TEMPLATE.md)
(14 sections, proof score ≥ 70, consent + approval before any external use).

## 9. Upsell path

After Proof Pack: Data/Revenue Pack → Managed Business OS. Ladder:
[`../../docs/OFFER_LADDER.md`](../../docs/OFFER_LADDER.md).

---

## Rules (hard)

- No auto-send. Every draft requires founder approval.
- No spam, no cold/scraped contacts.
- No guaranteed revenue.
- No fake proof — consent + approval before publishing anything.

---

## Success test (Private Launch proof)

5 manual messages · 2 Diagnostics · 1 offer · 1 paid Sprint · 1 Proof Pack.
That is the real proof Dealix *works* — not just that files exist.
