# دليل تعبئة warm list (20 جهة)

1. انسخ من القالب إن لزم: `cp data/warm_list.csv.template data/warm_list.csv`
2. عبّئ **20 صفاً** — علاقة `warm` فقط (لا cold).
3. ولّد المسودات: `python3 scripts/warm_list_outreach.py`
4. خصّص 5 رسائل: [`data/warm_list_personalized_drafts.yaml`](../../data/warm_list_personalized_drafts.yaml)
5. تأهيل كل رد: `POST /api/v1/service-setup/qualify`
6. تتبع: [`CEO_TOP50_TRACKER.csv`](CEO_TOP50_TRACKER.csv) — SLA 24h
