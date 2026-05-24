import { FounderPage } from "../../components/brand/founder-page";
import { MetricCard } from "../../components/brand/metric-card";
import { StatusBadge } from "../../components/brand/status-badge";

export default function CeoPage() {
  return (
    <FounderPage
      title="CEO Command Center"
      subtitle="One screen, one decision, one source."
      blocks={[
        {
          title: "Top CEO action",
          body: (
            <>
              <p style={{ margin: 0 }}>
                Approve A-priority outreach drafts for the active beachhead sector.
              </p>
              <a href="/approvals" className="dlx-cta" style={{ marginTop: 8 }}>
                Open approval queue
              </a>
            </>
          ),
        },
        {
          title: "Revenue",
          body: (
            <div className="dlx-grid">
              <MetricCard label="Cash collected" value="—" hint="finance/cash_collected.csv" />
              <MetricCard label="Pipeline" value="—" hint="growth/sector_targets.csv" />
              <MetricCard label="Weighted pipeline" value="—" />
              <MetricCard label="Follow-ups due" value="—" />
            </div>
          ),
        },
        {
          title: "Bottleneck",
          body: <p style={{ margin: 0 }}>Proposals are not converting into payment follow-ups.</p>,
        },
        {
          title: "Trust",
          body: (
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <StatusBadge tone="ok">0 A3 violations</StatusBadge>
              <StatusBadge tone="ok">0 suppression violations</StatusBadge>
              <StatusBadge tone="warn">Evidence missing: 2</StatusBadge>
            </div>
          ),
        },
        {
          title: "Workers",
          body: <p style={{ margin: 0 }}>Stale worker: followup_queue_worker · see /workers</p>,
        },
        {
          title: "Decision needed",
          body: (
            <p style={{ margin: 0 }}>
              Scale the ERP/CRM beachhead, or first repair the cybersecurity message angle?
            </p>
          ),
        },
      ]}
    />
  );
}
