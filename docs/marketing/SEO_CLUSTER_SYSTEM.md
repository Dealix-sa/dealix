# SEO Cluster System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Dealix builds SEO around clusters of evidence-bearing content, not
> around keyword chasing. This document defines how clusters are
> chosen, how they are produced, and how they are audited.

SEO at Dealix is a long-arc trust signal. The same operating
principles that govern the rest of the Marketing OS apply here:
sober voice, refusal-aware copy, evidence over opinion, no
guaranteed outcomes, no manufactured urgency. SEO clusters are
designed to attract buyers who arrive already half-convinced that
Dealix operates the way it claims.

## Operating Principles

- No content is produced solely for ranking. Every SEO asset
  carries evidence a buyer can use.
- No keyword strategy overrides the brand voice. The Brand Guardian
  reviews SEO drafts on the same terms as any other draft.
- No SEO asset promises revenue, sales, or meetings.
- No SEO asset uses unapproved proof or unredacted data.
- No SEO asset participates in link schemes, doorway pages, or
  any other Google-policy-violating tactic.

## What Is a Cluster?

A cluster is a coordinated set of pages and posts on a defined
sub-topic, organised around a single pillar page. The pillar page
answers the broad question; the cluster answers the specific
questions that branch off it.

A Dealix cluster has:

- One pillar page (long-form, 2,500–4,000 words).
- 5–12 supporting pages (1,000–2,000 words each).
- A consistent internal link structure pointing from supporting
  pages to the pillar.
- An evidence footer on every page (cited sources, data, method).
- A refusal-aware framing throughout.

## Cluster Selection Criteria

Dealix selects a new cluster only when:

- The cluster reflects a question Dealix is genuinely asked in the
  field.
- Dealix has at least one direct piece of evidence in the cluster
  (an audit ledger pattern, a sector observation, or a documented
  refusal).
- The cluster aligns with one of the rungs on the product ladder.
- The cluster is defensible — Dealix can stand behind every claim
  in it.

Clusters chosen against these criteria are tracked in
`marketing/seo_clusters.csv`.

## Cluster Pillars (Working List)

This list is the working selection. Each pillar links to one of
the operating loops.

- **Saudi B2B Revenue Operating System.** What the category is,
  what it is not, how Dealix defines it. (Governance loop.)
- **Trust-gated AI revenue agents.** What "trust-gated" means in
  operating practice; refusal markers; eval gates. (Governance
  loop.)
- **PDPL-aware B2B marketing.** How Saudi B2B marketers operate
  under PDPL; what changes for outreach, data, and proof.
  (Governance loop.)
- **Founder-led revenue operations.** Patterns for founders running
  their own revenue motion; the Founder Console teardown.
  (Operating lesson loop.)
- **Saudi sector revenue patterns.** Sector-specific observations
  (financial services, healthcare, public sector readiness, B2B
  services). (Evidence loop.)
- **B2B objection teardowns.** Recurring objections and the
  refusal-aware responses to them. (Objection loop.)
- **Saudi B2B sales discipline.** The discipline Dealix uses in
  sales conversations; sales scripts; pricing posture.
  (Operating lesson loop.)

## Anatomy of a Cluster Page

Each cluster page follows a consistent skeleton.

1. **Title.** Sentence-case, specific, no power words.
2. **Sub-title.** One sentence that names the buyer or the
   question.
3. **TL;DR block.** Three to five sentences summarising the page's
   evidence and refusal posture.
4. **Body.** Sections with H2/H3 hierarchy; tables where useful;
   short paragraphs; refusal callouts where relevant.
5. **Evidence footer.** Sources, methods, dates.
6. **CTA.** A single CTA (Diagnostic, sector report, governance
   teardown).
7. **Localisation block.** Arabic peer-page link where applicable.

## Voice and Copywriting

The same rules from `COPYWRITING_RULES.md` apply. SEO pages tend
to attract drift toward keyword stuffing, listicle padding, and
clickbait sub-heads; the Brand Guardian flags all three.

Banned patterns specific to SEO:

- "Ultimate guide to X" titles.
- "Top N ways to" structures.
- "What is X? (And why you need it)" frames.
- Keyword density gaming (repeating a keyword to hit a percentage).
- Hidden text or off-screen keyword blocks.
- Doorway pages.

## Localisation

Arabic and English are peer surfaces. An Arabic SEO cluster is
authored, not translated. Where the English pillar exists, the
Arabic pillar exists as a peer; the URL and structure may differ
to fit Arabic search patterns.

## Technical SEO

