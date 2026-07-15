from pathlib import Path

required = [
    "DEALIX_STAGE_GATED_ROADMAP.md",
    "DEALIX_30_DAY_EXECUTION_PLAN.md",
    "docs/ops/OPERATING_READINESS_LEVELS.md",
    "docs/founder/GO_NO_GO_DECISION_SYSTEM.md",
    "docs/ai_management/AI_THREAT_MODEL.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 300:
        failures.append(f"Too short: {file}")

checks = {
    "DEALIX_STAGE_GATED_ROADMAP.md": ["Stage 0", "Stage 1", "Revenue Sprint", "SaaS"],
    "DEALIX_30_DAY_EXECUTION_PLAN.md": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "docs/ops/OPERATING_READINESS_LEVELS.md": ["ORL 0", "ORL 9", "A3"],
    "docs/founder/GO_NO_GO_DECISION_SYSTEM.md": ["Go Criteria", "No-Go Criteria"],
    "docs/ai_management/AI_THREAT_MODEL.md": ["Prompt Injection", "Sensitive Information Disclosure"],
}

for file, terms in checks.items():
    path = Path(file)
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in terms:
            if term not in text:
                failures.append(f"{file} missing: {term}")

if failures:
    print("Stage-gated roadmap verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: stage-gated roadmap is ready.")
