"""
Prayer-time-aware business scheduling for Saudi Arabia.

Returns prayer windows for major Saudi cities and recommends optimal
meeting slots between prayers. Times are approximate (Umm al-Qura method
pre-computed for representative days). For production, integrate a
live prayer-time API (e.g., Aladhan) per-city per-day.

No guaranteed-outcome language. All times 24h local (AST = UTC+3).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/v1/prayer-schedule", tags=["Saudi Market"])

# ---------------------------------------------------------------------------
# City data + representative prayer windows (average, not astronomical)
# ---------------------------------------------------------------------------

_CITIES: dict[str, dict[str, Any]] = {
    "riyadh": {
        "name_ar": "الرياض",
        "name_en": "Riyadh",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Najd",
        "typical_windows": {
            "fajr": "05:00",
            "sunrise": "06:20",
            "dhuhr": "12:10",
            "asr": "15:30",
            "maghrib": "18:20",
            "isha": "19:50",
        },
    },
    "jeddah": {
        "name_ar": "جدة",
        "name_en": "Jeddah",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Makkah",
        "typical_windows": {
            "fajr": "05:10",
            "sunrise": "06:30",
            "dhuhr": "12:20",
            "asr": "15:40",
            "maghrib": "18:30",
            "isha": "20:00",
        },
    },
    "dammam": {
        "name_ar": "الدمام",
        "name_en": "Dammam",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Eastern Province",
        "typical_windows": {
            "fajr": "04:50",
            "sunrise": "06:10",
            "dhuhr": "12:00",
            "asr": "15:20",
            "maghrib": "18:10",
            "isha": "19:40",
        },
    },
    "khobar": {
        "name_ar": "الخبر",
        "name_en": "Al-Khobar",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Eastern Province",
        "typical_windows": {
            "fajr": "04:50",
            "sunrise": "06:10",
            "dhuhr": "12:00",
            "asr": "15:20",
            "maghrib": "18:10",
            "isha": "19:40",
        },
    },
    "mecca": {
        "name_ar": "مكة المكرمة",
        "name_en": "Mecca",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Makkah",
        "typical_windows": {
            "fajr": "05:10",
            "sunrise": "06:30",
            "dhuhr": "12:20",
            "asr": "15:40",
            "maghrib": "18:30",
            "isha": "20:00",
        },
    },
    "medina": {
        "name_ar": "المدينة المنورة",
        "name_en": "Medina",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Madinah",
        "typical_windows": {
            "fajr": "05:05",
            "sunrise": "06:25",
            "dhuhr": "12:15",
            "asr": "15:35",
            "maghrib": "18:25",
            "isha": "19:55",
        },
    },
    "tabuk": {
        "name_ar": "تبوك",
        "name_en": "Tabuk",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Tabuk",
        "typical_windows": {
            "fajr": "05:20",
            "sunrise": "06:40",
            "dhuhr": "12:30",
            "asr": "15:50",
            "maghrib": "18:40",
            "isha": "20:10",
        },
    },
    "abha": {
        "name_ar": "أبها",
        "name_en": "Abha",
        "timezone": "Asia/Riyadh",
        "utc_offset": "+03:00",
        "region": "Asir",
        "typical_windows": {
            "fajr": "05:15",
            "sunrise": "06:35",
            "dhuhr": "12:25",
            "asr": "15:45",
            "maghrib": "18:35",
            "isha": "20:05",
        },
    },
}

_PRAYER_ORDER = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

_PRAYER_NAMES: dict[str, dict[str, str]] = {
    "fajr":    {"ar": "الفجر",    "en": "Fajr (Dawn)"},
    "sunrise": {"ar": "الشروق",   "en": "Sunrise"},
    "dhuhr":   {"ar": "الظهر",    "en": "Dhuhr (Midday)"},
    "asr":     {"ar": "العصر",    "en": "Asr (Afternoon)"},
    "maghrib": {"ar": "المغرب",   "en": "Maghrib (Sunset)"},
    "isha":    {"ar": "العشاء",   "en": "Isha (Night)"},
}


def _time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


def _minutes_to_time(mins: int) -> str:
    return f"{mins // 60:02d}:{mins % 60:02d}"


def _compute_business_windows(windows: dict[str, str]) -> list[dict[str, str]]:
    """
    Compute optimal meeting windows in typical Saudi business day.
    Saudi offices open ~08:00, break for prayers (~15 min each), close ~17:00.
    Fridays: Jumu'ah prayer at Dhuhr means a long midday closure (~11:30-13:30).
    """
    slots = []

    dhuhr_m = _time_to_minutes(windows["dhuhr"])
    asr_m = _time_to_minutes(windows["asr"])
    maghrib_m = _time_to_minutes(windows["maghrib"])
    isha_m = _time_to_minutes(windows["isha"])

    # Morning window: 08:00 → Dhuhr - 20 min
    slots.append({
        "label_en": "Morning block",
        "label_ar": "وقت الصباح",
        "start": "08:00",
        "end": _minutes_to_time(dhuhr_m - 20),
        "duration_min": (dhuhr_m - 20) - 480,
        "quality": "excellent",
        "note_en": "Productive — no prayer interruption.",
        "note_ar": "مثالي — لا انقطاع للصلاة.",
    })

    # Post-Dhuhr window: Dhuhr + 30 min → Asr - 20 min
    post_dhuhr_start = dhuhr_m + 30
    post_dhuhr_end = asr_m - 20
    if post_dhuhr_end > post_dhuhr_start:
        slots.append({
            "label_en": "Post-Dhuhr block",
            "label_ar": "ما بعد الظهر",
            "start": _minutes_to_time(post_dhuhr_start),
            "end": _minutes_to_time(post_dhuhr_end),
            "duration_min": post_dhuhr_end - post_dhuhr_start,
            "quality": "good",
            "note_en": "Good for follow-ups and demos.",
            "note_ar": "مناسب للمتابعات والعروض التجريبية.",
        })

    # Post-Asr window: Asr + 20 min → Maghrib - 20 min
    post_asr_start = asr_m + 20
    post_asr_end = min(maghrib_m - 20, 17 * 60)  # cap at 17:00
    if post_asr_end > post_asr_start:
        slots.append({
            "label_en": "Late-afternoon block",
            "label_ar": "آخر النهار",
            "start": _minutes_to_time(post_asr_start),
            "end": _minutes_to_time(post_asr_end),
            "duration_min": post_asr_end - post_asr_start,
            "quality": "fair",
            "note_en": "Decision-makers often less available late afternoon.",
            "note_ar": "متخذو القرار أقل توافراً في وقت متأخر من النهار.",
        })

    return slots


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/cities", summary="List supported Saudi cities")
async def list_cities() -> dict[str, Any]:
    return {
        "cities": [
            {
                "id": cid,
                "name_ar": city["name_ar"],
                "name_en": city["name_en"],
                "region": city["region"],
                "timezone": city["timezone"],
            }
            for cid, city in _CITIES.items()
        ],
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/schedule/{city}", summary="Prayer times + business windows for a city")
async def get_city_schedule(city: str) -> dict[str, Any]:
    city_key = city.lower().replace("-", "").replace("_", "").replace(" ", "")
    matched = None
    for k, v in _CITIES.items():
        if k == city_key or k.replace("-", "") == city_key:
            matched = (k, v)
            break

    if not matched:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found. Use GET /api/v1/prayer-schedule/cities.",
        )

    city_id, data = matched
    windows = data["typical_windows"]
    business_slots = _compute_business_windows(windows)

    prayers = [
        {
            "prayer": p,
            "name_ar": _PRAYER_NAMES[p]["ar"],
            "name_en": _PRAYER_NAMES[p]["en"],
            "typical_time": windows[p],
            "is_break": p not in ("sunrise",),
        }
        for p in _PRAYER_ORDER
    ]

    return {
        "city_id": city_id,
        "city_name_ar": data["name_ar"],
        "city_name_en": data["name_en"],
        "timezone": data["timezone"],
        "prayers": prayers,
        "business_windows": business_slots,
        "friday_note_en": (
            "On Fridays (Jumu'ah), Dhuhr prayer runs ~40–60 min. "
            "Schedule important meetings before 11:30 or after 13:30."
        ),
        "friday_note_ar": (
            "يوم الجمعة: صلاة الجمعة تستغرق 40–60 دقيقة. "
            "جدّد اجتماعاتك قبل 11:30 أو بعد 13:30."
        ),
        "accuracy_note_en": "Representative average times — vary ±15 min by season and year.",
        "accuracy_note_ar": "أوقات تقريبية متوسطة — تتفاوت ±15 دقيقة حسب الفصل والسنة.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/best-meeting-times", summary="Best B2B meeting times across Saudi cities")
async def get_best_meeting_times(
    city: str = Query("riyadh", description="City ID (default: riyadh)"),
) -> dict[str, Any]:
    city_key = city.lower()
    if city_key not in _CITIES:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found. Use GET /api/v1/prayer-schedule/cities.",
        )

    data = _CITIES[city_key]
    windows = data["typical_windows"]
    dhuhr = _time_to_minutes(windows["dhuhr"])

    return {
        "city": city_key,
        "recommendations": [
            {
                "rank": 1,
                "window_en": f"09:00 – {_minutes_to_time(dhuhr - 20)}",
                "window_ar": f"٠٩:٠٠ – {_minutes_to_time(dhuhr - 20)}",
                "reason_en": "Morning hours — decision-makers fresh, no prayer break imminent.",
                "reason_ar": "ساعات الصباح — متخذو القرار نشيطون، لا صلاة قريبة.",
            },
            {
                "rank": 2,
                "window_en": f"{_minutes_to_time(dhuhr + 30)} – {_minutes_to_time(dhuhr + 120)}",
                "window_ar": f"{_minutes_to_time(dhuhr + 30)} – {_minutes_to_time(dhuhr + 120)}",
                "reason_en": "Post-Dhuhr — good for demos and proposal reviews.",
                "reason_ar": "ما بعد الظهر — مناسب للعروض ومراجعات المقترحات.",
            },
            {
                "rank": 3,
                "window_en": "Avoid 12:00–12:30 and 15:15–15:50",
                "window_ar": "تجنب 12:00–12:30 و 15:15–15:50",
                "reason_en": "Prayer times — attendees will step away.",
                "reason_ar": "أوقات الصلاة — المشاركون سيغادرون للصلاة.",
            },
        ],
        "ramadan_note_en": (
            "During Ramadan, shift all meetings 1–2 hours later. "
            "Avoid scheduling near Iftar (Maghrib time). "
            "Decisions near Eid are frequently postponed."
        ),
        "ramadan_note_ar": (
            "في رمضان، أخّر جميع الاجتماعات ساعة إلى ساعتين. "
            "تجنب الجدولة قرب الإفطار (وقت المغرب). "
            "القرارات قرب العيد تُؤجَّل كثيراً."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
