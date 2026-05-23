# Referral System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Driven by Growth · Built on Trust.

The Referral System is the discipline by which Dealix turns happy
customers into introductions and, eventually, additional revenue.
The system is owned by the Partner Revenue Agent (A2 max), governed
by explicit consent at every step, and surfaced through the Founder
Console.

## Source file

`customer_success/referral_queue.csv` in the private ops runtime:

| Column            | Notes                                                                   |
| ----------------- | ----------------------------------------------------------------------- |
| `id`              | Referral id.                                                            |
| `client`           | Referring customer name.                                                 |
| `referral_target`  | The target identity (anonymized to display only without consent).        |
| `status`           | `proposed`, `consent_pending`, `consent_granted`, `intro_sent`, `meeting_scheduled`, `won`, `lost`, `withdrawn`. |
| `owner`            | Internal owner (Partner Revenue Agent or founder).                       |

## Founder Console exposure

| Endpoint                                  | What it shows                                       |
| ----------------------------------------- | --------------------------------------------------- |
| `GET /customer-success/summary`           | Open referrals count.                                |

The referral queue endpoint is not yet exposed directly; a future
`/customer-success/referrals` endpoint will surface the queue.

## Consent discipline

Consent is the entire system. The Referral System never moves
forward on a referral without explicit, recorded customer consent.
Two consent points:

1. **Consent to ask.** Before the referral target is contacted, the
   referring customer must consent to the intro.
2. **Consent to use as proof.** If the referral becomes a public
   case (named introduction, joint marketing), separate consent is
   required (see `NO_OVERCLAIM_POLICY.md` and proof flow).

Consent is recorded as text or signed acknowledgment, attached to
the referral row via a payload reference.

## Lifecycle

```
proposed → consent_pending → consent_granted → intro_sent → meeting_scheduled → won | lost
                                                           ↓
                                                       withdrawn (any time)
```

| State                | Trigger                                                               |
| -------------------- | --------------------------------------------------------------------- |
| `proposed`            | Partner Revenue Agent identifies a candidate referral.                |
| `consent_pending`     | Outreach to the referring customer asking for consent (drafted, approved). |
| `consent_granted`     | Written consent received and logged.                                  |
| `intro_sent`          | Founder-approved intro sent. Audit recorded.                          |
| `meeting_scheduled`   | Target accepts the intro. Conversation moves to outreach queue.       |
| `won`                 | Deal closed with the target.                                          |
| `lost`                | Target declined or no further movement.                               |
| `withdrawn`           | Referring customer withdraws consent. All forward motion halts.       |

## Approval gates

| Action                            | Gate                                                                |
| --------------------------------- | ------------------------------------------------------------------- |
| Draft consent ask                  | Eval gate suites `no_guaranteed_claims`, `suppression_compliance`.  |
| Send consent ask                   | Founder approval (queued, A2).                                      |
| Move to `consent_granted`           | Manual confirmation from Partner Revenue Agent + audit row.          |
| Send intro                         | Founder approval (queued, A2).                                      |
| Mark as `won`                      | Proposal queue row must exist as `won`.                              |
| Use referral as proof              | Proof Safety Agent gate; separate consent.                          |

## Consent ask template

The Partner Revenue Agent drafts the ask following a Brand Guardian-
approved template. The template:

- Names the target by relationship only ("a procurement leader at a
  Saudi conglomerate") unless the referring customer prefers to name.
- Frames the ask as a method check, not a guaranteed outcome.
- Surfaces the option to withdraw at any time.
- Records the consent in a single, archivable artifact.

## Privacy posture

| Concern                          | Practice                                                          |
| -------------------------------- | ----------------------------------------------------------------- |
| Target identity exposure          | Anonymized in CSV by default; full identity stored in attachment.  |
| Cross-tenant data sharing         | Not allowed without separate consent.                              |
| Withdrawn consent                  | Forward motion stops; data retained only for audit purposes.       |
| PDPL alignment                     | Per `docs/PRIVACY_PDPL_READINESS.md`.                              |

## Revenue share

If a referral arrangement carries a revenue share, the share is
documented in the agreement with the referring customer. The Finance
Copilot tracks the share in a separate ledger (planned). Rev-share
terms are policy-gated by `pricing_commit_requires_approval`.

## Reporting

The Customer Success summary reports `referrals_open` as the count of
rows whose status is in `{proposed, consent_pending, consent_granted,
intro_sent, meeting_scheduled}`. Closed states (`won`, `lost`,
`withdrawn`) are excluded.

## Cadence

| Activity                        | Cadence    |
| ------------------------------- | ---------- |
| Identify candidate referrals     | Monthly    |
| Send consent asks (approved)     | As ready, founder-paced |
| Review withdrawn referrals       | Quarterly  |
| Audit consent records             | Quarterly  |

## What the Referral System will not do

- Send any referral message externally without founder approval.
- Use a customer's identity without recorded consent.
- Continue motion after consent withdrawal.
- Treat any referral as a guaranteed close.
- Bypass the suppression list (referral targets are also subject to
  suppression).

## Discipline

1. Consent is the system.
2. Every state has an audit row.
3. The Partner Revenue Agent is A2 max; the founder approves sends.
4. Withdrawn consent stops all motion.
5. Referrals are never used as outcome claims; they are pipeline.

## Cross-references

- `CUSTOMER_SUCCESS_OS.md` for the broader discipline.
- `CLIENT_HEALTH_SCORE_SYSTEM.md` for who is a good referrer.
- `SUPPRESSION_SYSTEM.md` for suppression integration.
- `NO_OVERCLAIM_POLICY.md` for phrasing.
