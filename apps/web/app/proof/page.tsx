import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getProofLibrary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProofPage() {
  const library = await getProofLibrary();
  return (
    <FounderShell active="/proof">
      <SectionHeading title="Proof Library" subtitle="Approved ProofPacks and case studies." />
      <BrandCard title="Library" source={library.source}>
        <RowsTable rows={library.data.rows} emptyMessage="No approved proof items yet." />
      </BrandCard>
    </FounderShell>
  );
}
