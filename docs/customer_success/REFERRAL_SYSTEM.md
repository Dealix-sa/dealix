# Referral System

The Referral System is the consent-based pathway that allows satisfied clients to introduce Dealix to others. It is the only outbound channel that compounds without paid distribution.

**Source of truth:** `$PRIVATE_OPS/referral_pipeline.csv`
**Owner:** Customer Success Lead
**Trust gate:** A2 — every referral ask requires founder approval before delivery; Dealix never sends outreach on the client's behalf.

## Eligibility

A client is eligible for a referral conversation when all three are true:

1. Health Score ≥ 8.0 for two consecutive months (`docs/customer_success/CLIENT_HEALTH_SCORE_SYSTEM.md`).
2. At least one verified outcome in the Value Ledger (`docs/08_value_os/VALUE_LEDGER.md`).
3. No open critical risk in the register.

Eligibility is computed weekly. The CS Lead proposes; the founder approves.

## Ask design

The referral ask is:

- One question.
- Bilingual EN + AR.
- Specific (named role and named sector preferred).
- Free of incentive bribery.
- Delivered in a working session or by founder DM, never by automated sequence.

## Reciprocation

Dealix does not offer cash referral bribes. A referrer who introduces a client that signs may receive, with their consent:

- Public acknowledgement (if they opt in).
- A learning credit on a future engagement (case by case, founder approved).
- An invitation to a private founder roundtable.

Reciprocation policy is documented in `$PRIVATE_OPS/referral_policy.md` and reviewed annually.

## Pipeline stages

| Stage | Definition |
|-------|-----------|
| Eligible | Eligibility criteria met |
| Asked | Ask delivered, awaiting response |
| Introduced | Client made the introduction |
| In conversation | Dealix has had a first call with the introduced party |
| Qualified | Introduced party fits ICP |
| Closed-won | Engagement signed |
| Closed-lost | Did not proceed |

Each stage transition is logged with timestamp, owner, and approval class.

## Failure modes

- **Pressure:** a client is asked twice after declining. Detection: pipeline state. Recovery: stop the ask, apologise, log.
- **Self-acting on a client's behalf:** Dealix contacts the introduced party before the client has made the introduction. Detection: policy engine. Recovery: pause, contact the client, apologise.
- **Consent decay:** a client's acknowledgement was given 12+ months ago. Detection: annual review. Recovery: re-confirm or remove.

## Recovery path

If referral pipeline data is lost, the founder freezes new asks for two weeks and reconstructs state from working-session notes. No referral activity proceeds on unverified state.

## Metrics

- Eligible clients per month.
- Ask acceptance rate.
- Introduction-to-qualified conversion (estimated).
- Time from introduction to qualified conversation.

## Disclaimer

Referrals are voluntary. Dealix does not guarantee referrals or compensate them by default. Estimated value is not Verified value.
