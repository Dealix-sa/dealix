# Dealix Marketing Asset Guide

How to build proposal documents, sales decks, social cards, and outreach drafts so they look and read like Dealix.

## 1. Asset families

| Asset                       | Source folder                              | Template               |
|-----------------------------|--------------------------------------------|------------------------|
| Proposal (AR + EN)          | `docs/proposals/`                          | `proposal-bilingual.md`|
| Sales deck                  | `docs/decks/`                              | `sales-deck.md`        |
| Sector report               | `docs/sector-reports/`                     | varies per sector      |
| Sample / Proof Pack         | `docs/proof-packs/` (private)              | `proof-pack.md`        |
| Social card (OG / LinkedIn) | `assets/brand/social/`                     | 1200×630 / 1080²       |
| Email outreach draft        | `data/marketing/outreach_drafts.csv`       | bilingual fields       |
| LinkedIn outreach draft     | `data/marketing/outreach_drafts.csv`       | bilingual fields       |
| Partner deck (co-brand)     | `docs/decks/partners/`                     | `partner-deck.md`      |

## 2. Proposal anatomy (canonical structure)

1. **Cover** — Customer name + Dealix lockup + date + proposal number.
2. **Executive summary** (AR + EN) — 1 paragraph each, lead with the metric.
3. **Diagnosis** — what we observed (data + interviews). No claims without source.
4. **Proposed engagement** — the rung on the offer ladder. Time-boxed.
5. **Deliverables** — concrete artefacts (data pack, draft pack, sample pack, dashboards).
6. **Trust & approval** — what we will NOT do without explicit approval.
7. **Pricing** — SAR, transparent, no hidden line items.
8. **Timeline** — day-by-day.
9. **KPIs** — what we measure, before and after.
10. **Acceptance & signature** — counter-signed by founder + customer.

## 3. Visual rules

- **Background:** Deep Navy `#0B1220` for digital decks; White for printed proposals.
- **Accent:** Emerald Teal `#00D1A1` — section dividers, KPI numbers, CTA highlights.
- **Type:** Inter + IBM Plex Sans Arabic. Display 700–800. Body 400–500.
- **Logo:** Lockup on cover and back. Icon-only in headers/footers of internal pages.
- **Photography:** Avoid stock photography. Prefer abstract Dealix gradients or product screenshots.

## 4. Bilingual layout patterns

| Pattern              | When to use                                        |
|----------------------|----------------------------------------------------|
| Side-by-side columns | Proposals (AR right column, EN left column)        |
| Stacked              | Decks where slide real estate is tight             |
| Separate documents   | Sector reports — one AR file, one EN file          |

Never auto-translate. Each language is written by a human or human-reviewed.

## 5. Social cards

- **Default OG card** — Dealix lockup centred on Deep Navy with one tagline line.
- **Blog post OG** — Lockup top-left, post title in white display 60–72px, sub-line in Soft Silver.
- **LinkedIn share card** — 1200×630, same template as OG.
- **Avatar** — Icon-only on Deep Navy. 1080×1080 with safe area 80px.

## 6. Email signature template

```
[Name]
[Title], Dealix
Intelligent Deals. Real Growth.
[email]   |   [phone]
dealix.io
```

No quotes. No "sent from my iPhone". No banner image (it breaks rendering in clients).

## 7. Outreach draft fields

Every outreach draft (Email or LinkedIn) must carry these fields before it can be queued for approval:

- `target_account` — company name
- `target_contact` — person name + title
- `channel` — `email` or `linkedin`
- `language` — `ar` or `en` or `bilingual`
- `subject` — for email only
- `body` — < 110 words for email, < 80 words for LinkedIn first-touch
- `personalisation_evidence` — citation / observation that justifies the message
- `proof_attached` — what artefact accompanies the message (or `none`)
- `approval_state` — `draft` / `queued` / `approved` / `held` / `rejected`
- `founder_note` — optional reviewer note

Drafts without all required fields cannot reach the approval queue.

## 8. Refusal copy (for sales rejections)

When declining a customer / partner request that violates doctrine:

> "We can't do that — here's why: [reason]. Here's what we *can* do that gives you the same outcome: [alternative]."

Never go silent on a refusal. Always give an alternative or a referral.
