# Content Command Center — مركز قيادة المحتوى

## Purpose
Single dashboard for content pipeline, published assets, performance, and approval status. Prevents post-by-vibe and ensures every piece is tied to a proof gate, audience, and evidence.

## Owner
Founder. Drafts may be prepared by analyst or contractor; founder publishes.

## Inputs
- Content strategy from `docs/content/CONTENT_STRATEGY.md`.
- Proof library entries from `docs/content/PROOF_LIBRARY.md`.
- Case studies from `docs/content/CASE_STUDY_SYSTEM.md`.
- Sector reports from `docs/content/SECTOR_REPORT_SYSTEM.md`.
- Engagement data from LinkedIn and X (manual export weekly).

## Outputs
- Pipeline table: idea → drafted → approved → scheduled → published.
- Weekly publish plan (LinkedIn + X).
- Monthly performance summary.
- Quarterly content audit.

## Dashboard Panels
1. **Pipeline** — count by stage; aging items flagged.
2. **Published this week** — channel, format, evidence link, engagement.
3. **Top performing (90d)** — by saves, comments, qualified replies.
4. **Approval queue** — items waiting on founder.
5. **Proof attached rate** — % of posts citing a documented proof artifact.
6. **Founder voice score** — manual check, 0-5.
7. **Bilingual coverage** — % posts with AR + EN versions.
8. **Disclosures present** — % posts with estimated-vs-verified disclosure where required.

## Rules
1. No post is published without an evidence link or explicit "no-proof opinion" tag.
2. No client name in content without written approval (see `docs/content/CASE_STUDY_SYSTEM.md`).
3. Posts that touch numbers carry the "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" line.
4. No bulk-send automation; posts are scheduled manually.
5. Founder voice required on owned channels; ghostwriting drafts are allowed, ghostwritten voice is not.

## Metrics
- Posts published per week (target: 3 LinkedIn, 5 X).
- Proof-attached rate (target ≥ 70%).
- Bilingual coverage (target 100% for sector content).
- Qualified inbound replies (count per month).
- Cost per published asset (founder hours + contractor).

## Cadence
- Weekly: pipeline review and publish plan.
- Monthly: performance review.
- Quarterly: audit and reshuffle.

## Evidence
- `evidence/content/<YYYY-MM>/pipeline.md`.
- Per-post evidence link.

## Verifier
Founder.

## Runtime Command
`make content-status` — prints pipeline counts, aging items, approval queue.

## Arabic Summary — ملخص عربي
لوحة قيادة المحتوى تعرض الأنبوب من فكرة إلى نشر، والأداء. كل نشرة ترتبط بدليل أو وسم رأي. الأرقام تحمل تنويه "تقديرية وليست مُتحقَّقة".
