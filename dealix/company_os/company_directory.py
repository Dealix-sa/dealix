"""Streaming Saudi company-directory ingestion and governed target scoring.

The source workbook is treated as a research dataset.  Imported contact values
are masked and optionally HMAC-hashed; the module never infers consent from the
presence of an email address or phone number.
"""
from __future__ import annotations

import hashlib
import hmac
import re
import unicodedata
import zipfile
from collections import Counter
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element

from defusedxml import ElementTree

from auto_client_acquisition.pipelines.normalize import (
    normalize_company_name,
    normalize_email,
    normalize_saudi_phone,
)

_MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
_NS = {"a": _MAIN_NS, "r": _REL_NS, "pr": _PACKAGE_REL_NS}


@dataclass(frozen=True)
class DirectoryCandidate:
    id: str
    company_name: str
    normalized_name: str
    city: str
    activity: str
    has_valid_email: bool
    has_valid_phone: bool
    email_masked: str | None
    phone_masked: str | None
    email_hmac: str | None
    phone_hmac: str | None
    source_sheet: str
    source_row_number: int
    source_fingerprint: str
    data_quality_score: float
    fit_score: float
    research_priority_score: float
    priority: str
    recommended_offer_id: str
    value_angle_ar: str
    relationship_status: str
    consent_status: str
    targeting_status: str
    suppression_reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DirectoryAnalysis:
    source_file: str
    source_sha256: str
    source_sheet: str
    populated_rows: int
    unique_candidates: int
    duplicate_rows: int
    invalid_email_rows: int
    invalid_phone_rows: int
    valid_email_rows: int
    valid_phone_rows: int
    target_ready_rows: int
    research_only_rows: int
    priority_counts: dict[str, int]
    top_cities: tuple[tuple[str, int], ...]
    top_activities: tuple[tuple[str, int], ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _column_index(reference: str) -> int:
    letters = "".join(char for char in reference if char.isalpha())
    result = 0
    for char in letters.upper():
        result = result * 26 + ord(char) - 64
    return max(result - 1, 0)


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        raw = archive.open("xl/sharedStrings.xml")
    except KeyError:
        return []
    strings: list[str] = []
    with raw:
        for _event, element in ElementTree.iterparse(raw, events=("end",)):
            if element.tag.endswith("}si"):
                text = "".join(
                    node.text or ""
                    for node in element.iter()
                    if node.tag.endswith("}t")
                )
                strings.append(text)
                element.clear()
    return strings


def _sheet_target(archive: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
    relationships = ElementTree.fromstring(
        archive.read("xl/_rels/workbook.xml.rels")
    )
    targets = {
        relation.attrib["Id"]: relation.attrib["Target"].lstrip("/")
        for relation in relationships.findall("pr:Relationship", _NS)
    }
    for sheet in workbook.findall("a:sheets/a:sheet", _NS):
        if sheet.attrib["name"] != sheet_name:
            continue
        relation_id = sheet.attrib[f"{{{_REL_NS}}}id"]
        target = targets[relation_id]
        return target if target.startswith("xl/") else f"xl/{target}"
    raise ValueError(f"sheet_not_found:{sheet_name}")


def _cell_text(cell: Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        return "".join(
            node.text or "" for node in cell.iter() if node.tag.endswith("}t")
        )
    value_node = cell.find("a:v", _NS)
    raw = value_node.text if value_node is not None and value_node.text else ""
    if cell_type == "s" and raw:
        try:
            return shared_strings[int(raw)]
        except (IndexError, ValueError):
            return ""
    return raw


def iter_xlsx_directory_rows(
    path: str | Path,
    *,
    sheet_name: str = "داتا كاملة",
) -> Iterator[tuple[int, dict[str, str]]]:
    """Yield populated source rows without loading the giant formatted range."""
    with zipfile.ZipFile(Path(path)) as archive:
        shared_strings = _shared_strings(archive)
        target = _sheet_target(archive, sheet_name)
        headers: list[str] = []
        with archive.open(target) as raw:
            for _event, element in ElementTree.iterparse(raw, events=("end",)):
                if not element.tag.endswith("}row"):
                    continue
                row_number = int(element.attrib.get("r", "0") or 0)
                values: dict[int, str] = {}
                for cell in element.findall("a:c", _NS):
                    value = _cell_text(cell, shared_strings).strip()
                    if value:
                        values[_column_index(cell.attrib.get("r", "A1"))] = value
                if values and not headers:
                    headers = [
                        values.get(index, "") for index in range(max(values) + 1)
                    ]
                elif values and headers:
                    row = {
                        header: values.get(index, "")
                        for index, header in enumerate(headers)
                        if header
                    }
                    if row.get("اسم الشركة", "").strip():
                        yield row_number, row
                element.clear()


def _mask_email(email: str | None) -> str | None:
    if not email or "@" not in email:
        return None
    local, domain = email.split("@", 1)
    visible = local[:1]
    return f"{visible}***@{domain}"


def _mask_phone(phone: str | None) -> str | None:
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 4:
        return "***"
    return f"+***{digits[-4:]}"


def _contact_hmac(value: str | None, key: bytes | None) -> str | None:
    if not value or not key:
        return None
    return hmac.new(key, value.encode("utf-8"), hashlib.sha256).hexdigest()


def _offer_and_angle(activity: str) -> tuple[str, str, float]:
    value = activity.casefold()
    manufacturing = ("صنع", "صناعة", "مصنع", "انتاج", "إنتاج")
    contracting = ("مقاول", "انشاء", "إنشاء", "تشييد", "صيانة", "عقار")
    logistics = ("شحن", "نقل", "لوجست", "مستودع", "تخزين")
    services = ("تسويق", "استشارات", "تقنية", "برمج", "تدريب", "تعليم")
    retail_hospitality = ("تجزئة", "مطعم", "فندق", "سياحة", "ضيافة", "بيع")
    health = ("صحي", "طبي", "عيادة", "مستشفى", "صيدل")
    if any(keyword in value for keyword in manufacturing):
        return (
            "operations_automation_os",
            "تقليل العمل اليدوي وربط المبيعات والتشغيل والتقارير بدليل أثر.",
            88.0,
        )
    if any(keyword in value for keyword in contracting):
        return (
            "executive_command_center_7500",
            "غرفة قيادة للمشاريع والمتابعة والتسليم والمخاطر والتحصيل.",
            84.0,
        )
    if any(keyword in value for keyword in logistics):
        return (
            "operations_automation_os",
            "توحيد الطلبات والمتابعة والتسليم والاستثناءات ومؤشرات التشغيل.",
            85.0,
        )
    if any(keyword in value for keyword in services):
        return (
            "growth_engine_os",
            "تأهيل الفرص وصناعة العروض والمتابعة وقياس القمع التجاري.",
            82.0,
        )
    if any(keyword in value for keyword in retail_hospitality):
        return (
            "client_experience_os",
            "ربط تجربة العميل والاستفسارات والتحويل والاحتفاظ في مسار واحد.",
            78.0,
        )
    if any(keyword in value for keyword in health):
        return (
            "client_experience_os",
            "تنظيم الاستفسارات وتجربة العميل مع تصعيد بشري وخصوصية مشددة.",
            70.0,
        )
    return (
        "free_mini_diagnostic",
        "تشخيص عبء الشركة وتحديد أعلى ثلاث فرص تشغيلية قابلة للقياس.",
        62.0,
    )


def _normalize_city(city: str) -> str:
    value = unicodedata.normalize("NFKC", city)
    value = re.sub(r"[\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", value)
    value = re.sub(r"\bcaf[eé]\b", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value).strip()
    aliases = {
        "مكة": "مكة المكرمة",
        "مكه": "مكة المكرمة",
        "المدينه المنوره": "المدينة المنورة",
        "المدينه": "المدينة المنورة",
        "جده": "جدة",
        "الرياض ": "الرياض",
    }
    return aliases.get(value, value)


def build_directory_candidate(
    row: dict[str, str],
    *,
    source_sheet: str,
    source_row_number: int,
    source_terms_verified: bool = False,
    hash_key: bytes | None = None,
) -> DirectoryCandidate:
    company_name = row.get("اسم الشركة", "").strip()
    normalized_name = normalize_company_name(company_name)
    city = _normalize_city(row.get("المدينة", "").strip())
    activity = row.get("وظيفة الشركة", "").strip()
    raw_email = row.get("الإيميل", "").strip()
    raw_phone = row.get("رقم التواصل", "").strip()
    email = normalize_email(raw_email)
    phone = normalize_saudi_phone(raw_phone)
    offer_id, angle, fit = _offer_and_angle(activity)

    quality = 30.0
    quality += 15.0 if city else 0.0
    quality += 20.0 if activity else 0.0
    quality += 5.0 if email else 0.0
    quality += 5.0 if phone else 0.0
    quality += 15.0  # source file + sheet + row provenance
    quality = min(100.0, quality)
    priority_score = round(fit * 0.65 + quality * 0.35, 2)
    if priority_score >= 82:
        priority = "P1_RESEARCH"
    elif priority_score >= 70:
        priority = "P2_RESEARCH"
    else:
        priority = "P3_RESEARCH"

    suppression_reasons = ["consent_not_proven", "relationship_not_proven"]
    if not source_terms_verified:
        suppression_reasons.append("source_terms_not_verified")
    fingerprint_input = "|".join(
        (normalized_name, city.casefold(), activity.casefold())
    )
    fingerprint = hashlib.sha256(fingerprint_input.encode("utf-8")).hexdigest()
    candidate_id = f"dir_{fingerprint[:20]}"
    return DirectoryCandidate(
        id=candidate_id,
        company_name=company_name,
        normalized_name=normalized_name,
        city=city,
        activity=activity,
        has_valid_email=email is not None,
        has_valid_phone=phone is not None,
        email_masked=_mask_email(email),
        phone_masked=_mask_phone(phone),
        email_hmac=_contact_hmac(email, hash_key),
        phone_hmac=_contact_hmac(phone, hash_key),
        source_sheet=source_sheet,
        source_row_number=source_row_number,
        source_fingerprint=fingerprint,
        data_quality_score=quality,
        fit_score=fit,
        research_priority_score=priority_score,
        priority=priority,
        recommended_offer_id=offer_id,
        value_angle_ar=angle,
        relationship_status="unknown",
        consent_status="unknown",
        targeting_status="research_only",
        suppression_reasons=tuple(suppression_reasons),
    )


def analyze_company_directory(
    path: str | Path,
    *,
    sheet_name: str = "داتا كاملة",
    source_terms_verified: bool = False,
    hash_key: bytes | None = None,
) -> tuple[DirectoryAnalysis, list[DirectoryCandidate]]:
    source_path = Path(path)
    source_sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
    candidates: list[DirectoryCandidate] = []
    seen: set[str] = set()
    duplicate_rows = 0
    invalid_email_rows = 0
    invalid_phone_rows = 0
    valid_email_rows = 0
    valid_phone_rows = 0
    populated_rows = 0
    cities: Counter[str] = Counter()
    activities: Counter[str] = Counter()
    priorities: Counter[str] = Counter()

    for row_number, row in iter_xlsx_directory_rows(source_path, sheet_name=sheet_name):
        populated_rows += 1
        raw_email = row.get("الإيميل", "").strip()
        raw_phone = row.get("رقم التواصل", "").strip()
        candidate = build_directory_candidate(
            row,
            source_sheet=sheet_name,
            source_row_number=row_number,
            source_terms_verified=source_terms_verified,
            hash_key=hash_key,
        )
        valid_email_rows += int(candidate.has_valid_email)
        valid_phone_rows += int(candidate.has_valid_phone)
        invalid_email_rows += int(bool(raw_email) and not candidate.has_valid_email)
        invalid_phone_rows += int(bool(raw_phone) and not candidate.has_valid_phone)
        if candidate.source_fingerprint in seen:
            duplicate_rows += 1
            continue
        seen.add(candidate.source_fingerprint)
        candidates.append(candidate)
        cities[candidate.city or "غير محدد"] += 1
        activities[candidate.activity or "غير محدد"] += 1
        priorities[candidate.priority] += 1

    analysis = DirectoryAnalysis(
        source_file=source_path.name,
        source_sha256=source_sha,
        source_sheet=sheet_name,
        populated_rows=populated_rows,
        unique_candidates=len(candidates),
        duplicate_rows=duplicate_rows,
        invalid_email_rows=invalid_email_rows,
        invalid_phone_rows=invalid_phone_rows,
        valid_email_rows=valid_email_rows,
        valid_phone_rows=valid_phone_rows,
        target_ready_rows=sum(
            candidate.targeting_status == "ready_to_draft" for candidate in candidates
        ),
        research_only_rows=sum(
            candidate.targeting_status == "research_only" for candidate in candidates
        ),
        priority_counts=dict(priorities),
        top_cities=tuple(cities.most_common(15)),
        top_activities=tuple(activities.most_common(20)),
    )
    return analysis, candidates
