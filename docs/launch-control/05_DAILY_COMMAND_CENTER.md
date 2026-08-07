# 05 — Daily Command Center

روتين يومي ثابت يحوّل النظام إلى إيقاع تشغيلي. الأوقات بتوقيت الرياض.
A fixed daily routine that turns the system into an operating rhythm (Riyadh time).

| Time | Action | Tool / output |
|---|---|---|
| 08:00 | Generate drafts | `commercial_generate_400_drafts.py --target 400` |
| 08:15 | Safety check | `commercial_safety_audit.py` → `safety_audit.json` |
| 08:30 | Review top 50 | `top_50_priority.md` — approve/edit/reject |
| 10:00 | Manual outreach (approved only) | founder sends individually |
| 13:00 | Discovery calls / follow-ups | calendar |
| 16:00 | Content / social (manual post) | `calendar_30_day.json` |
| 18:00 | CRM update | move stages per `crm_pipeline_schema.json` |
| 20:00 | Daily metrics & next actions | `daily_metrics.json` |

## Daily definition of done
- [ ] 400+ drafts generated and audited (PASS).
- [ ] Top 50 reviewed; approvals logged.
- [ ] Approved outreach sent **manually**.
- [ ] At least one founder post published manually.
- [ ] CRM stages updated; suppression honored.
- [ ] Metrics captured; tomorrow's top 3 set.

> If `commercial_safety_audit.py` is not PASS, **stop** — do not review or send. See the Failure Playbook.
