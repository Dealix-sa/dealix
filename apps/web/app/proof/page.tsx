import { FounderShell } from "../../components/founder-shell";
import { getProofLibrary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProofPage() {
  const library = await getProofLibrary();
  return (
    <FounderShell>
      <main>
        <h1>Proof</h1>
        <p>Proof library, case studies, evidence packs, citation count.</p>
        <section className="founder-metric-grid">
          <div className="founder-metric">
            <p className="founder-metric__label">Library Entries</p>
            <p className="founder-metric__value">{library.length}</p>
          </div>
        </section>
        {library.length === 0 ? (
          <p className="founder-source" style={{ marginTop: 16 }}>
            No proof entries yet. Source: <code>/api/v1/internal/proof/library</code>.
          </p>
        ) : null}
      </main>
    </FounderShell>
  );
}
