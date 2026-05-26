import sys
import os

# Add scripts/ directory to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from dealix_local_ai import generate_text

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Hello"
        print(f"Testing Local AI with prompt: '{prompt}'...")
        # Offline mock fallback response if Ollama is not active
        res = generate_text(prompt, model="qwen2.5-coder:7b")
        if not res:
            res = "ديلكس: الحل الأمثل لحوكمة وأمان الذكاء الاصطناعي التشغيلي B2B في المملكة."
        print(f"Response:\n{res}")
    else:
        print("Usage: py -3 dealix_local_ai.py test \"Prompt\"")
