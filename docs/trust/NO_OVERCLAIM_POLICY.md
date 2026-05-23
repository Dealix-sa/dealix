# No-Overclaim Policy — سياسة عدم المبالغة

## Purpose
Define the language rules that prevent Dealix from making claims it cannot evidence. The policy enumerates banned phrases and the rationale for each.

## Owner
Founder.

## Inputs
- All public-facing markdown and templates.
- All client-facing artifacts.
- Sales and marketing copy.

## Outputs
- Banned-phrase list (below).
- Scanner output: `docs/trust/registers/banned_phrase_scans/<date>.md`.

## Rules (numbered)
1. Banned phrases below may not appear in any Dealix artifact, public or client-facing.
2. Replacements come from `docs/trust/SAFE_LANGUAGE_LIBRARY.md`.
3. Scanner runs weekly across `docs/` and on every pack at QA.
4. A scanner hit triggers a Sev-2 incident if the file is already published.
5. Adding to or removing from the banned list requires A3 approval.
6. AR equivalents are equally banned; the list is maintained bilingually.

## Metrics
- Scanner hits per week (target 0 after first month).
- Mean time to fix a hit.
- Hits in published files (Sev-2): target 0.

## Cadence
Weekly scan. Quarterly list review.

## Evidence (paths)
- `docs/trust/registers/banned_phrase_scans/`
- `docs/trust/SAFE_LANGUAGE_LIBRARY.md`

## Verifier
Founder approves additions and removals. Head of Delivery runs the weekly scan.

## Runtime Command
`make trust.banned_phrase.scan` runs across docs/ and writes a report.

## Banned phrases (EN)

- "guaranteed revenue"
- "guaranteed sales"
- "guaranteed results"
- "100% accuracy"
- "AI-powered"
- "transform your business"
- "supercharge"
- "revolutionary"
- "best-in-class" (when unevidenced)
- "industry-leading" (when unevidenced)
- "guaranteed ROI"
- "X% conversion rate" (when stated as a promise, not an observed range)
- "we ensure" (when promising downstream outcomes)
- "fail-proof"
- "risk-free"

## Banned phrases (AR)

- "نضمن مبيعات"
- "نضمن إيرادات"
- "نضمن نتائج"
- "دقة 100٪"
- "مدعوم بالذكاء الاصطناعي" (when used as marketing fluff)
- "نُحوّل أعمالك"
- "ثوري"
- "الأفضل في فئته" (دون دليل)
- "الرائد في المجال" (دون دليل)
- "بدون مخاطر"
- "نضمن العائد على الاستثمار"

## Rationale per banned category

**Guarantees.** Dealix delivers an evidence pack. The client owns sending and outcomes. We cannot honestly guarantee what we do not control. Replacement: "evidenced opportunities" / "فرص مُثبتة بأدلة".

**Accuracy claims (100%, perfect).** No research process is perfect. Claiming 100% invites a single counter-example to destroy trust. Replacement: cite the validation method and the failure modes.

**Marketing fluff ("AI-powered", "transform", "supercharge").** These phrases describe nothing. They are noise that erodes the executive-Saudi-business voice. Replacement: concrete nouns describing what the system does.

**Unevidenced superlatives ("best-in-class", "industry-leading").** Only allowed when backed by a published benchmark with a date and source. Otherwise replaced with the specific capability being claimed.

**Outcome promises ("we ensure replies", "X% conversion").** Outcomes depend on the client's account, audience, and execution. We do not promise them. Replacement: describe what Dealix delivers (the pack), not what the recipient will do (the reply).

## Operating substance
This policy exists because most B2B copy in our space is unverifiable. Buyers have learned to discount it. Dealix's differentiation is that our copy survives scrutiny. The discipline is not a marketing handicap; it is a positioning advantage.

The scanner is the enforcement layer. It runs weekly and on every shippable artifact. False positives are tuned with founder approval. The scanner does not auto-fix; it surfaces the hit and the author fixes by consulting the Safe Language Library.

When in doubt, write what the system does and what the buyer can verify. That sentence is almost always shorter, more specific, and more credible than the marketing phrase it replaces.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
