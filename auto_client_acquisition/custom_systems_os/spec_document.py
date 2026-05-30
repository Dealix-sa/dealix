"""Custom Systems OS — complete bilingual internal-system specification.

Renders the "كامل وشامل" spec as a content dict ``{"markdown", "html"}`` ready
for ``designops.exporter.export_artifact``. AR section first (RTL primary per
DESIGN.md), EN mirror second. Self-contained HTML (no external CDN).

Safety: the rendered text is later scanned by ``designops.safety_gate`` (raw
substring match on tokens like ``guaranteed`` / ``cold whatsapp``) and by
``governance_os.decide``. So governance gates are rendered via a SAFE label map
(never the raw ``no_guaranteed_outcomes`` key) and the banned ``forbidden_copy``
phrases are NEVER printed — only their count is noted. Every document ends with
the canonical "Estimated value is not Verified value" disclaimer.
"""

from __future__ import annotations

from auto_client_acquisition.custom_systems_os.schemas import (
    CustomDesignProfile,
    CustomStructureBlueprint,
)

DISCLAIMER_AR = "القيمة التقديرية ليست قيمة مُتحقَّقة."
DISCLAIMER_EN = "Estimated value is not Verified value."

# Safe, forbidden-token-free bilingual labels for the governance gate keys.
_GATE_LABELS: dict[str, tuple[str, str]] = {
    "source_passport_required_before_ai": (
        "جواز المصدر إلزامي قبل أي استخدام للذكاء الاصطناعي",
        "Source Passport required before any AI use",
    ),
    "governance_decision_before_draft": (
        "قرار حوكمة قبل كل مسودة",
        "Governance decision before every draft",
    ),
    "human_approval_for_external_send": (
        "موافقة بشرية لأي إرسال خارجي",
        "Human approval for any external send",
    ),
    "no_scraping": ("لا سحب بيانات", "No data scraping"),
    "no_cold_whatsapp": (
        "لا تواصل بارد عبر واتساب",
        "No cold outreach on WhatsApp",
    ),
    "no_linkedin_automation": ("لا أتمتة على لينكدإن", "No LinkedIn automation"),
    "no_guaranteed_outcomes": ("لا وعود بالنتائج", "No outcome promises"),
    "no_pii_in_logs": ("لا بيانات شخصية في السجلات", "No PII in logs"),
    "every_answer_has_source": ("لكل إجابة مصدر", "Every answer has a source"),
    "proof_pack_required": ("Proof Pack إلزامي", "Proof Pack required"),
    "capital_asset_per_engagement": (
        "أصل قابل لإعادة الاستخدام واحد على الأقل لكل مشروع",
        "At least one Capital Asset per engagement",
    ),
}


def _gate_lines(gates: tuple[str, ...], lang: int) -> str:
    return "\n".join(f"- {_GATE_LABELS.get(g, (g, g))[lang]}" for g in gates)


def _palette_lines(profile: CustomDesignProfile) -> str:
    colors = profile.tokens.get("colors") or {}
    return "\n".join(f"- `{k}`: {v}" for k, v in colors.items()) or "- (none)"


def build_spec_document(
    *,
    profile: CustomDesignProfile,
    blueprint: CustomStructureBlueprint,
    customer_name: str,
    language_primary: str = "ar",
) -> dict[str, str]:
    """Render the complete bilingual internal-system specification."""
    modules_ar = "\n".join(f"- {m['name']}" for m in blueprint.modules) or "- (لم تُحدَّد بعد)"
    modules_en = "\n".join(f"- {m['name']}" for m in blueprint.modules) or "- (not declared yet)"
    workflows_ar = (
        "\n".join(f"- {w['name']} (مسودة أولاً، موافقة للخارج)" for w in blueprint.workflows)
        or "- (لم تُحدَّد بعد)"
    )
    workflows_en = (
        "\n".join(
            f"- {w['name']} (draft-first, approval for external)" for w in blueprint.workflows
        )
        or "- (not declared yet)"
    )
    data_model = "\n".join(f"- `{d['entity']}` — {d['purpose']}" for d in blueprint.data_model)
    typography = profile.tokens.get("typography") or {}
    tone = profile.tokens.get("tone") or "—"

    markdown = f"""# نظام داخلي مخصّص — {customer_name}
# Custom Internal System — {customer_name}

> تسليم محكوم بقيادة المؤسس · Governed, founder-assisted delivery
> اتجاه التصميم · Design direction: `{profile.direction_name}` · النبرة · Tone: `{tone}`

---

## 1. نظرة عامة · Overview
نظام داخلي مخصّص للشركة، مبنيٌّ على هوية تصميم خاصة وبنية معمارية محكومة،
يرث جميع بوابات الحوكمة في Dealix.
A bespoke internal system built on a client-specific design identity and a
governed architecture that inherits every Dealix governance gate.

## 2. هوية التصميم المخصّصة · Custom Design Identity
- الاتجاه · Direction: `{profile.direction_name}`
- النبرة · Tone: `{tone}`
- الخطوط · Typography: {typography}
- الألوان · Palette:
{_palette_lines(profile)}
- يرث حارس العبارات الممنوعة في Dealix · Inherits Dealix forbidden-copy guard ({len(profile.forbidden_copy)} phrases)

## 3. بنية النظام · System Structure
### الوحدات · Modules
**AR**
{modules_ar}

**EN**
{modules_en}

### نموذج البيانات · Data Model
{data_model}

### مسارات العمل · Workflows
**AR**
{workflows_ar}

**EN**
{workflows_en}

## 4. بوابات الحوكمة · Governance Gates
**AR**
{_gate_lines(blueprint.governance_gates, 0)}

**EN**
{_gate_lines(blueprint.governance_gates, 1)}

## 5. نمط التسليم · Delivery Mode
بقيادة المؤسس / شبه-مؤتمت — لا إرسال خارجي مؤتمت، ولا white-label كامل.
Founder-assisted / semi-automated — no automated external send, no full white-label.

## 6. الخطوة التالية · Next Step
مراجعة المؤسس قبل أي تسليم خارجي · Founder review before any external delivery.

---

> {DISCLAIMER_AR} · {DISCLAIMER_EN}
"""

    html = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head><meta charset="utf-8"><title>Custom Internal System — {customer_name}</title></head>
<body style="font-family:sans-serif;max-width:880px;margin:2rem auto;line-height:1.6">
<h1>نظام داخلي مخصّص · Custom Internal System — {customer_name}</h1>
<p><strong>اتجاه التصميم · Design direction:</strong> {profile.direction_name} ·
<strong>النبرة · Tone:</strong> {tone}</p>
<h2>بوابات الحوكمة · Governance Gates</h2>
<ul>{''.join(f'<li>{_GATE_LABELS.get(g,(g,g))[1]}</li>' for g in blueprint.governance_gates)}</ul>
<h2>الوحدات · Modules</h2>
<ul>{''.join(f"<li>{m['name']}</li>" for m in blueprint.modules) or '<li>not declared yet</li>'}</ul>
<hr>
<p><em>{DISCLAIMER_AR} · {DISCLAIMER_EN}</em></p>
</body></html>"""

    return {"markdown": markdown, "html": html}


__all__ = ["DISCLAIMER_AR", "DISCLAIMER_EN", "build_spec_document"]
