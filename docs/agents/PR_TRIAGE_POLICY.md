# Dealix PR Triage Policy — سياسة فرز طلبات الدمج

A repo with hundreds of open PRs needs a deterministic way to sort them so nothing
valuable is lost and nothing risky merges by accident. This policy + the
`scripts/triage_open_prs.py` tool produce a single triage report; humans decide.

---

## Buckets

`scripts/triage_open_prs.py` sorts every open PR into exactly one bucket (first match wins):

| Bucket | Signal | Default action |
|---|---|---|
| `draft` | PR marked draft | leave until author marks ready |
| `security` | title/label mentions security/auth/secret | review first, with care |
| `dependencies` | dependabot / bump / `deps` label | batch-review, let CI decide |
| `agent` | title mentions claude / codex / agent | check against the registry |
| `docs` | docs-only / `docs` label | fast-track if CI green |
| `needs_review` | everything else | rank by staleness |

Within each bucket, PRs are ordered by last-updated (most stale surfaced for a
close/rebase decision).

## Human decisions (agents do not merge)

For each PR a human picks one: **merge candidate · needs tests · needs rebase ·
stale (close) · risky (hold) · docs-only fast-track**. No agent merges to `main`
(see [`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md)).

## Hygiene rules

- A PR with no update in **30+ days** and conflicts → propose close with a note.
- A `security`-bucket PR is never fast-tracked; it gets a real review.
- An `agent`-bucket PR must keep `.claude/agents/` ↔ `.codex/agents/` parity
  (`make agents-audit`).
- Dependency PRs merge only when CI is fully green.

## Run it

```bash
make pr-triage      # or: python scripts/triage_open_prs.py
```

Output: `reports/pr_triage/OPEN_PR_TRIAGE.md` + `open_pr_triage.json`.

- **Locally / in CI:** the script uses the `gh` CLI when available (GitHub Actions
  runners have it; it reads `GITHUB_TOKEN`). If `gh` is unavailable it writes a
  SKIPPED report with instructions — it never fails the build.
- **From an agent session with GitHub MCP tools:** use `list_pull_requests` to pull
  the live list and write the same report shape, then apply this policy.

A weekly snapshot runs via [`.github/workflows/pr-triage.yml`](../../.github/workflows/pr-triage.yml).
