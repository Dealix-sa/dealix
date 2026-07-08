# Autonomous Company OS

Dealix operating as a company that runs itself — a stateful commercial loop with
durable memory, a decision brain, revenue tracking, and a daily Command Room.
Draft-only and approval-first: nothing is sent, published, or charged.

## One command
```
python scripts/commercial/run_company.py
```
Runs Money Now → Autonomous Growth → Autonomous Company → safety verify, then
points you at `reports/autonomous_company/command_room.html`.

Or run just the company cycle:
```
python scripts/commercial/run_autonomous_company.py --seed-inbox --top 10
```

## How it thinks each cycle
1. **Load memory** — `data/autonomous_company/state.json` (private CRM, gitignored).
2. **Ingest warm leads** — from `data/autonomous_company/inbox.json` (you fill it;
   only opted-in leads; the engine never scrapes or invents contacts).
3. **Derive stage from evidence** — a deal's real stage is the highest stage its
   evidence events prove. Record `payment_received` and it becomes `won`.
4. **Score & decide** — every deal is scored (closeness to revenue, value, waiting
   time, stalled-rescue) and gets a next-best action with a ready draft.
5. **Track revenue** — recognized revenue counts a deal only on `payment_received`;
   plus a conservative weighted-pipeline forecast.
6. **Render the Command Room** — one HTML page + markdown: KPIs, ranked actions,
   approval queue (drafts), stalled deals, and what the company learned.
7. **Persist & self-verify** — save memory, append a cycle to history, refuse to
   run if any live-send flag is on.

## Pipeline stages (mapped to the evidence chain)
`new → contacted → engaged → proposed → won → delivered → proof → referral`
(`lost` is terminal). Stages advance only when you record the real evidence event.

## Advancing a deal
Edit `data/autonomous_company/state.json` and append an event to the deal, e.g.
`{"event": "payment_received", "at": "2026-07-10"}`. The next cycle re-derives the
stage, updates revenue, and picks the new next-best action automatically.

## Outputs (gitignored — your private data)
- `reports/autonomous_company/command_room.html` — open this each morning.
- `reports/autonomous_company/command_room.md` + dated copy.
- `reports/autonomous_company/kpis.json`, `..._actions.json`.

## Safety
No auto-send, no auto-publish, no auto-charge, no scraping, no fake customers.
Not-opted-in leads never receive an outreach draft. Verify with
`python scripts/commercial/verify_autonomous_company.py`.
