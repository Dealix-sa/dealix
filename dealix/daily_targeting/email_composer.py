"""Personalized Arabic-primary email composer for daily targeting.

Composes sector-specific, pain-matched outreach emails per account.
No LLM calls — deterministic composition from account metadata.
All email body content is Arabic-first.
"""

from __future__ import annotations

from typing import Any


class EmailComposer:
    """Compose personalized Arabic-primary outreach emails for target accounts."""

    # Sector → list of pain points (Arabic)
    SECTOR_PAIN_POINTS: dict[str, list[str]] = {
        "real_estate": [
            "وقت استجابة للعملاء المحتملين يتجاوز 4 ساعات مما يفقد الصفقات",
            "ضعف تتبع أداء الوكلاء وتوزيع الفرص بينهم",
            "بيانات العملاء مبعثرة بين واتساب وإكسل والهاتف",
        ],
        "medical": [
            "نسبة عدم الحضور للمواعيد تتجاوز 25% وتكلف الكلينيك يومياً",
            "بيانات المرضى موزعة بين ورق وأنظمة غير متكاملة",
            "المتابعة مع المرضى بعد الزيارة تتم يدوياً وغير منتظمة",
        ],
        "training": [
            "تراجع معدلات التسجيل دون معرفة السبب الحقيقي",
            "تقارير الأداء تُعدّ يدوياً وتستغرق ساعات كل أسبوع",
            "انسحاب المتدربين في منتصف البرنامج دون إنذار مبكر",
        ],
        "marketing_agency": [
            "إعداد تقارير العملاء يدوياً يستهلك 12+ ساعة أسبوعياً",
            "صعوبة إثبات عائد الاستثمار للعميل بأرقام واضحة",
            "تتبع أداء الحملات موزع على أدوات منفصلة بدون صورة موحدة",
        ],
        "default": [
            "فقدان وقت العمل في مهام يدوية يمكن أتمتتها",
            "غياب رؤية موحدة على أداء الأعمال والفرص",
            "صعوبة اتخاذ قرارات سريعة بسبب تشتت البيانات",
        ],
    }

    # (min_score, offer_name_ar, offer_price_ar)
    OFFER_BY_SCORE: list[tuple[int, str, str]] = [
        (75, "نظام التشغيل بالذكاء الاصطناعي", "5,000 - 25,000 ريال"),
        (55, "حزمة العمليات المُدارة", "2,999 - 4,999 ريال/شهر"),
        (35, "حزمة البيانات", "1,500 ريال"),
        (20, "سبرينت استخبارات الإيرادات", "499 ريال"),
        (0,  "التشخيص المجاني", "مجاناً — بدون التزام"),
    ]

    # ROI narratives per sector (Arabic)
    _SECTOR_ROI: dict[str, str] = {
        "real_estate": (
            "وكالات العقارات التي طبّقت نظامنا خفّضت وقت الاستجابة من 4 ساعات إلى أقل من 15 دقيقة، "
            "مما رفع معدل إغلاق الصفقات بنسبة 30% في أول 60 يوماً."
        ),
        "medical": (
            "المراكز الطبية التي استخدمت نظامنا خفّضت نسبة عدم الحضور من 25% إلى أقل من 8%، "
            "مما وفّر ما يعادل 3 مواعيد إضافية يومياً لكل طبيب."
        ),
        "training": (
            "مراكز التدريب التي طبّقت نظامنا وفّرت 8 ساعات أسبوعياً في إعداد التقارير، "
            "ورفعت معدل إتمام البرامج بنسبة 20% بفضل التنبيهات المبكرة."
        ),
        "marketing_agency": (
            "وكالات التسويق التي استخدمت نظامنا وفّرت 12 ساعة أسبوعياً في إعداد التقارير، "
            "ورفعت رضا العملاء بنسبة 40% بفضل التقارير الآلية الاحترافية."
        ),
        "default": (
            "الشركات التي طبّقت نظامنا وفّرت في المتوسط 10 ساعات أسبوعياً من العمل اليدوي، "
            "وحسّنت قدرتها على اتخاذ القرار بشكل ملحوظ خلال أول 30 يوماً."
        ),
    }

    # Subject line templates per sector
    _SECTOR_SUBJECTS: dict[str, str] = {
        "real_estate": "كيف تضاعف استجابة وكالتك للعملاء عشرة أضعاف",
        "medical": "توقف عن خسارة مواعيد المرضى بهذه الطريقة",
        "training": "لماذا ينسحب متدربوك قبل نهاية البرنامج",
        "marketing_agency": "12 ساعة تضيع أسبوعياً في تقارير يدوية",
        "default": "كيف تحوّل بيانات شركتك إلى قرارات أسرع",
    }

    def _get_sector_key(self, sector: str) -> str:
        """Normalise sector string to an internal key."""
        s = sector.lower().strip()
        if any(k in s for k in ("real_estate", "عقار", "property", "realty")):
            return "real_estate"
        if any(k in s for k in ("medical", "clinic", "health", "طب", "صحة", "عيادة")):
            return "medical"
        if any(k in s for k in ("training", "education", "تدريب", "تعليم", "أكاديمي")):
            return "training"
        if any(k in s for k in ("marketing", "agency", "تسويق", "وكالة")):
            return "marketing_agency"
        return "default"

    def _pick_offer(self, score: int) -> tuple[str, str]:
        """Return (offer_name_ar, offer_price_ar) for a given ICP score."""
        for min_score, name, price in self.OFFER_BY_SCORE:
            if score >= min_score:
                return name, price
        return self.OFFER_BY_SCORE[-1][1], self.OFFER_BY_SCORE[-1][2]

    def compose(
        self,
        account: dict[str, Any],
        score: int,
        founder_name: str = "سامي",
    ) -> dict[str, Any]:
        """Compose a personalised Arabic-primary email for a target account.

        Args:
            account:       Account dict with at least company_name, contact_name,
                           email, sector, region.
            score:         ICP total score (0-100).
            founder_name:  Sender first name for signature (Arabic).

        Returns:
            Dict with keys: subject, body_ar, body_html, offer_matched,
            pain_points_used, to_email.

        Examples:
            >>> c = EmailComposer()
            >>> result = c.compose(
            ...     {"company_name": "Test Co", "contact_name": "Ahmad",
            ...      "email": "ahmad@test.sa", "sector": "real_estate", "region": "Riyadh"},
            ...     score=78,
            ... )
            >>> result["offer_matched"] == "نظام التشغيل بالذكاء الاصطناعي"
            True
            >>> len(result["pain_points_used"]) == 2
            True
        """
        sector_key = self._get_sector_key(account.get("sector", ""))
        pain_points = self.SECTOR_PAIN_POINTS.get(sector_key, self.SECTOR_PAIN_POINTS["default"])
        # Use the top 2 pain points for the email (keep body concise)
        selected_pains = pain_points[:2]

        offer_name, offer_price = self._pick_offer(score)
        roi_narrative = self._SECTOR_ROI.get(sector_key, self._SECTOR_ROI["default"])
        subject = self._SECTOR_SUBJECTS.get(sector_key, self._SECTOR_SUBJECTS["default"])

        contact_name = account.get("contact_name", "").strip() or "صاحب القرار"
        company_name = account.get("company_name", "شركتكم").strip()
        region = account.get("region", "").strip()

        region_phrase = f"في {region} " if region else ""

        pain_lines = "\n".join(f"- {p}" for p in selected_pains)

        body_ar = (
            f"السلام عليكم {contact_name}،\n\n"
            f"أتواصل معكم من فريق Dealix — نظام تشغيل البيانات للشركات السعودية.\n\n"
            f"لاحظنا أن شركات مثل {company_name} {region_phrase}تواجه تحديات شائعة في هذا القطاع:\n\n"
            f"{pain_lines}\n\n"
            f"هذا بالضبط ما يحله Dealix.\n\n"
            f"--- النتائج التي نحققها ---\n"
            f"{roi_narrative}\n\n"
            f"--- العرض المناسب لكم ---\n"
            f"بناءً على حجم نشاطكم، نقترح البدء بـ:\n"
            f"*{offer_name}* — {offer_price}\n\n"
            f"--- الخطوة التالية ---\n"
            f"طلب مكالمة 20 دقيقة أو شاهد كيف تحسّن بياناتك مجاناً:\n"
            f"https://dealix.me/diagnostic\n\n"
            f"مع تحياتي،\n"
            f"{founder_name}\n"
            f"Dealix | نظام تشغيل البيانات للشركات السعودية\n"
            f"https://dealix.me"
        )

        body_html = (
            f"<div dir='rtl' style='font-family: Arial, sans-serif; font-size: 15px; color: #222;'>"
            f"<p>السلام عليكم {contact_name}،</p>"
            f"<p>أتواصل معكم من فريق Dealix — نظام تشغيل البيانات للشركات السعودية.</p>"
            f"<p>لاحظنا أن شركات مثل <strong>{company_name}</strong> {region_phrase}تواجه تحديات شائعة في هذا القطاع:</p>"
            f"<ul>"
            + "".join(f"<li>{p}</li>" for p in selected_pains)
            + "</ul>"
            f"<p>هذا بالضبط ما يحله Dealix.</p>"
            f"<hr/>"
            f"<h3>النتائج التي نحققها</h3>"
            f"<p>{roi_narrative}</p>"
            f"<hr/>"
            f"<h3>العرض المناسب لكم</h3>"
            f"<p>بناءً على حجم نشاطكم، نقترح البدء بـ:<br/>"
            f"<strong>{offer_name}</strong> — {offer_price}</p>"
            f"<hr/>"
            f"<h3>الخطوة التالية</h3>"
            f"<p>طلب مكالمة 20 دقيقة أو شاهد كيف تحسّن بياناتك مجاناً:<br/>"
            f"<a href='https://dealix.me/diagnostic'>https://dealix.me/diagnostic</a></p>"
            f"<p>مع تحياتي،<br/>"
            f"<strong>{founder_name}</strong><br/>"
            f"Dealix | نظام تشغيل البيانات للشركات السعودية<br/>"
            f"<a href='https://dealix.me'>https://dealix.me</a></p>"
            f"</div>"
        )

        return {
            "subject": subject,
            "body_ar": body_ar,
            "body_html": body_html,
            "offer_matched": offer_name,
            "offer_price": offer_price,
            "pain_points_used": selected_pains,
            "to_email": account.get("email", ""),
            "contact_name": contact_name,
            "company_name": company_name,
        }
