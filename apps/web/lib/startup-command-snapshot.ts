export const startupCommandSnapshot = {
  generated_at: "not_generated_yet",
  company: "Dealix",
  positioning: "Saudi B2B AI Operating Systems company",
  mode: "founder_led_review_first",
  products: [
    { name: "Revenue Command Room OS", first_offer: "7-Day Revenue Command Room Sprint", setup_range_sar: "5000-12000", retainer_range_sar: "3000-12000", proof: "daily queue, proposal queue, weekly revenue memo" },
    { name: "Company Brain OS", first_offer: "14-Day Company Brain Sprint", setup_range_sar: "15000-35000", retainer_range_sar: "8000-25000", proof: "daily decision, risk radar, board memo" },
    { name: "Follow-up Recovery OS", first_offer: "7-Day Follow-up Recovery Sprint", setup_range_sar: "5000-12000", retainer_range_sar: "3000-10000", proof: "classified follow-up queue and owner report" }
  ],
  targets_loaded: 0,
  packs_generated: 0,
  priority_queue: [],
  review_actions: [],
  commands: [
    "python scripts/commercial/run_command_room_day.py",
    "python scripts/commercial/generate_startup_command_center.py",
    "npm --prefix apps/web run verify"
  ]
} as const;
