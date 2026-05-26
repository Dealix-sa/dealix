import sys

VALID_STAGES = [
    "ready_to_send",
    "outreach_sent",
    "followup_sent",
    "replied_interested",
    "details_sent",
    "call_booked",
    "proposal_sent",
    "invoice_sent",
    "paid",
    "delivery_started",
    "delivery_active",
    "proof_pack_created",
    "retainer_offered",
    "retainer_won",
    "retainer_lost",
    "complete",
    "nurture",
    "lost"
]

# Pipeline progression transitions map
ALLOWED_TRANSITIONS = {
    "ready_to_send": ["outreach_sent", "lost", "nurture"],
    "outreach_sent": ["followup_sent", "replied_interested", "details_sent", "lost", "nurture"],
    "followup_sent": ["replied_interested", "details_sent", "lost", "nurture"],
    "replied_interested": ["call_booked", "proposal_sent", "lost", "nurture"],
    "details_sent": ["call_booked", "proposal_sent", "lost", "nurture"],
    "call_booked": ["proposal_sent", "lost", "nurture"],
    "proposal_sent": ["invoice_sent", "paid", "lost", "nurture"],
    "invoice_sent": ["paid", "delivery_started", "lost"],
    "paid": ["delivery_started", "delivery_active"],
    "delivery_started": ["delivery_active", "proof_pack_created"],
    "delivery_active": ["proof_pack_created", "complete"],
    "proof_pack_created": ["retainer_offered", "complete"],
    "retainer_offered": ["retainer_won", "retainer_lost", "complete"],
    "retainer_won": ["complete"],
    "retainer_lost": ["complete", "nurture"],
    "complete": [],
    "nurture": ["ready_to_send", "outreach_sent"],
    "lost": ["ready_to_send"]
}

def validate_transition(client: str, current: str, target: str):
    print("==========================================")
    print(" PIPELINE STATE MACHINE TRANSITION GUARD ")
    print("==========================================")
    print(f"Client:       {client}")
    print(f"Current state: {current}")
    print(f"Target state:  {target}")
    
    if current not in VALID_STAGES:
        print(f"\n[FAIL] Blocked: Current state '{current}' is invalid.")
        sys.exit(1)
        
    if target not in VALID_STAGES:
        print(f"\n[FAIL] Blocked: Target state '{target}' is invalid.")
        sys.exit(1)
        
    allowed_targets = ALLOWED_TRANSITIONS.get(current, [])
    if target in allowed_targets:
        print(f"\n[PASS] Allowed transition: '{current}' -> '{target}' matches strict B2B operating flow.")
    else:
        print(f"\n[FAIL] Blocked: Transition '{current}' -> '{target}' is illegal under B2B anti-waste policies.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: py -3 scripts/pipeline_status_machine.py \"Client\" current_state target_state")
        sys.exit(1)
        
    client = sys.argv[1]
    curr = sys.argv[2]
    targ = sys.argv[3]
    validate_transition(client, curr, targ)
