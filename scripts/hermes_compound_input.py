import sys
import os
import subprocess

def process_compound(input_text: str):
    print("==========================================")
    print(" PROCESSING COMPOUND MARKET SIGNAL ")
    print("==========================================")
    print(f"Raw Input: '{input_text}'\n")
    
    # 1. Parse signal and log signal
    cmd_signal = [
        sys.executable,
        os.path.join("scripts", "hermes_capture_signal.py"),
        "--source", "compound_input",
        "--sector", "Logistics",
        "--text", input_text,
        "--why", "TGA National Address Mandate",
        "--offer", "Delivery Accuracy Sprint",
        "--first-action", "send outreach"
    ]
    
    # 2. Add opportunity
    cmd_radar = [
        sys.executable,
        os.path.join("scripts", "hermes_opportunity_radar.py")
    ]
    
    try:
        subprocess.run(cmd_signal, check=True)
        subprocess.run(cmd_radar, check=True)
        print("\nCompound processing successfully completed. Market signal translated to active pipeline wedge.")
    except subprocess.CalledProcessError as e:
        print(f"Error processing compound input: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_val = sys.argv[1] if len(sys.argv) > 1 else "أعلنت هيئة النقل عن تطبيق التحقق الإلزامي من العنوان الوطني للطرود."
    process_compound(test_val)
