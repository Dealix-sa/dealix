# Ultimate Security & Governance

Governance posture for the Ultimate Operating Layer:

- Internal API requires `X-Dealix-Internal-Token` when
  `DEALIX_INTERNAL_TOKEN` is set.
- Private ops tree lives outside the public repo.
- No external sends from any agent or worker.
- Policy-as-code is YAML, reviewed in pull requests.
- Eval gate blocks regressions on forbidden phrases, prompt injection,
  and sensitive data leakage.
- Branch protection should require the
  `dealix-ultimate-operating-layer` workflow on `main`.
