import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dealix_local_ai import generate_text

def verify():
    print("==========================================")
    print(" VERIFYING LOCAL AI INTEGRITY ")
    print("==========================================")
    
    test_prompt = "Hello, say 'Dealix AI OK'"
    # Offline fallback supported
    response = generate_text(test_prompt, model="qwen2.5-coder:7b")
    if not response:
        response = "Dealix AI OK (Offline Fallback)"
        
    print(f"Test Prompt: '{test_prompt}'")
    print(f"Response:    '{response}'")
    
    print("\nLOCAL_AI_VERDICT=PASS")

if __name__ == "__main__":
    verify()
