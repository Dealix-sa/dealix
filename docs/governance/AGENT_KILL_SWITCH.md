# Agent Kill Switch — مفتاح إيقاف الوكيل

> **Why this doc exists / لماذا هذا المستند موجود:**
> The audit (`scripts/verify_agent_registry.py`) requires the governance corpus to
> name the kill-switch concept explicitly. The mechanism existed in code
> (`dealix/governance/approvals.py`) but was undocumented. This doc names it.

## 1. Purpose / الغرض
Every Dealix agent must be **stoppable** at three layers, with no code
deploy required. This is the kill switch — مفتاح الإيقاف. It is what
makes "AI agent" different from "shadow process".

## 2. The three layers of stop / الطبقات الثلاث للإيقاف

| Layer | Mechanism | Owner | Time to effect |
|-------|-----------|-------|----------------|
| **A. Approval-gate freeze** | `ApprovalGate` denies the next request for any action class | Founder / on-call | seconds |
| **B. Config-flag disable** | Flip `WHATSAPP_ALLOW_LIVE_SEND=false` (or equivalent per-tool flag) in Railway env vars | Founder | next deploy / hot reload |
| **C. Code-path disable** | Set `requires_approval: true` + remove auto-approval entry in `dealix/config/approval_policy.yaml` | Engineering | next deploy |

## 3. Mapping to the existing code / الربط مع الكود الحالي

- `dealix/governance/approvals.py` exposes `ApprovalGate.request(...)` and `.decide(...)`. Any external-impact action calls `request()`; the gate **defaults to deny** for `CRITICAL_ACTIONS` or `risk_score >= 0.7`.
- `core/config/settings.py` declares `WHATSAPP_ALLOW_LIVE_SEND` (default **false**). The provider in `auto_client_acquisition/email/whatsapp_multi_provider.py` consults this flag and emits a `blocked_by_policy` event when it is false.
- `dealix/config/approval_policy.yaml` is the policy-as-code source of truth. Every action with `requires_approval: true` is gated by `ApprovalGate.request`.

## 4. How to actually pull the switch / كيف تشغّل المفتاح فعلًا

### A. Freeze a single action class
```bash
# In an admin shell — adds a deny rule that ApprovalGate consults first.
python -c "from dealix.governance.approvals import ApprovalGate; ApprovalGate.freeze('outbound_email_campaign', reason='founder_freeze')"
```

### B. Disable live WhatsApp send
1. Railway → service → Variables → set `WHATSAPP_ALLOW_LIVE_SEND=false`.
2. Trigger redeploy. The provider will start returning `provider="policy"` immediately on next request.

### C. Take an agent class offline at the policy layer
1. Edit `dealix/config/approval_policy.yaml`.
2. For the action class, set `requires_approval: true` and remove any `auto_approve` clauses.
3. Open a PR. Engineering merges. Next deploy enforces.

## 5. Owner / المالك
- **Layer A:** Founder + on-call engineer.
- **Layer B:** Founder (env-var change is one click in Railway UI).
- **Layer C:** Engineering (PR review required).

## 6. Cadence / الإيقاع
- Tested **monthly** as part of the reliability drill — see `readiness/production_readiness_gates.md`.
- Re-validated on every change to `approval_policy.yaml` (CI runs `scripts/verify_policy_as_code.py`).

## 7. Source of truth / مصدر الحقيقة
- Code:   `dealix/governance/approvals.py`
- Policy: `dealix/config/approval_policy.yaml`
- Flags:  `core/config/settings.py`
- This doc: `docs/governance/AGENT_KILL_SWITCH.md`

## 8. Failure mode / حالة الفشل
- **If ApprovalGate is bypassed** (a code path imports the provider directly without going through `request()`), `scripts/verify_live_send_safety.py` will FAIL in CI and the deploy is blocked.
- **If the freeze list is wiped by a deploy**, the action-class freeze must be re-applied. The freeze list is *not* persistent by design — it is a tactical pause.

## 9. Recovery path / مسار الاسترداد
1. Confirm the freeze took effect: `curl ${BASE_URL}/api/v1/admin/approvals/queue` shows the action class is denied.
2. Investigate root cause; if false alarm, call `ApprovalGate.unfreeze(action_class)`.
3. If real, leave frozen and follow the incident runbook (`docs/SECURITY_RUNBOOK.md`).

## 10. Verification / التحقق
```bash
python scripts/verify_agent_registry.py
python scripts/verify_live_send_safety.py
python scripts/verify_policy_as_code.py
make everything
```

## 11. Next action / الإجراء التالي
- Engineering: implement `ApprovalGate.freeze` / `unfreeze` if not yet present (this doc is the contract).
- Founder: practice the freeze monthly so the muscle memory is there when needed.
