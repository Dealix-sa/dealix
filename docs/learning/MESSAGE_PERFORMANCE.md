# Message Performance

How outbound messages are measured and improved.

## Metrics per message variant
- Sent count.
- Reply rate.
- Positive reply rate.
- Meeting-booked rate.
- Time to reply.

## Variants tracked
- Subject or opening line.
- CTA phrasing.
- Length.
- Channel (LinkedIn, email, WhatsApp).
- Sector.

## Process
- Each new variant gets a name and a hypothesis.
- Variants run until they have at least 25 sends.
- Top performer becomes the new baseline.
- Underperformers are retired and logged.

## Storage
- Raw send and reply data: `dealix-ops-private/learning/messages/`.
- Summary table updated weekly in this file.

## Rule
A message variant we cannot measure is a story we tell ourselves. If it is not measured, it is not in production.
