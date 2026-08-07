import { findWorkspace, loadDemoWorkspaces, loadWorkspaces } from "@/lib/client/portal";
import { ClientStatusCard } from "@/components/client/ClientStatusCard";
import { DeliverableList } from "@/components/client/DeliverableList";
import { ApprovalQueue } from "@/components/client/ApprovalQueue";
import { ProofTimeline } from "@/components/client/ProofTimeline";
import { NextReviewPanel } from "@/components/client/NextReviewPanel";
import { notFound } from "next/navigation";

export const dynamic = "force-static";

export async function generateStaticParams() {
  return [...loadDemoWorkspaces(), ...loadWorkspaces()].map((w) => ({ clientId: w.id }));
}

export default async function ClientWorkspacePage({ params }: { params: Promise<{ clientId: string }> }) {
  const { clientId } = await params;
  const w = findWorkspace(clientId);
  if (!w) notFound();
  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">{w.clientName}</h1>
      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <ClientStatusCard w={w} />
        <NextReviewPanel w={w} />
      </div>
      <section className="mt-10">
        <h2 className="text-xl font-semibold">Deliverables</h2>
        <div className="mt-3"><DeliverableList items={w.deliverables} /></div>
      </section>
      <section className="mt-10">
        <h2 className="text-xl font-semibold">Approvals</h2>
        <div className="mt-3"><ApprovalQueue items={w.approvals} /></div>
      </section>
      <section className="mt-10">
        <h2 className="text-xl font-semibold">Proof</h2>
        <div className="mt-3"><ProofTimeline items={w.proofItems} /></div>
      </section>
    </main>
  );
}
