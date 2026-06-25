export const founderDailyBriefSnapshot = {
  generated_at: "not_generated_yet",
  mode: "founder_led_review_first",
  executive_decision: "Run Startup OS Day, review top accounts, and prepare one scoped diagnostic proposal after qualification.",
  targets_loaded: 0,
  packs_generated: 0,
  products: [],
  top_accounts: [],
  founder_actions: [
    "Run python scripts/commercial/run_startup_os_day.py",
    "Open reports/startup_command_center/latest.md",
    "Open reports/founder_daily_brief/latest.md",
    "Review top P1 accounts first",
    "Prepare one scoped proposal only after qualification"
  ],
  hard_rules: [
    "no fake ROI",
    "no fake testimonials",
    "no live outbound by default",
    "source_url required",
    "pain is hypothesis until verified"
  ]
} as const;
