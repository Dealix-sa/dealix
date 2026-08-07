import { loadOutreachQueue } from "@/lib/crm/crm";
import { DraftPreview } from "@/components/crm/DraftPreview";

export const metadata = { title: "Review queue — Dealix" };
export const dynamic = "force-static";

export default function ReviewQueuePage() {
  const drafts = loadOutreachQueue();
  const pending = drafts.filter((d) => d.reviewStatus?.includes("pending"));
  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Review queue</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Pending: <b>{pending.length}</b>. No autosend. Approve manually with{" "}
        <code className="rounded bg-neutral-100 px-1">scripts/approve_outreach_draft.py</code>.
      </p>
      <div className="mt-8 space-y-4">
        {pending.map((d) => <DraftPreview key={d.id} draft={d} />)}
        {pending.length === 0 ? <p className="text-sm text-neutral-500">Queue empty.</p> : null}
      </div>
    </main>
  );
}
