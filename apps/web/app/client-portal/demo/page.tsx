import { loadDemoWorkspaces } from "@/lib/client/portal";
import { ClientStatusCard } from "@/components/client/ClientStatusCard";
import { DeliverableList } from "@/components/client/DeliverableList";
import { ApprovalQueue } from "@/components/client/ApprovalQueue";
import { ProofTimeline } from "@/components/client/ProofTimeline";
import { NextReviewPanel } from "@/components/client/NextReviewPanel";

export const metadata = { title: "Client Portal — Demo workspace" };
export const dynamic = "force-static";

export default function DemoWorkspacePage() {
  const w = loadDemoWorkspaces()[0];
  if (!w) return <main className="mx-auto max-w-2xl px-6 py-12"><p>Demo workspace not seeded.</p></main>;

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <span className="inline-block rounded-full bg-yellow-100 px-3 py-1 text-xs text-yellow-800">DEMO WORKSPACE — NOT A REAL CLIENT</span>
      <h1 className="mt-3 text-3xl font-semibold tracking-tight">{w.clientName}</h1>
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
