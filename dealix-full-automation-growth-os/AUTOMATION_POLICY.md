# Dealix Automation Policy

## المبدأ الجوهري

أقصى أتمتة ممكنة بدون حرق الحسابات أو البراند.
كل قرار تنفيذ يمر بـ Policy Gate قبل الإرسال.

## Execution Modes

| الوضع | يُستخدم عندما |
|-------|--------------|
| full_auto | inbound leads، opt-in channels، official APIs |
| controlled_auto | cold email B2B، warm leads، partner outreach |
| founder_approval | Tier A، legal/finance/health/gov، proposals، pricing |
| draft_only | LinkedIn outbound، website forms، communities |
| blocked | spam، fake identity، limit circumvention، captcha bypass |

## Policy Gate — شروط الحجب الإجباري

يُحجب التنفيذ تلقائياً إذا:
- Contact موجود في suppression list
- رسالة مكررة أُرسلت خلال آخر 30 يوم
- Email بدون unsubscribe link
- WhatsApp بدون opt-in موثّق
- LinkedIn auto-DM أو auto-connect
- X unsolicited DM
- Sector حساس (legal/health/gov) بدون موافقة المؤسس
- تجاوز الحصة اليومية
- Spam score مرتفع

## Risk Levels

| Level | نوع التنفيذ |
|-------|------------|
| Level 1 — Safe Full Auto | Inbound، opt-in، ad leads، webinar registrants |
| Level 2 — Controlled Auto | Cold email، follow-ups، partner outreach، retargeting |
| Level 3 — Assisted Manual | LinkedIn، website forms، high-ticket، gov |
| Level 4 — Never Automate | LinkedIn auto-DM، cold WhatsApp blast، CAPTCHA bypass، fake accounts |

## Inbox Strategy

كل inbox له دور محدد — ليس للالتفاف على القيود بل للفصل المنطقي:

| البريد | الغرض |
|--------|--------|
| sami@dealix.ai | Tier A founder-led |
| hello@dealix.ai | General inbound |
| gcc@dealix.ai | International GCC |
| legal@dealix.ai | Legal/professional services |
| ops@dealix.ai | Maintenance/FM/contracting |
| partners@dealix.ai | Partnerships/referrals |
| events@dealix.ai | Webinars/workshops |
