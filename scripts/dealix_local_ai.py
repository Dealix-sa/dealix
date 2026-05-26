import json
import urllib.request
import urllib.error
import sys

def generate_text(prompt: str, model: str = "qwen2.5-coder:7b", keep_alive: str = "5m", system_prompt: str = None) -> str:
    """
    Calls the local Ollama API to generate text.
    """
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive
    }
    
    if system_prompt:
        data["system"] = system_prompt

    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "").strip()
    except urllib.error.URLError as e:
        print(f"[Dealix Local AI] Error communicating with Ollama: {e}", file=sys.stderr)
        print("[Dealix Local AI] Please ensure Ollama is running.", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"[Dealix Local AI] Unexpected error: {e}", file=sys.stderr)
        return ""

if __name__ == "__main__":
    # Test script if run directly
    print(generate_text("Hello, say 'Ollama is working' if you hear me.", model="qwen2.5-coder:7b"))
