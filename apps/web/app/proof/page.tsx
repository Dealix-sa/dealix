import { FounderShell } from "../../components/founder-shell";
import { getProofLibrary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProofPage() {
  const proofs = await getProofLibrary();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Proof</h1>
        <p className="mt-2 max-w-3xl">
          Case studies, evidence packs, and outcomes Sami can show to
          new prospects. Empty until a delivery completes.
        </p>
        <section className="mt-8 rounded-2xl border p-6">
          {proofs.length === 0 ? (
            <p>No proof artefacts yet. Run a delivery to populate the library.</p>
          ) : (
            <ul className="grid gap-3">
              {proofs.map((proof) => (
                <li key={proof.id} className="rounded-xl border p-4">
                  <p className="font-semibold">{proof.title}</p>
                  <p className="text-sm">Customer: {proof.customer}</p>
                  <p>{proof.outcome}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
        <p className="mt-6 text-xs">
          Source: proof_library · Endpoint: /api/v1/internal/proof/library
        </p>
      </main>
    </FounderShell>
  );
}
