# Dealix — Launch Control Tower / برج التحكّم بالإطلاق

**Status:** canonical · **Owner:** Founder · **Updated:** 2026-06-06

Single board for Go / No-Go. Re-run the gates, then read the verdict.

```bash
python scripts/verify_dealix_positioning.py      && \
python scripts/verify_dealix_module_status.py    && \
python scripts/verify_dealix_growth_assets.py    && \
python scripts/verify_dealix_launch_readiness.py
```

---

## 1. No-Go conditions / شروط الرفض

You are **NOT** ready if any of these is true:

- A claim like "we guarantee more sales / نضمن زيادة المبيعات".
- Any `auto-send` or cold WhatsApp automation path.
- A future / planned module displayed as LIVE.
- Missing Proof Pack template.
- Missing Customer Folder template.
- Missing Claims Register.
- Missing Human Approval Policy.
- No clear Command Sprint offer.
- `npm run build` fails **without a known, logged cause**.

---

## 2. Private Launch Ready / جاهزية الإطلاق الخاص

All of these present and PASS:

| Gate | Required state | Source |
|---|---|---|
| Command Sprint offer | clear | `sales/COMMAND_SPRINT_ONE_PAGER.md` |
| Start / Diagnostic | clear | `sales/DIAGNOSTIC_SCRIPT.md` |
| Sales kit | ready | `sales/`, `docs/sales/` |
| Customer Folder template | ready | `docs/04_delivery/CUSTOMER_FOLDER_TEMPLATE.md` |
| Proof Pack template | ready | `docs/04_delivery/PROOF_PACK_TEMPLATE.md` |
| Claims Register | ready | `docs/03_governance/CLAIMS_REGISTER.md` |
| Human Approval Policy | ready | `docs/03_governance/HUMAN_APPROVAL_POLICY.md` |
| No unsafe claims | PASS | `verify_dealix_positioning.py` |
| Deliver first 3 customers manually | yes | `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md` |

---

## 3. Public Launch Ready / جاهزية الإطلاق العام

Private-Launch-ready **plus**:

| Gate | Required state |
|---|---|
| 3 paid Command Sprints | done |
| 3 Proof Packs | delivered |
| 1 case-safe story | published with consent + approval |
| `npm run build` | PASS (`reports/launch/npm_build.log`) |
| Privacy / Security / Trust pages | ready |
| Launch readiness score | 85+ |

---

## 4. Website minimum (Private Launch) / الحد الأدنى للموقع

| Surface | Route (frontend) |
|---|---|
| Home | `frontend/src/app/[locale]/page.tsx` |
| Command Sprint | `sales/COMMAND_SPRINT_ONE_PAGER.md` → page |
| Pricing | `frontend/src/components/gtm/PricingPage.tsx` |
| Start / Diagnostic | `frontend/src/app/[locale]/dealix-diagnostic/page.tsx` |
| Security / Trust | `frontend/src/app/[locale]/trust/page.tsx` |

SEO expansion is deferred until the CTA path (Diagnostic → Sprint) is clear.

---

## 5. Current verdict

Run `python scripts/verify_dealix_launch_readiness.py` and paste the SCORE +
verdict line here after each material change. The live snapshot is written to
`reports/launch/private_launch_readiness.md`.
