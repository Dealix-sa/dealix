# Claims Guide

> Practical guide for writing claims that will pass `claim_guard.py`.

## The Three-Question Test

Before writing any claim, ask:
1. **Is this true?** (factually accurate)
2. **Can I cite it?** (source URL or internal data)
3. **Would a regulator agree it's substantiated?** (Saudi PDPL / SDAIA / generic advertising standards)

If any answer is "no", rewrite.

## Examples — Bad vs Good

### Bad
> "Dealix saved a logistics client 40 hours per week with our AI-powered automation."

### Why bad
- No client identified or consented
- "40 hours" no source
- "AI-powered automation" no scope
- "Saved" implies measurement we may not have

### Good
> "In a recent Revenue Sprint, our scored prospect list and outreach drafts replaced ~6 hours of manual sourcing per week for the client team. The client's framing — not ours. (Evidence pack EP-2026-003.)"

### Bad
> "Industry-leading trust posture."

### Why bad
- "Industry-leading" is unverifiable boast
- No specifics

### Good
> "Every external send passes our claim_guard + approval matrix; approval log is auditable on request. (See docs/trust/APPROVAL_MATRIX.md.)"

### Bad
> "Guaranteed 30% increase in qualified leads."

### Why bad
- Guarantees require contract enforcement we don't offer
- Outcome promises violate `OFFER.md`
- Number has no basis

### Good
> "Sprint deliverable: 50 prospects scored ≥ 60 fit + 3 message variants. Reply rate depends on your sending discipline; typical first-week reply rate from comparable Sprints: 5-15% (n=2, small sample)."

## Allowed Modifiers

These soften claims so they fit evidence:
- "In our last N engagements..."
- "Based on n=X data points..."
- "Typical range observed: X–Y..."
- "Client-reported, unverified by us..."
- "Aligned with..." (instead of "compliant with")
- "Designed to..." (instead of "guarantees")

## Forbidden Modifiers

- "Often"
- "Many of our clients..."
- "Most companies..."
- "Industry data shows..." (without citation)
- "On average..." (without showing the average)

## Per-Channel Quick Reference

### LinkedIn post
- One claim max per post
- Cite or qualify
- Show your work (link to evidence pack or method note)

### Landing page
- Every headline → claim; every claim → evidence pack
- No outcome promises without explicit qualifier
- "What we don't do" section recommended

### Proposal
- Pricing concrete (per `PRICING_STRATEGY.md`)
- Scope explicit (in/out)
- No client-results promises ("we deliver the system; outcomes depend on your sending discipline")

### Case study
- Client name only with explicit consent
- Numbers only if measured + verifiable
- Method section required

### Email outreach
- One specific reason for outreach
- No "we help companies like yours" (lazy)
- No "trusted by industry leaders" (until literally true)

## Saudi-Specific Sensitivities

- Religious or cultural claims: avoid
- Government affiliations: never claim unless explicit
- Royal references: never use as social proof
- Compliance with Saudi regulations: cite specific regulation + how, not blanket "compliant"

## When You Need To Make A Big Claim

If you genuinely need to assert something material:
1. Produce evidence pack first (in `content/proof_library/`)
2. Run `claim_guard.py` with `--evidence-pack EP-NNN` flag
3. Founder approves
4. Advisor approves (for A3 or A4 claims)
5. Publish + monitor for response

## Quarterly Claim Review

Every quarter, founder reviews:
- All public surfaces (landing, README, recent posts)
- Pull list of all claims
- For each: is the evidence still current? Is the framing still honest?
- Update or retract anything stale

## What This Guide Refuses

- "Marketing language is different from product language"
- "Everyone exaggerates a bit"
- "We'll add the citation later"
- "Soft language without evidence" (qualifying weasel words don't fix overclaim)
