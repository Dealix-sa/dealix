export const commercialLaunchControlSnapshot = {
  generated_at: "not_generated_yet",
  company: "Dealix",
  release_name: "Commercial Launch Control",
  release_mode: "founder_led_commercial_launch",
  verdict: "NEEDS_LOCAL_RELEASE_GATE_REVIEW",
  launch_products: [
    "Revenue Command Room OS",
    "Company Brain OS",
    "Follow-up Recovery OS",
    "Client Delivery OS",
    "AI Trust and Governance OS"
  ],
  commercial_sprint_packages: [
    { name: "AI Revenue Diagnostic", price_range_sar: "0-1500", duration: "1-3 days", goal: "turn a company pain into a scoped sprint" },
    { name: "7-Day Revenue Command Room Sprint", price_range_sar: "5000-12000", duration: "7 days", goal: "build the first revenue command room and daily queue" },
    { name: "14-Day Company Brain Sprint", price_range_sar: "15000-35000", duration: "14 days", goal: "build decision desk, risk radar, and board memo workflow" }
  ],
  operating_reports: [],
  targets_loaded: 0,
  packs_generated: 0,
  founder_actions: [],
  proof_metrics: {},
  founder_next_actions: [
    "Run Startup OS Release Gate locally.",
    "Run apps/web verification locally.",
    "Review top P1 accounts.",
    "Prepare three discovery notes.",
    "Create one scoped diagnostic proposal only after qualification."
  ],
  merge_order: [
    "Review database foundation first.",
    "Rebase commercial launch pack on updated main.",
    "Run Startup OS Release Gate.",
    "Run apps/web verifier.",
    "Resolve conflicts and merge."
  ],
  launch_guardrails: [
    "review-first external action",
    "no fake ROI",
    "no fake testimonials",
    "source_url required",
    "proof pack required after every paid sprint"
  ]
} as const;
