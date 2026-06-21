# Go-Live Checklist — Dealix Production

**Last Updated**: 2026-06-21

All items must be ✅ before pushing to `main` and deploying to Railway production.

---

## 1. Safety Gates (non-negotiable)

- [ ] `EXTERNAL_SEND_ENABLED=false` in Railway production env
- [ ] `OUTBOUND_MODE=draft_only` in Railway production env
- [ ] `EMAIL_SEND_ENABLED=false` in Railway production env
- [ ] `WHATSAPP_SEND_ENABLED=false` in Railway production env
- [ ] `WHATSAPP_ALLOW_LIVE_SEND=false` in Railway production env
- [ ] `SMS_SEND_ENABLED=false` in Railway production env
- [ ] Run `python scripts/railway/check_env_contract.py` → `RAILWAY_ENV_CONTRACT=PASS`

---

## 2. Code Quality

- [ ] P0 tests pass: `make founder-p0`
- [ ] No secrets committed: `git log --all --oneline | head -20` — no `.env`, no API keys
- [ ] Security smoke: `make security-smoke`
- [ ] All new modules have corresponding tests in `tests/company/`

---

## 3. Infrastructure

- [ ] `DATABASE_URL` set in Railway to production PostgreSQL
- [ ] `APP_SECRET_KEY` is 32+ characters, unique to production
- [ ] `APP_ENV=production` set in Railway
- [ ] Alembic single head: `make alembic-heads`
- [ ] Railway service deploys cleanly (no build errors)

---

## 4. Frontend (apps/web)

- [ ] `npm run build` passes locally (Tailwind v3 pinned)
- [ ] `npm run typecheck` passes (no TypeScript errors)
- [ ] No `@tailwindcss/postcss` in package.json (v3 only)

---

## 5. Commercial Readiness

- [ ] Free Diagnostic landing page live and tested
- [ ] 499 SAR Micro Sprint intake form operational
- [ ] WhatsApp draft queue functional (drafts reviewed before send)
- [ ] Proposal template renders for at least one real client
- [ ] Proof Pack template tested end-to-end

---

## 6. Approval Gates (founder must sign off)

- [ ] Founder reviewed all outreach drafts in `company/runtime/outbox/`
- [ ] No automated sends scheduled without explicit activation
- [ ] PR to `main` approved by founder (not auto-merged)
- [ ] Railway deployment triggered manually, not by CI auto-deploy

---

## 7. Post-Deploy Verification

- [ ] API health endpoint returns 200
- [ ] `make production-smoke` passes against live URL
- [ ] Safety config endpoint confirms all gates closed
- [ ] First client intake flow tested manually in staging

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Founder | سامي عسيري | | |
| Tech Lead | — | | |

**Merge to main only after all items checked and signed.**
