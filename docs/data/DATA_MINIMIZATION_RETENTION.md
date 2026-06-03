# Data Minimization & Retention

## Purpose
Hold the minimum data needed for the minimum time needed.

## Minimization principles
- Ask only for the data fields needed to deliver the engagement.
- Do not store personal data of individuals beyond their role.
- Anonymize as soon as the personal identifier is no longer required.

## Retention windows
| Data | Retention | After window |
|---|---|---|
| Pipeline notes for closed-lost leads | 12 months | Delete personal fields; keep anonymized stats |
| Customer deliverables | 36 months | Archive; delete on customer request |
| Financial records | 7 years (KSA tax) | Archive |
| Approval logs | Lifetime | Keep |
| Evidence ledger | Lifetime | Keep |
| Outbound message drafts | 30 days | Delete |
| Sample artifacts (prospects who didn't buy) | 6 months | Delete |

## Right to be forgotten
- A KSA individual or company may request deletion of their personal data.
- We respond within 30 days.
- Deletion is recorded in `trust/redaction_log.csv` (without re-introducing the data).

## Encryption / access
- Encryption at rest for any directory containing personal data.
- Access logs in `people/access_log.csv` for production data.

## Audit
- Annual: review every retention bucket; delete what's past window.
- Quarterly: spot-check a random sample of personal-data files.

## What we never collect
- KSA national ID numbers unless legally required for an engagement.
- Health data unless explicitly contracted.
- Children's data (under 18).
