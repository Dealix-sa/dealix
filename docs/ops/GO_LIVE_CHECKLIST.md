# Go-Live Checklist

Use this checklist before any production deployment or client demo.

---

## 1. Environment Setup

- [ ] `.env` file created with all required variables from `docs/ops/ENVIRONMENT_VARIABLES.md`
- [ ] `DATABASE_URL` points to production MySQL instance
- [ ] WhatsApp credentials configured (if WhatsApp features are needed)
- [ ] `APP_ID` and `APP_SECRET` set for authentication
- [ ] All secrets stored outside the repository (not in `.env.example` or code)

## 2. Build Verification

- [ ] `npm run check` — TypeScript passes with zero errors
- [ ] `npm run build` — Production build succeeds
- [ ] `npm run outbound-dry` — Safety gate: PASS
- [ ] `npm run production-check` — Launch decision: GO (warnings acceptable, zero blockers)

## 3. Database Readiness

- [ ] MySQL 8.0+ accessible from app environment
- [ ] `npm run db:push` — Schema pushed successfully
- [ ] Tables created: deals, activities, prospects, drafts, signals, decisions, bookings
- [ ] Test query returns expected structure

## 4. Docker Deployment (if using containers)

- [ ] `docker compose up --build` completes without errors
- [ ] MySQL health check passes
- [ ] App health check passes (`http://localhost:3000`)
- [ ] `docker compose logs app` shows no startup errors

## 5. Safety and Compliance

- [ ] `OUTBOUND_MODE=draft_only` is the default
- [ ] `WHATSAPP_ALLOW_LIVE_SEND=false` unless explicitly approved
- [ ] `EXTERNAL_SEND_ENABLED=false` for all channels by default
- [ ] PDPL checklist reviewed (`docs/compliance/PDPL_CHECKLIST.md`)
- [ ] SDAIA AI compliance notes reviewed (`docs/compliance/SDAIA_AI_COMPLIANCE.md`)
- [ ] No hardcoded credentials in source code
- [ ] `.env` and `.env.local` are in `.gitignore`

## 6. Commercial Readiness

- [ ] Homepage message matches the actual product offer
- [ ] Pricing and packaging are internally aligned (`business/products/PRICING_AND_PACKAGING.md`)
- [ ] Booking flow is accessible and reviewed at `/book-call`
- [ ] Revenue Command Room displays correctly at `/command-room`
- [ ] Brain OS displays correctly at `/brain`
- [ ] No fabricated ROI numbers, fake testimonials, or unverified claims

## 7. Operational Readiness

- [ ] `npm run company-day` runs without errors
- [ ] `npm run command-room` generates expected output
- [ ] `npm run brain-day` runs governance + scorecard
- [ ] Client delivery templates are complete (`clients/_template/`)
- [ ] Report artifacts directory exists and is writable

## 8. Team Readiness

- [ ] Daily owner of Command Room is identified
- [ ] Weekly owner of Brain review is identified
- [ ] Draft approval reviewer is identified
- [ ] First 30-day operating goals are documented
- [ ] Incident handling path is identified (who responds to issues)

## 9. Go-Live Decision

| Gate | Status | Owner |
|------|--------|-------|
| Build passes | [ ] | Dev |
| Safety gates pass | [ ] | Dev |
| Database connected | [ ] | Ops |
| Secrets secured | [ ] | Ops |
| Commercial message reviewed | [ ] | Founder |
| Compliance docs reviewed | [ ] | Founder |
| Daily operations owner assigned | [ ] | Founder |

**Decision:** _____________ (GO / NO-GO)
**Date:** _____________
**Approved by:** _____________

---

## Post-Launch (First 72 Hours)

- [ ] Monitor application logs for errors
- [ ] Verify booking submissions are received
- [ ] Check WhatsApp webhook delivery (if enabled)
- [ ] Review first batch of draft messages before enabling live send
- [ ] Run `npm run production-check` daily for the first week
- [ ] Collect first feedback from daily Command Room usage
