# LinkedIn Outreach Guide

LinkedIn is a relationship surface, not a send channel. Dealix uses LinkedIn for founder voice, considered DMs, and content distribution. Automation tools and InMail sequences are not Dealix channels.

**Source of truth:** `$PRIVATE_OPS/linkedin_outreach_log.csv`
**Owner:** Founder
**Trust gate:** A2 — every direct message to a non-connection is reviewed before send.

## What's allowed

- A direct, named connection request from the founder with a specific reason.
- A DM to a 1st-degree connection in the context of an existing conversation.
- A reply to a comment on the founder's content.
- A DM to someone who has explicitly invited contact.

## What's not allowed

- Automated connection invites.
- Sequenced DMs (LinkedIn-native or third-party tools).
- Scraping LinkedIn for contact data.
- Posting on behalf of the founder without explicit per-post approval (A2).
- Buying or renting LinkedIn lead lists.

Blocked by `policies/dealix_control_policy.yaml`. LinkedIn automation tools are not on the Dealix tool allowlist.

## Anatomy of a Dealix LinkedIn DM

| Section | Length |
|---------|--------|
| Greeting (named) | 1 line |
| Reason (specific, evidenced) | 2-3 sentences |
| Offer (one named action) | 1 line |
| Sign-off | 1 line |

Total: under 80 words. Bilingual if recipient is Saudi business reader: AR first.

## Connection request

A connection request is treated as outreach. It carries a one-sentence note. No note is acceptable only for prior in-person meetings. Generic notes are not used.

## Founder voice on LinkedIn

Posting is governed by `docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md`. The system never posts on the founder's behalf. The agent drafts; the founder sends.

## Engagement

Comments on the founder's posts are read daily by the founder. Comments by named buyers may trigger Reply Routing (`docs/revenue/REPLY_ROUTING_SYSTEM.md`).

## Failure modes

- **Automated invite leak:** a tool sends invites without founder approval. Detection: weekly audit against connection history. Recovery: stop, apologise to recipients, remove tool.
- **Generic note:** a connection request goes out with no reason. Detection: pre-send check. Recovery: rewrite with specific reason.
- **Guarantee in DM:** a DM contains "guaranteed" language. Detection: lint. Recovery: rewrite, re-approve.

## Recovery path

If LinkedIn data shows any pattern of automated activity, the founder pauses all LinkedIn outbound, audits the tool stack, and re-enables only after a clean week.

## Metrics

- DMs sent per week (founder only).
- Reply rate (estimated).
- Connection acceptance rate (estimated).
- Automation incidents per quarter (target: 0).

## Disclaimer

LinkedIn is a respectful relationship channel. Dealix does not guarantee responses, meetings, or revenue. Estimated value is not Verified value.
