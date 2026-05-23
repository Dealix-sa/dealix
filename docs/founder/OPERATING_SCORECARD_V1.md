# Operating Scorecard v1

Generator: [`scripts/generate_operating_scorecard.py`](../../scripts/generate_operating_scorecard.py).

## What it scores

Eight 0–100 sub-scores:

* Revenue Score — derived from `cash_collected.csv` row count.
* Trust Score — derived from open incidents (start at 100, −10 per open).
* Runtime Score — derived from healthy workers vs. expected baseline.
* Founder Leverage Score — proposals in flight.
* Productization Score — productization candidates count.
* AI Governance Score — presence + validity of policy / registry / eval gate.
* Security Score — security checklist OK rows.
* Data Platform Score — presence of the lead intelligence base.

It picks the **lowest** score as the bottleneck and recommends the
"next best action" tied to that bottleneck.

## Output

`<private_ops>/founder/operating_scorecard.md` — markdown table that the
Founder Console renders in `/control-plane` and `/sovereign`.

## Run

```bash
make operating-scorecard PRIVATE_OPS=/opt/dealix-ops-private
```
