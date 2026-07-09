# Dealix Payment Evidence and Revenue Policy

## Purpose

Dealix must not count revenue based on intention, draft messages, verbal interest, or founder optimism. Revenue is counted only when there is payment evidence.

## Mandatory policy

```text
Revenue requires payment_received.
Closed-won requires payment_received + proof_pack_delivered + closed_won.
```

## Allowed evidence examples

- Bank transfer receipt.
- Approved invoice payment confirmation.
- Payment gateway confirmation in test/prod system, depending on environment.
- Written finance confirmation from the founder after checking the account.

## Not valid as revenue evidence

- A drafted offer.
- A WhatsApp message saying “interested”.
- A meeting booked.
- A verbal yes.
- A proposal sent.
- A payment link sent.
- A promise to transfer later.
- A fake/placeholder receipt.

## Manual first

For the first paid client, the system must be manual:

- Founder approves offer.
- Founder sends manually.
- Founder approves payment instruction.
- Founder confirms payment received.
- System logs evidence after confirmation.

## What automation can do

- Prepare the offer.
- Prepare the invoice/payment instruction draft.
- Prepare follow-up drafts.
- Prepare proof pack.
- Prepare daily report.
- Flag missing evidence.

## What automation cannot do in this slice

- Send the invoice automatically.
- Charge a card.
- Mark revenue as received.
- Mark closed-won without proof.
- Send reminders externally.
- Create public claims.

## Required event chain

```text
lead_selected
-> offer_drafted
-> founder_approved
-> offer_sent_manually
-> payment_instruction_approved
-> invoice_sent
-> payment_received
-> work_started
-> proof_pack_delivered
-> closed_won
```

## Failure states

| Failure | Meaning | Required fix |
|---|---|---|
| `amount_present_without_payment_received` | Amount exists but payment is not confirmed. | Do not count revenue. Add payment evidence. |
| `closed_won_before_proof_pack_delivered` | Closed-won marked too early. | Deliver proof pack first. |
| `proof_delivered_before_payment_received` | Work delivered before confirmed payment. | Add approval exception or request payment. |
| `fake_evidence_warning` | Evidence wording suggests fake/placeholder proof. | Replace with real evidence. |

## Founder checklist

Before saying “we got first revenue”, confirm:

- Payment was actually received.
- Evidence exists.
- Client identity is known.
- Amount is correct.
- Proof pack delivery status is tracked.
- The system has not exaggerated the result.

## Operational command

```bash
python scripts/commercial/run_first_paid_client_path.py
python scripts/commercial/verify_first_paid_client_path.py
```
