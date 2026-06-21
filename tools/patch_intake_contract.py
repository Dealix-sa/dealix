from pathlib import Path

p = Path("company/intake/intake_engine.py")
if not p.exists():
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("", encoding="utf-8")

original = p.read_text(encoding="utf-8")
backup = p.with_suffix(".py.bak")
backup.write_text(original, encoding="utf-8")

marker = "# --- DEALIX_P0_COMPATIBILITY_LAYER_20260621 ---"

compat = r'''
# --- DEALIX_P0_COMPATIBILITY_LAYER_20260621 ---
# Public compatibility contract for company intake tests and CLI users.
# Contract:
#   score(row) -> int
#   recommend(row) -> str

from typing import Any, Mapping


def _dealix_safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(str(value).strip().replace(",", ""))
    except Exception:
        return default


def score(row: Mapping[str, Any] | None) -> int:
    """Return an integer intake score from 0 to 100."""
    row = row or {}
    total = 40

    weekly_leads = _dealix_safe_int(row.get("weekly_leads"), 0)
    if weekly_leads >= 500:
        total += 35
    elif weekly_leads >= 100:
        total += 25
    elif weekly_leads >= 50:
        total += 15
    elif weekly_leads >= 10:
        total += 8

    problem = str(row.get("main_problem") or row.get("problem") or "").strip().lower()
    if problem:
        total += 15

    budget = str(row.get("budget_range") or row.get("budget") or "").strip().lower()
    if any(token in budget for token in ["75k", "75,000", "75000", "50k", "100k", "+"]):
        total += 10

    whatsapp = str(row.get("whatsapp") or row.get("has_whatsapp") or "").strip().lower()
    if whatsapp in {"yes", "true", "1", "y", "نعم"}:
        total += 5

    return max(0, min(100, int(total)))


def recommend(row: Mapping[str, Any] | None) -> str:
    """Recommend the best Dealix offer for an intake row."""
    row = row or {}
    problem = str(row.get("main_problem") or row.get("problem") or "").strip().lower()
    sector = str(row.get("sector") or "").strip().lower()
    text = f"{problem} {sector}"

    if any(token in text for token in ["whatsapp", "واتساب", "واتس", "inbox", "رسائل"]):
        return "WhatsApp / Inbox Follow-up OS"

    if any(token in text for token in ["review", "reviews", "تقييم", "تقييمات", "سمعة"]):
        return "Review Intelligence OS"

    if any(token in text for token in ["brand", "branding", "هوية", "براند"]):
        return "Brand Intelligence OS"

    if any(token in text for token in ["training", "تدريب", "academy", "أكاديمية"]):
        return "Growth Engine OS"

    if any(token in text for token in ["sales", "revenue", "مبيعات", "إيراد", "ايراد"]):
        return "Revenue Command Room OS"

    return "Revenue Command Room OS"
'''

# Strong fix: remove previous compatibility layer if any, then append clean final contract.
if marker in original:
    original = original.split(marker)[0].rstrip() + contract.
if marker in original:
    original = original.split(marker)[0].rstrip() + "\n"

new_text = original.rstrip() + "\n\n" + compat.strip() + "\n"
p.write_text(new_text, encoding="utf-8")

print("PATCHED:", p)
print("BACKUP:", backup)
