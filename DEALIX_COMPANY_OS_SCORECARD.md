# Dealix Company OS Scorecard

> Owner: Founder. Verify: `scripts/verify_company_os.py`. Updated each weekly
> CEO review and on every push to `main`.

Composite scorecard that rolls every operating system up into one number.
The verify script asserts each row below has an owning file and the
metric is calculable.

---

## Domains

| Domain | Owner file | Scorecard file | Verify script | Weight |
|--------|-----------|----------------|---------------|--------|
| Founder OS | `docs/founder/CEO_OPERATING_SYSTEM.md` | `readiness/scorecards/founder_os_scorecard.md` | `scripts/verify_founder_os.py` | 15 |
| Revenue OS | `docs/revenue/REVENUE_MODEL.md` | `readiness/scorecards/revenue_os_scorecard.md` | `scripts/verify_revenue_os.py` | 20 |
| Delivery OS | `docs/delivery/DELIVERY_QUALITY_STANDARD.md` | `readiness/scorecards/delivery_os_scorecard.md` | `scripts/verify_delivery_os.py` | 15 |
| Trust OS | `docs/trust/AUTONOMY_POLICY.md` | `readiness/scorecards/trust_os_scorecard.md` | `scripts/verify_trust_os.py` | 15 |
| Product OS | `docs/product/PRODUCT_PRINCIPLES.md` | `readiness/scorecards/product_os_scorecard.md` | `scripts/verify_product_os.py` | 10 |
| Learning OS | `docs/learning/LEARNING_ROUTER.md` | `readiness/scorecards/learning_os_scorecard.md` | `scripts/verify_learning_os.py` | 10 |
| Control Plane | `docs/control_plane/CONTROL_PLANE_ARCHITECTURE.md` | n/a | `scripts/verify_control_plane.py` | 10 |
| Public Safety | `docs/trust/PUBLIC_REPO_SAFETY.md` | n/a | `scripts/verify_public_safety.py` | 5 |

Total weight: 100.

---

## Composite

The composite score is computed by
`dealix/scoring/company_health_score.py`. Each domain returns a 0..100
score; the composite is a weight-normalized average.

Healthy band: ≥ 80. Watch band: 60–80. Alert band: < 60 triggers a CEO
alert in `docs/founder/CEO_ALERTS.md` and reprioritizes work via
`operating_intelligence/priority_engine.py`.

---

## Update Discipline

- Composite recomputed nightly by `scripts/export_company_os_status.py`.
- Verify run is required by branch protection on `main`.
- Weekly CEO review records the score and any actions in
  `founder/weekly_ceo_review.md` (private repo).
