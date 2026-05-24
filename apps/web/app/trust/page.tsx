import { FounderPage } from "../../components/brand/founder-page";
import { StatusBadge } from "../../components/brand/status-badge";

export default function TrustPage() {
  return (
    <FounderPage
      title="Trust"
      subtitle="Founder-approved actions only · forbidden claims blocked · evidence preserved."
      blocks={[
        {
          title: "Active gates",
          body: (
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <StatusBadge tone="ok">block_a3_auto_send</StatusBadge>
              <StatusBadge tone="ok">block_unapproved_payment_capture</StatusBadge>
              <StatusBadge tone="ok">block_outbound_without_consent_check</StatusBadge>
              <StatusBadge tone="ok">block_guaranteed_claims</StatusBadge>
              <StatusBadge tone="ok">enforce_suppression_list</StatusBadge>
            </div>
          ),
        },
        { title: "Ledgers", body: <p>trust/approval_decisions.csv · trust/trust_flags.csv · trust/incidents.csv</p> },
        { title: "Customer trust packet", body: <p>trust/customer_trust_packet.csv</p> },
      ]}
    />
  );
}
