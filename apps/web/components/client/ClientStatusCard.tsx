import type { Workspace } from "@/lib/client/portal";

export function ClientStatusCard({ w }: { w: Workspace }) {
  const done = w.deliverables.filter((d) => d.status === "done").length;
  const pct = w.deliverables.length ? Math.round((done / w.deliverables.length) * 100) : 0;
  return (
    <section className="rounded-2xl border border-neutral-200 bg-white p-6">
      <header className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold">{w.clientName}</h2>
          <p className="text-sm text-neutral-600">{w.offer} · started {w.startDate}</p>
        </div>
        <span className={`rounded-full px-3 py-1 text-xs font-medium ${
          w.status === "active" ? "bg-emerald-100 text-emerald-700" :
          w.status === "paused" ? "bg-yellow-100 text-yellow-800" :
          "bg-neutral-100 text-neutral-700"
        }`}>{w.status}</span>
      </header>
      <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-neutral-100">
        <div className="h-full bg-emerald-500" style={{ width: `${pct}%` }} />
      </div>
      <p className="mt-2 text-xs text-neutral-500">
        {done}/{w.deliverables.length} deliverables complete · next review {w.nextReview ?? "—"}
      </p>
    </section>
  );
}
