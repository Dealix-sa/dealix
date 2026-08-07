# Production Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| R-01 Auto-send enabled by mistake | Medium | Critical | All drafts marked `draft_pending_human_review`; no auto-send functions in code |
| R-02 Secrets committed | Medium | Critical | `check_no_secrets.py` + `.env.example` placeholders + CI gate |
| R-03 Demo data treated as real | Medium | High | Every demo record has `"demo": true`; production mode requires `lawful_basis_note` |
| R-04 CSV import overwrites CRM | Low | High | `json_store.py` creates `.bak` before every write; `--dry-run` default path |
| R-05 Weak legal boundaries | Medium | High | `lawful_basis_note` required in production; `terms_review_required` flag on connectors |
| R-06 Unpersuasive Arabic outreach | High | Medium | Arabic playbook + review checklist + hypothesis language enforced in `drafts.py` |
| R-07 Website build breaks | Medium | Medium | Add `npm install` to CI; typecheck + build gates |
| R-08 Missing follow-ups | High | Medium | `generate_followup_queue.py` + `add_followup.py` + pipeline report |
