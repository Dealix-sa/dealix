# Ultimate Delivery OS

Delivery is the bridge between an approved proposal and a successful
customer outcome. Tracked in `sales/proposal_queue.csv`:

* `status=open` — proposal sent (after founder approval).
* `status=accepted` — customer accepted; delivery scheduled.
* `status=delivering` — work in progress.
* `status=delivered` — work complete, awaiting acceptance.
* `status=accepted_delivered` — customer signed off.
* `status=churned` — engagement ended unsuccessfully.

The Founder Console renders `/delivery` from this CSV. Slippage shows
up as an open row with an old `updated_at`. A weekly worker (out of
scope for this commit) can flag rows that haven't moved in N days; the
Delivery Copilot agent will be that worker.
