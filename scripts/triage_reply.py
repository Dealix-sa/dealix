import sys
import json
import os
from datetime import datetime, timezone

# Add rich import if available
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console(force_terminal=True, color_system="auto")
except ImportError:
    class DummyConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = DummyConsole()

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")

def triage_reply(reply_text: str):
    """
    Classifies a customer reply into BANT / Objection categories:
    price_question, details_requested, call_interest, not_now, uses_ai, unknown
    """
    reply_lower = reply_text.lower()
    
    # 1. Rule-based parsing
    category = "unknown"
    reason = "Categorized via rule-based heuristics."
    suggested_reply = ""
    suggested_next_step = ""
    
    # Call interest keywords
    if any(w in reply_lower for w in ["مكالمة", "اجتماع", "رقم", "رقمي", "اتصال", "تواصل", "كلمني", "رابط", "calendly", "call", "meet"]):
        category = "call_interest"
        reason = "Prospect expressed interest in booking a call or meeting."
        suggested_reply = "ممتاز، هذا رابط حجز مكالمة سريعة لمدة 15 دقيقة لنستعرض التفاصيل المناسبة لعملكم: https://calendly.com/sami-assiri11/dealix-demo"
        suggested_next_step = "Book discovery call: py -3 scripts/new_discovery_call.py \"<Company>\""
        
    # Price question keywords
    elif any(w in reply_lower for w in ["سعر", "كم", "تكلفة", "بكم", "السعر", "الاسعار", "باقة", "باقات", "price", "cost"]):
        category = "price_question"
        reason = "Prospect asked about pricing or packages."
        suggested_reply = "الاستثمار يبدأ من 5,000 ريال لنسخة الـ Starter و 10,000-18,000 ريال للـ Standard، تشمل مخرجات كاملة وتسليم Proof Pack خلال 14 يوماً. هل يناسبكم تصور مختصر؟"
        suggested_next_step = "Mark details sent: py -3 scripts/mark_lead.py \"<Company>\" details_sent"
        
    # Details requested keywords
    elif any(w in reply_lower for w in ["تفاصيل", "معلومات", "شرح", "تصور", "ارسل", "أرسل", "details", "info"]):
        category = "details_requested"
        reason = "Prospect requested details or technical overview."
        suggested_reply = "أهلاً بك، يسعدني إرسال تصور مختصر يوضح كيف نساعد عملائنا على حوكمة استخدام الـ AI وتجنب مخاطر تسريب البيانات خلال 30 يوم. هل أرسله هنا أم عبر البريد؟"
        suggested_next_step = "Mark details sent: py -3 scripts/mark_lead.py \"<Company>\" details_sent"
        
    # Not now keywords
    elif any(w in reply_lower for w in ["ليس الآن", "بعدين", "مشغول", "غير مهتم", "not now", "later"]):
        category = "not_now"
        reason = "Prospect postponed the conversation."
        suggested_reply = "أتفهم تماماً. هل مناسب أن أتواصل معك بعد شهر لمتابعة المستجدات؟"
        suggested_next_step = "Mark lead as nurture: py -3 scripts/mark_lead.py \"<Company>\" nurture"

    # Default interested matching
    elif any(w in reply_lower for w in ["مهتم", "مهتمين", "أهلاً", "اهلا", "مرحبا", "سلام", "interested"]):
        category = "call_interest"
        reason = "Prospect showed general interest or positive response."
        suggested_reply = "أهلاً بك، يسعدنا اهتمامك. ما هو الوقت المناسب لمكالمة قصيرة نوضح فيها آلية التشخيص؟"
        suggested_next_step = "Book discovery call: py -3 scripts/new_discovery_call.py \"<Company>\""
        
    else:
        category = "unknown"
        reason = "Could not confidently classify. Defaulting to general info query."
        suggested_reply = "أهلاً بك، شكراً لردك. يسعدني الإجابة على أي استفسار لديكم حول Dealix لتنظيم وحوكمة الـ AI."
        suggested_next_step = "Mark lead as replied: py -3 scripts/mark_lead.py \"<Company>\" replied_interested"

    # Print beautiful panel
    result_panel = (
        f"[bold cyan]📥 Inbound Reply Triaged:[/bold cyan]\n"
        f"  [bold]Text:[/bold] '{reply_text}'\n"
        f"  [bold]Category:[/bold] [yellow]{category}[/yellow]\n"
        f"  [bold]Reason:[/bold] {reason}\n\n"
        f"[bold green]Suggested Reply Draft (Saudi Arabic):[/bold green]\n"
        f"  \"{suggested_reply}\"\n\n"
        f"[bold magenta]Recommended Next Command:[/bold magenta]\n"
        f"  {suggested_next_step}"
    )
    
    console.print(Panel(result_panel, title="Dealix Objection & Reply Triage", border_style="cyan"))
    
    # Save reply handling details to reply_handling_log.md for history audit
    log_file = os.path.join("docs", "ops", "reply_handling_log.md")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n| {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} | {category} | {reply_text[:50]}... | {category} triage complete. |\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/triage_reply.py \"<reply text>\"")
        sys.exit(1)
        
    reply = sys.argv[1]
    triage_reply(reply)
