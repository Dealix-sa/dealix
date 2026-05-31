# Dealix Full-Automation Growth OS

نظام يعمل 24/7 على كل القنوات ويقرر لكل قناة هل التنفيذ يكون Full Auto، Controlled Auto، Founder Approval، أو Blocked.

## المبدأ الأساسي

النظام لا يسأل: "هل هذه القناة ممكنة؟"
يسأل: **كيف أستخرج أعلى قيمة من القناة بدون ما أحرق الحساب أو الدومين أو البراند؟**

## Master Workflow

```
01_market_scan → 02_enrich_companies → 03_score_fit → 04_detect_language
→ 05_map_buyer → 06_route_offer → 07_route_channel → 08_generate_assets
→ 09_quality_gate → 10_risk_gate → 11_create_channel_jobs
→ 12_execute_allowed_jobs → 13_hold_risky_jobs → 14_capture_replies
→ 15_classify_replies → 16_book_meetings → 17_generate_proposals
→ 18_learn_and_update
```

## القنوات والأتمتة

| القناة | أقصى أتمتة | وضع التنفيذ |
|--------|------------|-------------|
| Email | عالية | controlled_auto |
| WhatsApp Business | عالية جداً (opt-in) | full_auto_after_opt_in |
| Instagram DM | عالية (inbound) | full_auto_for_inbound |
| Messenger | عالية (inbound) | full_auto_for_inbound |
| TikTok Leads | عالية | full_auto_for_leads |
| Google/Meta/LinkedIn Lead Forms | عالية | full_auto |
| LinkedIn Outbound | منخفضة | draft_only |
| X/Twitter | متوسطة | official_api_only |
| Telegram | متوسطة | opt_in_bot |
| Website Forms | متوسطة | assisted_manual |
| Calls | متوسطة | script_and_queue |
| Partners/Referrals | عالية في التحضير | controlled_auto |
| Retargeting Ads | عالية | full_auto |

## الطاقة اليومية المستهدفة

- 2,000–5,000 شركة تُمسح
- 300–500 brief مُعمّق
- 1,500–3,000 asset مولّد
- 100–500 رسالة controlled-auto
- 100% inbound auto-response
- 100% lead form auto-routing

## هيكل الملفات

```
config/          — إعدادات القنوات والمخاطر والحصص
memory/          — سجلات الشركات والعملاء والوظائف
agents/          — system prompts لكل agent
prompts/         — قوالب الرسائل لكل قناة
outputs/         — الأصول المولّدة وقوائم التنفيذ
```

## التشغيل

راجع `AUTOMATION_POLICY.md` لفهم قواعد التشغيل الكاملة.
راجع `ANTI_BAN_RULES.md` لفهم حماية الحسابات.
راجع `CHANNEL_EXECUTION_OS.md` للخريطة الكاملة للقنوات.
