# WhatsApp Client OS — Reports — تقارير

Founder-facing reports generated from the WhatsApp Client OS runtime stores
(`data/whatsapp/*.jsonl`, gitignored). They reflect only recorded events — no
invented funnel numbers.

## Generate — التوليد

```bash
python3 scripts/generate_whatsapp_reports.py
```

Writes into this directory:

| File | Contents |
| --- | --- |
| `WHATSAPP_METRICS.md` | Session, scan, card, handoff, and support counts |
| `WHATSAPP_SESSION_REVIEW.md` | Per-session flow / permission / turns / handoff |
| `WHATSAPP_ACTION_QUEUE.md` | Action cards with risk + governance decision |
| `WHATSAPP_HANDOFF_QUEUE.md` | Sessions awaiting a human |
| `WHATSAPP_CLIENT_ASSESSMENTS.md` | Readiness scores + recommended offers |

The generated `.md` outputs are runtime artifacts and are not committed.

See also: [`docs/whatsapp/`](../../docs/whatsapp/) ·
[`auto_client_acquisition/whatsapp_client_os/metrics.py`](../../auto_client_acquisition/whatsapp_client_os/metrics.py).

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة_
