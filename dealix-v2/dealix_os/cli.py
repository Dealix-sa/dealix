import argparse
import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dealix_os" / "data"

CAPABILITIES = ["Revenue", "Customer", "Operations", "Knowledge", "Data", "Governance", "Reporting"]

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u0600-\u06FF]+", "-", value)
    value = value.strip("-")
    return value or "untitled"

def safe_slug(value: str) -> str:
    return slugify(value)

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def append(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text)

def services():
    return read_json(DATA / "services.json")

def capabilities():
    return read_json(DATA / "capabilities.json")

def governance_rules():
    return read_json(DATA / "governance_rules.json")

def ensure_ledgers():
    ledgers_dir = ROOT / "ledgers"
    ledgers_dir.mkdir(parents=True, exist_ok=True)
    
    files = {
        "VALUE_LEDGER.md": "| Value ID | Timestamp | Client | Service | Value Type | Metric | Baseline | Result | Evidence | Next Value Opportunity |\n|---|---|---|---|---|---|---|---|---|---|\n",
        "CAPITAL_LEDGER.md": "| Capital ID | Timestamp | Project | Capital Type | Asset | Reusable | Sami | Next Use | Status |\n|---|---|---|---|---|---|---|---|---|\n",
        "AI_RUN_LEDGER.md": "| AI ID | Timestamp | Project | Task | Model | Prompt Version | Redacted | Schema | Cost | QA | Risk | Approval |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n",
        "GOVERNANCE_LEDGER.md": "| Gov ID | Timestamp | Context | Checked Text | Status | Violations | Approver | Date |\n|---|---|---|---|---|---|---|---|\n",
        "CLIENT_LEDGER.md": "| Client ID | Client Name | Sector | Lead Source | Stage | Status | Next Step | Owner |\n|---|---|---|---|---|---|---|---|\n",
        "PIPELINE_LEDGER.md": "| Pipeline ID | Timestamp | Client | Stage | Value | Probability | Status | Next Action |\n|---|---|---|---|---|---|---|---|\n",
        "PARTNER_LEDGER.md": "| Partner ID | Timestamp | Partner | Type | Status | Contact | Value |\n|---|---|---|---|---|---|---|\n",
        "RELATIONSHIP_LEDGER.md": "| Relationship ID | Timestamp | Contact | Company | Role | Status | Last Touch |\n|---|---|---|---|---|---|---|\n",
    }
    
    for filename, header in files.items():
        p = ledgers_dir / filename
        if not p.exists():
            write(p, header)

def create_client_pack(client_name_or_slug: str, sector: str, problem: str, service: str):
    slug = slugify(client_name_or_slug)
    client_dir = ROOT / "clients" / slug
    client_dir.mkdir(parents=True, exist_ok=True)
    
    profile_content = f"""# Client Profile: {client_name_or_slug}

Created: {now()}

## Company

{client_name_or_slug}

## Sector

{sector}

## Contact

-

## Business Problem

{problem}

## Current Stage

Lead / Diagnostic / Sprint / Pilot / Retainer / Enterprise

## Notes

-
"""
    write(client_dir / "CLIENT_PROFILE.md", profile_content)

    scorecard_content = f"""# Capability Scorecard: {client_name_or_slug}

| Capability | Level | Score | Evidence | Risk | Next Action |
|---|---:|---:|---|---|---|
| Revenue | 0 | 0/100 |  |  |  |
| Customer | 0 | 0/100 |  |  |  |
| Operations | 0 | 0/100 |  |  |  |
| Knowledge | 0 | 0/100 |  |  |  |
| Data | 0 | 0/100 |  |  |  |
| Governance | 0 | 0/100 |  |  |  |
| Reporting | 0 | 0/100 |  |  |  |

## Levels

0 = absent  
1 = manual  
2 = structured  
3 = AI-assisted  
4 = governed workflow  
5 = optimized operating system
"""
    write(client_dir / "CAPABILITY_SCORECARD.md", scorecard_content)

    deal_room_content = f"""# Deal Room: {client_name_or_slug}

## Client Information
- Name: {client_name_or_slug}
- Sector: {sector}

## Strategic Objective
- Target: {service}
- Problem to Solve: {problem}

## Engagement Overview
- Proposed Solution: {service}
- Key Metrics to Track: Value created, hours saved, quality improved

## Proposal & Pricing
- Initial Sprint Price: SAR 7,500 - 25,000 depending on final scope
- Value Floor: Realized ROI in first 30 days
- Upsell Path: Retention, custom module development
"""
    write(client_dir / "DEAL_ROOM.md", deal_room_content)

    expansion_content = f"""# Expansion Map: {client_name_or_slug}

## Current Service

{service}

## Proof Created

-

## Next Best Offers

1. Pilot Conversion Sprint
2. Monthly AI Operations Retainer
3. Custom Platform Module

## Why

Based on capability score improvement path.

## Decision Timing

At completion of current sprint.
"""
    write(client_dir / "EXPANSION_MAP.md", expansion_content)

    proof_pack_template_content = f"""# Proof Pack Template: {client_name_or_slug}

## Client: {client_name_or_slug}
## Service: {service}

## 1. Value Hypothesis
- What we planned to achieve
- Expected KPI: hours saved, data ranked, error reduction

## 2. Actual Result
- Baseline vs. Outcome
- Verified Evidence

## 3. Governance Audit
- Source Check: verified
- PII Check: verified
- Human Approval: obtained
- Claim Safety: confirmed
"""
    write(client_dir / "PROOF_PACK_TEMPLATE.md", proof_pack_template_content)

    written = [
        "CLIENT_PROFILE.md",
        "CAPABILITY_SCORECARD.md",
        "DEAL_ROOM.md",
        "EXPANSION_MAP.md",
        "PROOF_PACK_TEMPLATE.md"
    ]
    
    append(ROOT / "ledgers" / "CLIENT_LEDGER.md", f"| C-{datetime.now().strftime('%Y%m%d%H%M%S')} | {client_name_or_slug} | {sector} |  | Lead | New | Run diagnostic | Sami |\n")
    
    return client_dir, written

