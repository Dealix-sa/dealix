# Weekly Targeting Retrospective (Learning Loop)

> كل أسبوع النظام يتعلم: أي قطاع، أي زاوية، أي عرض، أي مصدر — يكرّر أو يوقف.

The learning loop closes the system: it reads the outcomes ledger and produces
next week's targeting plan. Engine: `scripts/targeting_learning_loop.py`.
Ledger: `data/targeting/outcomes.jsonl`.

---

## Questions it answers

- Which sector scored highest?
- Which sector replied most?
- Which angle produced diagnostics?
- Which message failed?
- Which offer closed?
- Which proof convinced the client?
- Which source produced bad (rejected) companies?
- Which queries to stop / double down on?

---

## Outcomes ledger format

One JSON object per line:

```json
{"date":"2026-05-27","company_name":"…","sector":"marketing_agency",
 "score":86,"grade":"A","angle":"revenue_os","offer":"command_sprint",
 "stage":"paid","message_angle":"proof_gap","source_type":"official_site","notes":"…"}
```

`stage` ∈ `no_reply | replied | diagnostic | paid | rejected`.

---

## Output: `out/weekly_targeting_retrospective.md`

- Best sector (by avg score) and most-replied sector.
- Best message angle (most diagnostics) and best closing offer.
- Avg score per sector.
- Sources that produced rejects.
- **Next week plan:** double down on / de-prioritise / stop ingesting from /
  lead with angle / lead with offer.

```bash
python scripts/targeting_learning_loop.py --out data/targeting/out
```

---

## Acceptance (learning)

- [ ] Every reply / reject / diagnostic / sale is logged.
- [ ] The system outputs the next targeting plan.

Tested by `tests/test_targeting_pipeline.py`.
