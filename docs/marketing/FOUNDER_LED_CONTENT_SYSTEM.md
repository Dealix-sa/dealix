# Founder-Led Content System

The Founder-Led Content System is the production line for the founder's public voice. The founder is the brand; the brand is the founder. The system protects time, claim safety, and bilingual parity.

**Source of truth:** `$PRIVATE_OPS/founder_content_queue.csv`
**Owner:** Founder + Content Strategist Lead
**Trust gate:** A1 — every founder post is reviewed before publish; the founder signs the send.

## Why founder-led

Saudi B2B buyers buy from people first. A trusted founder voice outperforms a polished brand voice in early-stage trust building. The system is built so the founder spends time on the thinking, not the formatting.

## Format menu

| Format | Length | Cadence |
|--------|--------|---------|
| Short post (LinkedIn / X) | 80-200 words | 2-3 / week |
| Long post | 500-900 words | 1 / week |
| Carousel | 6-10 frames | 1 / two weeks |
| Audio note | 2-5 minutes | 1 / two weeks |
| Live session | 25-40 minutes | 1 / month |

## Production process

1. Founder logs a raw thought in `$PRIVATE_OPS/founder_thoughts/YYYY-MM-DD.md` (text, voice memo, or video).
2. Content Strategist agent (`docs/ai/CONTENT_STRATEGIST_AGENT.md`) drafts the artifact in the chosen format.
3. Brand Guardian agent (`docs/ai/BRAND_GUARDIAN_AGENT.md`) lints for hype, claims, PII, and disclosure.
4. Bilingual parity: EN and AR drafted together; AR is not a translation, it is a parallel rewrite for Saudi readers.
5. Founder reviews, edits in place, and approves.
6. Marketing Lead schedules.
7. Founder posts from the founder account. The agent never posts on behalf of the founder without explicit per-post approval (A2).

## Voice rules

- First person singular when the founder asserts.
- "We" when the company commits.
- No "AI-powered". No "transform". No "supercharge".
- Concrete nouns, named verbs.
- Numbers are tagged Estimated or Verified.
- A case is "case-safe" unless the client has consented to be named.

## Failure modes

- **Voice drift:** the agent draft sounds generic. Detection: founder review. Recovery: re-draft with explicit examples from `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- **Auto-post leak:** a post publishes without explicit founder approval. Detection: policy engine. Recovery: pull post within 30 minutes, written correction, root cause filed.
- **Bilingual asymmetry:** EN posted, AR delayed by more than 24 hours. Detection: parity check. Recovery: AR delivered or EN withdrawn.

## Recovery path

If the system produces consistent voice drift, the founder pauses the agent draft pipeline and reverts to manual draft until the brand voice is recalibrated.

## Metrics

- Posts published per week by format.
- Founder approval cycle time (median minutes from draft to approval).
- Engagement by format (estimated).
- Inbound leads attributable to founder content (estimated).

## Disclaimer

Founder content is opinion and observation. It is not advice and does not constitute a guarantee. Estimated value is not Verified value.
