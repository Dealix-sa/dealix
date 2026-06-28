# Commercial Growth OS — Living Engagement Room reports

Latest output of the **living, multi-channel engagement loop** — the brain
deciding the next best action per account across WhatsApp, email, LinkedIn and
phone, and preparing the exact draft payloads.

| File | What it is |
|------|------------|
| `latest.json` | Full engagement snapshot: prioritised action plan, conversations (with reasoning traces), and prepared draft payloads per channel + their safety decisions. |
| `latest.md` | Human-readable engagement room: safety posture, summary, prioritised next best actions with the brain's rationale. |
| `README.md` | This file. |

## Regenerate

```bash
python scripts/commercial/run_commercial_engagement.py   # or: make commercial-engagement
python scripts/commercial/simulate_whatsapp_conversation.py  # or: make commercial-whatsapp-sim
```

## Safety note

Everything here is **draft-only**. No WhatsApp, email or LinkedIn message has
been transmitted; no calendar event written. Each payload carries a
`SafetyDecision` and `safe_to_send_now` is `false` under the default
fail-closed posture. Live transmission requires the safety gates in
`docs/commercial/CONTROLLED_LIVE_OUTBOUND_POLICY_AR.md` plus explicit approval.

Generated from `data/commercial/*.sample.json` — **no real client data**.
