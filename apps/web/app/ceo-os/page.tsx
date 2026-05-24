import { FounderPage } from "../../components/brand/founder-page";

export default function CeoOsPage() {
  return (
    <FounderPage
      title="CEO Operating System"
      subtitle="Daily, weekly, monthly founder cadence."
      blocks={[
        { title: "Daily", body: <p>CEO Daily Brief · top action · trust · workers · cash.</p> },
        { title: "Weekly", body: <p>CEO Weekly Review · capital allocation · decision log.</p> },
        { title: "Monthly", body: <p>Advisor / board pack · moat scorecard · strategy review.</p> },
        {
          title: "Cadence files",
          body: (
            <ul>
              <li>docs/founder/CEO_DAILY_BRIEF.md</li>
              <li>docs/founder/CEO_WEEKLY_REVIEW.md</li>
              <li>docs/founder/MONTHLY_ADVISOR_UPDATE.md</li>
            </ul>
          ),
        },
      ]}
    />
  );
}
