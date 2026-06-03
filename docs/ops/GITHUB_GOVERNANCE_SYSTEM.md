# GitHub Governance System

## Purpose
How Dealix uses GitHub safely as a single founder, while keeping the public/private boundary intact.

## Branches
- `main`: protected, requires CI green + 1 approval (founder self-approval allowed for solo phase).
- Feature branches: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`, `docs/<topic>`.
- Sprint branches: `claude/<sprint-id>` for AI-assisted sessions.
- Long-running spikes: kept local; never pushed.

## Pull requests
- Title format: `<type>: <imperative summary>` (e.g., `feat: add revenue ops verifier`).
- Body must include: motivation, what changed, how to verify.
- Linked issue or todo item when applicable.
- Draft PRs allowed; convert to ready only when verifier passes.

## Required CI checks (target state)
- Public safety scanner.
- Data boundary scanner.
- Security/reliability OS verifier.
- Implementation sprint pack verifier.
- Lint + tests.

## Labels (lightweight)
- `sprint-0` through `sprint-10`.
- `infra`, `docs`, `verifier`, `runtime`, `evidence`.
- `risk:high` for changes that touch trust, finance, or public claims.

## Issue policy
- Use issues for tracked bugs, blockers, and decisions that need a paper trail.
- Don't use issues for personal todos — those belong in `dealix-ops-private/founder/ceo_action_queue.md`.

## Secrets in GitHub
- Use GitHub Actions secrets only for CI-needed credentials.
- Never echo secrets in logs.
- Rotate any secret with a published commit immediately.

## Deletion / rewrite policy
- No force-push to `main`.
- Force-push elsewhere only with founder approval (logged in `trust/approval_log.csv`).
- Removing private data that leaked: rotate first, then rewrite history with founder approval.

## Reviewers
- Solo phase: founder. Optionally request AI ultrareview for second opinion.
- Contractor phase: contractor opens PR; founder approves.

## Tags & releases
- Semantic versioning for any externally exposed surface.
- Release notes live in `CHANGELOG.md`.
