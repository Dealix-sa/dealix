# Dealix Project Agent Skills

These project-level skills tell coding agents how to work on Dealix safely and repeatedly.

## Skills

| Skill | Purpose |
|---|---|
| `dealix-release-engineer` | Stabilize branches, PRs, CI, build, Railway, and safe release gates |
| `dealix-revenue-command-room` | Run target scoring, drafts, follow-ups, proposal briefs, and revenue reports |
| `dealix-company-brain-os` | Convert operating signals into daily founder decisions and weekly memos |
| `dealix-client-growth-operator` | Prepare controlled channel actions for email, WhatsApp, LinkedIn, phone, and proposals |
| `dealix-client-delivery-os` | Deliver client work through intake, diagnosis, scope, blueprint, proof pack, and handoff |
| `dealix-loop-operating-system` | Convert scripts into bounded operating loops with verifiers and reports |
| `dealix-trust-and-outbound-safety` | Review claims, privacy, consent, opt-out, approval cards, and outbound policy gates |
| `dealix-design-command-room` | Generate and review Dealix dashboards, decks, landing pages, proof packs, and prototypes through a design-system contract |

## Safety baseline

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Recommended order

1. Start with `dealix-release-engineer` when the repo, PR, CI, or deployment is unstable.
2. Use `dealix-loop-operating-system` to turn repeated work into bounded loops.
3. Use `dealix-revenue-command-room` to run the daily sales machine.
4. Use `dealix-company-brain-os` for daily decisions and board-level summaries.
5. Use `dealix-client-growth-operator` for client growth actions.
6. Use `dealix-client-delivery-os` for client implementation.
7. Use `dealix-design-command-room` for UI, dashboards, pages, decks, and proof-pack artifacts.
8. Use `dealix-trust-and-outbound-safety` before any external communication or public claim.
