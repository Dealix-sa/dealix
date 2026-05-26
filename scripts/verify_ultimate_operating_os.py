import os
import sys
import subprocess
import json

# Force UTF-8 encoding on standard streams to prevent Windows cp1252 encoding crashes
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Try importing rich for coloring
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console(force_terminal=True, color_system="auto")
except ImportError:
    class DummyConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = DummyConsole()

def run_step(cmd, desc):
    console.print(f"\n[bold yellow]🔄 STEP: {desc}[/bold yellow]")
    console.print(f"[dim]Command: {' '.join(cmd)}[/dim]")
    
    new_env = os.environ.copy()
    new_env["PYTHONIOENCODING"] = "utf-8"
    
    # We specify encoding='utf-8' to prevent cp1252 decoding crashes on Windows
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True, env=new_env, encoding="utf-8")
    if result.returncode != 0:
        console.print(f"[bold red]❌ FAILED: {desc}[/bold red]")
        console.print(f"[red]Error Output:[/red]\n{result.stderr}")
        console.print(f"[red]Standard Output:[/red]\n{result.stdout}")
        sys.exit(1)
        
    console.print(f"[bold green]✅ SUCCESS: {desc}[/bold green]")
    if result.stdout:
        console.print(result.stdout.strip())

def main():
    console.print(
        Panel.fit(
            "[bold green][Dealix] Dealix B2B Executive OS — Comprehensive Lifecycle Verification[/bold green]\n"
            "[dim]Simulating complete prospect-to-retainer loop for client: 'Al-Majd Group'[/dim]",
            border_style="green"
        )
    )
    
    client_name = "Al-Majd Group"
    
    # Pre-verification: clean up any legacy entries for Al-Majd Group to ensure idempotency
    prospects_file = os.path.join("data", "ledgers", "prospects.json")
    if os.path.exists(prospects_file):
        with open(prospects_file, "r", encoding="utf-8") as f:
            try:
                prospects = json.load(f)
            except Exception:
                prospects = []
        prospects = [p for p in prospects if p.get("company", "").lower() != client_name.lower()]
        with open(prospects_file, "w", encoding="utf-8") as f:
            json.dump(prospects, f, indent=2, ensure_ascii=False)
            
    # 1. Run Launch readiness gate
    run_step(
        ["powershell", "-File", "scripts/dealix-launch-mode.ps1"],
        "Launch Readiness Verification Gate"
    )
    
    # 2. Mark lead as outreach_sent (no literal double quotes in the passed string itself)
    run_step(
        ["py", "-3", "scripts/mark_lead.py", "Al-Majd Group", "outreach_sent", "First outbound intro sent"],
        "Mark Lead as Outreach Sent"
    )
    
    # 3. Triage customer reply
    run_step(
        ["py", "-3", "scripts/triage_reply.py", "أهلاً سامي، مهتمين جداً ونرغب في معرفة الأسعار والتشخيص"],
        "Triage Inbound Arabic Reply"
    )
    
    # 4. Book discovery call
    run_step(
        ["py", "-3", "scripts/new_discovery_call.py", "Al-Majd Group"],
        "Book Discovery Call & Generate Agenda Template"
    )
    
    # 5. Generate tailored Arabic Proposal
    run_step(
        ["py", "-3", "scripts/proposal_from_lead.py", "Al-Majd Group"],
        "Draft tailored Arabic Proposal"
    )
    
    # 6. Kickoff paid delivery / send invoice
    run_step(
        ["powershell", "-File", "scripts/start_paid_delivery.ps1", "-Client", "Al-Majd Group", "-Offer", "ai-trust", "-Amount", "5000"],
        "Initiate Paid Delivery & Invoice Send"
    )
    
    # 7. Confirm payment received
    run_step(
        ["powershell", "-File", "scripts/confirm_payment.ps1", "-Client", "Al-Majd Group"],
        "Confirm Payment Cleared & Transition State"
    )
    
    # 8. Complete sprint delivery & compile Proof Pack
    run_step(
        ["powershell", "-File", "scripts/complete_delivery.ps1", "-Client", "Al-Majd Group", "-Offer", "ai-trust"],
        "Complete Sprint Delivery, Log Proof and Offer Retainer"
    )
    
    # 9. Verify CLI status command integrity
    run_step(
        ["py", "-3", "dealix.py", "status"],
        "CLI dealix status Command Integrity Check"
    )
    
    # 10. Run CEO command readout
    run_step(
        ["py", "-3", "dealix.py", "ceo-review"],
        "CLI dealix ceo-review Command Check"
    )

    console.print("\n[bold green]🏆 Dealix is officially operating at maximum maturity! All systems green.[/bold green]")

if __name__ == "__main__":
    main()
