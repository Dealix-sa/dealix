# Notion Founder Command Center — Setup & Activation
# مركز قيادة المؤسس في Notion — الإعداد والتفعيل

> القيمة التقديرية ليست قيمة مُتحقَّقة · Estimated value is not Verified value

## What this is · ما هذا

A live cockpit in Notion to run Dealix every morning, fed by the existing engines and
governed by the 11 non-negotiables. It is already built and populated with real data.

لوحة قيادة حيّة في Notion لإدارة Dealix كل صباح، مغذّاة من محرّكات النظام ومحكومة بالـ11 مبدأً
غير القابل للتفاوض. وهي مبنيّة ومعبّأة بالبيانات الحقيقية بالفعل.

**Command Center page · صفحة المركز:**
`https://www.notion.so/370f589461b9812aa234c24164201630`

## The 7 boards · اللوحات السبع

| Board · اللوحة | Database ID (for env) | Data source · مصدر البيانات |
|---|---|---|
| مهام اليوم · Today (Top 4) | `4fe0c1286b5a4e6cbeccac5e50c6eb92` | `dealix_founder_daily_brief.build_brief()` |
| خطة ٩٠ يوماً · 90-Day Plan | `27e0ebb59a5c4faab021c1c15741bf8c` | `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` + Article-13 gate |
| الإيرادات والمؤشرات · Revenue & KPIs | `3565997531f8416c8f4ae029c23cd422` | `value_os.value_ledger.summarize()` |
| سلّم العروض · Offers & Pricing | `2b95ef13df6349c2ac0c51c238450c61` | `service_catalog.registry.list_offerings()` |
| Proof & Capital · الإثبات والأصول | `e76ca36fa1aa43a49ef81ad15e6132c3` | `capital_os.capital_ledger.list_assets()` |
| العملاء المحتملون · Prospects (CRM) | `bc17bef08cfa41f8991561924bbc4069` | compliant discovery (search) + `sales_os.icp_score` |
| مسودّات التواصل · Outreach Drafts | `5dc8c3b3bc0c4e04949840d26b0441b8` | draft builder (always `draft_only`) |

Each board carries a hidden `external_id` (idempotency key) and a `Source` column.
Sample rows are labelled `SAMPLE` (Doctrine #4 — no un-sourced claims).

## One-time setup to activate auto-sync · تفعيل المزامنة التلقائية (مرّة واحدة)

The boards above are live now. To make them **refresh automatically every morning**:

1. Create a Notion internal integration → copy the token (`secret_…` or `ntn_…`):
   `https://www.notion.so/my-integrations`
2. **Share the Command Center page with the integration** (top-right `•••` → Connections →
   your integration). Child boards inherit access. — هذه أكثر خطوة يُنسى تنفيذها.
3. Put the token and the 7 database IDs into `.env` (local) and as **GitHub Actions secrets**:
   ```
   NOTION_API_KEY=secret_xxx
   NOTION_DAILY_OPS_DB_ID=4fe0c1286b5a4e6cbeccac5e50c6eb92
   NOTION_PLAN_DB_ID=27e0ebb59a5c4faab021c1c15741bf8c
   NOTION_KPI_DB_ID=3565997531f8416c8f4ae029c23cd422
   NOTION_OFFERS_DB_ID=2b95ef13df6349c2ac0c51c238450c61
   NOTION_PROOF_DB_ID=e76ca36fa1aa43a49ef81ad15e6132c3
   NOTION_CRM_DB_ID=bc17bef08cfa41f8991561924bbc4069
   NOTION_OUTREACH_DB_ID=5dc8c3b3bc0c4e04949840d26b0441b8
   ```
4. Verify and run once:
   ```bash
   make env-check
   NOTION_MOCK_MODE=true python scripts/sync_founder_command_center_to_notion.py --dry-run --json
   make notion-sync          # live, once NOTION_API_KEY is set
   ```

After that, the sync runs daily via `.github/workflows/founder_notion_sync.yml`
(05:00 UTC = 08:00 Riyadh) and as an optional step inside
`scripts/run_founder_full_autopilot.py`.

## Activate compliant prospect discovery · تفعيل الاكتشاف المتوافق

The CRM fills with **real** Saudi prospects via search (never scraping — Doctrine #1).
Add at least one search key to `.env` / secrets, then the CRM populates on the next sync:

```
GOOGLE_SEARCH_API_KEY=  + GOOGLE_SEARCH_CX=     # primary
TAVILY_API_KEY=                                  # fallback
SERPAPI_API_KEY=  /  GOOGLE_MAPS_API_KEY=        # local discovery
```

Until a key is present, the CRM shows the structure with `SAMPLE`-labelled rows.

## Governance · الحوكمة

- Outreach rows are always written `draft_only — awaiting approval`, `Approved = false`.
  The sync is **write-only** to Notion and never sends. لا إرسال خارجي بلا موافقتك (المبدأ #8).
- All text is PII-redacted before any write (Doctrine #6).
- KPI values carry a value-ledger `tier` (estimated/observed/verified/client_confirmed);
  estimates are visibly not guarantees (Doctrine #5).
