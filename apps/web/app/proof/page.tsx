import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getProofLibrary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProofPage() {
  const data = await getProofLibrary();
  return (
    <FounderShell
      title={`Proof Library (${data.count})`}
      subtitle="Proof artefacts are never auto-published. Publishing is an A2 action requiring founder approval."
      source={data.source}
    >
      <DataTable columns={["proof_id", "customer", "kind", "status", "approved_by", "updated_at"]} rows={data.items} />
    </FounderShell>
  );
}
