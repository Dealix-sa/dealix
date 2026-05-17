# Commercial Operations — حزمة التنفيذ

مرتبطة بـ [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../MASTER_COMMERCIAL_OPERATING_PLAN_AR.md).

| ملف | الغرض |
|-----|--------|
| [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](EVIDENCE_EVENTS_CLOSE_PATH_AR.md) | مسار lead→proof + أحداث أدلة |
| [evidence_events_tracker.csv](evidence_events_tracker.csv) | تتبع يومي (انسخ صفوفاً) |
| [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](FIRST_PAID_DIAGNOSTIC_DOD_AR.md) | DoD أول إيراد مدفوع |
| [motion_a_agency/](motion_a_agency/) | قوالب Motion A (نطاق، Proof، توسع) |
| [PARTNER_ONBOARDING_KIT_AR.md](PARTNER_ONBOARDING_KIT_AR.md) | حزمة شراكة |
| [AEO_CONTENT_CALENDAR_AR.md](AEO_CONTENT_CALENDAR_AR.md) | جدول صفحات إجابة |
| [objection_engine_registry.yaml](objection_engine_registry.yaml) | اعتراض → أصل |
| [COMMERCIAL_WEEKLY_SCORECARD_AR.md](COMMERCIAL_WEEKLY_SCORECARD_AR.md) | Pilots + Proof أسبوعياً |
| [COMMERCIAL_GOVERNANCE_GATES_AR.md](COMMERCIAL_GOVERNANCE_GATES_AR.md) | بوابات امتثال وقنوات |
| [sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md](sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md) | عيّنة Proof للوكالات |
| [FOUNDER_GTM_BENCHMARKS_AR.md](FOUNDER_GTM_BENCHMARKS_AR.md) | مقارنة GTM خارجية |
| `drafts/` (gitignored) | مخرجات `generate_commercial_content_pack.py` |
| [targeting/agency_accounts_seed.csv](targeting/agency_accounts_seed.csv) | قائمة أهداف Motion A (وكالات) |
| [targeting/gtm_revenue_machine_import.json](targeting/gtm_revenue_machine_import.json) | بذرة Data OS لـ revenue-machine |
| [GATED_AUTO_SEND_RFC_AR.md](GATED_AUTO_SEND_RFC_AR.md) | استكشاع إرسال تلقائي (معطّل افتراضياً) |
| [aeo_drafts/](aeo_drafts/) | مسودات صفحات AEO (نشر لاحقاً) |

**سكربتات:** `run_founder_commercial_day.sh` (canonical) · `run_founder_revenue_day.sh` (wrapper + Business NOW) · `verify_dealix_commercial_go_live.sh` · `commercial_war_room_sync.py` (P0 + outreach drafts) · `rotate_agency_targets.py` · `queue_content_drafts_for_approval.py`

**محتوى / سوشال — أي سكربت؟**

| سكربت | متى | مخرج |
|--------|-----|------|
| `social_queue_today.py` | يومي (ضمن revenue/commercial day) | منشور LinkedIn اليوم |
| `generate_commercial_content_pack.py` | جمعة (`founder_content_weekly.yml`) | `operations/drafts/` |
| `generate_weekly_content_drafts.py` | عند الحاجة | `var/content_drafts/YYYY-Www.json` |

**GitHub Actions secrets (إنتاج):**

| Secret | مطلوب لـ |
|--------|---------|
| `DEALIX_API_BASE` | [daily-revenue-machine.yml](../../.github/workflows/daily-revenue-machine.yml) |
| `DEALIX_API_KEY` | revenue-machine/run |
| `DEALIX_ADMIN_API_KEY` | evidence sync (اختياري) |
| `DEALIX_SYNC_EVIDENCE` | `1` لمزامنة CSV |

**محلي:** `bash scripts/run_founder_commercial_day.sh` → `data/founder_briefs/DAILY_PACK_YYYY-MM-DD.md`
