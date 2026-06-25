export const commercialCommandSnapshot = {
  mode: "draft_only",
  ownerReviewRequired: true,
  targetsLoaded: 20,
  packsGenerated: 20,
  priorityQueue: [
    {
      company_name: "Salla",
      sector: "b2b_services",
      priority_value: 80,
      priority: "P1",
      recommended_offer: "Revenue Command Room OS",
      reason: "sector_fit, source_ok, pain_ready, review_ready"
    },
    {
      company_name: "Dr. Sulaiman Al Habib Medical Group",
      sector: "clinics",
      priority_value: 80,
      priority: "P1",
      recommended_offer: "Follow-up Recovery OS",
      reason: "sector_fit, source_ok, pain_ready, review_ready"
    },
    {
      company_name: "ROSHN",
      sector: "real_estate",
      priority_value: 80,
      priority: "P1",
      recommended_offer: "Revenue Command Room OS",
      reason: "sector_fit, source_ok, pain_ready, review_ready"
    }
  ],
  packs: [],
  commands: [
    "python scripts/commercial/run_sales_agent_company_brain_day.py",
    "python scripts/commercial/prepare_review_actions.py",
    "python scripts/commercial/generate_command_room_snapshot.py",
    "python scripts/saas/run_commercial_launch_day.py"
  ]
} as const;
