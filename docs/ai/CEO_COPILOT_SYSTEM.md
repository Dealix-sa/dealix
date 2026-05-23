# CEO Copilot System

`ceo_copilot` is the founder-facing summarizer agent. It:

- Reads private ops CSVs via `api.internal.runtime_reader`.
- Computes daily counts (leads, approved outreach, replies, proposals,
  payment follow-ups, worker failures, cash collected).
- Suggests one top action.

It never sends anything externally and never proposes A3 actions on its
own.
