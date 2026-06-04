# Daily Execution Rhythm

| Time | Action | Tool |
|------|--------|------|
| 08:00 | Generate drafts | `commercial_generate_400_drafts.py --target 400` |
| 08:10 | Safety audit | `commercial_safety_audit.py` |
| 08:15 | Review top 50, approve 20–50 manually | `top_50_priority.md` |
| 11:00 | Manual sends (founder only) + CRM update | `crm_pipeline_schema.json` |
| 14:00 | Manual follow-ups (only where a prior touch exists) | — |
| 17:00 | Classify replies, log objections, set tomorrow's focus | `next_actions.md` |
| 17:30 | Metrics snapshot | `commercial_metrics_summary.py` |

## Weekly
- Review reply rate and objection patterns.
- Rotate vertical focus based on signal.
- Refresh `media_social_calendar_generate.py` plan.

## Non-negotiables
- No automated sending, ever.
- No cold WhatsApp, no LinkedIn automation, no website auto-submit.
- Manual approval owner = founder.
