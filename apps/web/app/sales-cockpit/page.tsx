import { FounderShell } from "../../components/founder-shell";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

const stages: ReadonlyArray<[keyof Awaited<ReturnType<typeof getSalesFunnel>>, string]> = [
  ["lead_intelligence", "Lead Intelligence"],
  ["a_leads", "A Leads"],
  ["pending_approval", "Pending Approval"],
  ["approved_outreach", "Approved Outreach"],
  ["sent", "Sent"],
  ["replies", "Replies"],
  ["positive_replies", "Positive Replies"],
  ["samples", "Samples"],
  ["proposals", "Proposals"],
  ["payment_capture", "Payment Capture"],
];

export default async function SalesCockpitPage() {
  const funnel = await getSalesFunnel();
  return (
    <FounderShell title="Sales Cockpit">
      <p className="lead">
        Lead intelligence through payment capture. One row per funnel stage.
      </p>
      <section className="card">
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: "8px 4px", borderBottom: "1px solid #e2e8f0" }}>Stage</th>
              <th style={{ textAlign: "right", padding: "8px 4px", borderBottom: "1px solid #e2e8f0" }}>Count</th>
            </tr>
          </thead>
          <tbody>
            {stages.map(([key, label]) => (
              <tr key={key}>
                <td style={{ padding: "8px 4px", borderBottom: "1px solid #f1f5f9" }}>{label}</td>
                <td style={{ padding: "8px 4px", borderBottom: "1px solid #f1f5f9", textAlign: "right" }}>
                  {funnel[key]}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
