# Dealix IV4 Integration Layer

IV4 connects the leadership layer with commercial growth and negotiation output.

## What it connects

- DX3 leadership priorities.
- Commercial Growth OS summary.
- Negotiation Operator summary.
- Unified command queue.
- Reports and web snapshot.

## Run

```bash
python scripts/leadership/run_iv4.py
python scripts/leadership/generate_iv4_snapshot.py
python -m pytest -q tests/test_iv4.py
```

## Output

```text
reports/leadership/iv4/latest.json
reports/leadership/iv4/latest.md
apps/web/lib/iv4-snapshot.ts
apps/web/app/iv4/page.tsx
```

## Safety

IV4 is review first. It produces decisions and queue items, not live execution.
