import type { Workspace } from "@/lib/client/portal";

export function NextReviewPanel({ w }: { w: Workspace }) {
  const openRisks = w.risks.filter((r) => true);
  return (
    <section className="rounded-2xl bg-neutral-900 p-6 text-neutral-50">
      <p className="text-xs uppercase tracking-wide text-neutral-400">Next review</p>
      <p className="mt-1 text-2xl font-semibold">{w.nextReview ?? "TBD"}</p>
      <p className="mt-2 text-sm text-neutral-300">
        {openRisks.length} open risk{openRisks.length === 1 ? "" : "s"}. Agenda generated automatically from `request_client_approval.py` and `add_proof_item.py` outputs.
      </p>
    </section>
  );
}
