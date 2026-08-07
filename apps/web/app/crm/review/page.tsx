import { loadOutreachQueue, pendingReviewCount } from "@/lib/crm/crm";
import { DraftPreview } from "@/components/crm/DraftPreview";

export const metadata = { title: "Review queue — Dealix CRM" };
export const dynamic = "force-static";

export default function ReviewQueuePage() {
  const drafts = loadOutreachQueue();
  const pending = drafts.filter((d) => d.reviewStatus?.includes("pending"));
  const decided = drafts.filter((d) => !d.reviewStatus?.includes("pending"));

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-2xl font-semibold tracking-tight">Review queue</h1>
      <p className="mt-2 text-sm text-neutral-600">
        {pendingReviewCount(drafts)} pending. Approve or reject via:
      </p>
      <pre className="mt-3 overflow-x-auto rounded-lg bg-neutral-900 p-4 text-xs text-neutral-100">
{`python3 scripts/approve_outreach_draft.py --draft-id <id> --reviewer Sami
python3 scripts/reject_outreach_draft.py --draft-id <id> --reason "..."`}
      </pre>

      <h2 className="mt-10 text-xl font-semibold">Pending ({pending.length})</h2>
      <div className="mt-4 space-y-4">
        {pending.map((d) => <DraftPreview key={d.id} draft={d} />)}
        {pending.length === 0 ? <p className="text-sm text-neutral-500">Queue is empty.</p> : null}
      </div>

      <h2 className="mt-10 text-xl font-semibold">Decided ({decided.length})</h2>
      <div className="mt-4 space-y-4">
        {decided.slice(0, 10).map((d) => <DraftPreview key={d.id} draft={d} />)}
      </div>
    </main>
  );
}
