import { loadDemoWorkspaces, loadWorkspaces } from "@/lib/client/portal";

export const metadata = { title: "Client Success — Dealix" };
export const dynamic = "force-static";

export default function ClientSuccessPage() {
  const workspaces = [...loadDemoWorkspaces(), ...loadWorkspaces()];
  const healthy = workspaces.filter((w) => w.proofItems.length >= 1 && w.status === "active");
  const atRisk = workspaces.filter((w) => w.risks.length >= 1 || w.status === "paused");
  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Client Success</h1>
      <p className="mt-2 text-sm text-neutral-600">Signals from `business/proof/CLIENT_SUCCESS_SIGNALS.md`.</p>
      <section className="mt-8 grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
          <h2 className="text-lg font-semibold text-emerald-900">Healthy ({healthy.length})</h2>
          <ul className="mt-2 space-y-1 text-sm text-emerald-800">
            {healthy.map((w) => <li key={w.id}>· {w.clientName}</li>)}
          </ul>
        </div>
        <div className="rounded-2xl border border-red-200 bg-red-50 p-5">
          <h2 className="text-lg font-semibold text-red-900">At risk ({atRisk.length})</h2>
          <ul className="mt-2 space-y-1 text-sm text-red-800">
            {atRisk.map((w) => <li key={w.id}>· {w.clientName}</li>)}
          </ul>
        </div>
      </section>
    </main>
  );
}
