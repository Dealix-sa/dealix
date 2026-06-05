# Daily Operating Guide / دليل التشغيل اليومي

> **Purpose (EN):** What the founder runs every day.
>
> **الغرض (AR):** ما يشغّله المؤسس كل يوم.

_Layer: V9 — Strategic Moat & Enterprise Readiness OS_

## Morning / الصباح

- Review the daily brief (founder_brief_agent output) and the pipeline.
- Check customer health signals; act on amber/red accounts.
- Approve or revise any drafts queued from the prior day.

## Midday / منتصف اليوم

- Run demos from sandbox packs only (`scripts/demo_pack_generate.py`).
- Advance opportunities through the lifecycle stages.
- Capture one reusable asset (playbook, objection, proof) per engagement.

## End of Day / نهاية اليوم

- Update the relevant ledgers.
- Queue tomorrow's drafts for review (never auto-send).
- Confirm no secrets or boundary violations in today's work.

## Daily Verifier / المتحقق اليومي

```bash
python scripts/customer_lifecycle_verify.py
python scripts/agent_governance_verify.py
python scripts/cost_control_verify.py
```

---

## Operating Boundaries / حدود التشغيل

**AI prepares; the founder approves and sends.** Founder approval remains required.
