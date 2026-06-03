# Cold Email Sequences — English
# تسلسلات البريد البارد — الإنجليزية

**Path:** `docs/outreach/COLD_EMAIL_SEQUENCES_EN.md`
**Audience:** Founder + Draft Operator
**Last updated:** 2026-06-02
**Status:** Active — templates require review and editing before each send

---

## General Rules for All Sequences

1. Every message requires founder approval before sending — no exceptions. See [`docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md`](./FOUNDER_APPROVAL_QUEUE_AR.md).
2. A one-click unsubscribe line is mandatory in every message — enforced in `auto_client_acquisition/email/compliance.py` via `append_opt_out_line()`.
3. No fake Re: or Fwd: in subject lines. Subject lines must accurately reflect message content.
4. Personalization score must be P1 or above. A P0 draft is blocked by the factory gate. See [`docs/outreach/PERSONALIZATION_RULES_AR.md`](./PERSONALIZATION_RULES_AR.md).
5. No guaranteed sales figures — all estimates are prefaced with "in many sector cases" or "based on sector patterns."
6. Send timing respects the warm-up ramp. See `COLD_EMAIL_DRAFT_FACTORY_AR.md` Section 5.
7. After follow-up 2, the contact cycle stops. The account moves to `nurture` or `do_not_contact` state. No fourth outreach in a single cycle.
8. Do not send on behalf of the customer without explicit approval. Dealix drafts; the founder sends.
9. No purchased lists. No scraping. Every data source is documented. See [`docs/outreach/PROSPECT_RESEARCH_OS_AR.md`](./PROSPECT_RESEARCH_OS_AR.md).
10. Honor opt-out requests immediately — within 24 hours maximum. Add to suppression list permanently.

**Personalization Slots:**
- `{{COMPANY}}` — Company name
- `{{SECTOR_PAIN}}` — Sector pain from `research_agent.py`
- `{{PERSONALIZATION_NOTE}}` — Specific signal from research (minimum P1)
- `{{OFFER}}` — The offer: pilot_499 / pilot_999 / pilot_1500 / partnership
- `{{SENDER_NAME}}` — Sender name
- `{{CALENDLY_LINK}}` — Booking link

---

## Sequence 1 — First-Touch

**Goal:** Open a conversation with a new account. Generate genuine interest; do not request a purchase decision.

**Timing:** Day 0 (after founder approval)

**Daily draft cap for this type:** 100 drafts (see distribution table in `COLD_EMAIL_DRAFT_FACTORY_AR.md`)

---

### Subject Options

**Option A — Sector pain:**
```
{{COMPANY}} — response speed on inbound leads
```

**Option B — Direct question:**
```
One question about lead qualification — {{COMPANY}}
```

**Option C — Sector link:**
```
{{SECTOR}} in Saudi Arabia: inbound leads and response time
```

---

### Message Template

```
Hi {{COMPANY}} team,

{{PERSONALIZATION_NOTE}}

{{SECTOR_PAIN}}

Dealix responds to inbound inquiries in Gulf Arabic — it captures the necessary details
and passes qualified prospects to your sales team. It completes the work of your team;
it does not replace it.

{{OFFER}} — 7 days on your actual leads. You evaluate the results yourself. Then you decide.

Would 20 minutes this week work for you?
{{CALENDLY_LINK}}

{{SENDER_NAME}}
Dealix — https://dealix.me

— To unsubscribe, reply STOP.
```

**Single CTA:** Request for a 20-minute meeting — no multiple CTAs in one message.

**Compliance note:**
- `evidence_level` must be at minimum `sector_pattern`
- Do not present conversion figures as fact — present as sector-level estimates only

---

## Sequence 2 — Follow-Up 1

**Goal:** A light reminder. A quiet inquiry about interest.

**Timing:** 3 business days after first-touch with no reply

**Daily draft cap for this type:** 75 drafts

---

### Subject Options

**Option A:**
```
Following up — {{COMPANY}} and Dealix
```

**Option B:**
```
Did my message reach you? — {{COMPANY}}
```

**Option C (sector signal):**
```
Reminder — {{SECTOR}} leads and response time
```

---

### Message Template

```
Hi,

Following up on my previous message about qualifying inbound inquiries for {{COMPANY}}.

{{PERSONALIZATION_NOTE}}

If the timing works — 20 minutes is enough to show you how Dealix operates on real leads
in the {{SECTOR}} sector.
{{CALENDLY_LINK}}

If this is not a priority right now, let me know and I will reach out at a better time.

{{SENDER_NAME}}
Dealix — https://dealix.me

— To unsubscribe permanently, reply STOP or OPT OUT.
```

**Single CTA:** Meeting link or explicit request to reschedule with a date.

---

## Sequence 3 — Follow-Up 2

**Goal:** A final attempt before the contact cycle closes for this account.

**Timing:** 5 business days after follow-up 1 with no reply

**Daily draft cap for this type:** 50 drafts

**Note:** After this message the account moves automatically to close-loop or nurture. There is no fourth message in this cycle.

---

### Subject Options

**Option A:**
```
Last message — {{COMPANY}}
```

**Option B:**
```
{{COMPANY}} — Dealix pilot before end of month?
```

---

### Message Template

```
Hi {{COMPANY}} team,

This is my last message for now.

The {{SECTOR}} sector is competitive on inbound response speed. In many sector cases,
the difference between winning and losing a prospect is measured in minutes, not hours.

If this is a current priority for your team — one demo makes the picture clear:
{{CALENDLY_LINK}}

If not, no problem. I will keep your file and reach out at a better time.

{{SENDER_NAME}}
Dealix — https://dealix.me

— To unsubscribe permanently, reply STOP or OPT OUT.
```

