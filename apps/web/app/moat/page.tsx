import { FounderPage } from "../../components/brand/founder-page";

export default function MoatPage() {
  return (
    <FounderPage
      title="Moat Scorecard"
      subtitle="Data moat · proof moat · partner moat · sector knowledge moat."
      blocks={[
        { title: "Scorecard", body: <p>docs/moat/MOAT_SCORECARD.md</p> },
        { title: "Data moat", body: <p>docs/data/DATA_MOAT.md</p> },
        { title: "Verifier", body: <p><code>scripts/verify_scale_moat_system.py</code></p> },
      ]}
    />
  );
}
