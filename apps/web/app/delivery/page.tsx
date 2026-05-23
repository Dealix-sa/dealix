import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getDeliveryQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DeliveryPage() {
  const queue = await getDeliveryQueue();
  return (
    <FounderShell active="/delivery">
      <SectionHeading title="Delivery" subtitle="Deliverables waiting on humans." />
      <BrandCard title="Queue" source={queue.source}>
        <RowsTable rows={queue.data.rows} emptyMessage="No deliverables in flight." />
      </BrandCard>
    </FounderShell>
  );
}