**Single CTA:** Demo link or explicit request to stop outreach.

---

## Sequence 4 — Proposal-Intro

**Goal:** Send a tailored proposal after a meeting or explicit request.

**Timing:** Within 24 hours of `meeting_booked` or `proposal_needed` state

**Daily draft cap for this type:** 15 drafts

**Condition:** This sequence is used only for accounts in `meeting_booked` or `proposal_needed` state. It is never sent to an account that has not had a prior meeting or explicit request.

---

### Subject Options

**Option A:**
```
Dealix proposal for {{COMPANY}} — {{OFFER}} + details
```

**Option B:**
```
As discussed — Dealix plan for {{COMPANY}}
```

---

### Message Template

```
Hi {{COMPANY}} team,

Based on our discussion — attached is a summary of the proposal tailored to your
situation in the {{SECTOR}} sector.

The proposal includes:
- {{OFFER}} for 7 days on actual leads from your existing channels
- A weekly report of evidenced opportunities (no invented figures)
- Direct access to the founder throughout the pilot period

Suggested next step: review the proposal with your team and let me know your decision
within 5 business days.

[Attachment: Proposal summary — PDF]

If you need any clarification:
{{CALENDLY_LINK}}

{{SENDER_NAME}}
Dealix — https://dealix.me

— To unsubscribe, reply STOP.
```

**Single CTA:** Review the proposal and communicate a decision.

**Compliance note:**
- "Evidenced opportunities" — not "guaranteed sales"
- No guaranteed ROI figures in the message body
- Any attached document is subject to compliance review before sending

---

## Sequence 5 — Close-Loop (Breakup)

**Goal:** End the contact cycle respectfully. Leave the door open without pressure.

**Timing:** After follow-up 2 with no reply, or after proposal-intro with no reply for 10 days

**Daily draft cap for this type:** 10 drafts

**Outcome:** Account moves to `nurture` state (re-engage after 60–90 days) or `lost`.

---

### Subject Options

**Option A:**
```
{{COMPANY}} — closing the file
```

**Option B:**
```
Final note — Dealix and {{COMPANY}}
```

---

### Message Template

```
Hi,

I have not heard back — which is completely understandable. Your team has other priorities.

I will close this file now.

If priorities change and you need a solution for qualifying inbound inquiries in the
{{SECTOR}} sector at a later point — please do not hesitate to reach out:
{{CALENDLY_LINK}}

{{SENDER_NAME}}
Dealix — https://dealix.me

— If you do not want any future contact from Dealix, reply STOP and your address
will be added to our do-not-contact list immediately and permanently.
```

**Single CTA:** Link if priorities change, plus a clear path to permanent opt-out.

---

## Sequence Summary

| Stage | Day | Draft Type | No-Reply Action |
|---|---|---|---|
| First-touch | 0 | `first_touch` | Wait 3 business days |
| Follow-up 1 | +3 biz days | `follow_up_1` | Wait 5 business days |
| Follow-up 2 | +8 biz days | `follow_up_2` | Close-loop after 5 days |
| Close-loop | +13 biz days | `close_loop` | `nurture` or `lost` state |
| Proposal-intro | Post-meeting | `proposal_intro` | Context-specific follow-up |

**Standard contact cycle maximum:** 13 business days before active outreach stops.

---

## Send Volume Hard Limits (Reminder)

These are absolute ceilings enforced in `auto_client_acquisition/email/compliance.py`:

| Condition | Daily limit |
|---|---|
| SPF missing | 0 sends |
| SPF only (no DKIM) | 50 sends |
| SPF + DKIM (no DMARC) | 500 sends |
| All three + unsubscribe | Ramp applies (see `COLD_EMAIL_DRAFT_FACTORY_AR.md` Section 5) |
| Drafting (no send) | Up to 250 drafts per day |

Drafts and sends are different counters. 250 drafts per day is always permitted. 250 sends per day requires the full warm-up ramp to be completed first.

---

## Related Documents

- [`docs/outreach/COLD_EMAIL_SEQUENCES_AR.md`](./COLD_EMAIL_SEQUENCES_AR.md) — Arabic parallel of this document
- [`docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`](./COLD_EMAIL_DRAFT_FACTORY_AR.md) — Draft production conditions
- [`docs/outreach/PERSONALIZATION_RULES_AR.md`](./PERSONALIZATION_RULES_AR.md) — P0–P3 level definitions
- [`docs/outreach/PROSPECT_RESEARCH_OS_AR.md`](./PROSPECT_RESEARCH_OS_AR.md) — How signals are gathered
- [`docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md`](./COLD_EMAIL_COMPLIANCE_AR.md) — Full compliance rules
- [`docs/outreach/UNSUBSCRIBE_POLICY_AR.md`](./UNSUBSCRIBE_POLICY_AR.md) — Unsubscribe policy
- [`docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md`](./FOUNDER_APPROVAL_QUEUE_AR.md) — Approval process
- [`docs/commercial/PRODUCT_CATALOG_AR.md`](../commercial/PRODUCT_CATALOG_AR.md) — pilot_499 / pilot_999 / pilot_1500 offer details
- [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md) — Master GTM index
- `auto_client_acquisition/email/compliance.py` — `append_opt_out_line()` + send gates
- `auto_client_acquisition/email/daily_targeting.py` — Sequence scheduling

---

ملاحظة: هذا الملف باللغة الإنجليزية بتصميم. النسخة العربية الكاملة في `docs/outreach/COLD_EMAIL_SEQUENCES_AR.md`.

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
