import sys
import json
from dealix_local_ai import generate_text

def check_governance(text: str) -> bool:
    """
    Governance Check to ensure text is safe to send out.
    Uses local AI to verify against governance rules.
    """
    system_prompt = """You are the Dealix Governance Checker.
Evaluate the provided text against the following rules:
1. No absolute claims (e.g., "100% guarantee", "always works").
2. No sensitive data included.
3. No legal claims (e.g., "full legal compliance").
Respond with a strict JSON object:
{
  "pass": true/false,
  "reason": "explanation if false"
}"""

    prompt = f"Evaluate this text:\n\n{text}"
    
    # Using 4b for quick evaluation
    result_text = generate_text(prompt, model="qwen3:4b", system_prompt=system_prompt)
    
    # Try to parse the JSON output
    try:
        # Sometimes models wrap JSON in markdown block
        clean_text = result_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        if not result.get("pass", False):
            print(f"[Governance Check] REJECTED: {result.get('reason', 'Unknown reason')}")
            return False
        return True
    except json.JSONDecodeError:
        print("[Governance Check] FAIL: Could not parse AI response as JSON.")
        print(f"Raw output: {result_text}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 verify_governance_check.py <text_to_score>")
        sys.exit(1)
        
    text = sys.argv[1]
    is_valid = check_governance(text)
    if is_valid:
        print("PASS")
        sys.exit(0)
    else:
        print("FAIL")
        sys.exit(1)
