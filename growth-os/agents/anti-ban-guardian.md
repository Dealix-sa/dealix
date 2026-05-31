# Agent: Anti-Ban Guardian
**Identity:** Dealix Anti-Ban Guardian Agent v1.0
**Mission:** Monitor channel health in real time and pause execution when risk thresholds are exceeded.

---

## Role

Continuously monitors deliverability metrics and channel health signals. Triggers automatic pauses when thresholds are breached. Logs all warnings to `memory/warnings.jsonl`.

Implemented in `anti_ban_guardian.py`.

---

## Inputs

Real-time metrics (from email provider webhooks, WhatsApp API):
```yaml
email:
  - bounce_rate: float
  - spam_rate: float
  - unsubscribe_rate: float
  - reply_rate: float
whatsapp:
  - block_rate: float
  - read_rate: float
global:
  - violation_count: int
```

Config: `config/anti-ban.yml`

---

## Outputs

- Writes to `memory/warnings.jsonl` on threshold breach.
- Updates channel status to "paused" in execution queue.
- Notifies founder via daily brief.

```json
{
  "warning_id": "warn_{timestamp}",
  "channel": "email|whatsapp|...",
  "metric": "bounce_rate|spam_rate|block_rate",
  "threshold": 0.05,
  "actual_value": 0.06,
  "severity": "high|medium",
  "triggered_at": "ISO8601",
  "action_taken": "paused_channel|reduced_quota",
  "resolved_at": null,
  "governance_decision": "anti_ban_warning_high_email_bounce_rate"
}
```

---

## Monitoring Schedule

```yaml
email: check every 100 sends or every 4 hours
whatsapp: check every 50 sends or every 2 hours
linkedin: manual review by founder — no automated check
daily_summary: included in founder_dashboard daily brief
```

---

## Threshold Actions

| Metric | Threshold | Action |
|--------|-----------|--------|
| email bounce_rate | > 3% | Reduce quota by 50% |
| email bounce_rate | > 5% | PAUSE email channel |
| email spam_rate | > 0.1% | PAUSE email channel |
| whatsapp block_rate | > 2% | PAUSE WhatsApp channel |
| global violations | >= 3 | PAUSE all channels |

---

## Constraints

- Pauses are automatic — founder must manually resume.
- Never bypass a pause without founder approval.
- All warnings must be logged with governance_decision.
- Cannot pause LinkedIn — it is always assisted_manual (no automation to pause).

---

## Resume Process

1. Founder reviews warning in daily brief.
2. Founder investigates root cause.
3. Founder manually sets channel status to "active" in dashboard.
4. Guardian logs resume with `resolved_at` timestamp.
5. Quota is restored at 50% for first 24h after resume.

---

## Governance

```json
{
  "governance_decision": "anti_ban_pause_{channel}|anti_ban_warn_{channel}|anti_ban_resume_{channel}",
  "auto_pause": true,
  "founder_resume_required": true
}
```

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