def score_problem(problem: str):
    text = problem.lower()
    scores = {c: 0 for c in CAPABILITIES}

    keywords = {
        "Revenue": ["lead", "sales", "pipeline", "crm", "عميل", "مبيعات", "فرص", "عملاء", "leads"],
        "Customer": ["support", "reply", "customer", "ticket", "whatsapp", "دعم", "ردود", "واتساب"],
        "Operations": ["manual", "workflow", "process", "hours", "report", "يدوي", "تقرير", "تشغيل", "عملية"],
        "Knowledge": ["document", "knowledge", "search", "files", "policy", "ملفات", "معرفة", "مستندات"],
        "Data": ["data", "csv", "duplicate", "missing", "clean", "بيانات", "تكرار", "ناقص"],
        "Governance": ["risk", "policy", "approval", "compliance", "pii", "حوكمة", "مخاطر", "موافقة"],
        "Reporting": ["dashboard", "kpi", "executive", "summary", "لوحة", "مؤشرات", "إدارة"]
    }

    for cap, words in keywords.items():
        for w in words:
            if w in text:
                scores[cap] += 1

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        best = "Data"
    return best, scores

def recommend_service_for_capability(cap: str):
    svc = services()
    candidates = [k for k, v in svc.items() if v["capability"] == cap]
    return candidates[0] if candidates else "data-readiness"

def cmd_doctor(args):
    print("Dealix Founder OS Doctor")
    print("========================")
    print(f"Root: {ROOT}")
    checks = [
        ("README", ROOT / "README.md"),
        ("Services JSON", DATA / "services.json"),
        ("Capabilities JSON", DATA / "capabilities.json"),
        ("Governance Rules", DATA / "governance_rules.json"),
        ("Ledgers", ROOT / "ledgers"),
        ("Clients", ROOT / "clients"),
        ("Sales", ROOT / "sales"),
    ]
    ok = True
    for name, path in checks:
        exists = path.exists()
        ok = ok and exists
        print(f"{name:24} {'OK' if exists else 'MISSING'}")
    print("")
    print("Status:", "READY" if ok else "NEEDS REPAIR")

def cmd_services(args):
    data = services()
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for key, svc in data.items():
        print(f"{key}")
        print(f"  Name: {svc['name']}")
        print(f"  Capability: {svc['capability']}")
        print(f"  Starts at: SAR {svc['price_starts_at']}")
        print(f"  KPI: {svc['kpi']}")
        print(f"  Upsell: {svc['upsell']}")
        print("")

