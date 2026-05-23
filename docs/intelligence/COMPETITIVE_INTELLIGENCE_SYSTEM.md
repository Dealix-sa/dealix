# Competitive Intelligence System

**Owner:** Strategy Office
**Source of truth:** This doc + `docs/positioning/COMPETITIVE_NARRATIVE.md`

## Purpose

Competitive intelligence at Dealix is operational, not voyeuristic. The goal is to know enough about the categories and patterns Dealix competes with to:

1. Sharpen the positioning narrative.
2. Anticipate objections.
3. Spot category drift in the market that requires Dealix to respond.
4. Identify partnership candidates (some competitors are integration partners, not enemies).

## What we monitor

| Category | Examples | What we watch |
|---|---|---|
| CRM platforms | HubSpot, Salesforce, Zoho | KSA pricing, Arabic rollout, AI feature additions |
| Sales engagement | Salesloft, Outreach, Apollo (engagement layer) | KSA presence, founder-buyer messaging |
| Conversation intelligence | Gong, Chorus | KSA expansion signals |
| AI sales agents | Various, evolving | Trust-gate claims, regional examples |
| Generic agencies | Saudi B2B agencies | Sprint-like productized offers, retainer pricing |
| Scraping vendors | Apollo (data), ZoomInfo, scrapers | KSA buyer adoption signals (anti-pattern Dealix avoids) |
| Saudi B2B consultancies | Local firms | Sector positioning, partnership openings |

## What we do NOT monitor

- Individual sales reps' activity.
- Private customer rosters.
- Anything that requires scraping a competitor surface.

Competitive monitoring stops at publicly available information and conversation with industry peers under normal professional norms.

## Monitoring rhythm

| Activity | Cadence |
|---|---|
| Public surface scan (websites, blog, careers) | Monthly per category |
| Public messaging diff (track changes in H1, H2, claims) | Quarterly |
| Pricing intelligence (where public) | Quarterly |
| Partner/integration network scan | Quarterly |
| Saudi launch / KSA hire signals | Continuous via public news |

Each scan produces a short note. The note answers: what changed, does it threaten the Dealix category, do we need to respond.

## Three response patterns

When a competitive signal lands, the response is one of three actions:

### 1. Ignore (default)

Most competitor changes do not require a response. A new feature in a CRM, a new logo in a competitor's wall, a new blog post in an adjacent category — these go in the note and stay there.

### 2. Sharpen positioning

If a competitor adopts language adjacent to Dealix's category (e.g., another vendor starts calling itself a "Revenue OS"), Dealix sharpens its own positioning:

- Add explicit rules the competitor does not enforce.
- Re-publish category-language docs.
- Update the comparison row in `docs/positioning/COMPETITIVE_NARRATIVE.md`.

### 3. Engage as partner

If a competitor's product is actually complementary (e.g., a CRM that integrates with Dealix), Dealix opens a partnership conversation:

- Add to the partner pipeline.
- Map joint customer scenarios.
- Define integration boundaries.

## Anti-pattern: feature wars

Dealix does not respond to a competitor's feature release by building a matching feature. The Revenue OS category is defined by architecture (gates, Proof Packs, Capital Loop), not by feature parity.

A feature war is a sign that positioning has weakened. The recovery is positioning, not feature.

## Competitive intelligence and the customer

- Discovery calls: if a buyer mentions a competitor, listen, confirm what they value, and answer using `docs/positioning/COMPETITIVE_NARRATIVE.md`.
- Decks: do not include competitor logos. Comparison happens in conversation, not on slides.
- Proposals: do not name competitors. The proposal is about the customer.

## Competitive intelligence storage

- Notes live in `docs/intelligence/competitive-notes/` (private; not in this commit).
- Public-facing comparisons live in `docs/positioning/COMPETITIVE_NARRATIVE.md`.
- Sector-specific competitive maps appear in sector reports under aggregated, non-identifying language.

## Trust gate

| Action | Approval class |
|---|---|
| Internal competitive note | A0 — Self |
| Updated comparison row in COMPETITIVE_NARRATIVE.md | A1 — Strategy Office |
| Public statement referencing a competitor | A3 — Founder |
| Partnership outreach to a "competitor" | A2 — Founder + Strategy Office |

## Failure mode

- Dealix becomes reactive — features chase a competitor's roadmap.
- A competitor's launch produces a panicked positioning update that drifts from the category.
- Public-facing copy disparages a competitor and reads defensive.

## Recovery path

1. Pull the reactive copy.
2. Re-anchor to category language in `CATEGORY_CREATION_OS.md`.
3. Sit with the signal for 72 hours before any further response.

## Cross-links

- Competitive narrative: `docs/positioning/COMPETITIVE_NARRATIVE.md`
- Category creation: `docs/positioning/CATEGORY_CREATION_OS.md`
- Objection handling: `docs/positioning/OBJECTION_HANDLING.md`

## Disclaimer

Competitive observations are positional, not predictive. Dealix does not guarantee category outcomes or competitor behavior. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
