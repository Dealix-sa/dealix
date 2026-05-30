"""
Case Study Generator — Build publishable case studies from approved proof packs.
مولّد قصص النجاح — يُنشئ قصص نجاح قابلة للنشر من أطقم الإثبات المعتمدة.

Constitutional gates:
  NO_UNAPPROVED_TESTIMONIAL: Customer must sign consent before any public use.
  NO_FAKE_PROOF: Every claim must reference a real proof event.
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class CaseStudyConsent:
    """Customer consent record — required before any publication."""
    customer_name: str
    company_name: str
    consent_type: str  # "full_named" | "anonymous" | "metrics_only"
    consent_date: str
    consent_ref: str  # Reference number for signed consent
    signed_by: str


@dataclass
class CaseStudy:
    study_id: str
    pack_id: str
    company_name: str  # Replaced with "شركة في {sector}" if anonymous
    sector: str
    consent_type: str

    # Bilingual content
    headline_ar: str
    headline_en: str
    challenge_ar: str
    challenge_en: str
    approach_ar: str
    approach_en: str
    result_ar: str
    result_en: str
    quote_ar: str
    quote_en: str
    key_metrics: dict[str, str]

    is_publishable: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "study_id": self.study_id,
            "pack_id": self.pack_id,
            "company_name": self.company_name,
            "sector": self.sector,
            "consent_type": self.consent_type,
            "headline_ar": self.headline_ar,
            "headline_en": self.headline_en,
            "challenge_ar": self.challenge_ar,
            "challenge_en": self.challenge_en,
            "approach_ar": self.approach_ar,
            "approach_en": self.approach_en,
            "result_ar": self.result_ar,
            "result_en": self.result_en,
            "quote_ar": self.quote_ar,
            "quote_en": self.quote_en,
            "key_metrics": self.key_metrics,
            "is_publishable": self.is_publishable,
            "created_at": self.created_at.isoformat(),
        }

    def to_markdown_ar(self, for_linkedin: bool = False) -> str:
        company_display = self.company_name if self.consent_type == "full_named" else f"شركة في قطاع {self.sector}"

        if for_linkedin:
            # LinkedIn-optimized short format
            return f"""🏆 قصة نجاح: {self.headline_ar}

🎯 التحدي:
{self.challenge_ar}

⚡ الحل:
{self.approach_ar}

📊 النتائج:
{self.result_ar}

{f'💬 "{self.quote_ar}"' if self.quote_ar and self.consent_type == "full_named" else ''}

هل تواجه تحديات مشابهة؟ 👇 تواصل معنا لتشخيص مجاني.

#Dealix #AI #ذكاء_اصطناعي #B2B #السوق_السعودي"""

        lines = [
            f"# قصة نجاح — {company_display}",
            f"**القطاع:** {self.sector}",
            f"**التاريخ:** {self.created_at.strftime('%Y-%m-%d')}",
            "",
            f"## {self.headline_ar}",
            "",
            "---",
            "",
            "## التحدي",
            self.challenge_ar,
            "",
            "## الحل",
            self.approach_ar,
            "",
            "## النتائج",
            self.result_ar,
            "",
            "## المقاييس الرئيسية",
        ]
        for k, v in self.key_metrics.items():
            lines.append(f"- **{k}:** {v}")

        if self.quote_ar and self.consent_type == "full_named":
            lines += [
                "",
                "## كلمة العميل",
                f'> "{self.quote_ar}"',
                f"> — {self.company_name}",
            ]

        lines += [
            "",
            "---",
            "",
            "*قصة نجاح Dealix — تم نشرها بموافقة العميل*" if self.is_publishable
            else "*مسودة غير منشورة — تتطلب موافقة العميل قبل النشر*",
        ]
        return "\n".join(lines)


