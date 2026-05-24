# LinkedIn Queue Machine

| Field | Value |
|---|---|
| Purpose | Draft LinkedIn connection notes and InMail messages for scored accounts |
| Inputs | account scores, buyer personas, trigger events, suppression list |
| Outputs | `linkedin_queue.csv`, audit events |
| Approval class | External action — manual operator send only |
| Trust gate | Brand check, suppression, profile validity |
| Owner | Distribution Operator |
| Worker | `worker_linkedin_queue` |
| KPI | Acceptance rate, reply quality |
| Failure mode | Profile unreachable → row marked `unreachable`, audited |
| Recovery | Re-validate weekly; remove if persistently unreachable |

## Draft contract

```yaml
queue: linkedin_queue
fields:
  - draft_id
  - account_id
  - persona_id
  - linkedin_profile_url
  - message_type            # connect | inmail | comment
  - text_en
  - text_ar
  - suppression_check
  - brand_check
  - trust_check
  - status                  # draft | approved | declined | deferred | sent
  - created_at
  - source
```

## Compliance

- No scraping of LinkedIn. Profiles must be supplied by the founder, partner, or operator.
- No automated send via LinkedIn APIs we do not have a contract for.
- Sending is operator-initiated and out-of-band.

## Brand notes

- Connect notes max 270 characters.
- InMail body 90-160 words.
- No emojis unless the persona file permits.
- Bilingual when the profile language signal is mixed.
