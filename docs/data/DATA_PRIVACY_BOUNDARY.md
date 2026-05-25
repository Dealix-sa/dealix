# Data Privacy Boundary
## Purpose
Define which data can exist in public repo, private ops, local-only files, or external systems.
## Data Classes
### Public
- templates
- policies
- demo data
- documentation
- safe examples
### Private Ops
- leads
- client names
- proposals
- revenue logs
- payments
- approvals
- delivery reports
- feedback
### Local Only
- real dashboard JSON
- secrets
- API keys
- raw exports
- private snapshots
### Never Commit
- API keys
- passwords
- access tokens
- personal data exports
- real customer confidential data
- payment credentials
## Rules
- No real leads in public repo.
- No real client names in public proof without approval.
- No real dashboard JSON committed.
- No secrets in Git.
- No AI output containing private data published without review.
## Evidence
- .gitignore
- public safety verifier
- GitHub secret scanning
- approval log
