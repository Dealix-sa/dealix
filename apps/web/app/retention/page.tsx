import { loadDemoWorkspaces, loadWorkspaces } from "@/lib/client/portal";

export const metadata = { title: "Retention — Dealix" };
export const dynamic = "force-static";

export default function RetentionPage() {
  const workspaces = [...loadDemoWorkspaces(), ...loadWorkspaces()];
  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Retention</h1>
      <p className="mt-2 text-sm text-neutral-600">Active workspaces and renewal cadence.</p>
      <div className="mt-8 space-y-3">
        {workspaces.map((w) => (
          <div key={w.id} className="rounded-xl border border-neutral-200 p-4 text-sm">
            <p className="font-medium">{w.clientName}</p>
            <p className="text-neutral-600">{w.offer} · started {w.startDate} · next review {w.nextReview ?? "—"} · {w.proofItems.length} proof item(s)</p>
          </div>
        ))}
      </div>
      <section className="mt-10 rounded-2xl border border-neutral-200 p-6">
        <h2 className="text-lg font-semibold">Generate reports</h2>
        <pre className="mt-3 overflow-x-auto rounded-lg bg-neutral-900 p-4 text-xs text-neutral-100">
{`python3 scripts/generate_retention_risk_report.py
python3 scripts/generate_retainer_expansion_plan.py
python3 scripts/generate_monthly_client_review.py`}
        </pre>
      </section>
    </main>
  );
}
