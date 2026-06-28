# Dealix DX3

DX3 expands the leadership command layer with ranked priorities, lane counts, a weekly memo lane, reports, tests, and a small web page.

## Lanes

CEO, growth, sales, partners, marketing, success, delivery, trust, pricing, and board.

## Run

```bash
python scripts/leadership/run_dx3.py
python scripts/leadership/generate_dx3_snapshot.py
python -m pytest -q tests/test_dx3.py
```

## Output

```text
reports/leadership/dx3/latest.json
reports/leadership/dx3/latest.md
apps/web/lib/dx3-snapshot.ts
apps/web/app/dx3/page.tsx
```
