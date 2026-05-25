# AI System Inventory — جرد أنظمة الذكاء الاصطناعي

## Purpose
Maintain the complete list of every model, agent, and prompt asset Dealix uses, with owner, risk class, autonomy level, and last review date. The inventory is the foundation for AI governance.

## Owner
Founder. Per-agent owners listed in the table.

## Inputs
- New agent or prompt requests.
- Model usage logs.
- Audit findings.

## Outputs
- Inventory table (below, kept current).
- Change log of inventory updates.

## Rules (numbered)
1. No agent runs against any client artifact unless it is in the inventory.
2. Every inventory row has owner, autonomy level, risk class, last review date.
3. Inventory is reviewed monthly; missing rows are added or running agents are stopped.
4. Adding a row at autonomy A2 or above requires the release gate.
5. Removing a row requires confirming the agent is no longer running.
6. Prompts are versioned; the inventory references the prompt path and version.

## Metrics
- Inventory completeness (running agents matching inventory rows, target 100).
- Stale rows (last review older than 60 days, target 0).
- New rows added per quarter.

## Cadence
Updated continuously. Reviewed monthly.

## Evidence (paths)
- `docs/ai_management/AI_SYSTEM_INVENTORY.md` (this file).
- `docs/ai_management/prompts/<agent>/<version>.md` for prompt assets.

## Verifier
Founder.

## Runtime Command
`make ai.inventory.check` confirms running agents match this file.

## Inventory table

| agent_id | name | model_class | prompt_path | owner | autonomy | risk_class | last_review |
|---|---|---|---|---|---|---|---|
| AG-001 | Sprint scaffolder | text-gen | `prompts/sprint_scaffolder/v1.md` | Head of Delivery | A1 | low | 2026-05-01 |
| AG-002 | Lead table validator | classifier | `prompts/lead_validator/v1.md` | Data lead | A0 | low | 2026-05-01 |
| AG-003 | Sector notes drafter | text-gen | `prompts/sector_notes/v1.md` | Head of Delivery | A1 | medium | 2026-05-01 |
| AG-004 | Message variant drafter | text-gen | `prompts/message_drafter/v1.md` | Head of Delivery | A1 | medium | 2026-05-01 |
| AG-005 | Banned-phrase scanner | classifier | `prompts/banned_scanner/v1.md` | Founder | A0 | low | 2026-05-01 |
| AG-006 | Evidence index builder | structured-gen | `prompts/evidence_indexer/v1.md` | Head of Delivery | A1 | low | 2026-05-01 |
| AG-007 | QA checklist drafter | text-gen | `prompts/qa_drafter/v1.md` | Head of Delivery | A1 | low | 2026-05-01 |

Add a row when a new agent is approved through the release gate. Mark an agent retired when it is decommissioned; do not delete the row.

## Risk class definitions

**Low.** Internal tooling, no client-facing output, no irreversible action. Examples: validators, scanners, scaffolders.

**Medium.** Drafts client-facing content but always under human review. Examples: message drafter, sector notes drafter.

**High.** Reserved. No high-risk agent is currently in inventory. Any future high-risk agent requires a quarterly review cadence and explicit founder sign-off per use.

## Operating substance
The inventory is small because the agent surface area is small by design. Dealix is not building a sprawling agent estate; it is building a few well-governed agents that produce evidence-grade output.

Each row is short on purpose. The inventory is a roster, not a manual. The manual for each agent lives at its prompt path. The prompt path is versioned so a regression in agent behavior can be traced to a prompt change.

Monthly review touches every row. The review asks: is this agent still running? At the level the row says? With the prompt the row references? If any answer is no, the row is updated or the agent is stopped. We do not let inventory drift; drift is how AI risk hides.

Adding an agent at A2 or above is the most consequential operation against this inventory. The release gate (`AI_AGENT_RELEASE_GATE.md`) is the only path to A2. There is no shortcut.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
