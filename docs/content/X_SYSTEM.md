# X (Twitter) System — منظومة منصة X

## Purpose
Define X cadence and rules. X is the secondary channel — used to test ideas, share sector signals, and engage with ecosystem operators. Lower friction than LinkedIn; same voice and evidence standards.

## Owner
Founder. Drafts may be queued; posting is manual.

## Inputs
- `docs/content/CONTENT_STRATEGY.md`.
- `docs/content/FOUNDER_VOICE.md`.
- Idea backlog tagged by pillar.

## Outputs
- 5 posts per week + 1 thread.
- Weekly engagement export.

## Post Types
| Type | Pattern | Frequency |
|---|---|---|
| Signal | One-line sector observation + source | 2x per week |
| Principle | One operating rule | 1x per week |
| Question | A focused question to ecosystem (no engagement-bait) | 1x per week |
| Thread | Long-form (5-9 tweets), one topic, evidence-attached | 1x per week |
| Reply | Substantive replies to ecosystem operators | Ad-hoc |

## Cadence
- Mon/Wed/Fri primary post slots (Riyadh morning).
- Thread on Tuesday or Thursday.
- No posting after 9pm local.
- No tweetstorms longer than 9 tweets.

## Rules
1. Every claim with a number carries the disclosure or a source link.
2. No subtweets. No anonymous attacks. No dunking.
3. No retweet-for-reach behavior.
4. No DM-blast or follow-unfollow.
5. Threads cite evidence (case-safe or public source).
6. Bilingual mix: 60% Arabic, 40% English on signals; threads always have a bilingual summary.
7. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" on any post with numbers.

## Approval Flow
- Single posts: founder posts directly after self-check.
- Threads: drafted, voice-checked, then published.
- No analyst posts unsupervised.

## Metrics
- Posts per week (target 5 + 1 thread).
- Qualified replies and DMs (count).
- Thread save rate.
- Banned-word incidents (target 0).

## Evidence
- Weekly export under `evidence/content/x/<YYYY-Www>.md`.

## Verifier
Founder.

## Runtime Command
`make x-plan WEEK=<YYYY-Www>` — prints next-week post plan and thread topic.

## Arabic Summary — ملخص عربي
خمس منشورات أسبوعيًا وموضوع طويل واحد. نفس الصوت، نفس معايير الأدلة، نفس التنويه على الأرقام. لا أتمتة، لا حشد متابعين. القيم التقديرية ليست مُتحقَّقة.
