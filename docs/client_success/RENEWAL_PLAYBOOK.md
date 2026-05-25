# Renewal Playbook — دليل التجديد

## Purpose
A scripted, evidence-based renewal conversation for every retainer client. Run at T-30 days from contract end. Eliminates last-minute scrambling and protects both Dealix and client from drift.

## Owner
Founder for first 10 renewals. Delivery analyst leads subsequently, founder counter-signs.

## Inputs
- Engagement history (90 days minimum).
- Outcomes vs goals (verified).
- Health score trajectory.
- Feedback log.
- Tier from `docs/client_success/CLIENT_TIERING.md`.

## Outputs
- Renewal decision: renew / renew-modified / decline (mutual).
- Signed renewal SOW or amicable close.
- Updated entry in `docs/client_success/CLIENT_SUCCESS_COMMAND_CENTER.md`.

## T-30 to T-0 Timeline
| When | Action |
|---|---|
| T-30 | Renewal review internal: pull outcomes, health, feedback |
| T-25 | Founder reads, decides recommended path: renew / modify / decline |
| T-21 | Renewal conversation scheduled (45 min) |
| T-14 | Conversation held |
| T-7 | Written proposal sent (`templates/PROPOSAL_RENEWAL.md.j2`) |
| T-3 | Decision in hand |
| T-0 | Signed or amicable close |

## The Conversation Decision Tree
1. **Strong outcomes + high health (≥ 80)** → Propose renewal at same scope or modest expansion (see `docs/client_success/UPSELL_PLAYBOOK.md` gates).
2. **Mixed outcomes + stable health (60-79)** → Propose renewal at same scope with a refined success measure.
3. **Weak outcomes or low health (< 60)** → Propose either a scoped-down 30-day proof-of-fit or amicable close.
4. **Critical incident in last 30 days** → Default to amicable close unless client explicitly requests retention plan.

## Conversation Script (Open)
- Bilingual opening: "Our agreement renews in 14 days. Before discussing next term, I want to look at this term honestly."
- Walk through verified outcomes (numbers, sources).
- Walk through what did not work.
- Ask: "Does Dealix's next 90 days serve a clear priority for you?"
- Listen. Do not pitch in this part of the call.

## Rules
1. No automatic renewal. Conversation required.
2. No price increase without a corresponding outcome or scope justification.
3. No discount as primary tool to retain; outcomes first.
4. Amicable close is an acceptable outcome and is documented without grievance.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected renewal-term outcomes.
6. No upsell stacked into renewal conversation; treat as a separate decision.

## Metrics
- Renewal rate (rolling 12 months).
- Net revenue retention.
- Modified-renewal rate (signals scope mismatch upstream).
- Amicable-close rate (acceptable; tracks discipline).

## Cadence
- Per-client renewal cycle.

## Evidence
- `evidence/renewal/<client_id>/<YYYY-MM-DD>/` with brief, proposal, decision.

## Verifier
Founder.

## Runtime Command
`make renewal-prep CLIENT=<id>` — pulls outcomes, health, feedback; prints recommended path.

## Arabic Summary — ملخص عربي
محادثة تجديد منظمة في T-30. مسارات أربعة: تجديد، تعديل، إغلاق ودي. لا تجديد تلقائي. لا تخفيض كأداة احتفاظ أولى. القيم التقديرية ليست مُتحقَّقة.
