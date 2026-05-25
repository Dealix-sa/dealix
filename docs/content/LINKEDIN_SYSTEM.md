# LinkedIn System — منظومة لينكدإن

## Purpose
Define LinkedIn cadence, post types, and approval flow. LinkedIn is Dealix's primary owned channel for Saudi B2B buyers. No bots, no automation, no DM blast.

## Owner
Founder publishes. Analyst drafts on request. Contractor may research but not post.

## Inputs
- `docs/content/CONTENT_STRATEGY.md` pillars.
- `docs/content/FOUNDER_VOICE.md` rubric.
- Proof library from `docs/content/PROOF_LIBRARY.md`.
- Weekly publish plan from `docs/content/CONTENT_COMMAND_CENTER.md`.

## Outputs
- 3 posts per week scheduled and published manually.
- Engagement export every Friday.
- Qualified inbound reply log.

## Post Types (5)
| Type | Pattern | Frequency |
|---|---|---|
| Sprint log | What we did this sprint, what we learned, what we killed | Weekly |
| Sector signal | One observation + methodology disclosure | Weekly |
| Operating principle | One rule + the cost of breaking it | Bi-weekly |
| Case-safe pattern | Anonymized client pattern + lesson | When evidence allows |
| Refusal post | What we refused to do and why | Monthly |

## Cadence
- Sunday morning, Tuesday afternoon, Thursday morning (Riyadh time).
- No weekend posting.
- No more than 1 post per day.

## Approval Flow
1. Draft prepared (analyst or founder).
2. Voice check via `docs/content/FOUNDER_VOICE.md`.
3. Evidence link attached or "opinion" tag set.
4. Disclosure line if numbers present.
5. Founder reads, edits, schedules.
6. After publish, engagement logged Friday.

## Rules
1. No DM automation. No connection-request automation. No follower scraping.
2. No client name without written approval.
3. No engagement-bait ("agree?", "comment YES").
4. No quoting unverified statistics.
5. Bilingual AR + EN where the post addresses both audiences; otherwise primary language matches the lead audience.
6. Disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" on any post that includes numbers.

## Metrics
- Posts published per week (target 3).
- Qualified inbound replies (count, source).
- Saves vs likes ratio.
- Proof-attached rate (target ≥ 70%).
- Follower growth (vanity metric — tracked but not optimized for).

## Evidence
- Each post evidence link.
- Weekly engagement export under `evidence/content/linkedin/<YYYY-Www>.md`.

## Verifier
Founder. Voice check is the gate.

## Runtime Command
`make linkedin-plan WEEK=<YYYY-Www>` — prints next-week plan with assigned post types and evidence slots.

## Arabic Summary — ملخص عربي
ثلاث منشورات أسبوعيًا، يدويًا، بصوت المؤسس. لا روبوتات، لا أتمتة، لا قص بيانات. كل رقم تنويه. القيم التقديرية ليست مُتحقَّقة.
