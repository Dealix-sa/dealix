"""
Hijri calendar utilities for Saudi market — Gregorian↔Hijri conversion,
Saudi national/public holidays, and Islamic month names in AR/EN.

All conversions use the Reingold tabular algorithm (±1 day accuracy vs.
astronomical observation; Saudi moon-sighting can shift by ±1 day).

Uses Python's datetime.date ordinals (R.D. = proleptic Gregorian day 1
= January 1, 1 CE = ordinal 1) so _gregorian_to_fixed/_fixed_to_gregorian
are simply toordinal() / fromordinal().
"""
from __future__ import annotations

import datetime
import math
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/hijri", tags=["Saudi Market"])

# ---------------------------------------------------------------------------
# Calendar engine (Reingold tabular Islamic calendar)
# ---------------------------------------------------------------------------

# 1 Muharram 1 AH = July 19, 622 CE (proleptic Gregorian) = ordinal 227015
_ISLAMIC_EPOCH: int = datetime.date(622, 7, 19).toordinal()  # 227015


def _islamic_to_fixed(hy: int, hm: int, hd: int) -> int:
    return (
        hd
        + math.ceil(29.5 * (hm - 1))
        + (hy - 1) * 354
        + (3 + 11 * hy) // 30
        + _ISLAMIC_EPOCH
        - 1
    )


def gregorian_to_hijri(gy: int, gm: int, gd: int) -> tuple[int, int, int]:
    fixed = datetime.date(gy, gm, gd).toordinal()
    year = (30 * (fixed - _ISLAMIC_EPOCH) + 10646) // 10631
    prior = fixed - _islamic_to_fixed(year, 1, 1)
    month = (11 * prior + 330) // 325
    day = fixed - _islamic_to_fixed(year, month, 1) + 1
    return year, month, day


def hijri_to_gregorian(hy: int, hm: int, hd: int) -> tuple[int, int, int]:
    d = datetime.date.fromordinal(_islamic_to_fixed(hy, hm, hd))
    return d.year, d.month, d.day


# ---------------------------------------------------------------------------
# Hijri month metadata
# ---------------------------------------------------------------------------

_HIJRI_MONTHS: list[dict[str, Any]] = [
    {"number": 1,  "name_ar": "محرم",          "name_en": "Muharram",    "sacred": True,  "days": 30},
    {"number": 2,  "name_ar": "صفر",            "name_en": "Safar",       "sacred": False, "days": 29},
    {"number": 3,  "name_ar": "ربيع الأول",     "name_en": "Rabi al-Awwal",  "sacred": False, "days": 30},
    {"number": 4,  "name_ar": "ربيع الآخر",     "name_en": "Rabi al-Thani",  "sacred": False, "days": 29},
    {"number": 5,  "name_ar": "جمادى الأولى",   "name_en": "Jumada al-Awwal","sacred": False, "days": 30},
    {"number": 6,  "name_ar": "جمادى الآخرة",   "name_en": "Jumada al-Thani","sacred": False, "days": 29},
    {"number": 7,  "name_ar": "رجب",            "name_en": "Rajab",           "sacred": True,  "days": 30},
    {"number": 8,  "name_ar": "شعبان",          "name_en": "Sha'ban",         "sacred": False, "days": 29},
    {"number": 9,  "name_ar": "رمضان",          "name_en": "Ramadan",         "sacred": True,  "days": 30},
    {"number": 10, "name_ar": "شوال",           "name_en": "Shawwal",         "sacred": False, "days": 29},
    {"number": 11, "name_ar": "ذو القعدة",      "name_en": "Dhul Qa'dah",     "sacred": True,  "days": 30},
    {"number": 12, "name_ar": "ذو الحجة",       "name_en": "Dhul Hijjah",     "sacred": False, "days": 29},
]

_MONTH_BY_NUMBER = {m["number"]: m for m in _HIJRI_MONTHS}


# ---------------------------------------------------------------------------
# Saudi national holidays (fixed Gregorian dates + approximate Hijri events)
# ---------------------------------------------------------------------------

_FIXED_HOLIDAYS = [
    {
        "name_ar": "اليوم الوطني السعودي",
        "name_en": "Saudi National Day",
        "gregorian_month": 9,
        "gregorian_day": 23,
        "type": "national",
        "description_en": "Unification of Saudi Arabia, 23 September 1932.",
    },
    {
        "name_ar": "يوم التأسيس",
        "name_en": "Saudi Founding Day",
        "gregorian_month": 2,
        "gregorian_day": 22,
        "type": "national",
        "description_en": "Founding of the First Saudi State, 22 February 1727.",
    },
]

