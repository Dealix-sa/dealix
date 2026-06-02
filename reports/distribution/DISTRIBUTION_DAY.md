# Distribution Day — يوم التصريف

Generated (UTC): 2026-06-02T20:39:11.009386+00:00

> approval-first — لا إرسال خارجي. هذه نتيجة تشغيل المسودات والمتابعات والعروض والمقاييس.

## `$ python3 scripts/generate_distribution_drafts.py`

exit code: `0`

```text
prospects: 8 | drafts: 8 | pending_approval: 8
wrote: data/drafts/drafts.jsonl
wrote: reports/distribution/DRAFT_QUEUE_REVIEW.md
DEALIX_DISTRIBUTION_DRAFTS=PASS
```

## `$ python3 scripts/review_draft_queue.py`

exit code: `0`

```text
drafts in queue: 8 | pending_approval: 8
wrote: reports/distribution/DRAFT_QUEUE_REVIEW.md
DEALIX_DRAFT_QUEUE=PASS
```

## `$ python3 scripts/generate_followup_queue.py`

exit code: `0`

```text
followups: 3 | due now: 3
wrote: data/followups/followups.jsonl
wrote: reports/distribution/FOLLOWUP_QUEUE.md
DEALIX_FOLLOWUP_QUEUE=PASS
```

## `$ python3 scripts/generate_proposal_draft.py`

exit code: `0`

```text
proposal drafts: 2
wrote: data/proposals/<prospect>.md
wrote: reports/distribution/PROPOSAL_DRAFT_REPORT.md
DEALIX_PROPOSAL_DRAFTS=PASS
```

## `$ python3 scripts/check_draft_quality.py`

exit code: `0`

```text
checked: 8 | violations: 0
wrote: reports/distribution/DRAFT_QUALITY_GATE.md
DEALIX_DRAFT_QUALITY_GATE=PASS
```

## `$ python3 scripts/distribution_metrics.py`

exit code: `0`

```text
drafts: 8 | followups: 3 | due: 3
wrote: reports/distribution/DISTRIBUTION_METRICS.md
DEALIX_DISTRIBUTION_METRICS=PASS
```

## Verdict

**PASS**
