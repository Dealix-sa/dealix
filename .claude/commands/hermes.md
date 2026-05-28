---
description: Dispatch an intent through Hermes orchestrator with doctrine guarantees.
argument-hint: "<intent>"
allowed-tools: Bash
---

# /hermes — Dispatch via the Hermes orchestrator

Run a single Hermes dispatch from inside Claude Code, with doctrine
checks, audit logging, and routed sub-agent selection.

When the user invokes `/hermes <intent>`, do this:

1. Run the CLI:

   ```bash
   python -m dealix.hermes "$ARGUMENTS"
   ```

2. Parse the output:
   - `decision: approved` + envelope returned → tell the user which
     sub-agent was routed (`dealix-pm` / `-engineer` / `-content` /
     `-sales` / `-delivery`) and the provider/model used.
   - `decision: needs_approval` → tell the user the draft was queued
     to `approval_center`; surface the channel (`email` / `whatsapp`
     / `linkedin_dm`) so they know what they will approve.
   - `decision: rejected` → quote the matched rule(s) and the safe
     alternative verbatim. Do NOT improvise around the refusal.
   - `decision: kill_switched` → halt; remind the user to unset
     `HERMES_KILL_SWITCH` after the incident review.

3. If the user wants the routed sub-agent to actually execute the
   work, follow up with the `Agent` tool using the sub-agent's name
   (e.g. `dealix-engineer`) and pass the intent + the doctrine
   constraints from the envelope.

4. NEVER bypass a refusal. NEVER paste API keys into the chat.

Charter: `docs/institutional/HERMES_CHARTER.md`.
Ops manual: `docs/ops/HERMES_OPS_GUIDE.md`.
