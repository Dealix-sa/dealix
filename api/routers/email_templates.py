"""
Saudi B2B email template library for Dealix sales outreach.

All templates are for human review and manual sending ONLY.
No automation, no cold outreach, no LinkedIn automation, no scraping.

Prefix: /api/v1/email-templates
Tags: Sales
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/email-templates", tags=["Sales"])

# ---------------------------------------------------------------------------
# Template data
# ---------------------------------------------------------------------------

_EMAIL_TEMPLATES: list[dict[str, Any]] = [
    {
        "template_id": "warm_intro",
        "name_en": "Warm Introduction",
        "name_ar": "مقدمة دافئة",
        "use_case_en": "First touch after a referral or mutual introduction. Use only when you have a named referrer.",
        "timing_guidance_en": (
            "Tuesday through Thursday, 9–11am KSA time. "
            "Never during Ramadan weeks 1–2. Avoid the day after a public holiday."
        ),
        "subject_line_en": "Introduction from [REFERRER_NAME] — [COMPANY_NAME]",
        "subject_line_ar": "مقدمة من [REFERRER_NAME] — [COMPANY_NAME]",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "[REFERRER_NAME] suggested I reach out to you directly. "
            "I am [SENDER_NAME] at Dealix — we work with Saudi B2B companies to surface revenue "
            "intelligence their current systems are missing.\n\n"
            "[REFERRER_NAME] mentioned that [COMPANY_NAME] is navigating [CONTEXT_NOTE]. "
            "I believe there may be a relevant fit worth a brief conversation.\n\n"
            "Would a 20-minute call this week or next work for you? "
            "I am happy to work around your schedule.\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "اقترح [REFERRER_NAME] أن أتواصل معك مباشرة. "
            "أنا [SENDER_NAME] في ديليكس — نعمل مع شركات B2B السعودية للكشف عن ذكاء الإيرادات "
            "الذي تفتقده أنظمتها الحالية.\n\n"
            "ذكر [REFERRER_NAME] أن [COMPANY_NAME] تتعامل مع [CONTEXT_NOTE]. "
            "أعتقد أن هناك توافقاً محتملاً يستحق محادثة قصيرة.\n\n"
            "هل تناسبك مكالمة لمدة 20 دقيقة هذا الأسبوع أو الأسبوع القادم؟ "
            "يسعدني التكيف مع جدولك.\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Do not mention pricing. Do not attach anything. "
            "Do not use the word 'guaranteed'. Never use cold outreach language."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
    {
        "template_id": "post_event_leap",
        "name_en": "Post-LEAP Conference Follow-Up",
        "name_ar": "متابعة ما بعد مؤتمر LEAP",
        "use_case_en": (
            "Follow-up within 72 hours of meeting at LEAP or another major Saudi tech event. "
            "Only use when you had a real in-person conversation."
        ),
        "timing_guidance_en": (
            "Send within 48–72 hours of the event while the memory is fresh. "
            "Sunday or Monday morning KSA time is best. Avoid Friday."
        ),
        "subject_line_en": "Great to meet you at LEAP — [COMPANY_NAME]",
        "subject_line_ar": "سعيد بلقائك في LEAP — [COMPANY_NAME]",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "It was genuinely good to meet you at LEAP. "
            "Your perspective on [CONTEXT_NOTE] stayed with me.\n\n"
            "As I mentioned, Dealix helps Saudi B2B companies like [COMPANY_NAME] "
            "turn operational data into verified revenue decisions — with a built-in "
            "ZATCA and PDPL governance layer.\n\n"
            "I would like to follow through on our conversation. "
            "Would you be open to a 30-minute session this week — "
            "no slides, just a structured conversation around your priorities?\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "كان من دواعي سروري حقاً مقابلتك في LEAP. "
            "وجهة نظرك في [CONTEXT_NOTE] بقيت معي.\n\n"
            "كما ذكرت، تساعد ديليكس شركات B2B السعودية مثل [COMPANY_NAME] "
            "على تحويل البيانات التشغيلية إلى قرارات إيرادات موثقة — مع طبقة "
            "حوكمة مدمجة لزاتكا و PDPL.\n\n"
            "أود المتابعة على محادثتنا. "
            "هل أنت منفتح على جلسة مدتها 30 دقيقة هذا الأسبوع — "
            "بدون شرائح، فقط محادثة منظمة حول أولوياتك؟\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Do not attach a proposal. Do not mention price. "
            "Avoid generic conference follow-up language — reference the actual conversation."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
    {
        "template_id": "free_diagnostic_offer",
        "name_en": "Free Diagnostic Offer",
        "name_ar": "عرض التشخيص المجاني",
        "use_case_en": (
            "Offer the no-obligation 7-day Revenue Diagnostic after initial qualification. "
            "Use only when the prospect has shown genuine interest."
        ),
        "timing_guidance_en": (
            "Send Tuesday through Thursday, 10am–12pm KSA time. "
            "Do not send if you have not spoken to the prospect at least once. "
            "Avoid the last two days before Eid."
        ),
        "subject_line_en": "Your complimentary Revenue Diagnostic — [COMPANY_NAME]",
        "subject_line_ar": "تشخيص الإيرادات المجاني لك — [COMPANY_NAME]",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "Following our conversation, I would like to offer [COMPANY_NAME] "
            "a complimentary 7-day Revenue Diagnostic — no obligation, no contract required.\n\n"
            "What the diagnostic covers:\n"
            "- Top 3 revenue or efficiency gaps in your current operations\n"
            "- ZATCA Phase 2 readiness check\n"
            "- PDPL data exposure summary\n"
            "- A prioritized action list you keep regardless of next steps\n\n"
            "The session takes approximately 60 minutes of your time. "
            "Everything is documented and bilingual.\n\n"
            "Would this Thursday or the following Monday work for you?\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "بعد محادثتنا، أود أن أعرض على [COMPANY_NAME] "
            "تشخيصاً مجانياً للإيرادات لمدة 7 أيام — بدون أي التزام أو عقد.\n\n"
            "ما يغطيه التشخيص:\n"
            "- أفضل 3 ثغرات في الإيرادات أو الكفاءة في عملياتك الحالية\n"
            "- فحص جاهزية زاتكا المرحلة الثانية\n"
            "- ملخص تعرض بيانات PDPL\n"
            "- قائمة أولويات عمل تحتفظ بها بصرف النظر عن الخطوات التالية\n\n"
            "تستغرق الجلسة حوالي 60 دقيقة من وقتك. "
            "كل شيء موثق وثنائي اللغة.\n\n"
            "هل يناسبك يوم الخميس القادم أو الاثنين التالي؟\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Do not use 'free' and 'guaranteed' in the same message. "
            "Do not imply the diagnostic will automatically lead to a paid engagement. "
            "Never cold-send this template."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
    {
        "template_id": "proposal_send",
        "name_en": "Proposal Send",
        "name_ar": "إرسال العرض التجاري",
        "use_case_en": (
            "Send the tailored proposal after founder review and approval. "
            "Only use after completing the closing checklist."
        ),
        "timing_guidance_en": (
            "Send Tuesday or Wednesday, 9–11am KSA time. "
            "Never send a proposal on Thursday — too close to the weekend. "
            "Allow at least 48 hours before following up."
        ),
        "subject_line_en": "Your Dealix Revenue Intelligence Proposal — [COMPANY_NAME]",
        "subject_line_ar": "عرض ديليكس لذكاء الإيرادات — [COMPANY_NAME]",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "Attached is your tailored Revenue Intelligence proposal for [COMPANY_NAME]. "
            "It is based entirely on what we discussed — the gaps you identified and "
            "the outcomes that matter most to your business.\n\n"
            "Key points inside:\n"
            "- Proposed scope aligned to your top 3 priorities\n"
            "- Implementation timeline with Saudi calendar considerations\n"
            "- Investment and payment terms in SAR\n"
            "- ZATCA/PDPL coverage included\n\n"
            "I am available for any questions before you review with your team. "
            "I suggest we plan a 30-minute review call for [CONTEXT_NOTE].\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "مرفق عرض ذكاء الإيرادات المصمم خصيصاً لـ [COMPANY_NAME]. "
            "إنه مبني بالكامل على ما ناقشناه — الثغرات التي حددتها "
            "والنتائج الأكثر أهمية لأعمالك.\n\n"
            "النقاط الرئيسية بداخله:\n"
            "- النطاق المقترح المتوافق مع أفضل 3 أولويات لديك\n"
            "- الجدول الزمني للتنفيذ مع اعتبارات التقويم السعودي\n"
            "- الاستثمار وشروط الدفع بالريال السعودي\n"
            "- تغطية زاتكا/PDPL مشمولة\n\n"
            "أنا متاح لأي أسئلة قبل مراجعتك مع فريقك. "
            "أقترح أن نخطط لمكالمة مراجعة لمدة 30 دقيقة في [CONTEXT_NOTE].\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Never send without founder sign-off. "
            "Do not include ROI guarantees or projected outcome percentages "
            "unless backed by a completed diagnostic. "
            "Do not send to more than one contact without consent."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
    {
        "template_id": "post_meeting_follow_up",
        "name_en": "Post-Meeting Follow-Up",
        "name_ar": "متابعة ما بعد الاجتماع",
        "use_case_en": (
            "Send after a discovery call or any substantive meeting. "
            "Recap key takeaways and confirm next steps while the conversation is fresh."
        ),
        "timing_guidance_en": (
            "Send within 2–4 hours of the meeting ending. "
            "If the meeting ends after 4pm KSA, send first thing the following morning. "
            "Do not send on Friday."
        ),
        "subject_line_en": "Meeting recap — [COMPANY_NAME] / Dealix",
        "subject_line_ar": "ملخص الاجتماع — [COMPANY_NAME] / ديليكس",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "Thank you for your time today. I found our conversation genuinely valuable.\n\n"
            "Key takeaways from my side:\n"
            "1. [CONTEXT_NOTE]\n"
            "2. The priority areas you identified\n"
            "3. The timeline constraints we discussed\n\n"
            "Agreed next steps:\n"
            "- [COMPANY_NAME]: [action and owner]\n"
            "- Dealix ([SENDER_NAME]): [action and deadline]\n\n"
            "Please let me know if I have missed anything or misrepresented any point — "
            "I want to make sure we are fully aligned before the next step.\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "شكراً لوقتك اليوم. وجدت محادثتنا قيّمة حقاً.\n\n"
            "النقاط الرئيسية من جانبي:\n"
            "1. [CONTEXT_NOTE]\n"
            "2. مجالات الأولوية التي حددتها\n"
            "3. قيود الجدول الزمني التي ناقشناها\n\n"
            "الخطوات التالية المتفق عليها:\n"
            "- [COMPANY_NAME]: [الإجراء والمسؤول]\n"
            "- ديليكس ([SENDER_NAME]): [الإجراء والموعد النهائي]\n\n"
            "يرجى إعلامي إذا فاتني أي شيء أو أسأت تمثيل أي نقطة — "
            "أريد التأكد من أننا متوافقان تماماً قبل الخطوة التالية.\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Do not include a sales pitch in the recap. "
            "Do not speculate about outcomes not discussed in the meeting. "
            "Keep it factual and aligned to what was actually said."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
    {
        "template_id": "post_eid_reengagement",
        "name_en": "Post-Eid Re-engagement",
        "name_ar": "إعادة التواصل بعد العيد",
        "use_case_en": (
            "Re-engage a warm prospect who went quiet during the Eid period. "
            "Send 3–5 days after Eid Al-Fitr or Eid Al-Adha."
        ),
        "timing_guidance_en": (
            "Send Tuesday through Thursday, 9–11am KSA time. "
            "Wait at least 3 full working days after Eid before sending. "
            "Do not send on the first working day back — executives are catching up on backlog."
        ),
        "subject_line_en": "Eid greetings — following up from [SENDER_NAME], Dealix",
        "subject_line_ar": "تهنئة العيد — متابعة من [SENDER_NAME]، ديليكس",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "Eid Mubarak! I hope you and your family had a wonderful celebration "
            "and a restful break.\n\n"
            "As business gets back to full pace, I wanted to check in on "
            "[CONTEXT_NOTE] that we discussed before the holiday.\n\n"
            "If the timing is right to pick this up, I am available for a brief call "
            "this week or next — entirely at your convenience.\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "عيد مبارك! آمل أن يكون قد مرّ عليك وعلى عائلتك احتفالٌ رائع "
            "وراحةٌ مستحقة.\n\n"
            "مع عودة الأعمال إلى وتيرتها الكاملة، أردت التحقق من "
            "[CONTEXT_NOTE] الذي ناقشناه قبل العطلة.\n\n"
            "إذا كان التوقيت مناسباً لاستكمال هذا الأمر، أنا متاح لمكالمة قصيرة "
            "هذا الأسبوع أو الأسبوع القادم — في الوقت الذي يناسبك تماماً.\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Do not lead with a sales pitch — the greeting must feel genuine. "
            "Do not reference pricing or deadlines in this email. "
            "Avoid sending before 3 working days post-Eid."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
    {
        "template_id": "sprint_upsell",
        "name_en": "Sprint Delivery Upsell to Managed Ops",
        "name_ar": "ترقية ما بعد Sprint إلى العمليات المُدارة",
        "use_case_en": (
            "Send after Sprint delivery, when the Proof Pack has been reviewed and "
            "the client has seen verified results. Upsell path to Managed Ops retainer."
        ),
        "timing_guidance_en": (
            "Send within 48 hours of the Sprint Proof Pack review meeting. "
            "Tuesday or Wednesday preferred. Do not send if the client expressed reservations — "
            "resolve those first."
        ),
        "subject_line_en": "Your Sprint results + what comes next — [COMPANY_NAME]",
        "subject_line_ar": "نتائج Sprint الخاصة بك وما يأتي بعد ذلك — [COMPANY_NAME]",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "It was a productive Sprint. As documented in the Proof Pack you reviewed, "
            "[COMPANY_NAME] achieved [CONTEXT_NOTE] over the engagement period.\n\n"
            "The natural next step — if you want to sustain and compound these results — "
            "is the Dealix Managed Ops retainer. Here is what that looks like:\n\n"
            "- A dedicated AI operator (10 hours per month)\n"
            "- Monthly revenue intelligence dashboard\n"
            "- Ongoing ZATCA compliance monitoring\n"
            "- Quarterly business review with Proof Pack\n\n"
            "I am proposing this because the data from your Sprint shows a clear "
            "continuation case — not as a default upsell.\n\n"
            "Would you like to review the Managed Ops terms this week?\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "كان Sprint منتجاً. كما هو موثق في حزمة الإثبات التي راجعتها، "
            "حققت [COMPANY_NAME] [CONTEXT_NOTE] خلال فترة المشاركة.\n\n"
            "الخطوة التالية المنطقية — إذا كنت تريد الحفاظ على هذه النتائج ومضاعفتها — "
            "هي عقد العمليات المُدارة من ديليكس. إليك كيف يبدو ذلك:\n\n"
            "- مشغّل ذكاء اصطناعي مخصص (10 ساعات في الشهر)\n"
            "- لوحة تحكم ذكاء الإيرادات الشهرية\n"
            "- مراقبة مستمرة للامتثال لزاتكا\n"
            "- مراجعة أعمال ربع سنوية مع حزمة إثبات\n\n"
            "أقترح هذا لأن البيانات من Sprint الخاص بك تُظهر حالة استمرار واضحة — "
            "ليس كترقية افتراضية.\n\n"
            "هل تريد مراجعة شروط العمليات المُدارة هذا الأسبوع؟\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Never imply guaranteed future results beyond what the Proof Pack documented. "
            "Do not use pressure language. "
            "Only send after a completed Proof Pack review — never speculatively."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
    {
        "template_id": "renewal_reminder",
        "name_en": "Renewal Reminder (60 Days)",
        "name_ar": "تذكير التجديد (60 يوماً)",
        "use_case_en": (
            "Notify the client of an upcoming engagement renewal 60 days in advance. "
            "Use to open the renewal conversation with time to negotiate if needed."
        ),
        "timing_guidance_en": (
            "Send exactly 60 days before the renewal date. "
            "Tuesday through Thursday, 9–11am KSA time. "
            "Avoid sending during Ramadan or immediately before a public holiday."
        ),
        "subject_line_en": "Your Dealix engagement renews in 60 days — [COMPANY_NAME]",
        "subject_line_ar": "تجديد مشاركتك مع ديليكس خلال 60 يوماً — [COMPANY_NAME]",
        "body_en": (
            "Dear [CLIENT_NAME],\n\n"
            "Your Dealix engagement with [COMPANY_NAME] is scheduled to renew in 60 days "
            "on [CONTEXT_NOTE].\n\n"
            "I wanted to reach out well in advance so that we have time to:\n"
            "1. Review the value delivered over the past period\n"
            "2. Align on the scope and any adjustments for the next term\n"
            "3. Ensure there are no procurement or approval bottlenecks on your side\n\n"
            "I will send a renewal proposal shortly. In the meantime, "
            "please let me know if there are any priorities or changes on your end.\n\n"
            "Best regards,\n[SENDER_NAME]"
        ),
        "body_ar": (
            "عزيزي [CLIENT_NAME]،\n\n"
            "مشاركتك مع ديليكس لـ [COMPANY_NAME] مقررة للتجديد خلال 60 يوماً "
            "في [CONTEXT_NOTE].\n\n"
            "أردت التواصل مسبقاً حتى يكون لدينا وقت كافٍ لـ:\n"
            "1. مراجعة القيمة المقدمة خلال الفترة الماضية\n"
            "2. التوافق على النطاق وأي تعديلات للفترة القادمة\n"
            "3. التأكد من عدم وجود أي عوائق في المشتريات أو الموافقات من جانبكم\n\n"
            "سأرسل مقترح التجديد قريباً. في هذه الأثناء، "
            "يرجى إعلامي بأي أولويات أو تغييرات من جانبكم.\n\n"
            "مع أطيب التحيات،\n[SENDER_NAME]"
        ),
        "avoid_en": (
            "Do not assume automatic renewal — always confirm intent explicitly. "
            "Do not include pricing in this first renewal touchpoint. "
            "Never send this template as a cold or first-touch email."
        ),
        "governance_note_en": "Human review and manual send required — no automation permitted.",
    },
]

# ---------------------------------------------------------------------------
# Cultural rules
# ---------------------------------------------------------------------------

_SAUDI_EMAIL_RULES: list[dict[str, Any]] = [
    {
        "rule_id": "SAR-001",
        "rule_en": "Always greet with the appropriate title (Dr., Eng., Sheikh) if known. "
                   "Using the wrong or absent title signals a lack of preparation.",
        "rule_ar": "ابدأ دائماً باللقب المناسب (د., م., الشيخ) إذا كان معروفاً. "
                   "استخدام لقب خاطئ أو غيابه يُشير إلى نقص في التحضير.",
    },
    {
        "rule_id": "SAR-002",
        "rule_en": "If the client communicates in Arabic, write the entire email in Arabic first. "
                   "An English version may be appended, but Arabic must lead.",
        "rule_ar": "إذا تواصل العميل بالعربية، اكتب البريد الإلكتروني بالكامل بالعربية أولاً. "
                   "يمكن إلحاق نسخة إنجليزية، لكن يجب أن تتصدر العربية.",
    },
    {
        "rule_id": "SAR-003",
        "rule_en": "Never send on Friday. Friday is Jumu'ah — a sacred day of rest and prayer. "
                   "Emails sent on Friday are often not opened until Sunday, losing urgency.",
        "rule_ar": "لا ترسل يوم الجمعة أبداً. الجمعة هي يوم الجمعة — يوم مقدس للراحة والصلاة. "
                   "الرسائل المُرسلة يوم الجمعة كثيراً ما لا تُفتح حتى الأحد، مما يُفقدها إلحاحها.",
    },
    {
        "rule_id": "SAR-004",
        "rule_en": "Reduce email cadence during Ramadan to a maximum of one email per week. "
                   "Avoid weeks 1 and 2 entirely for new outreach. "
                   "Business decisions slow significantly during fasting hours.",
        "rule_ar": "قلّل تواتر الرسائل خلال رمضان إلى حد أقصى رسالة واحدة في الأسبوع. "
                   "تجنب الأسبوعين الأول والثاني تماماً للتواصل الجديد. "
                   "تتباطأ قرارات الأعمال بشكل ملحوظ خلال ساعات الصيام.",
    },
    {
        "rule_id": "SAR-005",
        "rule_en": "Keep subject lines short — 6 to 8 words maximum. "
                   "Saudi executives predominantly read email on mobile devices. "
                   "Long subject lines are truncated and lose impact.",
        "rule_ar": "اجعل سطور الموضوع قصيرة — 6 إلى 8 كلمات كحد أقصى. "
                   "يقرأ المسؤولون السعوديون البريد الإلكتروني بشكل رئيسي على الأجهزة المحمولة. "
                   "سطور الموضوع الطويلة تُقطع وتفقد تأثيرها.",
    },
    {
        "rule_id": "SAR-006",
        "rule_en": "Never discuss price in a cold or warm introductory email. "
                   "Earn the meeting first. Pricing introduced too early signals low value "
                   "and damages the relationship before it begins.",
        "rule_ar": "لا تناقش السعر أبداً في رسالة بريد تمهيدية باردة أو دافئة. "
                   "اكسب الاجتماع أولاً. تقديم التسعير مبكراً يُشير إلى انخفاض القيمة "
                   "ويُضر بالعلاقة قبل أن تبدأ.",
    },
    {
        "rule_id": "SAR-007",
        "rule_en": "WhatsApp follow-up is acceptable ONLY after email and only if the client "
                   "has already engaged (opened, replied, or attended a meeting). "
                   "WhatsApp must never be the first or cold contact channel. "
                   "Documented opt-in consent is required before any WhatsApp message.",
        "rule_ar": "المتابعة عبر واتساب مقبولة فقط بعد البريد الإلكتروني وفقط إذا كان العميل "
                   "قد تفاعل بالفعل (فتح الرسالة أو رد عليها أو حضر اجتماعاً). "
                   "يجب ألا يكون واتساب القناة الأولى أو البادئة بالتواصل. "
                   "مطلوب موافقة الاشتراك الموثقة قبل أي رسالة واتساب.",
    },
]

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------


class EmailDraftRequest(BaseModel):
    template_id: str = Field(..., description="Template ID from GET /templates")
    client_name: str = Field(..., max_length=120, description="Full name of the recipient")
    client_company: str = Field(..., max_length=120, description="Recipient's company name")
    sender_name: str = Field(..., max_length=120, description="Name of the human sender")
    context_notes: str = Field(
        default="",
        max_length=500,
        description="Optional context to inject into [CONTEXT_NOTE] placeholder",
    )


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------

_TEMPLATE_INDEX: dict[str, dict[str, Any]] = {
    t["template_id"]: t for t in _EMAIL_TEMPLATES
}


def _draft_email(req: EmailDraftRequest) -> dict[str, Any]:
    """
    Look up the template and fill in known placeholders.
    Returns the filled draft with governance metadata.
    """
    template = _TEMPLATE_INDEX.get(req.template_id)
    if template is None:
        raise KeyError(req.template_id)

    replacements = {
        "[CLIENT_NAME]": req.client_name,
        "[COMPANY_NAME]": req.client_company,
        "[SENDER_NAME]": req.sender_name,
        "[CONTEXT_NOTE]": req.context_notes if req.context_notes else "[CONTEXT_NOTE]",
    }

    def _fill(text: str) -> str:
        for placeholder, value in replacements.items():
            text = text.replace(placeholder, value)
        return text

    return {
        "template_id": req.template_id,
        "subject_line_en": _fill(template["subject_line_en"]),
        "body_en": _fill(template["body_en"]),
        "subject_line_ar": _fill(template["subject_line_ar"]),
        "body_ar": _fill(template["body_ar"]),
        "timing_guidance_en": template["timing_guidance_en"],
        "avoid_en": template["avoid_en"],
        "governance_note_en": template["governance_note_en"],
        "governance_decision": "APPROVAL_FIRST",
        "disclaimer_en": (
            "This draft is for human review only. "
            "Review, personalise, and send manually. "
            "Do not automate delivery of this template."
        ),
        "disclaimer_ar": (
            "هذه المسودة للمراجعة البشرية فقط. "
            "راجعها وخصّصها وأرسلها يدوياً. "
            "لا تُؤتمت تسليم هذا النموذج."
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/templates", summary="List all email templates (summary view)")
async def list_templates() -> dict[str, Any]:
    """Return summary list of all available email templates."""
    summaries = [
        {
            "template_id": t["template_id"],
            "name_en": t["name_en"],
            "name_ar": t["name_ar"],
            "use_case_en": t["use_case_en"],
        }
        for t in _EMAIL_TEMPLATES
    ]
    return {
        "governance_decision": "ALLOW_WITH_REVIEW",
        "total": len(summaries),
        "templates": summaries,
        "note_en": (
            "All templates require human review and manual sending. "
            "No automated delivery is permitted."
        ),
        "note_ar": (
            "تتطلب جميع النماذج مراجعة بشرية وإرسالاً يدوياً. "
            "لا يُسمح بالتسليم الآلي."
        ),
    }


@router.get("/templates/{template_id}", summary="Full detail for a single email template")
async def get_template(template_id: str) -> dict[str, Any]:
    """Return the full template including body, subject, timing, and governance note."""
    template = _TEMPLATE_INDEX.get(template_id)
    if template is None:
        available = sorted(_TEMPLATE_INDEX.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_id}' not found. Available: {available}",
        )
    return {
        "governance_decision": "ALLOW_WITH_REVIEW",
        "template": template,
    }


@router.get("/cultural-rules", summary="Saudi B2B email cultural rules")
async def cultural_rules() -> dict[str, Any]:
    """Return the full set of Saudi B2B email cultural guidelines."""
    return {
        "governance_decision": "ALLOW_WITH_REVIEW",
        "total": len(_SAUDI_EMAIL_RULES),
        "rules": _SAUDI_EMAIL_RULES,
        "note_en": (
            "These rules apply to all outbound email activity for Saudi B2B prospects. "
            "Non-compliance risks damaging client relationships."
        ),
        "note_ar": (
            "تنطبق هذه القواعد على جميع نشاطات البريد الإلكتروني الصادرة "
            "لعملاء B2B السعوديين. عدم الامتثال يُخاطر بالإضرار بعلاقات العملاء."
        ),
    }


@router.post("/draft", summary="Generate a filled email draft for human review")
async def draft_email(body: EmailDraftRequest) -> dict[str, Any]:
    """
    Fill in template placeholders with provided client details.
    Returns a draft for human review and manual send only.
    """
    try:
        result = _draft_email(body)
    except KeyError:
        available = sorted(_TEMPLATE_INDEX.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Template '{body.template_id}' not found. Available: {available}",
        )
    return result
