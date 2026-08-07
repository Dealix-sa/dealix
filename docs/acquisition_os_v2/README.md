# Dealix Acquisition OS v2 — الفهرس الرئيسي / Master Index

نظام اكتساب عملاء **محكوم** (governed) لشركة Dealix السعودية. هذه الحزمة لا تكرّر محتوى المستودع — تكتب الجديد بالكامل، وتربط الموجود عبر روابط نسبية (قاعدة AGENTS.md: "avoid duplicating docs — link instead").

> **هذا الملف هو العمود الفقري.** ابدأ من [START_HERE_AR.md](START_HERE_AR.md) ثم ارجع لهذا الفهرس عند الحاجة.

## القواعد غير القابلة للمساومة (الـ 11) — مفروضة في كل ملف

1. **لا scraping إنتاجي.** مصادر الشركات = قنوات عامة/رسمية فقط ([SAUDI_DATA_SOURCE_CATALOG.md](../ops/SAUDI_DATA_SOURCE_CATALOG.md)). "استخراج أرقام الشركات" يُعاد تأطيره كـ **سورسينج محكوم من قنوات عامة** — لا حصاد أرقام شخصية عشوائية.
2. **لا أتمتة واتساب باردة.** واتساب = opt-in / حساب أعمال موثّق من Meta فقط ([WHATSAPP_META_VERIFICATION.md](../ops/WHATSAPP_META_VERIFICATION.md)).
3. **لا أتمتة LinkedIn.** Warm intros يدوية فقط — ليست خدمة أتمتة.
4. **لا إرسال جماعي (mass send).** كل رسالة مُخصّصة وبموافقة.
5. **كل قالب تواصل يشير إلى الموافقة + الانسحاب (opt-out).**
6. **لا ادعاءات بلا مصدر.**
7. **لا ضمان نتائج بيع.** نقول "تقديري" أو "نمط case-safe".
8. **لا PII في السجلّات.**
9. **لا إجراء خارجي بلا موافقة بشرية.**
10. **كل إحصائية طرف ثالث** (HubSpot/McKinsey…) تُوسَم كـ **ادعاء خارجي** باسم المصدر، لا كبيانات Dealix.
11. **PDPL أولاً** في كل خطوة.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

## خريطة الأقسام الـ 14

