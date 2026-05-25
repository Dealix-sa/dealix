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
        ("Strategy", ROOT / "strategy"),
        ("Core", ROOT / "core"),
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

def cmd_new_client(args):
    slug = slugify(args.slug)
    client = ROOT / "clients" / slug
    client.mkdir(parents=True, exist_ok=True)

    write(client / "CLIENT_PROFILE.md", f"""# Client Profile: {args.name}

Created: {now()}

## Company

{args.name}

## Sector

{args.sector}

## Contact

-

## Business Problem

-

## Current Stage

Lead / Diagnostic / Sprint / Pilot / Retainer / Enterprise

## Notes

-
""")

    write(client / "CAPABILITY_SCORECARD.md", f"""# Capability Scorecard: {args.name}

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
""")

    write(client / "AI_OPERATING_MODEL.md", f"""# Client AI Operating Model: {args.name}

## Business Goals

-

## Use Cases

-

## Data Sources

-

## Human Approval Points

-

## Governance Rules

-

## Reports

-

## Metrics

-

## Operating Cadence

Daily:  
Weekly:  
Monthly:  

## Dealix Role

Diagnostic / Sprint / Pilot / Retainer / Enterprise
""")

    write(client / "EXPANSION_MAP.md", f"""# Expansion Map: {args.name}

## Current Service

-

## Proof Created

-

## Next Best Offers

1.
2.
3.

## Why

-

## Decision Timing

-
""")

    append(ROOT / "ledgers" / "CLIENT_LEDGER.md", f"| C-{datetime.now().strftime('%Y%m%d%H%M%S')} | {args.name} | {args.sector} |  | Lead | New | Run diagnostic | Sami |\n")
    print(f"Created client workspace: {client}")

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