_HIJRI_HOLIDAYS = [
    {
        "name_ar": "عيد الفطر",
        "name_en": "Eid al-Fitr",
        "hijri_month": 10,
        "hijri_day_start": 1,
        "duration_days": 3,
        "type": "religious",
        "business_impact": "full_closure",
        "description_en": "End of Ramadan. Full closure 3+ days; actual dates depend on moon sighting.",
    },
    {
        "name_ar": "عيد الأضحى",
        "name_en": "Eid al-Adha",
        "hijri_month": 12,
        "hijri_day_start": 10,
        "duration_days": 4,
        "type": "religious",
        "business_impact": "full_closure",
        "description_en": "Feast of Sacrifice. Full closure 4+ days; actual dates depend on moon sighting.",
    },
    {
        "name_ar": "رأس السنة الهجرية",
        "name_en": "Islamic New Year",
        "hijri_month": 1,
        "hijri_day_start": 1,
        "duration_days": 1,
        "type": "religious",
        "business_impact": "partial_closure",
        "description_en": "1 Muharram — start of the new Hijri year.",
    },
    {
        "name_ar": "يوم عرفة",
        "name_en": "Day of Arafah",
        "hijri_month": 12,
        "hijri_day_start": 9,
        "duration_days": 1,
        "type": "religious",
        "business_impact": "reduced_hours",
        "description_en": "9 Dhul Hijjah — day before Eid al-Adha.",
    },
]


