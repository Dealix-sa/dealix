import { FounderPage } from "../../components/brand/founder-page";
import { StatusBadge } from "../../components/brand/status-badge";

const WORKERS = [
  "outreach_queue_worker",
  "followup_queue_worker",
  "payment_capture_worker",
  "proposal_drafter",
  "sample_pack_drafter",
  "campaign_factory",
  "lead_intelligence_collector",
  "trust_monitor",
];

export default function WorkersPage() {
  return (
    <FounderPage
      title="Workers / Machines"
      subtitle="Every machine is registered, observable, and has a kill switch."
      blocks={[
        {
          title: "Registered workers",
          body: (
            <table className="dlx-table">
              <thead>
                <tr><th>Worker</th><th>State</th><th>Kill switch</th></tr>
              </thead>
              <tbody>
                {WORKERS.map((w) => (
                  <tr key={w}>
                    <td>{w}</td>
                    <td><StatusBadge tone="ok">healthy</StatusBadge></td>
                    <td><code>scripts/update_worker_state.py</code></td>
                  </tr>
                ))}
              </tbody>
            </table>
          ),
        },
        { title: "State file", body: <p>runtime/worker_state.csv</p> },
      ]}
    />
  );
}
