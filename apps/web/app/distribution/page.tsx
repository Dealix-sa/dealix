import {
  ConsolePage,
  PlaceholderTable,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { StatusBadge } from "../../components/brand/StatusBadge";
import { loadInternal } from "../../lib/runtime-client";

type DistributionSummary = {
  outbound_drafts: number | null;
  approved_today: number | null;
  queued_linkedin: number | null;
  queued_email: number | null;
  queued_contact_forms: number | null;
  follow_ups_open: number | null;
};

const machines = [
  "outbound_draft_machine",
  "linkedin_queue_machine",
  "email_draft_machine",
  "contact_form_queue_machine",
  "follow_up_machine",
  "reply_router_machine",
  "nurture_machine",
  "partner_referral_machine",
  "abm_strategic_account_machine",
  "proof_to_demand_machine",
];

export default async function DistributionPage() {
  const payload = await loadInternal<DistributionSummary>(
    "/api/v1/internal/founder/distribution",
    {
      outbound_drafts: null,
      approved_today: null,
      queued_linkedin: null,
      queued_email: null,
      queued_contact_forms: null,
      follow_ups_open: null,
    }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/distribution"
      title="Distribution War Machine"
      subtitle="Drafts, queues, follow-ups — never auto-sent"
      source={payload.source}
      intro={
        <p style={{ color: "var(--dx-text-secondary)", margin: 0 }}>
          Every machine drafts, queues, recommends. No machine sends, posts, or
          publishes externally. All external action requires a recorded A2
          approval.
        </p>
      }
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Outbound drafts" value={fmt(payload.data.outbound_drafts)} />
        <MetricCard label="Approved today" value={fmt(payload.data.approved_today)} />
        <MetricCard label="Follow-ups open" value={fmt(payload.data.follow_ups_open)} />
        <MetricCard label="Queued LinkedIn" value={fmt(payload.data.queued_linkedin)} />
        <MetricCard label="Queued email" value={fmt(payload.data.queued_email)} />
        <MetricCard label="Queued contact forms" value={fmt(payload.data.queued_contact_forms)} />
      </div>

      <SectionHeading title="Machines" />
      <BrandCard>
        <table className="dx-table">
          <thead>
            <tr>
              <th>Machine</th>
              <th>Approval class</th>
              <th>External action</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((m) => (
              <tr key={m}>
                <td>{m}</td>
                <td>
                  <StatusBadge tone="a2">A2</StatusBadge>
                </td>
                <td>
                  <StatusBadge tone="warning">never auto</StatusBadge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </BrandCard>

      <SectionHeading title="Draft queue" />
      <BrandCard>
        <PlaceholderTable
          columns={["Channel", "Account", "Owner", "Score", "Created", "Status"]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
