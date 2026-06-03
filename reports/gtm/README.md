# reports/gtm — Market Production OS reports

Generated, human-readable GTM reports. These are **drafts/plans for the founder**
— nothing here sends, charges, or commits.

| File | Generator | Purpose |
| --- | --- | --- |
| `GTM_DAILY_COMMAND.md` | `scripts/gtm_daily_command.py` | The founder's single daily order: draft production status, top-50 approval queue, reputation-safe sending batch plan, warnings, tomorrow recommendation. |
| `DRAFT_QUALITY_REPORT.md` | `scripts/gtm_quality_gate.py` | Per-draft pass/block verdicts from the quality gate over a drafts JSONL file. |

Regenerate:

```bash
python3 scripts/gtm_daily_command.py --domain-age-days 10 --domain-health healthy
python3 scripts/gtm_quality_gate.py --report reports/gtm/DRAFT_QUALITY_REPORT.md
```

The committed copies are generated from the synthetic, PII-free sample data in
`data/gtm/` so reviewers can see the shape without a live pipeline.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
