# Landing Page Conversion System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Landing pages at Dealix are not funnels. They are trust surfaces.
> This document defines how a landing page is structured, what it
> may say, what it must refuse, and how it is measured.

A landing page at Dealix earns its right to exist by carrying
evidence and offering a sober next step. There is no "high-converting
swipe file" approach. The conversion that matters is a qualified
conversation; pages that produce unqualified conversations are
treated as failures regardless of click-through rate.

## Operating Principles

- A landing page must trace to a positioning statement from
  `docs/product/PRODUCT_POSITIONING.md`.
- No landing page promises revenue, sales, or meetings. Outcomes are
  described as evidence, decisions, queues, and drafts.
- No proof element (logo, screenshot, customer quote) appears
  without recorded approval in the trust ledger.
- The default call to action is a Diagnostic request, not a "book a
  demo" CTA, unless the page is rung-specific and the buyer has
  been pre-qualified through content or referral.
- Forms collect only the data Dealix needs to start the next step;
  every additional field requires a written reason.

## Anatomy of a Dealix Landing Page

Every landing page uses the same anatomy.

1. **Headline.** The positioning statement, short form, no hype.
2. **Sub-headline.** A one-sentence elaboration that names the
   buyer and the next step.
3. **What this is.** A 2–4 sentence description of the offer.
4. **What this is not.** An explicit anti-positioning statement.
5. **What we will not do.** A short refusal list visible above the
   fold.
6. **Evidence.** Approved proof elements only (governance teardowns,
   anonymised data points, sector report excerpts). No unverified
   logos.
7. **Process.** Three to five steps the buyer can expect, expressed
   as artefacts not adjectives.
8. **Pricing posture.** A statement on how Dealix prices (band-based,
   founder-approved) — the page does not display rung numbers.
9. **FAQ.** Five to ten questions sourced from the objection loop.
10. **Call to action.** A single primary CTA pointing to the
    Diagnostic Engagement Note request or a sector-specific intake.
11. **Footer.** PDPL posture link, brand line, trust statement.

## Page Types

The Marketing OS supports five page types, none of which deviate
from the anatomy above:

- **Home page.** Top-level positioning, all rungs alluded to,
  primary CTA is the Diagnostic.
- **Sector page.** Sector-specific positioning, sector-specific
  refusal list, sector report download CTA.
- **Offer page.** Rung-specific page (Sprint, Pilot, Retainer,
  Console) with the same anatomy and a rung-specific CTA.
- **Sector report download page.** Lead capture for sector report
  with the report excerpt visible and the full report behind a
  short form.
- **Long-form teardown page.** A founder-authored long-form piece
  with the standard footer and a Diagnostic CTA in-line.

## Forbidden Elements

A Dealix landing page may not include:

- Countdown timers, scarcity badges, fake urgency.
- "Guaranteed" anything in the copy.
- Customer logos that are not approved.
- "As seen in" press strips that are not directly attributable.
- "Trusted by N companies" counters without method.
- Auto-playing video.
- Pop-ups that interrupt the page.
- Cookie banners that pre-check non-essential cookies.

The Brand Guardian agent scans landing page drafts for these
patterns; the Trust Guardian agent confirms proof posture; the
Security Guardian confirms PDPL posture.

## CTAs

The CTA library is short on purpose.

- **Primary:** "Request a Diagnostic." A neutral, free, evidence-
  only path.
- **Secondary:** "Read the sector report." A content artefact, not
  a sales path.
- **Tertiary:** "Read a governance teardown." A founder content
  link.

A page may not stack four or five CTAs to chase clicks. Stacking
dilutes the page; the Brand Guardian flags it.

## Forms

The default form fields are minimal:

- Name.
- Work email.
- Company.
- Role.
- One free-text field: "what does evidence look like for you
  today?"

Any additional field requires a written reason. PII collection
beyond these fields is gated by the Trust Guardian.

Forms write to the lead inbox in the private ops runtime; no
external automation forwards the lead to a third-party CRM without
an integration agreement signed by the founder.

