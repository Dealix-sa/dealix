# Day 30 — Go/No-Go Checklist for Wave 2 Expansion

**Date:** Run this on Day 30 of the activation plan.  
**Owner:** Founder  
**Decision:** Proceed to Wave 2 (SAR 30K MRR target) or extend Day 1-30 sprint.

---

## Section A — Revenue Gates (ALL must be ✓ to proceed)

| Gate | Target | How to verify | Status |
|------|--------|---------------|--------|
| A1. Paid contracts | ≥ 3 paying customers | `SELECT count(*) FROM payments WHERE status='paid'` | ☐ |
| A2. MRR baseline | ≥ SAR 4,500/mo | `SELECT sum(amount_halalas)/100 FROM payments WHERE status='paid' AND created_at > now()-'30d'::interval` | ☐ |
| A3. Moyasar live mode | `DEALIX_MOYASAR_MODE=live` set | Check Railway Variables → `DEALIX_MOYASAR_MODE` | ☐ |
| A4. First payment received | At least 1 confirmed Moyasar webhook | Check `payments` table in production DB | ☐ |

---

## Section B — Product Gates (≥ 4/5 must be ✓)

| Gate | Target | How to verify | Status |
|------|--------|---------------|--------|
| B1. Sprint demo load | < 1s on cache hit | `curl -w "%{time_total}" https://api.dealix.me/api/v1/sprint/sample` | ☐ |
| B2. Proof Pack PDF | Generates without error | `POST /api/v1/sprint/render/pdf` → check `content-type: application/pdf` | ☐ |
| B3. Company Brain v1 | Present in Sprint output | `run.company_brain["status"] == "company_brain_v1_ready"` | ☐ |
| B4. Customer Portal | Shows real data for a customer | Open `https://dealix.me/ar/customer-portal?handle=<handle>` | ☐ |
| B5. WhatsApp notification | Fires on payment | Trigger test payment → check WhatsApp | ☐ |

---

## Section C — Infrastructure Gates (ALL must be ✓)

| Gate | Target | How to verify | Status |
|------|--------|---------------|--------|
| C1. Redis live | `REDIS_URL` set (non-localhost) | Railway Variables → `REDIS_URL` | ☐ |
| C2. API health | `/healthz` returns 200 | `curl https://api.dealix.me/healthz` | ☐ |
| C3. DB migrations | All migrations applied | `alembic current` matches latest head | ☐ |
| C4. CI Python checks | Green on main | Check GitHub Actions → CI → `main` branch | ☐ |

---

## Section D — GTM Gates (≥ 3/4 must be ✓)

| Gate | Target | How to verify | Status |
|------|--------|---------------|--------|
| D1. Demo page live | `/ar/demo` loads Sprint results | Open `https://dealix.me/ar/demo` | ☐ |
| D2. ZATCA landing | `/ar/zatca-readiness` quiz works | Open `https://dealix.me/ar/zatca-readiness` | ☐ |
| D3. Partners page | `/ar/partners` shows 5K SAR reward | Open `https://dealix.me/ar/partners` | ☐ |
| D4. Warm leads imported | ≥ 15 leads in DB | `SELECT count(*) FROM leads WHERE tier1_source IN ('warm_intro','founder_observation')` | ☐ |

---

## Section E — Safety Gates (ALL must be ✓ — non-negotiable)

| Gate | Status |
|------|--------|
| E1. No cold WhatsApp — `no_cold_whatsapp` hard gate active | ☐ |
| E2. No fake revenue — all payment amounts from real Moyasar webhooks | ☐ |
| E3. PDPL audit log — PII access logged in `audit_logs` table | ☐ |
| E4. Railway token revoked — `acb503f0-8198-4542-9ccc-e1f4bec3d7cc` revoked from dashboard | ☐ |

---

## Go / No-Go Decision Logic

```
if (A1 AND A2 AND A3 AND A4) AND (B ≥ 4) AND (C1-C4) AND (D ≥ 3) AND (E1-E4):
    GO → Execute Wave 2 (90-day plan):
         - ZATCA differentiator campaign
         - Partner OS activation (5 partner targets)
         - Multi-tenant RBAC enforcement
         - CEO Top-50 lead scoring → approval queue
else:
    NO-GO → Extend sprint:
         - Identify specific failing gates
         - Set 7-day remediation window
         - Re-run checklist
```

---

## If GO: Immediate Wave 2 Actions

1. **Run**: `python scripts/import_seed_leads.py` to import 15 warm leads into DB
2. **Activate**: `python scripts/ceo_top50_execute.py` to begin lead scoring
3. **Deploy**: ZATCA differentiator campaign (`/{locale}/zatca-readiness` already live)
4. **Recruit**: Reach out to first 3 partner targets (CRM consultants, lawyers, agencies)
5. **Set target**: SAR 30,000 MRR within 60 days from Go decision

---

## Smoke Test Commands (run all before decision)

```bash
# API health
curl -s https://api.dealix.me/healthz | jq .status

# Sprint demo cache speed
time curl -s https://api.dealix.me/api/v1/sprint/sample > /dev/null

# Proof Pack PDF
curl -s -X POST https://api.dealix.me/api/v1/sprint/render/pdf \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $DEALIX_API_KEY" \
  -d '{"customer_handle":"demo","proof_pack":{}}' \
  --output /tmp/proof.pdf && file /tmp/proof.pdf

# Business NOW snapshot (should show _cache_hit after first call)
curl -s https://api.dealix.me/api/v1/business-now/snapshot | jq ._cache_hit

# Railway surfaces
python scripts/verify_railway_surfaces.py

# Full regression suite
pytest tests/ -q --no-cov -x
```
