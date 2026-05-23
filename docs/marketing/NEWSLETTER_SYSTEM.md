# Newsletter System

The newsletter is the steady, opt-in channel that builds Dealix's earned-attention base. It is bilingual, evidence-forward, and weekly.

**Source of truth:** `$PRIVATE_OPS/newsletter_state.csv`
**Owner:** Marketing Lead
**Trust gate:** A1 for content; A2 for any change to the subscriber list or sending domain.

## Cadence and format

| Slot | Length |
|------|--------|
| One-paragraph founder note (EN + AR) | 150 words each |
| One observation from the Revenue Factory (EN + AR) | 200 words each |
| One case-safe pattern (EN + AR) | 200 words each |
| One link recommendation (EN + AR) | 50 words each |
| Disclaimer | 1 line |

Total: about 1,300 words. One send per week. Day fixed (Tuesday morning Riyadh time).

## Subscription discipline

- Single opt-in by default. Double opt-in for any list imported from a partner.
- Unsubscribe is a one-click action and is honoured immediately.
- No re-engagement of an unsubscribed contact without explicit re-opt-in.

## Production

1. Marketing Lead drafts the week using the calendar (`docs/marketing/CONTENT_CALENDAR_SYSTEM.md`).
2. Brand Guardian lints (`docs/ai/BRAND_GUARDIAN_AGENT.md`).
3. Bilingual parity check.
4. Founder approves at A1.
5. Send. Logged in `newsletter_state.csv` with send-time, open rate, click rate.

## Sending infrastructure

Send is through a provider that supports:

- PDPL-aware data handling.
- One-click unsubscribe.
- Verified domain (SPF, DKIM, DMARC aligned).
- Send-time audit logs.

Provider change requires founder approval.

## Failure modes

- **Send to suppressed contact:** a unsubscribed contact receives the newsletter. Detection: pre-send check + audit. Recovery: contact removed, written apology, root cause filed.
- **Bilingual asymmetry:** EN sent, AR delayed. Detection: parity check. Recovery: AR is a send blocker.
- **Open-rate collapse:** open rate drops more than 50% in a week. Detection: post-send check. Recovery: investigate domain reputation, content quality, send time.

## Recovery path

If newsletter governance is in doubt (list integrity, send authenticity), the founder pauses send until the list and the sending infrastructure are recertified.

## Metrics

- Active subscribers.
- Open rate (estimated).
- Click rate (estimated).
- Unsubscribe rate per send.
- Inbound conversations attributed to newsletter (estimated).

## Disclaimer

The newsletter is reading material. It does not promise outcomes. Estimated value is not Verified value.
