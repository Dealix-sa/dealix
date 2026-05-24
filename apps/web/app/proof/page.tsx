import { FounderPage } from "../../components/brand/founder-page";

export default function ProofPage() {
  return (
    <FounderPage
      title="Proof System"
      subtitle="Every external claim must trace back to approved evidence."
      blocks={[
        { title: "Approved library", body: <p>proof/proof_library.csv</p> },
        { title: "Approval queue", body: <p>proof/proof_approval_queue.csv</p> },
        { title: "Folder", body: <p>assets/sales/proof_safe/</p> },
      ]}
    />
  );
}
