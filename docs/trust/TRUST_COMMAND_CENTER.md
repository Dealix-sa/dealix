# Trust Command Center

Single source of truth for **what Dealix is allowed to do without a human in the loop**.

This is the **Tier 0 contract** between Dealix automations and the world. If a behaviour is
not on the green list, it is forbidden. The verifier `scripts/verify_tier0_safety.py`
enforces this.

## Green list — allowed without human approval

| Action | Bounds |
|---|---|
| Read public/internal repo files | any path inside this repo |
| Read private-ops files | only files under `--private-ops` path |
| Write to private-ops files | only files matching `*.md`, `*.csv`, `*.json`, `*.yaml` |
| Run verifier scripts | anything matching `scripts/verify_*.py` |
| Generate drafts (DMs, proposals, emails) | written to disk, not sent |
| Compute / display dashboards | read-only |
| Open a local browser tab | not navigating to third-party APIs with credentials |

## Red list — forbidden without explicit founder approval per action

| Action | Why |
|---|---|
| Send external messages (email, WhatsApp, LinkedIn, SMS, voice) | irreversible, brand-damaging |
| Charge customers / move money | irreversible |
| Sign contracts / agree to terms | binding |
| Create/modify cloud infra (DNS, hosting, secrets) | costs + outages |
| Push to `main` directly | merges go through PR |
| Force-push, hard-reset, branch deletion on shared branches | data loss |
| Scrape any third party without ToS check + rate limits | legal |
| Mass cold outreach automated | spam + brand |

## Approval log

Every red-list action that *did* happen is appended to:

```
trust/approval_log.csv
```

Required columns:

```
timestamp, action, scope, approver, approval_evidence, reversible_within
```

`approval_evidence` must be a path to a screenshot, email, or commit hash —
not "verbal" alone.

## How an automation requests approval

```python
from dealix_cli.approvals import request_approval

request_approval(
    action="send_dm",
    scope="lead_id=42, channel=linkedin",
    body_path="drafts/dm_42_v1.md",
)
```

This appends a row to `founder/approvals_waiting.md` and exits 0 *without*
performing the action. The founder reviews, approves manually, and the
automation re-runs.

## Trust boundary terms — never weaken these

The following phrases must remain unchanged in this file. `scripts/verify_trust_boundary_terms.py`
hard-fails if any are deleted or weakened:

- "No external send is automated."
- "Every red-list action that *did* happen is appended to"
- "approval_evidence must be a path"
- "force-push, hard-reset, branch deletion on shared branches"

## Related

- `scripts/verify_tier0_safety.py` — enforces the green/red lists.
- `scripts/verify_no_autonomous_external_actions.py` — greps codebase for forbidden patterns.
- `scripts/verify_trust_boundary_terms.py` — enforces the phrase contract above.
- `docs/founder/GO_NO_GO_DECISION_SYSTEM.md` — how the founder approves quickly.
