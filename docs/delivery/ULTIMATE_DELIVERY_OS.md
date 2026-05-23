# Ultimate Delivery OS

`delivery/delivery_queue.csv` is the queue of in-flight deliverables.
The `delivery_copilot` agent summarizes this queue and surfaces it on
`/delivery`.

States used:

- `intake`
- `in_progress`
- `qa`
- `handoff`
- `closed`
