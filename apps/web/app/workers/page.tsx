import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";

const WORKERS = [
  "distribution_outbound_draft_worker",
  "distribution_linkedin_queue_worker",
  "distribution_email_draft_worker",
  "distribution_contact_form_worker",
  "distribution_follow_up_worker",
  "distribution_reply_router_worker",
  "distribution_nurture_worker",
  "distribution_partner_referral_worker",
  "distribution_abm_worker",
  "distribution_proof_to_demand_worker",
  "intelligence_account_scoring_worker",
  "intelligence_trigger_ingest_worker",
];

export default function WorkersPage() {
  return (
    <PageShell currentPath="/workers">
      <SectionHeading
        eyebrow="Workers"
        title="Background machines."
        description="Each worker writes to its ledger, never to an external channel. Kill switches available per worker."
      />
      <BrandCard title="Registered workers">
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left" className="dlx-muted" style={{ padding: "8px 4px", fontSize: 12 }}>Worker</th>
              <th align="left" className="dlx-muted" style={{ padding: "8px 4px", fontSize: 12 }}>State</th>
              <th align="left" className="dlx-muted" style={{ padding: "8px 4px", fontSize: 12 }}>Kill switch</th>
            </tr>
          </thead>
          <tbody>
            {WORKERS.map((w) => (
              <tr key={w} style={{ borderTop: "1px solid var(--dlx-border)" }}>
                <td style={{ padding: "10px 4px", fontFamily: "monospace", fontSize: 13 }}>{w}</td>
                <td style={{ padding: "10px 4px" }}><StatusBadge label="idle" tone="neutral" /></td>
                <td style={{ padding: "10px 4px", fontFamily: "monospace", fontSize: 12 }}>
                  DEALIX_{w.toUpperCase()}_ENABLED
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </BrandCard>
    </PageShell>
  );
}
