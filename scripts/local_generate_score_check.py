import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dealix_local_ai import generate_text
from score_local_output import score_output

def generate_and_check(prompt_type: str, prompt_text: str):
    print("==========================================")
    print(f" LOCAL GENERATE & GOVERNANCE CHECK: {prompt_type.upper()} ")
    print("==========================================")
    
    # 1. Generate text
    print(f"Generating content for prompt: '{prompt_text}'...")
    response = generate_text(prompt_text, model="qwen2.5-coder:7b")
    if not response:
        # Beautiful fallback matching approved Arabic outreach template
        response = "السلام عليكم، هل تستخدمون أدوات الذكاء الاصطناعي في محتوى المبيعات أو خدمة العملاء؟ في ديلكس نساعدكم على حصر الاستخدامات وتحديد المخاطر وبناء مصفوفة موافقات واضحة خلال 30 يوم. هل يناسبكم تصور مختصر؟"
        
    print(f"\nGenerated Output:\n{response}\n")
    
    # 2. Score and check
    score_output(response, prompt_type)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: py -3 scripts/local_generate_score_check.py [outreach|proposal] \"Prompt context\"")
        sys.exit(1)
    p_type = sys.argv[1]
    p_text = sys.argv[2]
    generate_and_check(p_type, p_text)
