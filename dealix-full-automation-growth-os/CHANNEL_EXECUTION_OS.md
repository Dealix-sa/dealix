# Dealix Channel Execution OS

الخريطة الكاملة لكل قناة وأقصى ما يمكن أتمتته بشكل آمن.

## Channel Brain

لكل شركة تدخل النظام:

```
Company found → Enriched → Sector detected → Language detected
→ Buyer mapped → Offer selected → Channel risk checked
→ Channel pack generated → Execution mode selected
→ Send / queue / approve / skip
→ Reply captured → Learning updated
```

## Email OS

**الوضع:** controlled_auto
**الحد:** 50-150 رسالة/inbox/يوم (7 inboxes)
**الشروط:** SPF + DKIM + DMARC + suppression + opt-out + personalization >= 85

## WhatsApp Business OS

**الوضع:** full_auto_after_opt_in
**الشروط:** opt-in موثّق + approved templates + STOP keywords handler
**النافذة الحرة:** 24 ساعة بعد رد المستخدم

## Instagram / Messenger OS

**الوضع:** full_auto_for_inbound
**API:** Official Meta Messaging API فقط
**النافذة:** 24 ساعة من آخر رسالة مستخدم

## TikTok OS

**الوضع:** full_auto_for_leads
**الأدوات:** Instant Forms + Messaging Ads + Message Assistant

## LinkedIn OS

**الوضع:** draft_only — لا أتمتة خارجية أبداً
**المسموح:** Lead Gen Forms، Founder content، Manual Tier A outreach
**الممنوع:** auto-DM، auto-connect، scraping، bulk messages

## X/Twitter OS

**الوضع:** official_api_only
**المسموح:** scheduled posts، reply to mentions، DM after permission

## Telegram OS

**الوضع:** opt_in_bot
**الأدوات:** Bot API، community channel

## Paid Ads OS

**الوضع:** full_auto
**Lead to CRM to response:** 100% automated
**Channels:** Google + Meta + LinkedIn + TikTok + Retargeting

## Calls OS

**الوضع:** script_and_queue
**الأتمتة:** التحضير فقط — الإنسان يتصل
**الهدف:** 20-50 مكالمة/يوم

## Partner OS

**الوضع:** controlled_auto (email) + draft_only (LinkedIn)
**الهدف:** 50 partner/يوم بحثاً، 20 جاهز للمؤسس

## Content / Brand OS

**الوضع:** draft + scheduled publishing
**الهدف اليومي:** 3 عربي + 1 إنجليزي + 10 تعليق + 1 فيديو
