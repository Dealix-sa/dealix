# No External Action Without Approval / لا إجراء خارجي بدون موافقة

**Status:** Binding operating gate for Dealix.
**Owner:** Founder.
**Related:** [`../governance/APPROVAL_POLICY.md`](../governance/APPROVAL_POLICY.md) ·
[`../governance/HUMAN_IN_THE_LOOP_MATRIX.md`](../governance/HUMAN_IN_THE_LOOP_MATRIX.md) ·
[`../governance/AI_ACTION_LEVELS.md`](../governance/AI_ACTION_LEVELS.md)

This document defines the action levels that gate everything Dealix (human or
agent) does on behalf of the company or a customer. CLAUDE.md and AGENTS.md
carry this as context; real enforcement lives in verification scripts, the
customer **Approval Register** (`customers/<slug>/06_approval_register.md`), and
CI gates. Documentation alone is not enforcement.

---

## Action levels / مستويات الإجراء

| Level | Name | Meaning / المعنى | Who may proceed |
| --- | --- | --- | --- |
| **A0** | Internal draft | A rough internal artifact, never seen outside the team | Generated internally |
| **A1** | Internal analysis | Research, diagnostics, scoring — internal only | Generated internally |
| **A2** | Customer-facing draft | Anything that *could* be shown to a customer | **Founder review required before use** |
| **A3** | External action | Anything that actually leaves the building | **Explicit founder approval required** |
| **A4** | Financial / legal / security action | Money, contracts, credentials, data-sharing | **Explicit founder approval + evidence** |
| **A5** | Destructive action | Irreversible deletion / teardown | **Forbidden unless the founder explicitly requests it** |

### Rules / القواعد
1. **A0 / A1** can be generated internally without approval.
2. **A2** requires founder review before the draft is used anywhere.
3. **A3** requires explicit founder approval, logged in the Approval Register.
4. **A4** requires explicit founder approval **and** attached evidence
   (invoice, contract, DPA, consent record).
5. **A5** is forbidden by default; only the founder can explicitly request it,
   and it is logged.

A default-deny posture applies: if the level is ambiguous, treat it as the
**higher** level and stop for approval.

---

## Where each surface lands / تصنيف القنوات

| Surface / القناة | Default level | Notes |
| --- | --- | --- |
| **Email** | A3 | Drafting = A2; sending = A3. No auto-send. |
| **WhatsApp** | A3 | No cold automation, ever. Manual send only, after approval. |
| **LinkedIn** | A3 | No automation/scraping. Manual, approved messages only. |
| **Website publishing** | A3 | Going live is external. |
| **Customer reports** (Proof Pack, diagnostic) | A2 → A3 | Draft = A2; sending to the customer = A3. |
| **Payment links** | A4 | Money path → approval + evidence. |
| **Public case studies** | A4 | External + reputational; needs customer publication consent + evidence. |
| **GitHub actions** (push, PR, release, deploy) | A3 / A4 | Code push/PR = A3; production deploy / secret changes = A4. Never A5 history rewrites without explicit request. |

---

## Hard prohibitions / محظورات قاطعة
- No real external sending during dry runs or simulations.
- No fake or projected result presented as a real, achieved result.
- No guaranteed-revenue or guaranteed-outcome language.
- No publishing a customer's name without written publication consent.
- No cold WhatsApp automation, LinkedIn automation, or scraping.
- No future/unbuilt module presented as live.

## Enforcement hooks / نقاط الإنفاذ
- Per-customer **Approval Register** logs every A2+ action and its decision.
- `scripts/run_dealix_e2e_dry_run.py` fails if any stage attempts a real
  external action or presents fake proof.
- `scripts/verify_dealix_launch_readiness.py` checks that this gate and the
  approval policy exist and that no auto-send language is present.
- `.github/workflows/dealix-launch-gates.yml` runs the above on every change,
  read-only, with no secrets printed.