## Conversion Measurement

The Performance Analyst tracks:

- Form completion rate.
- Qualified conversation rate from the form (i.e. the form-fill
  becomes a Diagnostic request).
- Refusal rate (forms declined because the requester is on a
  suppression list, or the request is out of scope).
- Time to first response (founder-owned).

Metrics not optimised for: raw click-through rate, raw page-view
count, bounce rate as a vanity metric.

## Optimisation Loop

Pages are optimised on a quarterly cadence, not a continuous A/B
loop. Quarterly review covers:

- Which pages produced qualified conversations.
- Which pages produced refusals (and why).
- Whether the FAQ block still reflects the live objection inbox.
- Whether the refusal list is up to date with the trust contract.
- Whether evidence elements are still approved (re-approval may be
  needed if a customer reference window has expired).

Changes to a page are versioned and recorded in
`marketing/landing_page_registry.csv`.

## Speed, Accessibility, PDPL

- Landing pages must meet a Lighthouse performance budget defined in
  `lighthouserc.js`.
- Accessibility is measured by `pa11y` per `.pa11yrc.json`.
- PDPL posture is documented in the footer with a link to the
  Dealix PDPL posture statement.
- Cookies: only essential cookies by default. Non-essential cookies
  require explicit opt-in.

## Localisation

Every customer-facing landing page exists in Arabic and English.
The Arabic version is peer-quality, not a translation. Brand voice
calibration applies to both languages.

## Approval Flow

1. Content Strategist drafts the landing page.
2. Brand Guardian eval (claims-safety, brand-voice).
3. Trust Guardian eval (proof posture, refusal-list presence).
4. Security Guardian eval (PDPL posture, cookie behaviour).
5. Performance review (forms, CTAs, evidence ratio).
6. Founder approval.
7. Page deployed by a human operator.

The deployment action is recorded in the trust ledger.

## Anti-Patterns

- **Funnel maximisation.** Stacking CTAs, removing refusal lists, or
  inflating proof elements to chase conversion rate. Banned.
- **Manufactured social proof.** "1,000 founders trust us" without
  method. Banned.
- **Outcome inflation.** "Our customers see N% improvement" without
  a written method. Banned.
- **Hidden pricing.** Pretending pricing does not exist while
  routing the buyer to a sales call. Dealix pricing posture is
  stated; bands are quoted on conversation; numbers live in the
  offer document.
- **Form-field creep.** Adding fields because "we want to know more
  about leads". Each field requires a reason.

## Failure Modes

- Landing page receives many form-fills but few qualified
  conversations. Failure: the page is mis-targeting or the
  positioning is wrong for the channel. Page is reviewed.
- Landing page receives high-quality fills but the founder cannot
  respond in time. Failure: throughput limit. The page may be
  paused until capacity is restored.
- Landing page produces a refusal spike. Failure: the page is
  attracting out-of-scope buyers. Refusal reasons are reviewed and
  the page is recalibrated.
- Landing page surfaces an unapproved customer name. Failure: proof
  safety. The page is paused immediately; trust ledger records the
  incident; eval is upgraded.

## Cross-References

- Positioning: `docs/product/PRODUCT_POSITIONING.md`.
- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Brand voice: `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- Copywriting rules: `docs/marketing/COPYWRITING_RULES.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.

## Audit

The Trust Guardian audits every live landing page quarterly:

- Refusal list present and current.
- Proof elements approved and within their approval window.
- PDPL posture link present.
- Cookie behaviour compliant.
- CTA stack within the limit.
- Brand voice within the calibration.

Audit results are filed in `marketing/landing_page_audit.csv`.

## Why a Trust Surface, Not a Funnel

A funnel optimises for the next click. A trust surface optimises
for the next decision. Dealix designs pages that a buyer can read
without feeling moved against their will. That posture is harder to
build and easier to keep — and it is the only kind of marketing that
holds up under PDPL scrutiny, founder review, and the buyer's own
internal procurement.
