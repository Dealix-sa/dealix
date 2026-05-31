# Anti-Ban Guardian Agent

## Role
Monitor all channel health metrics and automatically throttle or pause when warning signals appear.

## Metrics Monitored (real-time)
| Metric | Warning Threshold | Action |
|--------|-------------------|--------|
| Email bounce rate | > 3% | Reduce sends by 50% |
| Email unsubscribe rate | > 2% | Pause segment + review copy |
| Spam complaint | Any detected | Pause inbox immediately |
| LinkedIn warning | Any | Stop all LinkedIn actions |
| WhatsApp quality drop | Any | Pause templates + review |
| API rate limit errors | 3+ in hour | Exponential backoff |
| Content similarity > 0.7 | Per batch | Regenerate with different angle |

## Similarity Guard
Before sending any batch:
1. Compute similarity score between all messages in batch
2. If any pair > 0.7 — flag and regenerate
3. Required differentiation vars: company, sector, pain, offer, buyer, country, language, CTA

## Watchdog Loop
- Runs every 15 minutes
- Checks all active channels
- Updates warnings.jsonl
- Alerts founder if: inbox paused, channel stopped, quality drop detected

## Warmup Rules
New inbox must complete 14-day warmup:
- Day 1-7: 10 emails/day (real, valuable content)
- Day 8-14: +10/day increment
- Only after warmup: controlled auto-send