- Site is rendered server-side or pre-rendered; client-only
  content is not used for primary copy.
- Canonical tags are correct.
- Sitemap is current.
- Robots.txt is conservative; non-public pages (e.g. internal
  Founder Console) are excluded.
- `hreflang` tags pair Arabic and English peers.
- Page speed meets the Lighthouse budget in `lighthouserc.js`.
- Accessibility meets the `pa11y` budget in `.pa11yrc.json`.
- Structured data (Article, FAQ) is added only where it accurately
  describes the page.

## Link Practices

- Internal links: supporting pages link to the pillar; the pillar
  links to all supporting pages.
- External outbound links: cited sources only. No paid links.
- Inbound links: earned through content quality. Dealix does not
  buy links, exchange links, or participate in PBNs.
- Guest posts: rare, founder-led, only on outlets that align with
  the Dealix voice and refusal posture.

## Refusal-Aware SEO

Each cluster page surfaces a refusal callout where relevant.
Examples:

- On a page about "B2B outreach": "What Dealix will not do — execute
  external sends on your behalf; promise meetings; bypass
  suppression lists."
- On a page about "sales pricing": "What Dealix will not do —
  publish per-rung pricing; quote a number outside the band; commit
  pricing verbally."

Refusal callouts are not asides; they are part of the trust contract
made visible to the search-driven reader.

## Approval Flow

1. Content Strategist drafts the page within an approved cluster.
2. Brand Guardian eval (claims-safety, brand-voice, keyword-
   stuffing detection).
3. Trust Guardian eval (refusal callout presence, proof posture).
4. Performance Analyst review (technical SEO, internal link
   structure).
5. Founder approval.
6. Page deployed by a human operator.
7. Trust ledger entry recorded with the page id and version.

## Refresh Cadence

- Pillar pages: refreshed annually or when a governance change
  affects the topic.
- Supporting pages: refreshed every 12–18 months.
- Sector pages: refreshed quarterly to align with sector reports.

A refresh requires the same approval flow as a new page.

## Eval Tests

The SEO-cluster eval set includes:

- Claims-safety scan.
- Brand-voice scan.
- Keyword-stuffing detection.
- Internal link integrity (broken links, orphan pages).
- Canonical and sitemap integrity.
- `hreflang` integrity between Arabic and English peers.
- Refusal callout presence on relevant pages.

A page that fails any test is removed from public display until
remediated.

## Failure Modes

- A page is published with guaranteed-outcome wording. Failure:
  claims safety. Retracted; eval upgraded.
- A page uses keyword stuffing. Failure: brand drift. Returned to
  the Content Strategist for rewrite.
- A cluster's pillar page rises in ranking while supporting pages
  do not. Failure: weak supporting structure. Cluster is reviewed
  in the quarterly audit.
- A page's evidence ages out. Failure: governance miss. Page is
  refreshed or retired.
- A backlink campaign appears in third-party tools. Failure:
  someone has bought links pointing to Dealix without permission.
  Disavow process triggered; trust ledger records the incident.

## Anti-Patterns

- "We will A/B test the rules." The rules are not subject to A/B
  testing.
- "We will write 100 thin pages to dominate the long tail." Banned.
- "We will hide a sales-y CTA in the middle of a content page."
  Banned.
- "We will run a link exchange with friendly sites." Banned.
- "We will scrape competitor outlines and rewrite them." Banned —
  Dealix writes from operating evidence, not from competitor
  inventories.

## Metrics That Matter

The Performance Analyst tracks:

- Organic sessions per cluster, segmented by intent (informational
  vs. evaluative vs. transactional).
- Qualified conversations sourced from organic.
- Refusal rate from organic-sourced fills.
- Refresh cadence adherence.
- Backlink quality (manual review, not raw count).

Metrics not optimised for: total page count, keyword position
fluctuations, "domain authority" from third-party tools.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Content calendar: `docs/marketing/CONTENT_CALENDAR_SYSTEM.md`.
- Copywriting rules: `docs/marketing/COPYWRITING_RULES.md`.
- Brand voice: `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- Landing page system: `docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md`.

## Why Clusters

A cluster outperforms a single page over time because it forms a
defensible body of work that a search engine can recognise as
genuine expertise. Dealix builds clusters because the alternative —
chasing single keywords with thin pages — collapses under the first
algorithm update and does nothing for trust.

A buyer who finds Dealix through a cluster has read enough to know
the voice, the refusal posture, and the operating loop before they
ever fill the form. The form-fill that follows is high-quality
because the buyer has self-qualified through the content. That is
the only kind of SEO conversion worth producing.
