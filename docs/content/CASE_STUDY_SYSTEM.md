# Case Study System

> A case study is a high-trust artifact. Build it slowly. Protect it.

## When a customer is case-study eligible

All true:

- They are an active retainer **or** had a completed Sprint with positive
  outcomes.
- They are willing to be named (written consent).
- The named outcomes are verifiable.
- The customer is at Tier A or B.

## Case Study Workflow

1. **Founder asks the customer** for a case study, citing what would be
   included.
2. **Customer agrees in writing** (email is sufficient).
3. **Founder drafts** the case study, with all numbers and quotes drawn
   from real evidence.
4. **Customer reviews and approves** the final draft in writing.
5. **Consent letter** stored in `dealix-ops-private/content/case_study_consents/`.
6. **Case study published** in `docs/proof/` or as a PDF.
7. **Indexed** in `PROOF_LIBRARY.md`.

## Case Study Template

```
# [Customer name] — [outcome verb] [outcome noun]

## Customer
Sector, size, geo, decision-maker role.

## Challenge
What were they trying to do? Why was the existing approach insufficient?

## Approach
What we did, in concrete terms.

## Outcome
- Number 1 [with evidence reference]
- Number 2 [with evidence reference]
- Quote from customer [verified verbatim]

## What we learned
One paragraph, honest.

## Consent
On file at [reference], dated [date], signed by [name + role].
```

## Forbidden in case studies

- Outcomes we cannot back with our ledgers.
- Quotes the customer did not actually say.
- Implication of a guarantee.
- Customer data that the customer has not consented to publish.

## Retraction

If a customer withdraws consent later:

- Remove the public case study within 7 days.
- Replace with anonymised version (only if anonymisation is true and
  customer agrees in writing).
- Log the retraction.

## Review

Quarterly:
- New consents collected.
- Existing case studies re-confirmed (consent still valid).
- Case studies retired (customer left, consent expired).