def get_holidays_for_gregorian_year(year: int) -> list[dict[str, Any]]:
    """Return all Saudi holidays (Gregorian + Hijri) for a given Gregorian year."""
    holidays: list[dict[str, Any]] = []

    # Fixed Gregorian holidays
    for h in _FIXED_HOLIDAYS:
        try:
            date = datetime.date(year, h["gregorian_month"], h["gregorian_day"])
            hy, hm, hd = gregorian_to_hijri(year, h["gregorian_month"], h["gregorian_day"])
            holidays.append({
                **h,
                "gregorian_date": date.isoformat(),
                "hijri_date": f"{hd} {_MONTH_BY_NUMBER[hm]['name_en']} {hy} AH",
                "hijri_date_ar": f"{hd} {_MONTH_BY_NUMBER[hm]['name_ar']} {hy} هـ",
            })
        except ValueError:
            pass

    # Hijri holidays — compute approximate Gregorian date
    # Try both Hijri years that overlap this Gregorian year
    for hijri_year in range(
        gregorian_to_hijri(year, 1, 1)[0],
        gregorian_to_hijri(year, 12, 31)[0] + 1,
    ):
        for h in _HIJRI_HOLIDAYS:
            try:
                gy, gm, gd = hijri_to_gregorian(
                    hijri_year, h["hijri_month"], h["hijri_day_start"]
                )
                if gy == year:
                    holidays.append({
                        **{k: v for k, v in h.items() if k not in ("hijri_month", "hijri_day_start")},
                        "gregorian_date": datetime.date(gy, gm, gd).isoformat(),
                        "hijri_date": (
                            f"{h['hijri_day_start']} "
                            f"{_MONTH_BY_NUMBER[h['hijri_month']]['name_en']} "
                            f"{hijri_year} AH"
                        ),
                        "hijri_date_ar": (
                            f"{h['hijri_day_start']} "
                            f"{_MONTH_BY_NUMBER[h['hijri_month']]['name_ar']} "
                            f"{hijri_year} هـ"
                        ),
                        "note_ar": "التاريخ تقريبي ±١ يوم حسب رؤية الهلال",
                        "note_en": "Date is approximate ±1 day — confirmed by official moon sighting.",
                    })
            except (ValueError, KeyError):
                pass

    holidays.sort(key=lambda x: x["gregorian_date"])
    return holidays


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class ConvertRequest(BaseModel):
    year: int = Field(..., ge=1800, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/months", summary="Hijri months with AR/EN names")
async def list_hijri_months() -> dict[str, Any]:
    return {
        "months": _HIJRI_MONTHS,
        "note_en": "Days per month alternate 30/29; actual length depends on moon sighting.",
        "note_ar": "أيام الشهر تتناوب 30/29 يوماً؛ الطول الفعلي يعتمد على رؤية الهلال.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/convert/gregorian-to-hijri", summary="Convert Gregorian date → Hijri")
async def gregorian_to_hijri_endpoint(
    year: int = Query(..., ge=1800, le=2100, description="Gregorian year"),
    month: int = Query(..., ge=1, le=12, description="Gregorian month"),
    day: int = Query(..., ge=1, le=31, description="Gregorian day"),
) -> dict[str, Any]:
    try:
        datetime.date(year, month, day)  # validate
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    hy, hm, hd = gregorian_to_hijri(year, month, day)
    month_meta = _MONTH_BY_NUMBER[hm]
    return {
        "gregorian": {"year": year, "month": month, "day": day,
                      "iso": f"{year:04d}-{month:02d}-{day:02d}"},
        "hijri": {
            "year": hy,
            "month": hm,
            "day": hd,
            "month_name_ar": month_meta["name_ar"],
            "month_name_en": month_meta["name_en"],
            "formatted_ar": f"{hd} {month_meta['name_ar']} {hy} هـ",
            "formatted_en": f"{hd} {month_meta['name_en']} {hy} AH",
            "is_sacred_month": month_meta["sacred"],
        },
        "accuracy_note_en": "Tabular algorithm ±1 day. Official Saudi dates follow moon sighting.",
        "accuracy_note_ar": "حساب جدولي ±١ يوم. التواريخ الرسمية تتبع رؤية الهلال في المملكة.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/convert/hijri-to-gregorian", summary="Convert Hijri date → Gregorian")
async def hijri_to_gregorian_endpoint(
    year: int = Query(..., ge=1, le=1600, description="Hijri year"),
    month: int = Query(..., ge=1, le=12, description="Hijri month (1=Muharram)"),
    day: int = Query(..., ge=1, le=30, description="Hijri day"),
) -> dict[str, Any]:
    month_meta = _MONTH_BY_NUMBER.get(month)
    if not month_meta:
        raise HTTPException(status_code=422, detail=f"Invalid Hijri month: {month}")

    gy, gm, gd = hijri_to_gregorian(year, month, day)
    return {
        "hijri": {
            "year": year, "month": month, "day": day,
            "month_name_ar": month_meta["name_ar"],
            "month_name_en": month_meta["name_en"],
            "formatted_ar": f"{day} {month_meta['name_ar']} {year} هـ",
            "formatted_en": f"{day} {month_meta['name_en']} {year} AH",
        },
        "gregorian": {
            "year": gy, "month": gm, "day": gd,
            "iso": f"{gy:04d}-{gm:02d}-{gd:02d}",
        },
        "accuracy_note_en": "Tabular algorithm ±1 day.",
        "accuracy_note_ar": "حساب جدولي ±١ يوم.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/holidays/{year}", summary="Saudi public holidays for a Gregorian year")
async def get_saudi_holidays(year: int) -> dict[str, Any]:
    if not (2000 <= year <= 2050):
        raise HTTPException(status_code=422, detail="Year must be 2000–2050.")
    holidays = get_holidays_for_gregorian_year(year)
    return {
        "year": year,
        "total_holidays": len(holidays),
        "holidays": holidays,
        "disclaimer_en": (
            "Hijri-based holidays are computed dates. "
            "Official public holidays are declared by the Saudi government."
        ),
        "disclaimer_ar": (
            "تواريخ الأعياد الهجرية محسوبة تقريبياً. "
            "الأعياد الرسمية تُعلن من قِبَل الحكومة السعودية."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/ramadan/{year}", summary="Approximate Ramadan start/end for a Gregorian year")
async def get_ramadan_dates(year: int) -> dict[str, Any]:
    if not (2000 <= year <= 2050):
        raise HTTPException(status_code=422, detail="Year must be 2000–2050.")

    results = []
    for hijri_year in range(
        gregorian_to_hijri(year, 1, 1)[0],
        gregorian_to_hijri(year, 12, 31)[0] + 1,
    ):
        start_g = hijri_to_gregorian(hijri_year, 9, 1)   # 1 Ramadan
        end_g = hijri_to_gregorian(hijri_year, 9, 30)    # 30 Ramadan
        if start_g[0] == year or end_g[0] == year:
            results.append({
                "hijri_year": hijri_year,
                "start_gregorian": f"{start_g[0]:04d}-{start_g[1]:02d}-{start_g[2]:02d}",
                "end_gregorian": f"{end_g[0]:04d}-{end_g[1]:02d}-{end_g[2]:02d}",
                "duration_days": 30,
                "business_impact_ar": "انخفاض ساعات العمل — عادةً 6 ساعات يومياً بدلاً من 8.",
                "business_impact_en": "Reduced working hours — typically 6 h/day instead of 8.",
                "sales_note_ar": "قرارات الشراء تتباطأ في النصف الأول وتتسارع قبل عيد الفطر.",
                "sales_note_en": "Purchase decisions slow in first half, accelerate before Eid al-Fitr.",
            })

    return {
        "gregorian_year": year,
        "ramadan_occurrences": results,
        "accuracy_note_en": "±1 day — confirmed by official Saudi moon-sighting announcement.",
        "accuracy_note_ar": "±١ يوم — يُؤكد بإعلان رؤية الهلال الرسمي في المملكة.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
