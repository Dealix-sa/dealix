# Landing Page Conversion System

The Landing Page Conversion System is the discipline for designing, testing, and improving the pages that convert anonymous attention into a named conversation.

**Source of truth:** `$PRIVATE_OPS/landing_page_state.csv`
**Owner:** Marketing Lead
**Trust gate:** A1 for copy and experiment launch; A2 for pricing changes on any page.

## Page anatomy

| Section | Purpose | Length |
|---------|---------|--------|
| Hero | Single-sentence positioning + sub-line | 2 sentences |
| Proof strip | 3-5 case-safe anchors | 1 line each |
| What it does | Three Revenue Factory stations in plain language | 200-300 words |
| Trust | One paragraph on policy, gates, audit | 100-150 words |
| Pricing | Reference prices linked to `docs/product/DEALIX_PRODUCT_LADDER.md` | Table |
| FAQ | 6-10 questions, evidence-forward | 400-700 words |
| CTA | One primary action (book a diagnostic) | One button |
| Disclosure | Standard estimated-vs-verified line | 1 line |

Bilingual EN + AR. Every page has a `/ar/...` mirror with matching structure.

## CTA discipline

One primary action per page. Common patterns:

- "Book a 30-minute diagnostic call" (rung 1).
- "See a sector report" (top of funnel).
- "Read a case-safe summary" (mid funnel).

Multiple CTAs dilute decision. Secondary CTAs (newsletter, sector report subscription) appear in the footer, not the body.

## Experiments

| Element | Tested |
|---------|--------|
| Hero copy | Variants A/B/C, equal traffic |
| Proof anchor order | Permutations |
| FAQ inclusion | Items added or removed |
| CTA label | Variant test |
| Bilingual mirror | EN and AR scored separately |

Every experiment has:

- Stated hypothesis.
- Pre-registered metric.
- Sample-size pre-commitment.
- Stop rule.

The experiment register lives in `docs/performance/EXPERIMENT_BACKLOG.md`.

## Failure modes

- **Spurious win:** experiment ended early on a non-pre-registered metric. Detection: experiment audit. Recovery: re-run with discipline; do not deploy.
- **Pricing drift:** a page lists a price below the reference. Detection: copy audit. Recovery: pull or correct.
- **Hype creep:** a hero sentence promises an outcome. Detection: lint. Recovery: rewrite to factory-language.

## Recovery path

If experiment data quality is in doubt, the Marketing Lead pauses all active experiments until tracking is recertified.

## Metrics

- Visitor-to-CTA conversion by page (estimated).
- CTA-to-qualified-conversation rate (estimated).
- Experiment win rate (estimated).
- Bilingual page parity score.

## Disclaimer

Pages describe what Dealix is. They do not promise outcomes. Estimated value is not Verified value.
