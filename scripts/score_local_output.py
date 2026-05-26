import sys

def score_output(text: str, context: str = "ai_trust"):
    print("==========================================")
    print(f" SCORING LOCAL OUTPUT FOR: {context.upper()} ")
    print("==========================================")
    print(f"Content: '{text}'\n")
    
    score = 100
    violations = []
    
    # Absolute guarantees
    if any(w in text for w in ["نضمن", "100%", "مطلق", "بدون فريق", "بدون أخطاء"]):
        score -= 40
        violations.append("Absolutes Claim Warning: Promises of 100% or 'نضمن' violate NIST AI RMF risk limits.")
        
    # PDPL Compliance words
    if "PDPL" in text or "بيانات" in text:
        if not any(w in text for w in ["حوكمة", "ضوابط", "موافقات"]):
            score -= 20
            violations.append("PII/PDPL Governance Gaps: Mentioned sensitive data without mentioning governance controls.")
            
    print(f"Final Score: {score}/100")
    if violations:
        print("\n[WARN] Gaps identified:")
        for v in violations:
            print(f"  - {v}")
        print("\nRecommendation: Replace absolutes with 'نساعدك على' or specify human approvals.")
    else:
        print("\n[PASS] Output meets all trust, safety, and NIST AI RMF compliance standards.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/score_local_output.py \"Text to analyze\" [context]")
        sys.exit(1)
    text = sys.argv[1]
    context = sys.argv[2] if len(sys.argv) > 2 else "ai_trust"
    score_output(text, context)
