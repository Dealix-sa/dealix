# QA Checklist — قائمة فحص الجودة

## Purpose
Single, independent quality gate before any pack ships. The QA operator runs this checklist end-to-end and signs the QA log. A failed item blocks shipping.

## Owner
QA operator (rotational role). Head of Delivery is the appeal owner.

## Inputs
- Built pack at `docs/audit/sprints/SPRINT_<ID>/pack/`.
- Intake, scoring calibration, schema reference.

## Outputs
- Signed QA log: `docs/audit/sprints/SPRINT_<ID>/qa_log.md`.
- Defect list (if any) routed to the builder.

## Rules (numbered)
1. The QA operator is not the pack builder. No exceptions.
2. Each item is marked pass / fail / N/A with a one-line note.
3. A single fail blocks ship. The pack returns to G3.
4. The QA log is signed with date and initials.
5. Defects are described in plain language with a path reference.
6. No verbal approvals. All approvals are written.

## Metrics
- QA first-pass rate: target ≥ 80%.
- Mean defects per failed pack.
- Mean time from defect-found to defect-fixed.

## Cadence
Per sprint at G4.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/qa_log.md`

## Verifier
Head of Delivery countersigns the QA log.

## Runtime Command
`make sprint.qa.run SPRINT=<ID>` — opens the checklist file with the sprint paths pre-filled.

## Checklist

**Schema & data.**
1. Lead table validates against `LEAD_TABLE_SCHEMA.md` with zero errors.
2. Every row has `source_url` and `source_captured_at`.
3. Every row has three scores and a total.
4. No PII columns. No personal email, phone, or national ID anywhere in the pack.
5. Excluded rows are in `excluded.csv`, with reasons.
6. Row count matches contracted lead count.

**Sources & evidence.**
7. `pack/sources/index.md` lists every cited source.
8. Each source file contains URL + capture timestamp + relevance note.
9. Spot-check 10 random rows: source URL resolves to a public page or is annotated as archived.

**Messages.**
10. Two variants per channel, AR + EN parallel.
11. Word counts in range (80–160 words per variant).
12. No banned phrases (run language scanner).
13. Every claim cites an evidence path.
14. No fabricated personalization; only public-signal references.
15. No urgency manipulation. No promises of outcomes.

**Report.**
16. Report follows `REPORT_TEMPLATE.md` structure.
17. Limitations section present and concrete.
18. Recommendations framed as evidenced opportunities, not forecasts.
19. AR and EN sections mirror in structure and length.

**Sequence map.**
20. Sequence is framed as recommendation, not automation.
21. No instruction implies Dealix will send.

**Intake & exclusions.**
22. Geo, sector, deal-size band, channels in scope match the intake.
23. Named exclusions are absent from the lead table.
24. Any sending-on-behalf request has A3 approval logged.

**Manifest & packaging.**
25. SHA256 manifest present and accurate.
26. README.md present in the pack with the orientation paragraph.
27. ZIP opens cleanly; no orphan files.

## Operating substance
QA is independent, written, and non-negotiable. We do not ship a pack on a "looks fine" review. The pattern of failures over time is what trains the team and updates the templates; that pattern only emerges if QA is logged honestly.

QA operators are rotated across sprints so no single operator becomes the de-facto template. Rotation also protects against fatigue blindness, where the same eyes miss the same defects repeatedly. The first time a new QA operator runs the checklist, the Head of Delivery shadows them on one sprint.

Defects are not embarrassments. They are inputs to the learning loop. A defect found at QA is cheap; the same defect found by a client is expensive. We optimize for QA catching the defects.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