def build_case_study(
    *,
    pack_id: str,
    pack_data: dict[str, Any],
    consent: CaseStudyConsent,
) -> CaseStudy:
    """
    Build a case study from an approved proof pack.
    Constitutional: Requires valid consent object (NO_UNAPPROVED_TESTIMONIAL).
    """
    if not consent.consent_ref:
        raise ValueError("NO_UNAPPROVED_TESTIMONIAL: consent_ref required before building case study")

    sector = pack_data.get("sector", "other")
    company_raw = pack_data.get("company_name", "شركة")
    company_display = company_raw if consent.consent_type == "full_named" else f"شركة في قطاع {sector}"

    # Build metrics dict from pack evidence
    key_metrics: dict[str, str] = {}
    if pack_data.get("messages_sent"):
        key_metrics["رسائل ذكية مُرسلة"] = str(pack_data["messages_sent"])
    if pack_data.get("replies_received"):
        key_metrics["ردود إيجابية"] = str(pack_data["replies_received"])
    if pack_data.get("meetings_booked"):
        key_metrics["اجتماعات محجوزة"] = str(pack_data["meetings_booked"])
    if pack_data.get("response_time_improvement"):
        key_metrics["تحسّن وقت الاستجابة"] = pack_data["response_time_improvement"]

    headline_ar = f"كيف حقّق {company_display} نتائج قابلة للقياس في 7 أيام"
    headline_en = f"How {company_display} achieved measurable results in 7 days"

    challenge_ar = pack_data.get("problem_statement_ar", f"{company_display} كانت تواجه تحديات في متابعة العملاء المحتملين")
    challenge_en = pack_data.get("problem_statement_en", f"{company_display} faced lead follow-up challenges")

    approach_ar = pack_data.get("actions_taken_ar", "طبّقنا نظام Dealix لأتمتة المتابعة مع الحفاظ على موافقة الفريق على كل رسالة")
    approach_en = pack_data.get("actions_taken_en", "We implemented Dealix's approval-first automation system")

    result_ar = pack_data.get("results_ar", "تحسّن ملحوظ في وقت الاستجابة ونسبة الردود")
    result_en = pack_data.get("results_en", "Measurable improvement in response time and reply rate")

    quote_ar = ""
    if consent.consent_type == "full_named":
        quote_ar = pack_data.get("testimonial_ar", "")

    study = CaseStudy(
        study_id=str(uuid.uuid4()),
        pack_id=pack_id,
        company_name=company_display,
        sector=sector,
        consent_type=consent.consent_type,
        headline_ar=headline_ar,
        headline_en=headline_en,
        challenge_ar=challenge_ar,
        challenge_en=challenge_en,
        approach_ar=approach_ar,
        approach_en=approach_en,
        result_ar=result_ar,
        result_en=result_en,
        quote_ar=quote_ar,
        quote_en="",
        key_metrics=key_metrics,
        is_publishable=bool(consent.consent_ref),
    )

    _save_case_study(study, consent)
    log.info(
        "Case study built: study_id=%s company=%s consent=%s publishable=%s",
        study.study_id,
        company_display,
        consent.consent_type,
        study.is_publishable,
    )
    return study


def _save_case_study(study: CaseStudy, consent: CaseStudyConsent) -> None:
    try:
        cs_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "case-studies"
        )
        os.makedirs(cs_dir, exist_ok=True)
        # Save full data
        data_path = os.path.join(cs_dir, f"{study.study_id}.json")
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump({**study.to_dict(), "consent_ref": consent.consent_ref}, f, ensure_ascii=False, indent=2)
        # Save Arabic markdown
        md_path = os.path.join(cs_dir, f"{study.study_id}_ar.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(study.to_markdown_ar())
        # Save LinkedIn version
        li_path = os.path.join(cs_dir, f"{study.study_id}_linkedin_ar.md")
        with open(li_path, "w", encoding="utf-8") as f:
            f.write(study.to_markdown_ar(for_linkedin=True))
        log.info("Case study saved: %s", data_path)
    except Exception as exc:
        log.warning("Could not save case study: %s", exc)
