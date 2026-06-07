#!/usr/bin/env python3
"""Dealix Daily Draft Pack — approval-gated warm-intro drafts for today's accounts.

Pipeline:  target universe  →  daily selection  →  bilingual drafts (per account)
           →  data/outreach/drafts/YYYY-MM-DD/{INDEX.md, pack.json, <slug>.md}

Doctrine (hard gates):
  - NO live send. Every draft is ``approval_required`` (#8).
  - NO prospect PII. The contact name is an explicit founder-fill placeholder —
    the founder supplies the real name only when they secure the warm intro (#6).
  - Every account is sourced (enforced upstream by dealix_target_universe) (#4/#7).
  - Every customer-facing file ends with the bilingual estimated-value disclaimer.

Run:  python3 scripts/dealix_daily_draft_pack.py --top 10
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.dealix_target_universe import Account, build_today_plan, load_accounts, daily_selection  # noqa: E402

DRAFTS_ROOT = REPO_ROOT / "data" / "outreach" / "drafts"
CONTACT_PLACEHOLDER = "[اسم جهة الاتصال — يُعبّأ عند المقدمة الدافئة / contact name — fill at warm intro]"
DISCLAIMER = (
    "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value"
)


def _slug(name: str) -> str:
    s = re.sub(r"[^\w؀-ۿ]+", "-", name.strip()).strip("-")
    return s[:60] or "account"


def _load_warm_intro_generator():
    """Isolated import of the warm-intro generator (needs only pydantic).

    Avoids executing ``dealix/commercial/__init__`` (which pulls heavy siblings).
    Returns (WarmIntroGenerator, WarmIntroRequest) or (None, None) on failure.
    """
    mod_name = "_dealix_warm_intro"
    path = REPO_ROOT / "dealix" / "commercial" / "warm_intro_generator.py"
    try:
        spec = importlib.util.spec_from_file_location(mod_name, path)
        if spec is None or spec.loader is None:
            return None, None
        mod = importlib.util.module_from_spec(spec)
        # Register before exec so pydantic v2 can resolve forward refs
        # (the module uses `from __future__ import annotations`, so annotations
        # like `datetime` are strings resolved via sys.modules[cls.__module__]).
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
        # Rebuild models now that the module namespace (incl. datetime) exists.
        for cls_name in ("OutreachDraft", "OutreachDraftBundle", "WarmIntroRequest"):
            cls = getattr(mod, cls_name, None)
            if cls is not None and hasattr(cls, "model_rebuild"):
                cls.model_rebuild()
        return mod.WarmIntroGenerator, mod.WarmIntroRequest
    except Exception as exc:  # pragma: no cover - environment dependent
        print(f"[warn] warm_intro_generator unavailable ({exc}); using fallback", file=sys.stderr)
        return None, None


def _fallback_bundle(account: Account, founder: str) -> dict[str, Any]:
    """Dependency-free bilingual drafts so the pack always produces output."""
    company = account.company
    pain = account.pain_hypothesis or "الإيراد"
    wa = [
        {
            "channel": "whatsapp",
            "variant": 1,
            "tone": "warm_referral",
            "body_ar": (
                f"السلام عليكم،\nأنا {founder} من Dealix — نشغّل الإيراد والـAI بطريقة "
                f"محكومة ومثبتة للشركات السعودية. وصلتني سيرتكم عبر معرفة مشتركة.\n"
                f"عندي ملاحظة سريعة حول {pain} في {company} — 10 دقائق هذا الأسبوع؟"
            ),
            "body_en": (
                f"Hello,\nI'm {founder} from Dealix — we run governed, proven revenue & AI "
                f"ops for Saudi B2B. We have a mutual connection.\n"
                f"I have a quick observation about {pain} at {company} — 10 mins this week?"
            ),
            "approval_status": "approval_required",
        },
        {
            "channel": "whatsapp",
            "variant": 2,
            "tone": "question",
            "body_ar": (
                f"مرحباً،\nسؤال مباشر: كيف تتابعون {pain} حالياً في {company}؟\n"
                f"نسأل لأن معظم نظرائكم يفقدون إيراداً هنا — وعندنا تشخيص مجاني محكوم."
            ),
            "body_en": (
                f"Hi,\nDirect question: how do you currently handle {pain} at {company}?\n"
                f"Most peers leak revenue here — we offer a free governed diagnostic."
            ),
            "approval_status": "approval_required",
        },
    ]
    email = [
        {
            "channel": "email",
            "variant": 1,
            "tone": "professional",
            "subject_line": f"تشخيص محكوم مجاني لـ {company} | Free governed diagnostic for {company}",
            "body_ar": (
                f"السلام عليكم،\n\nاسمي {founder}، مؤسس Dealix — نظام تشغيل الإيراد المحكوم "
                f"للشركات السعودية B2B (PDPL أصلاً، الموافقة أولاً).\n"
                f"لاحظنا فرضية حول {pain} في {company}.\n\n"
                f"أقترح تشخيصاً مجانياً (30 دقيقة) لأكبر 3 فرص — بمصدر وأدلة.\n\n"
                f"هل يناسبكم هذا الأسبوع؟\n\nتحياتي،\n{founder}"
            ),
            "body_en": (
                f"Hello,\n\nI'm {founder}, founder of Dealix — the governed Revenue OS for "
                f"Saudi B2B (PDPL-native, approval-first).\n"
                f"We have a hypothesis about {pain} at {company}.\n\n"
                f"I'd offer a free 30-min diagnostic of your top 3 opportunities — sourced "
                f"and evidenced.\n\nDoes this week work?\n\nBest,\n{founder}"
            ),
            "approval_status": "approval_required",
        }
    ]
    return {"whatsapp_drafts": wa, "email_drafts": email, "llm_used": False, "engine": "fallback"}


def generate_account_drafts(account: Account, founder: str, gen, req_cls) -> dict[str, Any]:
    if gen is None or req_cls is None:
        return _fallback_bundle(account, founder)
    try:
        req = req_cls(
            prospect_name=CONTACT_PLACEHOLDER,
            company_name=account.company,
            sector=account.sector or "b2b_services",
            pain_context=account.pain_hypothesis,
            founder_name=founder,
            language="ar",
        )
        bundle = gen.generate(req)
        d = bundle.to_dict()
        d["engine"] = "warm_intro_generator"
        return d
    except Exception as exc:  # pragma: no cover
        print(f"[warn] generator failed for {account.company} ({exc}); fallback", file=sys.stderr)
        return _fallback_bundle(account, founder)


def _render_account_md(account: Account, bundle: dict[str, Any], founder: str) -> str:
    a = account.to_dict()
    lines: list[str] = []
    lines.append(f"# {account.company} — مسودات تواصل دافئ / Warm Outreach Drafts")
    lines.append("")
    lines.append(f"- **ICP score:** {a['icp_score']}/100")
    lines.append(f"- **Segment / Tier / City:** {account.segment} · {account.tier} · {account.city}")
    lines.append(f"- **Recommended offer:** `{account.offer_id}`")
    lines.append(f"- **Why now:** {account.why_now}")
    lines.append(f"- **Pain hypothesis:** {account.pain_hypothesis}")
    lines.append(f"- **Source (public):** {account.source_url}")
    lines.append(f"- **Contact status:** {account.contact_status} — **{CONTACT_PLACEHOLDER}**")
    lines.append(f"- **Engine:** {bundle.get('engine', 'n/a')}")
    lines.append("")
    lines.append("> ⚠️ **APPROVAL REQUIRED — لا إرسال بارد / NO COLD SEND.** "
                 "هذه مسودات بحث عامة. لا ترسل قبل: (1) مقدمة دافئة/أساس قانوني، "
                 "(2) تعبئة الاسم الحقيقي، (3) موافقتك. / Public-research drafts. Do not send "
                 "before: (1) a warm intro / lawful basis, (2) filling the real name, (3) your approval.")
    lines.append("")

    wa = bundle.get("whatsapp_drafts", [])
    if wa:
        lines.append("## WhatsApp / واتساب")
        for d in wa:
            lines.append(f"### Variant {d.get('variant')} — _{d.get('tone','')}_  `{d.get('approval_status','approval_required')}`")
            lines.append("**AR**")
            lines.append("")
            lines.append("```")
            lines.append(d.get("body_ar", "").strip())
            lines.append("```")
            lines.append("**EN**")
            lines.append("")
            lines.append("```")
            lines.append(d.get("body_en", "").strip())
            lines.append("```")
            lines.append("")

    em = bundle.get("email_drafts", [])
    if em:
        lines.append("## Email / بريد")
        for d in em:
            lines.append(f"### Variant {d.get('variant')} — _{d.get('tone','')}_  `{d.get('approval_status','approval_required')}`")
            if d.get("subject_line"):
                lines.append(f"**Subject:** {d.get('subject_line')}")
                lines.append("")
            lines.append("**AR**")
            lines.append("")
            lines.append("```")
            lines.append(d.get("body_ar", "").strip())
            lines.append("```")
            lines.append("**EN**")
            lines.append("")
            lines.append("```")
            lines.append(d.get("body_en", "").strip())
            lines.append("```")
            lines.append("")

    lines.append("## Approval checklist / قائمة الموافقة")
    lines.append("- [ ] مقدمة دافئة أو أساس قانوني موجود / Warm intro or lawful basis exists")
    lines.append("- [ ] الاسم الحقيقي مُعبّأ / Real contact name filled")
    lines.append("- [ ] المحتوى صحيح وبلا ادعاءات غير مصدرة / Content accurate, no un-sourced claims")
    lines.append("- [ ] موافقة المؤسس على الإرسال اليدوي / Founder approves manual send")
    lines.append("")
    lines.append(f"---\n_{DISCLAIMER}_")
    return "\n".join(lines)


def build_pack(*, top_n: int = 10, on_date: date | None = None, founder: str = "بسام",
               rotate: bool = False, out_root: Path | None = None) -> dict[str, Any]:
    plan = build_today_plan(top_n=top_n, on_date=on_date, rotate=rotate)
    accounts = {a.company: a for a in load_accounts()}
    sel_accounts = daily_selection(list(accounts.values()), top_n=top_n, on_date=on_date, rotate=rotate)

    gen_cls, req_cls = _load_warm_intro_generator()
    gen = gen_cls() if gen_cls else None

    d = on_date or datetime.now(UTC).date()
    out_dir = (out_root or DRAFTS_ROOT) / d.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    pack_items: list[dict[str, Any]] = []
    index_lines: list[str] = []
    index_lines.append(f"# Dealix — مسودات اليوم / Daily Draft Pack — {d.isoformat()}")
    index_lines.append("")
    index_lines.append(f"- Universe: **{plan['universe_size']}** sourced accounts · today's batch: **{len(sel_accounts)}**")
    index_lines.append("- Policy: **warm-intro-first · sourced · no PII · no cold/scraping · approval-required**")
    index_lines.append("")
    index_lines.append("> " + plan["founder_note_ar"])
    index_lines.append(">")
    index_lines.append("> " + plan["founder_note_en"])
    index_lines.append("")
    index_lines.append("## Daily quotas / الحصص اليومية")
    index_lines.append("- ✅ Approved touches: 10 · Follow-ups: 5 · Partner conversations: 1 · Evidence events: ≥1")
    index_lines.append("")
    index_lines.append("## Today's accounts / حسابات اليوم")
    index_lines.append("")
    index_lines.append("| # | Company | Score | Segment | Offer | Drafts file |")
    index_lines.append("|---|---|---|---|---|---|")

    for i, account in enumerate(sel_accounts, start=1):
        bundle = generate_account_drafts(account, founder, gen, req_cls)
        slug = f"{i:02d}-{_slug(account.company)}"
        md = _render_account_md(account, bundle, founder)
        (out_dir / f"{slug}.md").write_text(md, encoding="utf-8")
        n_drafts = len(bundle.get("whatsapp_drafts", [])) + len(bundle.get("email_drafts", []))
        pack_items.append({
            "rank": i,
            "company": account.company,
            "icp_score": account.icp_score(),
            "segment": account.segment,
            "offer_id": account.offer_id,
            "source_url": account.source_url,
            "drafts_file": f"{slug}.md",
            "draft_count": n_drafts,
            "engine": bundle.get("engine"),
            "approval_status": "approval_required",
            "governance_decision": "research_only",
        })
        index_lines.append(
            f"| {i} | {account.company} | {account.icp_score()} | {account.segment} "
            f"| `{account.offer_id}` | [{slug}.md]({slug}.md) |"
        )

    index_lines.append("")
    index_lines.append("## How to use / طريقة الاستخدام")
    index_lines.append("1. لكل حساب: احصل على مقدمة دافئة أو تأكد من أساس قانوني. / Secure a warm intro or lawful basis.")
    index_lines.append("2. عبّئ الاسم الحقيقي في المسودة. / Fill the real contact name.")
    index_lines.append("3. راجع وعدّل، ثم **أرسل يدوياً بنفسك**. / Review, edit, then **send manually yourself**.")
    index_lines.append("4. سجّل النتيجة في War Room / CRM. / Log the outcome in War Room / CRM.")
    index_lines.append("")
    index_lines.append(f"---\n_{DISCLAIMER}_")

    (out_dir / "INDEX.md").write_text("\n".join(index_lines), encoding="utf-8")

    try:
        out_dir_label = str(out_dir.relative_to(REPO_ROOT))
    except ValueError:
        out_dir_label = str(out_dir)
    pack = {
        "generated_at": datetime.now(UTC).isoformat(),
        "date": d.isoformat(),
        "founder": founder,
        "universe_size": plan["universe_size"],
        "batch_size": len(sel_accounts),
        "out_dir": out_dir_label,
        "items": pack_items,
        "policy": plan["policy"],
        "disclaimer": DISCLAIMER,
    }
    (out_dir / "pack.json").write_text(
        json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return pack


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Daily Draft Pack")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--date", type=str, default="")
    ap.add_argument("--founder", type=str, default="", help="founder name (or env DEALIX_FOUNDER_NAME)")
    ap.add_argument("--rotate", action="store_true")
    args = ap.parse_args(argv)

    import os
    founder = args.founder or os.environ.get("DEALIX_FOUNDER_NAME") or "بسام"
    on_date = date.fromisoformat(args.date) if args.date else None

    pack = build_pack(top_n=args.top, on_date=on_date, founder=founder, rotate=args.rotate)
    print(f"✅ Draft pack written: {pack['out_dir']}")
    print(f"   {pack['batch_size']} accounts · {sum(it['draft_count'] for it in pack['items'])} drafts "
          f"(all approval_required)")
    print(f"   Open: {pack['out_dir']}/INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
