export const commercialLaunchControlSnapshot = {
  "generated_at": "2026-06-30T11:35:56.673598+00:00",
  "company": "Dealix",
  "release_name": "Commercial Launch Control",
  "release_mode": "founder_led_commercial_launch",
  "verdict": "READY_FOR_FOUNDER_LED_COMMERCIAL_SPRINT",
  "launch_products": [
    "Revenue Command Room OS",
    "Company Brain OS",
    "Follow-up Recovery OS",
    "Client Delivery OS",
    "AI Trust and Governance OS"
  ],
  "commercial_sprint_packages": [
    {
      "name": "AI Revenue Diagnostic",
      "price_range_sar": "0-1500",
      "duration": "1-3 days",
      "goal": "turn a company pain into a scoped sprint"
    },
    {
      "name": "7-Day Revenue Command Room Sprint",
      "price_range_sar": "5000-12000",
      "duration": "7 days",
      "goal": "build the first revenue command room and daily queue"
    },
    {
      "name": "14-Day Company Brain Sprint",
      "price_range_sar": "15000-35000",
      "duration": "14 days",
      "goal": "build decision desk, risk radar, and board memo workflow"
    },
    {
      "name": "Monthly Managed OS",
      "price_range_sar": "3000-25000 monthly",
      "duration": "monthly",
      "goal": "operate and improve the client system with proof packs"
    }
  ],
  "operating_reports": [
    {
      "path": "reports/startup_release_gate/latest.json",
      "status": "PASS"
    },
    {
      "path": "reports/startup_command_center/latest.json",
      "status": "PASS"
    },
    {
      "path": "reports/founder_daily_brief/latest.json",
      "status": "PASS"
    },
    {
      "path": "reports/startup_proof_pack/latest.json",
      "status": "PASS"
    }
  ],
  "targets_loaded": 0,
  "packs_generated": 0,
  "founder_actions": [
    "Run `python3 scripts/dealix_founder_daily_brief.py` for today's brief.",
    "Review top P1 accounts in the pipeline.",
    "Send first warm-intro WhatsApp via dealix_first_warm_intros.py"
  ],
  "proof_metrics": {
    "service_offerings_count": 17,
    "wave13_verified": true,
    "hard_gates_immutable": true
  },
  "founder_next_actions": [
    "Finish or merge the database foundation before merging the commercial launch pack.",
    "Run Startup OS Release Gate locally.",
    "Run apps/web verification locally.",
    "Review top P1 accounts and prepare three discovery notes.",
    "Create one scoped diagnostic proposal only after qualification.",
    "Keep every sensitive external action owner-reviewed."
  ],
  "merge_order": [
    "Review and finish PR 787 first if it remains open",
    "Rebase PR 788 on updated main",
    "Run Startup OS Release Gate",
    "Run apps/web verifier",
    "Resolve conflicts and only then merge PR 788"
  ],
  "launch_guardrails": [
    "review-first external action",
    "no fake ROI",
    "no fake testimonials",
    "no guaranteed revenue claim",
    "source_url required",
    "pain remains a hypothesis until verified",
    "proof pack required after every paid sprint"
  ]
} as const;
