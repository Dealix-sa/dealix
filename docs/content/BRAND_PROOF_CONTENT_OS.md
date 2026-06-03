# Brand, Proof, Content OS

## Purpose
Build a reputation backed by proof, not by overclaim.

## Pillars
- Brand positioning — `docs/content/BRAND_POSITIONING_SYSTEM.md`
- Founder voice — `docs/content/FOUNDER_VOICE_SYSTEM.md`
- Proof level policy — `docs/content/PROOF_LEVEL_POLICY.md`
- Proof approval — `docs/content/PROOF_APPROVAL_SYSTEM.md`
- Content production — `docs/content/CONTENT_PRODUCTION_SYSTEM.md`
- LinkedIn system — `docs/content/LINKEDIN_SYSTEM.md`
- Case studies — `docs/content/CASE_STUDY_SYSTEM.md`
- Sector reports — `docs/content/SECTOR_REPORT_SYSTEM.md`
- Content → pipeline — `docs/content/CONTENT_TO_PIPELINE_SYSTEM.md`

## Operating rules
1. Every claim is sourced.
2. Every named case is approved in writing.
3. Every post is checked by `scripts/review_content_claims.py` for high-risk patterns.
4. The proof library is the source of truth for what we can say externally.

## Cadence
- Daily: capture proof candidates from delivery work.
- Weekly: publish 1–2 founder posts.
- Monthly: 1 anonymized or named case study (if available).
- Quarterly: 1 sector report.

## Owners
- Founder writes / approves all external content.
- Content sub-agent assists with drafting and formatting only.

## What we never do
- Generate testimonials.
- Quote anonymous "industry benchmarks" without source.
- Use stock-photo case studies.

## Verifier
`python scripts/verify_brand_proof_content_os.py`
