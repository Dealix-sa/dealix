# Channel Policy

**Global rule:** the system only **generates drafts**. No SMTP, no API send,
no browser automation, no scraping. The founder reviews and sends manually.
Source: `config/commercial_channels.json`.

---

## Email (cold + follow-up)

**Allowed:** draft generation only.
**Forbidden:** SMTP, send APIs, bulk sending, scraping personal emails.

- Every draft **must** contain a working opt-out line.
- Before *any* real sending the founder must complete a **domain readiness
  checklist** and run a **separate ramp plan** — this OS does not send.

### Domain readiness checklist (must be green before manual sending)

- [ ] **SPF** record published
- [ ] **DKIM** signing configured
- [ ] **DMARC** policy published (start at `p=none`, monitor, then tighten)
- [ ] **Google Postmaster** tools set up and monitored
- [ ] **Bounce tracking** in place
- [ ] **Unsubscribe / opt-out** handling operational
- [ ] **Warm-up ramp plan** (start low volume, increase gradually)
- [ ] **Suppression list owner** named and process documented

> Cold email is **GO for drafting, NO-GO for sending** until the checklist is
> signed off by the founder.

---

## LinkedIn

**Allowed:** manual draft only.
**Forbidden:** browser automation, scraping, auto-connect, auto-message, bots.

The founder copies each draft and sends it by hand. There is no automation of
any kind. **NO-GO for any LinkedIn automation.**

---

## WhatsApp

**Allowed:** reply templates for inbound messages or clearly opted-in contacts.
**Forbidden:** cold outreach, sending, broadcast.

- **No cold WhatsApp outreach — ever.**
- Every WhatsApp draft is `status = manual_review_only`.
- Templates exist only to help the founder reply faster to people who already
  reached out or explicitly opted in.

> **NO-GO for WhatsApp cold outreach.**

---

## Website / contact forms

**Allowed:** draft generation only.
**Forbidden:** auto-submit.

The founder copies the draft and submits it manually.

---

## Summary Go/No-Go

| Channel | Drafting | Sending |
|---------|----------|---------|
| Cold email | ✅ GO | ⛔ NO-GO until domain checklist signed off |
| Follow-up | ✅ GO | ⛔ Manual only, genuine prior touch required |
| LinkedIn | ✅ GO (manual) | ⛔ NO-GO for any automation |
| WhatsApp | ✅ GO (inbound/opt-in templates) | ⛔ NO-GO for cold outreach |
| Website forms | ✅ GO | ⛔ Manual submit only |
