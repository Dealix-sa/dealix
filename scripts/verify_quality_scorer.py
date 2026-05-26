import sys
from dealix_local_ai import generate_text

def score_quality(text: str) -> bool:
    """
    Quality Scorer to reject bad outreach templates before they reach governance or humans.
    Returns True if valid, False if rejected.
    """
    
    bad_phrases = [
        "عزيزي العميل",
        "عزيزي سامي",
        "نضمن",
        "امتثال كامل",
        "بدون مخاطر",
        "تقييم مجاني",
        "الأفضل في العالم"
    ]
    
    for phrase in bad_phrases:
        if phrase in text:
            print(f"[Quality Scorer] REJECTED: Contains forbidden phrase '{phrase}'")
            return False
            
    # Check for basic structure
    if "?" not in text and "؟" not in text:
         print("[Quality Scorer] REJECTED: Missing Call to Action (CTA) question.")
         return False
         
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 verify_quality_scorer.py <text_to_score>")
        sys.exit(1)
        
    text = sys.argv[1]
    is_valid = score_quality(text)
    if is_valid:
        print("PASS")
        sys.exit(0)
    else:
        print("FAIL")
        sys.exit(1)