| # | القسم | ملفات هذه الحزمة | يبني على (موجود في المستودع) |
|---|-------|------------------|------------------------------|
| 00 | Command Center | [CEO_MASTER_OPERATING_SYSTEM_AR.md](00_COMMAND_CENTER/CEO_MASTER_OPERATING_SYSTEM_AR.md) | [board_decision_system/CEO_COMMAND_CENTER.md](../board_decision_system/CEO_COMMAND_CENTER.md) · [commercial/operations/CEO_90_DAY_OKR_AR.md](../commercial/operations/CEO_90_DAY_OKR_AR.md) · [ops/FOUNDER_OPERATING_SYSTEM_AR.md](../ops/FOUNDER_OPERATING_SYSTEM_AR.md) |
| 01 | Market Intelligence | [README.md](01_MARKET_INTELLIGENCE/README.md) (index) · [COMPANY_WEAKNESS_SIGNALS_AR.md](01_MARKET_INTELLIGENCE/COMPANY_WEAKNESS_SIGNALS_AR.md) | [commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md](../commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md) · [ops/SAUDI_DATA_SOURCE_CATALOG.md](../ops/SAUDI_DATA_SOURCE_CATALOG.md) |
| 02 | Daily Lead Engine | [DAILY_COMPANY_NUMBERS_SOP.md](02_DAILY_LEAD_ENGINE/DAILY_COMPANY_NUMBERS_SOP.md) · [LEAD_SCORING_MODEL_V2_AR.md](02_DAILY_LEAD_ENGINE/LEAD_SCORING_MODEL_V2_AR.md) · [DAILY_REPORT_TEMPLATE_AR.md](02_DAILY_LEAD_ENGINE/DAILY_REPORT_TEMPLATE_AR.md) | [ops/SAUDI_LEAD_MACHINE_AR.md](../ops/SAUDI_LEAD_MACHINE_AR.md) · [ops/LEAD_MACHINE_TOOLING.md](../ops/LEAD_MACHINE_TOOLING.md) · [ops/DAILY_COMMERCIAL_LOOP_AR.md](../ops/DAILY_COMMERCIAL_LOOP_AR.md) |
| 03 | Outreach System | [WHATSAPP_OUTREACH_PACK_AR.md](03_OUTREACH_SYSTEM/WHATSAPP_OUTREACH_PACK_AR.md) · [EMAIL_OUTREACH_PACK_AR.md](03_OUTREACH_SYSTEM/EMAIL_OUTREACH_PACK_AR.md) · [LINKEDIN_WARM_INTRO_AR.md](03_OUTREACH_SYSTEM/LINKEDIN_WARM_INTRO_AR.md) · [CALL_AND_VOICE_NOTES_AR.md](03_OUTREACH_SYSTEM/CALL_AND_VOICE_NOTES_AR.md) · [FOLLOWUP_14_DAY_CADENCE_AR.md](03_OUTREACH_SYSTEM/FOLLOWUP_14_DAY_CADENCE_AR.md) · [OPT_OUT_AND_CONSENT_MESSAGES_AR.md](03_OUTREACH_SYSTEM/OPT_OUT_AND_CONSENT_MESSAGES_AR.md) | [commercial/MARKET_INTELLIGENCE_EMAIL_TEMPLATES_AR.md](../commercial/MARKET_INTELLIGENCE_EMAIL_TEMPLATES_AR.md) · [ops/WHATSAPP_META_VERIFICATION.md](../ops/WHATSAPP_META_VERIFICATION.md) · [design-skills/dealix-linkedin-warm-intro-draft](../../design-skills/dealix-linkedin-warm-intro-draft/SKILL.md) |
| 04 | Sales Packages | [README.md](04_SALES_PACKAGES/README.md) (index) · [OFFERS_AND_PRICING_AR.md](04_SALES_PACKAGES/OFFERS_AND_PRICING_AR.md) · [MINI_AUDIT_ONE_PAGER_AR.md](04_SALES_PACKAGES/MINI_AUDIT_ONE_PAGER_AR.md) · [ROI_ASSUMPTIONS_AR.md](04_SALES_PACKAGES/ROI_ASSUMPTIONS_AR.md) | [commercial/DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) (مصدر حقيقة الأسعار) · [commercial/FOUNDER_SALES_PLAYBOOK_AR.md](../commercial/FOUNDER_SALES_PLAYBOOK_AR.md) |
| 05 | Marketer Enablement | [MARKETER_FIELD_MANUAL_AR.md](05_MARKETER_ENABLEMENT/MARKETER_FIELD_MANUAL_AR.md) · [DISCOVERY_CALL_GUIDE_AR.md](05_MARKETER_ENABLEMENT/DISCOVERY_CALL_GUIDE_AR.md) · [OBJECTION_HANDLING_AR.md](05_MARKETER_ENABLEMENT/OBJECTION_HANDLING_AR.md) · [ROLEPLAY_TRAINING_AR.md](05_MARKETER_ENABLEMENT/ROLEPLAY_TRAINING_AR.md) · [QUALITY_RUBRIC_AR.md](05_MARKETER_ENABLEMENT/QUALITY_RUBRIC_AR.md) | [commercial/sales/DEALIX_DISCOVERY_SCRIPT_AR.md](../commercial/sales/DEALIX_DISCOVERY_SCRIPT_AR.md) · [commercial/sales/DEALIX_OBJECTION_HANDLING_AR.md](../commercial/sales/DEALIX_OBJECTION_HANDLING_AR.md) |
| 06 | Client Explanation | [EXPLAIN_DEALIX_TO_CLIENT_AR.md](06_CLIENT_EXPLANATION/EXPLAIN_DEALIX_TO_CLIENT_AR.md) · [CLIENT_FAQ_AR.md](06_CLIENT_EXPLANATION/CLIENT_FAQ_AR.md) | [commercial/MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md](../commercial/MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md) |
| 07 | Closing & Delivery | [README.md](07_CLOSING_AND_DELIVERY/README.md) (index) · [SALES_TO_DELIVERY_HANDOFF_AR.md](07_CLOSING_AND_DELIVERY/SALES_TO_DELIVERY_HANDOFF_AR.md) · [ONBOARDING_SUCCESS_PLAN_AR.md](07_CLOSING_AND_DELIVERY/ONBOARDING_SUCCESS_PLAN_AR.md) | [design-skills/dealix-customer-onboarding-guide](../../design-skills/dealix-customer-onboarding-guide/SKILL.md) · [delivery_os/P1_DELIVERY_SOP_AR.md](../delivery_os/P1_DELIVERY_SOP_AR.md) |
| 08 | Compliance & Governance | [SAUDI_PDPL_AND_WHATSAPP_RULES_AR.md](08_COMPLIANCE_GOVERNANCE/SAUDI_PDPL_AND_WHATSAPP_RULES_AR.md) · [ANTI_SPAM_POLICY_AR.md](08_COMPLIANCE_GOVERNANCE/ANTI_SPAM_POLICY_AR.md) · [OPT_OUT_AND_CONSENT_MESSAGES_AR.md](08_COMPLIANCE_GOVERNANCE/OPT_OUT_AND_CONSENT_MESSAGES_AR.md) · [do_not_contact_schema.json](08_COMPLIANCE_GOVERNANCE/do_not_contact_schema.json) | [commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) · [commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md](../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md) |
| 09 | Repo Integration | [README.md](09_REPO_INTEGRATION/README.md) (spec/map فقط — لا كود) | [AGENTS.md](../../AGENTS.md) · [api/routers/commercial.py](../../api/routers/commercial.py) |
| 10 | Dashboards / CSV | [leads_template.csv](10_DASHBOARDS_CSV/leads_template.csv) · [daily_numbers_template.csv](10_DASHBOARDS_CSV/daily_numbers_template.csv) · [pipeline_template.csv](10_DASHBOARDS_CSV/pipeline_template.csv) · [do_not_contact_template.csv](10_DASHBOARDS_CSV/do_not_contact_template.csv) | [ops/FOUNDER_METRICS_DASHBOARD_SPEC_AR.md](../ops/FOUNDER_METRICS_DASHBOARD_SPEC_AR.md) |
| 11 | Prompt Library | [SEARCH_PROMPTS_AR.md](11_PROMPT_LIBRARY/SEARCH_PROMPTS_AR.md) · [OFFER_WRITING_PROMPTS_AR.md](11_PROMPT_LIBRARY/OFFER_WRITING_PROMPTS_AR.md) · [CALL_REVIEW_PROMPTS_AR.md](11_PROMPT_LIBRARY/CALL_REVIEW_PROMPTS_AR.md) | [ops/SAUDI_DATA_SOURCE_CATALOG.md](../ops/SAUDI_DATA_SOURCE_CATALOG.md) |
| 12 | Ready-to-Use Packs | [SECTOR_MESSAGES_AR.md](12_READY_TO_USE_PACKS/SECTOR_MESSAGES_AR.md) · [SHORT_PERSUASION_LINES_AR.md](12_READY_TO_USE_PACKS/SHORT_PERSUASION_LINES_AR.md) | [commercial/MARKET_INTELLIGENCE_SALES_CHAMPION_PACK_AR.md](../commercial/MARKET_INTELLIGENCE_SALES_CHAMPION_PACK_AR.md) |
| 13 | Automation Backlog | [GITHUB_ISSUES_BACKLOG.md](13_AUTOMATION_BACKLOG/GITHUB_ISSUES_BACKLOG.md) | [ops/LEAD_MACHINE_TOOLING.md](../ops/LEAD_MACHINE_TOOLING.md) |

## ملفات جديدة بالكامل مقابل فهارس/روابط

- **Net-new (محتوى تشغيلي كامل):** الأقسام 00, 02, 03, 05, 06, جزء 04, 08, 10, 11, 12, 13.
- **Index/link فقط (لا تكرار):** 01, 04 (README), 07 (README), 09.

## ماذا أعيد تأطيره ليطابق القواعد

- "استخراج أرقام الشركات" → **سورسينج محكوم من قنوات عامة** (لا أرقام شخصية).
- رسالة المؤسس الافتتاحية على واتساب → نسخة **opt-in + opt-out + قائمة على فجوة**.
- إحصائيات HubSpot/McKinsey → **ادعاءات خارجية موسومة بمصدرها**، لا بيانات Dealix.
- أسعار السبيك (Free/499/1,500/2,999…) → الأسعار المعتمدة في المستودع هي **مصدر الحقيقة** (انظر [04 OFFERS_AND_PRICING](04_SALES_PACKAGES/OFFERS_AND_PRICING_AR.md)).

---
**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
