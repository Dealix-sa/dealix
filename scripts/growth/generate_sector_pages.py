#!/usr/bin/env python3
"""Generate sector landing-page briefs for the Dealix Self-Growth OS.

Offline, deterministic. Writes one brief per sector to reports/growth/sector_pages/.
Each brief is a STRUCTURE (headline, outcome, sample output, trust, ONE CTA, FAQ)
plus a technical-SEO checklist (canonical, hreflang ar/en, structured data,
sitemap, robots) — not finished marketing copy. Founder writes/approves final copy.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "growth" / "sector_pages"

# sector slug -> (arabic name, pain focus)
SECTORS = {
    "consulting": ("الاستشارات", "proof + command + offers"),
    "training": ("التدريب", "conversion + proof + academy"),
    "marketing-agencies": ("وكالات التسويق", "client reporting + proof"),
    "it-services": ("خدمات IT", "delivery + support + client memory"),
    "recruitment": ("التوظيف", "pipeline + follow-up + operations"),
    "facility-management": ("التشغيل وإدارة المرافق", "SLA + delivery visibility"),
}

SECTION_TEMPLATE = """# Sector Page Brief — {ar_name} (`/ar/industries/{slug}`)

Generated: {ts}

> STRUCTURE for founder copy. One CTA only. No guaranteed-revenue claims.
> Value references are estimates, not Verified value.

## Conversion structure (required blocks)

1. **Pain headline** — اكتب الألم المحدد لقطاع {ar_name}: {pain}.
2. **Specific outcome** — ماذا يتغير بعد Command Sprint (وضوح، Next Action Board، Proof Register).
3. **How Dealix works** — Signal → Decision → Draft → Approval → Execution → Proof.
4. **Sample output** — اعرض Sample Command Pack / Proof Register (anonymized).
5. **Trust / gates** — Approval-first AI، حوكمة، خصوصية.
6. **Offer** — Command Sprint (entry).
7. **CTA (single)** — **ابدأ تشخيص Dealix**.
8. **FAQ** — عالج اعتراضات القطاع (عندنا CRM / AI خطر / السعر / ما عندنا بيانات).

## Technical SEO checklist (build correctly from day one)

- [ ] `<title>` + meta description موجهة لقطاع {ar_name}
- [ ] canonical URL مضبوط
- [ ] hreflang ar/en متبادل بين النسختين
- [ ] structured data (Service / FAQPage) صحيحة وقابلة للتحقق
- [ ] الصفحة مضافة إلى sitemap.xml
- [ ] robots.txt يسمح بالزحف
- [ ] محتوى بصيغة سؤال/جواب لظهور AI answers (انظر AI_SEARCH_GEO_STRATEGY.md)

## Single CTA

> **ابدأ تشخيص Dealix** → /ar/business-os-score أو /ar/command-sprint
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).isoformat()
    index = [
        "# Sector Pages Index — Dealix Self-Growth OS",
        "",
        f"Generated: {ts}",
        "",
        "| Slug | Sector | Pain focus | Route |",
        "|---|---|---|---|",
    ]
    for slug, (ar_name, pain) in SECTORS.items():
        brief = SECTION_TEMPLATE.format(ar_name=ar_name, slug=slug, pain=pain, ts=ts)
        (OUT / f"{slug}.md").write_text(brief, encoding="utf-8")
        index.append(f"| `{slug}` | {ar_name} | {pain} | `/ar/industries/{slug}` |")
    index += ["", f"Total sector briefs: {len(SECTORS)}", ""]
    (OUT / "INDEX.md").write_text("\n".join(index), encoding="utf-8")
    print(f"DEALIX_GROWTH_SECTOR_PAGES=PASS ({len(SECTORS)} sectors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
