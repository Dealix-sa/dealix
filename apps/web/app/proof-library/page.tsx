import { FounderPage } from "../../components/brand/founder-page";

export default function ProofLibraryPage() {
  return (
    <FounderPage
      title="Proof Library"
      subtitle="Founder-approved customer results only · forbidden claims are blocked."
      blocks={[
        { title: "Library", body: <p>proof/proof_library.csv</p> },
        { title: "Pending approval", body: <p>proof/proof_approval_queue.csv</p> },
        { title: "Case study candidates", body: <p>proof/case_study_candidates.csv</p> },
        { title: "Demand assets", body: <p>proof/proof_to_demand_assets.csv</p> },
      ]}
    />
  );
}