def cmd_capabilities(args):
    data = capabilities()
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for name, cap in data.items():
        print(f"{name}")
        print(f"  Purpose: {cap['purpose']}")
        print(f"  Problems: {', '.join(cap['common_problems'])}")
        print(f"  Services: {', '.join(cap['services'])}")
        print("")

def cmd_assess(args):
    cap, scores = score_problem(args.problem)
    svc_key = recommend_service_for_capability(cap)
    svc = services().get(svc_key, {})
    result = {
        "problem": args.problem,
        "recommended_capability": cap,
        "recommended_service": svc_key,
        "service_name": svc.get("name", svc_key),
        "kpi": svc.get("kpi", ""),
        "price_starts_at": svc.get("price_starts_at", ""),
        "scores": scores,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

def cmd_recommend_sprint(args):
    cap, scores = score_problem(args.problem)
    svc_key = recommend_service_for_capability(cap)
    svc = services().get(svc_key, {})
    print(f"Recommended Sprint: {svc.get('name', svc_key)}")
    print(f"Capability: {svc.get('capability', cap)}")
    print(f"Starts at: SAR {svc.get('price_starts_at', '')}")
    print(f"KPI: {svc.get('kpi', '')}")
    print("")
    print("Deliverables:")
    for item in svc.get("deliverables", []):
        print(f"- {item}")
    print("")
    print(f"Upsell: {svc.get('upsell', '')}")

def governance_check_text(text: str):
    t = text.lower()
    flags = []
    if any(x in t for x in ["guaranteed", "guarantee", "مضمون", "نضمن", "ضمان"]):
        flags.append("guaranteed_claim")
    if any(x in t for x in ["whatsapp", "واتساب"]):
        flags.append("whatsapp_sensitive")
    if any(x in t for x in ["send automatically", "auto-send", "إرسال تلقائي", "ارسل تلقائيا"]):
        flags.append("external_action_requires_approval")
    if any(x in t for x in ["scrape", "scraping", "اكشط", "سحب بيانات"]):
        flags.append("source_permission_required")
    if any(x in t for x in ["phone", "email", "رقم", "جوال", "ايميل", "بريد"]):
        flags.append("pii_check_required")
    decision = "ALLOW" if not flags else "REVIEW_REQUIRED"
    if "autonomous" in t or "بدون موافقة" in t:
        decision = "BLOCK_OR_APPROVAL_REQUIRED"
        flags.append("autonomy_risk")
    return {"decision": decision, "flags": sorted(set(flags))}

def cmd_governance_check(args):
    print(json.dumps(governance_check_text(args.text), ensure_ascii=False, indent=2))

def cmd_score(args):
    cap, scores = score_problem(args.problem)
    total = sum(scores.values())
    print(json.dumps({
        "problem": args.problem,
        "recommended_capability": cap,
        "score_total": total,
        "scores": scores,
        "recommended_service": recommend_service_for_capability(cap),
    }, ensure_ascii=False, indent=2))

def cmd_new_client(args):
    ensure_ledgers()
    name = args.name if args.name else args.slug
    client_dir, written = create_client_pack(name, args.sector, "", "data-readiness")
    print(f"Created client workspace: {client_dir}")
    for p in written:
        print(f"- {p}")

def cmd_client_pack(args):
    ensure_ledgers()
    client_dir, written = create_client_pack(args.client, args.sector, args.problem, args.service)
    print(f"Client pack created: {client_dir}")
    for p in written:
        print(f"- {p}")

def cmd_value(args):
    ensure_ledgers()
    row = f"| V-{datetime.now().strftime('%Y%m%d%H%M%S')} | {now()} | {args.client} | {args.service} | {args.value_type} | {args.metric} | {args.baseline} | {args.result} | {args.evidence} | {args.next_value} |\n"
    append(ROOT / "ledgers" / "VALUE_LEDGER.md", row)
    print("Value ledger updated.")

def cmd_capital(args):
    ensure_ledgers()
    row = f"| C-{datetime.now().strftime('%Y%m%d%H%M%S')} | {now()} | {args.project} | {args.capital_type} | {args.asset} | {args.reusable} | Sami | {args.next_use} | Created |\n"
    append(ROOT / "ledgers" / "CAPITAL_LEDGER.md", row)
    print("Capital ledger updated.")

def cmd_ai_run(args):
    ensure_ledgers()
    row = f"| AI-{datetime.now().strftime('%Y%m%d%H%M%S')} | {now()} | {args.project} | {args.task} | {args.model} | {args.prompt_version} | {args.redacted} | {args.schema} | {args.cost} | {args.qa} | {args.risk} | {args.approval} |\n"
    append(ROOT / "ledgers" / "AI_RUN_LEDGER.md", row)
    print("AI run ledger updated.")

def cmd_proof_pack(args):
    ensure_ledgers()
    slug = safe_slug(args.client)
    out = ROOT / "reports" / f"proof-pack-{slug}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    svc = services().get(args.service, {"name": args.service, "kpi": args.metric, "upsell": args.next_value})
    text = f"""# Proof Pack: {args.client}

Generated: {now()}

## Service

{svc.get("name", args.service)}

## Value Type

{args.value_type}

## KPI

{args.metric}

## Baseline

{args.baseline}

## Result

{args.result}

## Evidence

{args.evidence}

## Governance

- Source check: required
- PII check: required
- Human approval: required for external use
- Claim safety: required
- Audit log: required

## Next Value Opportunity

{args.next_value}

## Recommended Next Step

Discuss expansion map and convert proof into pilot or retainer.
"""
    write(out, text)
    print(f"Proof pack generated: {out}")

def cmd_proposal(args):
    data = services()
    if args.service not in data:
        print(f"Unknown service: {args.service}")
        print("Available:", ", ".join(data.keys()))
        return

    svc = data[args.service]
    out = ROOT / "sales" / "proposals" / f"proposal-{safe_slug(args.client)}-{args.service}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    text = f"""# Proposal: {svc['name']}

## Client

{args.client}

## Problem

{args.problem}

## Recommended Sprint

{svc['name']}

## Why This Sprint

This sprint targets {svc['capability']} Capability and is designed to create measurable proof quickly.

## Deliverables

{chr(10).join("- " + d for d in svc.get("deliverables", []))}

## Timeline

{svc.get("timeline", "")}

## Success Metric

{svc.get("kpi", "")}

## Governance

- Source check
- PII check
- Human approval
- Claim safety
- Audit log
- Proof pack

## Price Starts At

SAR {svc.get("price_starts_at", "")}

## Next Step

Run diagnostic call and confirm scope.
"""
    write(out, text)
    print(f"Proposal generated: {out}")

def cmd_outreach(args):
    cap, _ = score_problem(args.problem)
    svc_key = recommend_service_for_capability(cap)
    svc = services().get(svc_key, {})
    msg = f"""السلام عليكم،

لاحظت أن {args.company} تعمل في قطاع {args.sector}. الفكرة المناسبة ليست استخدام AI بشكل عام، بل Sprint قصير يبني قدرة تشغيلية واضحة حول: {args.problem}

الاقتراح الأولي:
{svc.get("name", svc_key)}

الهدف:
{svc.get("kpi", "")}

المخرجات:
{chr(10).join("- " + d for d in svc.get("deliverables", []))}

Dealix لا تبني سبام أو وعود مبيعات مبالغ فيها؛ نركز على بيانات جاهزة، workflow واضح، موافقة بشرية، وحزمة إثبات أثر.

إذا مناسب، أقدر أرسل تصور صفحة واحدة للـ Sprint.
"""
    print(msg)

def cmd_dashboard(args):
    ensure_ledgers()
    print("Dealix Founder Dashboard")
    print("========================")
    ledger_files = [
        "VALUE_LEDGER.md",
        "CAPITAL_LEDGER.md",
        "AI_RUN_LEDGER.md",
        "GOVERNANCE_LEDGER.md",
        "CLIENT_LEDGER.md",
        "PIPELINE_LEDGER.md",
        "PARTNER_LEDGER.md",
        "RELATIONSHIP_LEDGER.md",
    ]
    for name in ledger_files:
        p = ROOT / "ledgers" / name
        if not p.exists():
            print(f"{name:28} missing")
            continue
        rows = [
            line for line in p.read_text(encoding="utf-8").splitlines()
            if line.startswith("|") and not line.startswith("|---")
        ]
        count = max(0, len(rows) - 1)
        print(f"{name:28} {count} entries")
    print("")
    print("Next founder questions:")
    print("1. What did we sell?")
    print("2. What proof did we create?")
    print("3. What asset did we add?")
    print("4. What risk did we control?")
    print("5. What can become a product module?")

def cmd_monthly_review(args):
    ensure_ledgers()
    out = ROOT / "reports" / f"monthly-review-{datetime.now().strftime('%Y%m')}.md"
    ledger_names = ["VALUE_LEDGER.md", "CLIENT_LEDGER.md", "PIPELINE_LEDGER.md", "CAPITAL_LEDGER.md", "GOVERNANCE_LEDGER.md"]
    lines = [f"# Dealix Monthly Review\n\nGenerated: {now()}\n\n## Ledger Snapshot\n"]
    for name in ledger_names:
        p = ROOT / "ledgers" / name
        rows = []
        if p.exists():
            rows = [line for line in p.read_text(encoding="utf-8").splitlines() if line.startswith("|") and not line.startswith("|---")]
        lines.append(f"- {name}: {max(0, len(rows)-1)} entries")
    lines.append("\n## CEO Decisions\n\n1.\n2.\n3.\n")
    write(out, "\n".join(lines))
    print(f"Monthly review generated: {out}")

def build_parser():
    parser = argparse.ArgumentParser(prog="dealix", description="Dealix Founder OS CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("doctor")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("services")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_services)

    p = sub.add_parser("capabilities")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_capabilities)

    p = sub.add_parser("new-client")
    p.add_argument("slug")
    p.add_argument("--name", default="")
    p.add_argument("--sector", default="Unknown")
    p.set_defaults(func=cmd_new_client)

    p = sub.add_parser("assess")
    p.add_argument("problem")
    p.set_defaults(func=cmd_assess)

    p = sub.add_parser("recommend-sprint")
    p.add_argument("problem")
    p.set_defaults(func=cmd_recommend_sprint)

    p = sub.add_parser("governance-check")
    p.add_argument("text")
    p.set_defaults(func=cmd_governance_check)

    p = sub.add_parser("score")
    p.add_argument("problem")
    p.set_defaults(func=cmd_score)

    p = sub.add_parser("client-pack")
    p.add_argument("--client", required=True)
    p.add_argument("--sector", default="Unknown")
    p.add_argument("--problem", default="")
    p.add_argument("--service", default="lead-intelligence")
    p.set_defaults(func=cmd_client_pack)

    p = sub.add_parser("value")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--value-type", default="Business")
    p.add_argument("--metric", required=True)
    p.add_argument("--baseline", default="unknown")
    p.add_argument("--result", required=True)
    p.add_argument("--evidence", default="manual entry")
    p.add_argument("--next-value", default="next sprint")
    p.set_defaults(func=cmd_value)

    p = sub.add_parser("capital")
    p.add_argument("--project", required=True)
    p.add_argument("--capital-type", required=True)
    p.add_argument("--asset", required=True)
    p.add_argument("--reusable", default="Yes")
    p.add_argument("--next-use", required=True)
    p.set_defaults(func=cmd_capital)

    p = sub.add_parser("ai-run")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--model", default="local")
    p.add_argument("--prompt-version", default="v1.0")
    p.add_argument("--redacted", default="Yes")
    p.add_argument("--schema", default="Markdown")
    p.add_argument("--cost", default="0")
    p.add_argument("--qa", default="0")
    p.add_argument("--risk", default="Medium")
    p.add_argument("--approval", default="Required")
    p.set_defaults(func=cmd_ai_run)

    p = sub.add_parser("proof-pack")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--value-type", default="Business")
    p.add_argument("--metric", required=True)
    p.add_argument("--baseline", default="unknown")
    p.add_argument("--result", required=True)
    p.add_argument("--evidence", default="manual entry")
    p.add_argument("--next-value", default="next sprint")
    p.set_defaults(func=cmd_proof_pack)

    p = sub.add_parser("proposal")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--problem", required=True)
    p.set_defaults(func=cmd_proposal)

    p = sub.add_parser("offer")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--problem", required=True)
    p.set_defaults(func=cmd_proposal)

    p = sub.add_parser("outreach")
    p.add_argument("--company", required=True)
    p.add_argument("--sector", required=True)
    p.add_argument("--problem", required=True)
    p.set_defaults(func=cmd_outreach)

    p = sub.add_parser("dashboard")
    p.set_defaults(func=cmd_dashboard)

    p = sub.add_parser("monthly-review")
    p.set_defaults(func=cmd_monthly_review)

    return parser

def main():
    DATA.mkdir(parents=True, exist_ok=True)
    ensure_ledgers()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()