def cmd_assess(args):
    cap, scores = score_problem(args.problem)
    svc_key = recommend_service_for_capability(cap)
    svc = services()[svc_key]
    result = {
        "problem": args.problem,
        "recommended_capability": cap,
        "recommended_service": svc_key,
        "service_name": svc["name"],
        "kpi": svc["kpi"],
        "price_starts_at": svc["price_starts_at"],
        "why": f"The problem appears closest to {cap} capability.",
        "scores": scores
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

def cmd_recommend_sprint(args):
    cap, scores = score_problem(args.problem)
    svc_key = recommend_service_for_capability(cap)
    svc = services()[svc_key]
    print(f"Recommended Sprint: {svc['name']}")
    print(f"Capability: {svc['capability']}")
    print(f"Starts at: SAR {svc['price_starts_at']}")
    print(f"KPI: {svc['kpi']}")
    print(f"Proof Type: {svc['proof_type']}")
    print("")
    print("Deliverables:")
    for d in svc["deliverables"]:
        print(f"- {d}")
    print("")
    print(f"Upsell: {svc['upsell']}")

def cmd_proof(args):
    row = f"| V-{datetime.now().strftime('%Y%m%d%H%M%S')} | {now()} | {args.client} | {args.service} | {args.value_type} | {args.metric} | {args.baseline} | {args.result} | {args.evidence} | {args.next_value} |\n"
    append(ROOT / "ledgers" / "VALUE_LEDGER.md", row)
    print("Value ledger updated.")

def cmd_capital(args):
    row = f"| C-{datetime.now().strftime('%Y%m%d%H%M%S')} | {now()} | {args.project} | {args.capital_type} | {args.asset} | {args.reusable} | Sami | {args.next_use} | Created |\n"
    append(ROOT / "ledgers" / "CAPITAL_LEDGER.md", row)
    print("Capital ledger updated.")

def cmd_ai_run(args):
    row = f"| AI-{datetime.now().strftime('%Y%m%d%H%M%S')} | {now()} | {args.project} | {args.task} | {args.model} | {args.prompt_version} | {args.redacted} | {args.schema} | {args.cost} | {args.qa} | {args.risk} | {args.approval} |\n"
    append(ROOT / "ledgers" / "AI_RUN_LEDGER.md", row)
    print("AI run ledger updated.")

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
    result = governance_check_text(args.text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def cmd_proof_pack(args):
    client_slug = slugify(args.client)
    out = ROOT / "reports" / f"proof-pack-{client_slug}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    svc = services().get(args.service, {"name": args.service, "kpi": args.metric, "proof_type": args.value_type, "upsell": args.next_value})
    text = f"""# Proof Pack: {args.client}

Generated: {now()}

## Service

{svc['name'] if 'name' in svc else args.service}

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

def cmd_outreach(args):
    company = args.company
    sector = args.sector
    problem = args.problem
    cap, _ = score_problem(problem)
    svc_key = recommend_service_for_capability(cap)
    svc = services()[svc_key]

    msg = f"""السلام عليكم،

لاحظت أن {company} تعمل في قطاع {sector}. الفكرة التي أراها مناسبة ليست استخدام AI بشكل عام، بل Sprint قصير يبني قدرة تشغيلية واضحة حول: {problem}

الاقتراح الأولي:
{svc['name']}

الهدف:
{svc['kpi']}

المخرجات:
{chr(10).join("- " + d for d in svc['deliverables'])}

الشيء المهم أن Dealix لا تبني سبام أو وعود مبيعات مبالغ فيها؛ نركز على بيانات جاهزة، workflow واضح، موافقة بشرية، وحزمة إثبات أثر.

إذا مناسب، أقدر أرسل تصور صفحة واحدة للـ Sprint.
"""
    print(msg)

def cmd_offer(args):
    data = services()
    if args.service not in data:
        print(f"Unknown service: {args.service}")
        print("Available:", ", ".join(data.keys()))
        return
    svc = data[args.service]
    out = ROOT / "sales" / "proposals" / f"proposal-{slugify(args.client)}-{args.service}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    text = f"""# Proposal: {svc['name']}

## Client

{args.client}

## Problem

{args.problem}

## Recommended Sprint

{svc['name']}

## Why This Sprint

This sprint targets {svc['capability']} Capability and is designed to produce measurable proof quickly.

## Deliverables

{chr(10).join("- " + d for d in svc['deliverables'])}

## Timeline

{svc['timeline']}

## Success Metric

{svc['kpi']}

## Governance

- Source check
- PII check
- Human approval
- Claim safety
- Audit log
- Proof pack

## Price Starts At

SAR {svc['price_starts_at']}

## Next Step

Run diagnostic call and confirm scope.
"""
    write(out, text)
    print(f"Proposal generated: {out}")

def cmd_dashboard(args):
    print("Dealix Founder Dashboard")
    print("========================")
    ledger_files = [
        "VALUE_LEDGER.md",
        "CAPITAL_LEDGER.md",
        "AI_RUN_LEDGER.md",
        "GOVERNANCE_LEDGER.md",
        "CLIENT_LEDGER.md",
        "PIPELINE_LEDGER.md",
    ]
    for f in ledger_files:
        p = ROOT / "ledgers" / f
        if p.exists():
            rows = [line for line in p.read_text(encoding="utf-8").splitlines() if line.startswith("|") and not line.startswith("|---")]
            count = max(0, len(rows) - 1)
            print(f"{f:24} {count} entries")
        else:
            print(f"{f:24} missing")
    print("")
    print("Next founder questions:")
    print("1. What did we sell?")
    print("2. What proof did we create?")
    print("3. What asset did we add?")
    print("4. What risk did we control?")
    print("5. What can become a product module?")

def cmd_score(args):
    cap, scores = score_problem(args.problem)
    print(f"Problem: {args.problem}")
    print(f"Recommended Capability: {cap}")
    print("Scores:")
    for capability, score in scores.items():
        print(f"  - {capability}: {score}")

def cmd_client_pack(args):
    client_slug = slugify(args.client)
    client_dir = ROOT / "clients" / client_slug
    if not client_dir.exists():
        print(f"Client '{args.client}' not found.")
        return

    profile_path = client_dir / "CLIENT_PROFILE.md"
    scorecard_path = client_dir / "CAPABILITY_SCORECARD.md"
    ai_model_path = client_dir / "AI_OPERATING_MODEL.md"
    expansion_map_path = client_dir / "EXPANSION_MAP.md"

    print(f"# Client Pack: {args.client}")
    print("==========================")

    if profile_path.exists():
        print("\n## Client Profile")
        print(profile_path.read_text(encoding="utf-8"))
    else:
        print("\n## Client Profile (Not Found)")

    if scorecard_path.exists():
        print("\n## Capability Scorecard")
        print(scorecard_path.read_text(encoding="utf-8"))
    else:
        print("\n## Capability Scorecard (Not Found)")

    if ai_model_path.exists():
        print("\n## AI Operating Model")
        print(ai_model_path.read_text(encoding="utf-8"))
    else:
        print("\n## AI Operating Model (Not Found)")

    if expansion_map_path.exists():
        print("\n## Expansion Map")
        print(expansion_map_path.read_text(encoding="utf-8"))
    else:
        print("\n## Expansion Map (Not Found)")

def cmd_value(args):
    print("Value command executed.")
    print("This command is intended to interact with value-related data and operations.")
    print("For now, it serves as a placeholder.")
    value_ledger_path = ROOT / "ledgers" / "VALUE_LEDGER.md"
    if value_ledger_path.exists():
        print("\n--- Value Ledger ---")
        print(value_ledger_path.read_text(encoding="utf-8"))
    else:
        print("\nValue ledger not found.")

def cmd_proposal(args):
    print("Proposal command executed.")
    print("This command is intended to generate client proposals.")
    # Re-using cmd_offer for proposal generation as per the task's implied structure
    cmd_offer(argparse.Namespace(client=args.client, service=args.service, problem=args.problem))

def cmd_monthly_review(args):
    print("Dealix Monthly Review")
    print("=====================")
    print(f"Review Period: {args.period}")

    print("\nSummary:")
    print("- Key Performance Indicators (KPIs) will be displayed here.")
    print("- Client progress and value delivered will be summarized.")
    print("- Strategic recommendations for the next month will be provided.")

    print("\nLedger Snapshots:")
    ledger_files = [
        "VALUE_LEDGER.md",
        "CLIENT_LEDGER.md",
        "PIPELINE_LEDGER.md",
        "CAPITAL_LEDGER.md",
        "AI_RUN_LEDGER.md",
        "GOVERNANCE_LEDGER.md",
    ]
    for f in ledger_files:
        p = ROOT / "ledgers" / f
        if p.exists():
            rows = [line for line in p.read_text(encoding="utf-8").splitlines() if line.startswith("|") and not line.startswith("|---")]
            count = max(0, len(rows) - 1)
            print(f"- {f:24}: {count} entries")
        else:
            print(f"- {f:24}: missing")

    print("\nStrategic Recommendations:")
    print("- Focus on deepening client relationships.")
    print("- Identify opportunities for service expansion.")
    print("- Continuously improve AI operating models.")

def main():
    parser = argparse.ArgumentParser(prog="dealix", description="Dealix Founder OS CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor")

    p = sub.add_parser("services")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("capabilities")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("new-client")
    p.add_argument("slug")
    p.add_argument("--name", required=True)
    p.add_argument("--sector", default="Unknown")

    p = sub.add_parser("assess")
    p.add_argument("problem")

    p = sub.add_parser("recommend-sprint")
    p.add_argument("problem")

    p = sub.add_parser("proof")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--value-type", required=True)
    p.add_argument("--metric", required=True)
    p.add_argument("--baseline", default="unknown")
    p.add_argument("--result", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--next-value", required=True)

    p = sub.add_parser("capital")
    p.add_argument("--project", required=True)
    p.add_argument("--capital-type", required=True)
    p.add_argument("--asset", required=True)
    p.add_argument("--reusable", default="Yes")
    p.add_argument("--next-use", required=True)

    p = sub.add_parser("ai-run")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--model", default="deepseek/deepseek-chat")
    p.add_argument("--prompt-version", default="v1.0")
    p.add_argument("--redacted", default="Yes")
    p.add_argument("--schema", default="Markdown")
    p.add_argument("--cost", default="0")
    p.add_argument("--qa", default="0")
    p.add_argument("--risk", default="Medium")
    p.add_argument("--approval", default="Required")

    p = sub.add_parser("governance-check")
    p.add_argument("text")

    p = sub.add_parser("proof-pack")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--value-type", required=True)
    p.add_argument("--metric", required=True)
    p.add_argument("--baseline", default="unknown")
    p.add_argument("--result", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--next-value", required=True)

    p = sub.add_parser("outreach")
    p.add_argument("--company", required=True)
    p.add_argument("--sector", required=True)
    p.add_argument("--problem", required=True)

    p = sub.add_parser("offer")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--problem", required=True)

    p = sub.add_parser("score")
    p.add_argument("problem")

    p = sub.add_parser("client-pack")
    p.add_argument("--client", required=True)

    p = sub.add_parser("value")
    # Add arguments for value command if needed in the future

    p = sub.add_parser("proposal")
    p.add_argument("--client", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--problem", required=True)

    p = sub.add_parser("monthly-review")
    p.add_argument("--period", default="current")

    sub.add_parser("dashboard")

    args = parser.parse_args()

    if args.cmd == "doctor":
        cmd_doctor(args)
    elif args.cmd == "services":
        cmd_services(args)
    elif args.cmd == "capabilities":
        cmd_capabilities(args)
    elif args.cmd == "new-client":
        cmd_new_client(args)
    elif args.cmd == "assess":
        cmd_assess(args)
    elif args.cmd == "recommend-sprint":
        cmd_recommend_sprint(args)
    elif args.cmd == "proof":
        cmd_proof(args)
    elif args.cmd == "capital":
        cmd_capital(args)
    elif args.cmd == "ai-run":
        cmd_ai_run(args)
    elif args.cmd == "governance-check":
        cmd_governance_check(args)
    elif args.cmd == "proof-pack":
        cmd_proof_pack(args)
    elif args.cmd == "outreach":
        cmd_outreach(args)
    elif args.cmd == "offer":
        cmd_offer(args)
    elif args.cmd == "score":
        cmd_score(args)
    elif args.cmd == "client-pack":
        cmd_client_pack(args)
    elif args.cmd == "value":
        cmd_value(args)
    elif args.cmd == "proposal":
        cmd_proposal(args)
    elif args.cmd == "monthly-review":
        cmd_monthly_review(args)
    elif args.cmd == "dashboard":
        cmd_dashboard(args)

if __name__ == "__main__":
    main()
