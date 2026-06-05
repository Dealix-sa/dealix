# سجل الإدعاءات — Claims Register

> **القاعدة الذهبية / The Iron Rule:** لا يُنشر أي إدعاء خارجي بدون صف في هذا السجل.
> **No external-facing claim ships without a row in this register.**

## الدور / Role

This register is the single source of truth for **every** claim that reaches a customer-facing
surface (landing page, `frontend/` funnel, decks, proposals, ads, social, email, WhatsApp).

Every claim must resolve to exactly one **Status**:

- **Evidence-backed** — linked to a Proof Pack (see `PROOF_PACK_POLICY.md`) or enforced in code/tests.
- **Hypothesis** — explicitly framed as a belief/target, never as a fact. Must read as a hypothesis on the surface.
- **Rewritten** — the original (unsafe) claim was rewritten into a safe form; the row records both.

Canonical doctrine: `CLAUDE.md`, `docs/00_constitution/NON_NEGOTIABLES.md`,
`docs/00_constitution/WHAT_DEALIX_REFUSES.md`. Module status labels: `docs/00_platform_truth/MODULE_STATUS_MAP.md`.

## القواعد الصارمة / Hard rules encoded here

- Never **guarantee revenue or financial outcomes**. Any revenue/ROI statement is a Hypothesis at best.
- Never imply **fake proof, fake testimonials, or fake scarcity**. No "limited seats" without a real cap.
- Never present a **FUTURE / BETA / INTERNAL / DOCS_ONLY** module as `LIVE`. Tag the module status in the claim.
- No claim is "Evidence-backed" unless the Evidence link points to a real Proof Pack ref or a passing test/code path.

## كيف تُضيف إدعاء / How to add a claim

1. Write the exact claim text as it appears on the surface.
2. Cite the surface as `path:line` or page name.
3. Choose Status. If Hypothesis, ensure the surface phrasing is hypothesis-framed.
4. Add Evidence link (Proof Pack ID, test path, or `n/a — hypothesis`).
5. Set Owner. Get **Approved by** (founder) before it ships. Stamp Date.

## السجل / The Register

| Claim | Surface (page/file) | Status | Evidence link (Proof Pack ref) | Owner | Approved by | Date |
|---|---|---|---|---|---|---|
| Approval-first: every external action is human-gated before send | `landing/index.html`; `frontend/src/` funnel | Evidence-backed | Enforced: `HUMAN_APPROVAL_POLICY.md` + approval-gate tests (zero auto-send) | proof-governance-reviewer | Founder | 2026-06-05 |
| Dealix never auto-sends — you draft, a human approves, then it sends | `landing/index.html` (hero sub) | Evidence-backed | `HUMAN_APPROVAL_POLICY.md`; queue-only send path in code | engineer | Founder | 2026-06-05 |
| The Command Sprint delivers a Proof Pack | `landing/sprint`; `frontend/src/.../sprint` | Hypothesis | n/a — hypothesis until first paid Proof Pack is delivered | sales | _pending_ | _pending_ |
| Command Sprint delivers a Proof Pack in 7 days | `frontend/src/.../sprint` | Hypothesis | n/a — target SLA, not yet proven on paid engagement | sales | _pending_ | _pending_ |
| Saudi-first AI Business Operating System | `landing/index.html` (positioning) | Evidence-backed | Positioning doctrine: `CLAUDE.md` Identity; Arabic-first product | brand-director | Founder | 2026-06-05 |
| Your data is never used to train models | `landing/`; `frontend/` trust section | Evidence-backed | `DATA_RETENTION_POLICY.md` (no-training clause) | proof-governance-reviewer | Founder | 2026-06-05 |
| Turns scattered WhatsApp, Excel, and meetings into one governed rhythm | `landing/index.html` (value prop) | Rewritten | Was "automates your whole business"; rewritten to capability-only, no outcome promise | brand-director | Founder | 2026-06-05 |
| Market Intelligence OS is live | `frontend/src/.../platform` | Rewritten | Status-corrected per `MODULE_STATUS_MAP.md`; surface must show real label, not `LIVE` | website-architect | _pending_ | _pending_ |

> Rows with `_pending_` in **Approved by** are **blocked from shipping** until a founder approval and date are stamped.
