# Ultimate Revenue Factory

The revenue factory is the pipeline:

```
market accounts → lead intelligence → scoring → outreach drafts →
approval → send/draft queue → follow-up → replies → samples →
proposals → payment capture → delivery → retention → proof → referrals
```

Each stage has:

- a private ops CSV (e.g. `outreach/outreach_queue.csv`)
- an agent that drafts/scores (e.g. `outreach_draft_agent`)
- a founder approval gate where required (A2 or A3)
- an entry in the audit log on decision

No stage performs external sends from the repo. Sending is the
founder's deterministic step after approval.
