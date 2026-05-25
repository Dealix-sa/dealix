# Founder Voice Guide — دليل صوت المؤسس

## Purpose
Define how Bassam writes and is written for. Voice is Arabic-first, plain, evidence-based, executive. This guide is the test every draft passes before publishing.

## Owner
Founder. Drafts can be prepared by analysts or contractors; voice is the founder's.

## Inputs
- Founder past writings (LinkedIn posts, decision logs).
- Saudi executive register references (Aramco quarterly reports, MCIT publications).
- The non-negotiables list.

## Outputs
- This guide.
- Voice rubric used in `docs/content/CONTENT_COMMAND_CENTER.md` approval.
- Sample paragraphs (do / don't).

## Voice Principles
1. **Arabic first on Arabic readers**. English is a parallel translation, not a translation gloss.
2. **Concrete nouns**. "Three signed SOWs" not "many clients".
3. **Decisive verbs**. "We refuse" not "we generally do not prefer".
4. **Numbers carry disclosure**. Every number labelled estimated or verified.
5. **No hype words**. Banned: supercharge, transform, revolutionize, unleash, game-changer, AI-powered (as adjective), 10x, hack.
6. **No emojis**.
7. **No model name** mentioned in copy.
8. **Saudi context first**. Riyals, Hijri dates where relevant, local sectors, local regulators.

## Sentence Shape
- Short to medium sentences. Avoid stacks of subordinate clauses.
- One idea per paragraph.
- Lists when comparing or sequencing; prose for argument.

## Pronouns
- "We" for Dealix actions.
- "I" sparingly, for direct founder positions.
- Never "you guys" or "folks".

## Examples — Do
> "Three Saudi B2B sprints closed in April. Two delivered on time, one delayed by client data. Median sprint margin: 62%. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة."

> "نرفض إرسال رسائل خارجية بالنيابة عن العميل دون موافقة مكتوبة. هذا ليس تفضيلًا، بل سياسة."

## Examples — Don't
> "We supercharge your sales pipeline with AI-powered automation that transforms your business."

> "Our revolutionary platform unleashes 10x growth for B2B leaders."

## Rules
1. Every published piece passes a 60-second voice check by founder.
2. Banned words trigger rejection.
3. No anonymous "thought leadership"; founder signs.
4. The disclosure line appears on every customer-facing piece.
5. Translations are parallel, not literal; same length and same structure.

## Metrics
- Founder voice rubric score (manual, 0-5).
- Banned-word incidents per quarter (target 0).
- Bilingual parity (length and structure).

## Cadence
- Per-post check.
- Quarterly review of banned-word list and examples.

## Evidence
- `evidence/content/voice/<YYYY-Qn>_review.md`.

## Verifier
Founder.

## Runtime Command
`make voice-check FILE=<path>` — scans for banned words, missing disclosure, emoji presence; refuses to mark ready if any issue.

## Arabic Summary — ملخص عربي
صوت المؤسس عربي أولًا، واضح، مُسنَد بأدلة، تنفيذي. لا كلمات تسويقية مُبالغ بها. لا رموز تعبيرية. الأرقام تحمل تنويه التقدير. المؤسس يوقّع. القيم التقديرية ليست مُتحقَّقة.
