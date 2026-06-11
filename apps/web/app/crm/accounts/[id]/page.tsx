import { loadAccounts, loadOutreachQueue } from "@/lib/crm/crm";
import { StageBadge } from "@/components/crm/StageBadge";
import { ReviewStatusBadge } from "@/components/crm/ReviewStatusBadge";
import { DraftPreview } from "@/components/crm/DraftPreview";
import { notFound } from "next/navigation";

export const dynamic = "force-static";

export async function generateStaticParams() {
  const accounts = loadAccounts();
  return accounts.map((a) => ({ id: a.id }));
}

export default async function AccountPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const a = loadAccounts().find((x) => x.id === id);
  if (!a) notFound();
  const drafts = loadOutreachQueue().filter((d) => d.accountId === id);

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <a href="/crm" className="text-sm text-blue-700 hover:underline">← CRM</a>
      <header className="mt-3 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">{a.name}</h1>
          <p className="mt-1 text-sm text-neutral-600">{a.segment} · {a.city} · score {a.score}</p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <StageBadge stage={a.stage} />
          <ReviewStatusBadge status={a.reviewStatus} />
        </div>
      </header>

      <section className="mt-8 grid gap-4 sm:grid-cols-2">
        <Info label="Visible signal" value={a.visibleSignal} />
        <Info label="Weakness hypothesis" value={a.weaknessHypothesis} />
        <Info label="Recommended offer" value={a.recommendedOffer} />
        <Info label="Source" value={`${a.sourceType} — ${a.sourceNote}`} />
        <Info label="Next action" value={`${a.nextAction} (${a.nextActionDate})`} />
        <Info label="Setup / MRR (SAR)" value={`${a.setupValue.toLocaleString()} / ${a.monthlyValue.toLocaleString()}`} />
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold">Outreach drafts ({drafts.length})</h2>
        <div className="mt-3 space-y-4">
          {drafts.map((d) => <DraftPreview key={d.id} draft={d} />)}
          {drafts.length === 0 ? <p className="text-sm text-neutral-500">No drafts queued.</p> : null}
        </div>
      </section>
    </main>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-neutral-200 p-4">
      <p className="text-xs uppercase tracking-wide text-neutral-500">{label}</p>
      <p className="mt-1 text-sm text-neutral-800">{value}</p>
    </div>
  );
}
