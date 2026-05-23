# Launch Asset Checklist — Dealix

## الدور — Role

قائمة فحص أصول السوق التي يجب أن تكون جاهزة ومرئية قبل أي حملة. تُفحص آليًا عبر `scripts/verify_launch_readiness.py`.

## القائمة — Checklist

| # | Asset | Required source | Verifier hook |
| --- | --- | --- | --- |
| 1 | Logo assets | `docs/brand/` | logo files exist |
| 2 | Brand tokens | `docs/brand/BRAND_TOKENS.md` | exists |
| 3 | Website / landing | `apps/web/app/page.tsx` | builds |
| 4 | Founder Console | `apps/web/app/agents/page.tsx` | exists |
| 5 | Sample offer | `<private_ops>/sales/sample_offer.md` | exists |
| 6 | Proposal template | `<private_ops>/sales/proposal_template.md` | exists |
| 7 | Sales script | `<private_ops>/sales/sales_script.md` | exists |
| 8 | Objection handling | `<private_ops>/sales/objections.md` | exists |
| 9 | Target sectors | `<private_ops>/launch/target_sector.yaml` | exists |
| 10 | Lead source list | `<private_ops>/sales/lead_sources.csv` | exists |
| 11 | Outreach drafts | `<private_ops>/distribution/queues.json` | parseable |
| 12 | Approval queue | `<private_ops>/distribution/approvals.csv` | exists |
| 13 | Suppression list | `<private_ops>/distribution/suppression.csv` | exists |
| 14 | Follow-up queue | `<private_ops>/distribution/followups.csv` | exists |
| 15 | Sample factory | `<private_ops>/factory/samples/` | not empty |
| 16 | Payment capture | env: `MOYASAR_*` configured | configured |
| 17 | Delivery checklist | `docs/launch/LAUNCH_ASSET_CHECKLIST.md` | this file |
| 18 | Proof rules | `docs/00_constitution/NON_NEGOTIABLES.md` | exists |
| 19 | Trust rules | `docs/risk/AI_AGENT_RISK_MODEL.md` | exists |
| 20 | Eval gate | `scripts/verify_prompt_output_quality.py` | green |
| 21 | Internal API token | env: `INTERNAL_ADMIN_KEY` | configured |
| 22 | CI green | `.github/workflows/dealix-execution-launch-layer.yml` | passes |
| 23 | Frontend build | `npm --prefix apps/web run build` | passes |

## قواعد القائمة — Rules

- لا حملة active إذا أي عنصر من 1–23 ينقص.
- العناصر تحت `<private_ops>/` تُختبر فقط إذا تم تمرير `PRIVATE_OPS=...` للأداة.
- أي عنصر يخص "إثبات" أو "نشر علني" يحتاج موافقة Trust gate.

## الملكية — Ownership

- Owner: Founder.
- Verifier: `scripts/verify_launch_readiness.py`.
- Review: قبل بدء كل حملة جديدة.
