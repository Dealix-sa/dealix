# Delivery Report Template — قالب تقرير التسليم

## Purpose
Define the structure of the delivery report that accompanies every Revenue Sprint pack. The report is the narrative layer over the raw artifacts (lead table, sector notes, messages, sources). It is what the client reads first and what gets cited in any future case study or renewal conversation.

## Owner
Head of Delivery. Founder reviews and signs off on the first three sprints per ICP.

## Inputs
- Cleared QA log (G4).
- Final lead table and sources index.
- Sector notes and exclusion list.
- Client intake document.

## Outputs
- `pack/DELIVERY_REPORT.md` (AR + EN sections).
- One executive-summary page (≤ 400 words, bilingual).
- Citations list linking every claim to a source file.

## Rules (numbered)
1. Every quantitative claim cites a source path inside `pack/sources/`.
2. No language from the banned list in `docs/trust/NO_OVERCLAIM_POLICY.md`.
3. Estimated values are labelled "Estimated" and never aggregated as if Verified.
4. Limitations section is mandatory; an empty limitations section fails QA.
5. The report does not include client-confidential data inside source citations beyond what the client provided.
6. Findings are evidence-anchored. A finding without a citation is removed.
7. Recommendations are sized (effort / time / cost band) and prioritized.
8. Next-action list belongs to the client; Dealix does not commit to actions outside the agreed SOW.

## Metrics
- Median report length: 6–12 pages narrative + lead table appendix.
- Citation density: at least 1 source per quantitative claim. Target 100%.
- QA defects raised on report content: ≤ 1 per sprint.
- Client cites the report in renewal conversation: target ≥ 60% by sprint #5.

## Cadence
Once per sprint at G4 → handed off at G5.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/pack/DELIVERY_REPORT.md`
- `docs/audit/sprints/SPRINT_<ID>/pack/sources/`
- `docs/audit/sprints/SPRINT_<ID>/qa_log.md`

## Verifier
Head of Delivery. Founder for the first three sprints per ICP. QA checklist enforces structure.

## Runtime Command
`make sprint.report.scaffold SPRINT=<ID>` — writes the report skeleton from this template.

## Report document structure

**Section 1 — Executive summary (≤ 400 words, AR + EN).** What the sprint set out to do, what was delivered, the two or three findings that matter most, the headline limitation. No marketing language.

**Section 2 — Scope recap.** One paragraph restating the SOW: ICP definition, channels, geo, exclusions, deliverable list. Anchors the rest of the report.

**Section 3 — Method.** How leads were sourced, how scoring was applied (link to `SCORING_RULES.md`), how messages were drafted, what was excluded and why. The reader should be able to reproduce the approach.

**Section 4 — Findings.** Numbered findings. Each finding has: (a) one-sentence claim, (b) evidence cite, (c) the rows in the lead table that support it, (d) a numeric anchor where possible. Findings are factual; interpretation belongs in Section 5.

**Section 5 — Recommendations.** Prioritized list. Each recommendation has: action, expected effect, effort band (S/M/L), cost band, owner side (client / Dealix), prerequisite.

**Section 6 — Limitations.** Explicit list of what the data does not cover. Sample size limits, source coverage gaps, regional gaps, signal recency, exclusions. A weak limitations section is a QA failure.

**Section 7 — Next actions.** Three to five steps the client can take next. Belongs to the client; Dealix does not auto-commit.

**Section 8 — Appendix.** Lead table reference, sources index, sector notes, exclusion list. The appendix is referenced, not duplicated.

## Operating substance
The report is the artifact that survives the engagement. The lead table gets consumed; the messages get sent or edited; the sources get checked once. The report is what gets re-read at renewal, what gets shared internally at the client side, and what gets cited when the client introduces Dealix to a peer.

Two patterns kill report quality. First, narrative inflation — writing what sounds impressive instead of what the data says. The fix is the citation rule: every claim cites a source, and a claim without a citation is removed before QA. Second, soft limitations — burying the gaps in qualifications. The fix is the explicit Section 6 with concrete sentences ("we did not cover X", "the sample is N, which is below Y for inference about Z").

A report that overclaims sells the next sprint and loses the third. A report that under-claims and over-evidences loses the second sprint and wins the fourth, fifth, and tenth.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
